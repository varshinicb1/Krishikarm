#include <Arduino.h>
#include <LoRa.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <TinyGPS++.h>
#include <esp_task_wdt.h>

// WDT Timeout
#define WDT_TIMEOUT 10

// LoRa Pins
#define LORA_SCK   12
#define LORA_MISO  13
#define LORA_MOSI  11
#define LORA_CS    10
#define LORA_RST   9
#define LORA_IRQ   14

// I2C Pins
#define I2C_SDA    21
#define I2C_SCL    22

// Analog Pins
#define SOIL_PIN   1
#define PH_PIN     2
#define BATT_PIN   3

// GPS Pins
#define GPS_RX     19
#define GPS_TX     18

// Node config
#define NODE_ID 101
#define SYNC_WORD 0x4B // 'K' for Krishikarm

Adafruit_BME280 bme;
TinyGPSPlus gps;
HardwareSerial gpsSerial(1);

// Packed Struct for LoRa Payload
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

void setup() {
  Serial.begin(115200);
  
  // Init WDT
  esp_task_wdt_init(WDT_TIMEOUT, true);
  esp_task_wdt_add(NULL);

  gpsSerial.begin(9600, SERIAL_8N1, GPS_RX, GPS_TX);
  
  // Setup I2C & Sensors
  Wire.begin(I2C_SDA, I2C_SCL);
  if (!bme.begin(0x76, &Wire)) {
    Serial.println("WARN: BME280 init failed, continuing...");
  }

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
    LoRa.setTxPower(20); // Max power for rural range
    LoRa.setSpreadingFactor(10); // Better range, slower rate
  }

  // Setup ADC
  analogReadResolution(12); // 0-4095
}

void enterDeepSleep(uint16_t batt_mv) {
  uint32_t sleep_time_mins = 30; // Default sleep
  
  // Adaptive power saving
  if (batt_mv < 3300) {
    sleep_time_mins = 120; // Sleep longer if battery is critically low
    Serial.println("Battery Critical: Adaptive sleep to 120 mins");
  } else if (batt_mv < 3600) {
    sleep_time_mins = 60;  // Save power
    Serial.println("Battery Low: Adaptive sleep to 60 mins");
  }

  Serial.printf("Going to sleep for %u minutes...\n", sleep_time_mins);
  esp_sleep_enable_timer_wakeup((uint64_t)sleep_time_mins * 60 * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {
  esp_task_wdt_reset(); // Feed WDT

  // 1. Gather GPS (Wait up to 2.5 seconds for fresh sentence)
  unsigned long start = millis();
  while(millis() - start < 2500) {
    while(gpsSerial.available()) {
      gps.encode(gpsSerial.read());
    }
  }

  // 2. Read Sensors
  float t = bme.readTemperature();
  float h = bme.readHumidity();
  if (isnan(t)) t = 0;
  if (isnan(h)) h = 0;
  
  // Read soil moisture (12-bit ADC mapping)
  int soil_raw = analogRead(SOIL_PIN);
  uint8_t soil_pct = map(soil_raw, 4095, 1000, 0, 100); 
  if (soil_pct > 100) soil_pct = 100;

  // Read pH (calibrated voltage slope)
  int ph_raw = analogRead(PH_PIN);
  float ph = 7.0 + ((ph_raw - 2048) / 200.0);
  if (ph < 0) ph = 0;

  // Read Battery (Voltage divider)
  int batt_raw = analogRead(BATT_PIN);
  // ADC * 3.3V / 4095 * Div Ratio (e.g. 2.0) -> roughly
  uint16_t batt_mv = (uint16_t)((batt_raw / 4095.0) * 3300.0 * 2.0); 
  if (batt_mv == 0) batt_mv = 3700; // fallback mock if not connected

  // 3. Build Packet
  TelemetryPacket packet;
  packet.node_id = NODE_ID;
  packet.timestamp = gps.time.isValid() ? gps.time.value() : 0;
  packet.lat = gps.location.isValid() ? gps.location.lat() : 0.0;
  packet.lng = gps.location.isValid() ? gps.location.lng() : 0.0;
  packet.temp = (int16_t)(t * 100);
  packet.humidity = (uint16_t)(h * 100);
  packet.soil_moisture = soil_pct;
  packet.ph_level = (uint8_t)(ph * 10);
  packet.battery_mv = batt_mv;
  
  // 4. Calculate Checksum
  packet.crc16 = 0; // zero out before calculating
  packet.crc16 = calculateCRC16((uint8_t*)&packet, sizeof(packet) - 2);

  // 5. Transmit 3 times for robustness (unacknowledged transmission)
  for (int i=0; i<3; i++) {
    LoRa.beginPacket();
    LoRa.write((uint8_t*)&packet, sizeof(packet));
    LoRa.endPacket();
    delay(500); // 500ms spacing between redundant packets
    esp_task_wdt_reset();
  }
  
  Serial.println("Telemetry batch transmitted.");

  // 6. Deep Sleep
  enterDeepSleep(batt_mv);
}
