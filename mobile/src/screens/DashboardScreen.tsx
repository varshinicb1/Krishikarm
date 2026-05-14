import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator, RefreshControl } from 'react-native';

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://10.0.2.2:8000';

export default function DashboardScreen({ navigation }: any) {
  const [telemetry, setTelemetry] = useState({
    soilMoisture: '--',
    temp: '--',
    ph: '--',
    lastUpdate: 'Never'
  });
  
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = async () => {
    try {
      setError(null);
      const res = await fetch(`${API_BASE_URL}/api/v1/farm/farm_001/analytics`);
      if (!res.ok) throw new Error('Failed to fetch data');
      const data = await res.json();
      
      if (data.telemetry) {
        setTelemetry({
          soilMoisture: data.telemetry.soil_moisture?.toFixed(1) || '--',
          temp: data.telemetry.temp?.toFixed(1) || '--',
          ph: data.telemetry.ph_level?.toFixed(1) || '--',
          lastUpdate: new Date(data.telemetry.timestamp || Date.now()).toLocaleTimeString()
        });
      }
      
      if (data.analytics) {
        setAnalytics(data.analytics);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={loading} onRefresh={fetchDashboardData} />
      }
    >
      {error && (
        <View style={styles.errorBox}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      )}

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Real-time Telemetry</Text>
        <Text style={styles.cardMetric}>💧 Soil Moisture: {telemetry.soilMoisture}%</Text>
        <Text style={styles.cardMetric}>🌡️ Temperature: {telemetry.temp}°C</Text>
        <Text style={styles.cardMetric}>🧪 pH Level: {telemetry.ph}</Text>
        <Text style={styles.cardSub}>Last Updated: {telemetry.lastUpdate}</Text>
      </View>
      
      {analytics && (
        <View style={styles.card}>
          <Text style={styles.cardTitle}>AI Analytics</Text>
          <Text style={styles.cardMetric}>
            🌱 Yield Prediction: {analytics.crop_yield_prediction?.value} {analytics.crop_yield_prediction?.unit}
          </Text>
          <Text style={styles.cardMetric}>
            🐛 Pest Risk: {analytics.pest_disease_risk?.risk_level}
          </Text>
        </View>
      )}

      <View style={styles.actionGrid}>
        <TouchableOpacity 
          style={styles.actionBtn}
          onPress={() => navigation.navigate('Sync')}
        >
          <Text style={styles.btnText}>Sync Node</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.actionBtn}
          onPress={() => navigation.navigate('Alerts')}
        >
          <Text style={styles.btnText}>Advisory</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f3f4f6',
    padding: 16,
  },
  errorBox: {
    backgroundColor: '#fee2e2',
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
  },
  errorText: {
    color: '#ef4444',
    textAlign: 'center',
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 20,
    elevation: 3,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 12,
    color: '#374151',
  },
  cardMetric: {
    fontSize: 16,
    color: '#4b5563',
    marginBottom: 8,
  },
  cardSub: {
    fontSize: 12,
    color: '#9ca3af',
    marginTop: 12,
  },
  actionGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  actionBtn: {
    flex: 1,
    backgroundColor: '#10b981',
    padding: 16,
    borderRadius: 8,
    marginHorizontal: 5,
    alignItems: 'center',
  },
  btnText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  }
});
