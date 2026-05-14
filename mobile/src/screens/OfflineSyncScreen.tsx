import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function OfflineSyncScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Node Synchronization</Text>
      <Text>Connect to Node 2 (Gateway) via BLE/WiFi to pull latest telemetry.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
  }
});
