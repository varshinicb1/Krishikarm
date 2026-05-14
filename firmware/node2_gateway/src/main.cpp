#include <Arduino.h>
#include <LoRa.h>
#include <SPI.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <esp_task_wdt.h>

#define WDT_TIMEOUT 15

// LoRa Pins
#define LORA_SCK   12
#define LORA_MISO  13
#define LORA_MOSI  11
#define LORA_CS    10
#define LORA_RST   9
#define LORA_IRQ   14

// Audio / I2S Pins
#define I2S_DOUT      25
#define I2S_BCLK      26
#define I2S_LRC       27

#define SYNC_WORD 0x4B // 'K' for Krishikarm

// BLE UUIDs
#define SERVICE_UUID           "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID    "beb5483e-36e1-4688-b7f5-ea07361b26a8"

BLECharacteristic *pCharacteristic;
bool deviceConnected = false;
bool oldDeviceConnected = false;

// Shared struct
#pragma pack(push, 1)
struct TelemetryPacket {
  uint16_t header = 0x4B4B;
  uint16_t node_id;
  uint32_t timestamp;
  float lat;
  float lng;
  int16_t temp;
  uint16_t humidity;
  uint8_t soil_moisture;
  uint8_t ph_level;
  uint16_t battery_mv;
  uint16_t crc16;
};
#pragma pack(pop)

// FreeRTOS Queue for passing packets from LoRa thread to BLE thread
QueueHandle_t packetQueue;

// Utility: Calculate CRC16 (CCITT)
uint16_t calculateCRC16(const uint8_t *data, size_t length) {
  uint16_t crc = 0xFFFF;
  for (size_t i = 0; i < length; i++) {
    crc ^= (uint16_t)data[i] << 8;
    for (uint8_t j = 0; j < 8; j++) {
      if (crc & 0x8000) crc = (crc << 1) ^ 0x1021;
      else crc <<= 1;
    }
  }
  return crc;
}

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      Serial.println("Mobile App Connected via BLE.");
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
      Serial.println("Mobile App Disconnected.");
    }
};

void setup() {
  Serial.begin(115200);

  // Init WDT
  esp_task_wdt_init(WDT_TIMEOUT, true);
  esp_task_wdt_add(NULL);

  // Initialize Queue to buffer up to 10 incoming packets
  packetQueue = xQueueCreate(10, sizeof(TelemetryPacket));

  // Setup BLE
  BLEDevice::init("KrishiKarm_Gateway");
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ   |
                      BLECharacteristic::PROPERTY_NOTIFY
                    );

  pService->start();
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);
  pAdvertising->setMinPreferred(0x12);
  BLEDevice::startAdvertising();
  Serial.println("BLE Started. Advertising...");

  // Setup LoRa
  SPI.begin(LORA_SCK, LORA_MISO, LORA_MOSI, LORA_CS);
  LoRa.setPins(LORA_CS, LORA_RST, LORA_IRQ);
  
  int lora_retries = 0;
  while (!LoRa.begin(433E6) && lora_retries < 5) {
    Serial.println("LoRa init failed. Retrying...");
    delay(1000);
    lora_retries++;
  }
  
  if (lora_retries < 5) {
    LoRa.setSyncWord(SYNC_WORD);
    LoRa.setSpreadingFactor(10); 
    Serial.println("LoRa receiver active.");
  }
}

void loop() {
  esp_task_wdt_reset();

  // Handle BLE Disconnect/Reconnect state changes
  if (!deviceConnected && oldDeviceConnected) {
      delay(500); // give the bluetooth stack the chance to get things ready
      BLEDevice::startAdvertising(); // restart advertising
      Serial.println("Restarted Advertising");
      oldDeviceConnected = deviceConnected;
  }
  if (deviceConnected && !oldDeviceConnected) {
      oldDeviceConnected = deviceConnected;
  }

  // 1. Process Incoming LoRa packets
  int packetSize = LoRa.parsePacket();
  if (packetSize == sizeof(TelemetryPacket)) {
    TelemetryPacket rxPacket;
    LoRa.readBytes((uint8_t*)&rxPacket, sizeof(TelemetryPacket));
    
    if (rxPacket.header == 0x4B4B) {
      // Validate CRC
      uint16_t expected_crc = rxPacket.crc16;
      rxPacket.crc16 = 0; // zero out for check
      uint16_t actual_crc = calculateCRC16((uint8_t*)&rxPacket, sizeof(TelemetryPacket) - 2);
      
      if (expected_crc == actual_crc || expected_crc == 0xFFFF) { // Accept 0xFFFF as dev mock mode
        Serial.printf("Valid Packet Node %d | Temp: %.2f | Soil: %d%%\n", 
          rxPacket.node_id, 
          rxPacket.temp / 100.0, 
          rxPacket.soil_moisture
        );
        
        // Restore CRC and push to queue
        rxPacket.crc16 = expected_crc;
        if(xQueueSend(packetQueue, &rxPacket, 0) != pdTRUE) {
          Serial.println("Queue full, dropping packet.");
        }
      } else {
        Serial.printf("CRC mismatch! Expected: %04X, Got: %04X\n", expected_crc, actual_crc);
      }
    }
  }

  // 2. Process Queue -> BLE Notification
  TelemetryPacket txPacket;
  if (xQueueReceive(packetQueue, &txPacket, 0) == pdTRUE) {
    if (deviceConnected) {
      pCharacteristic->setValue((uint8_t*)&txPacket, sizeof(TelemetryPacket));
      pCharacteristic->notify();
      Serial.println("Notified BLE client.");
      delay(20); // Small delay to avoid BLE congestion
    } else {
      // If disconnected, packet is dropped from queue. 
      // Could push it back to front of queue, but sensor data goes stale quickly.
      Serial.println("Dropped packet due to no BLE connection.");
    }
  }

  delay(10);
}
