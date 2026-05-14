import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StatusBar } from 'expo-status-bar';

// Placeholder Screens
import DashboardScreen from './src/screens/DashboardScreen';
import OfflineSyncScreen from './src/screens/OfflineSyncScreen';
import AlertsScreen from './src/screens/AlertsScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      <Stack.Navigator 
        initialRouteName="Dashboard"
        screenOptions={{
          headerStyle: { backgroundColor: '#10b981' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: 'bold' },
        }}
      >
        <Stack.Screen 
          name="Dashboard" 
          component={DashboardScreen} 
          options={{ title: 'KrishiKarm — कृषिकर्म' }}
        />
        <Stack.Screen 
          name="Sync" 
          component={OfflineSyncScreen} 
          options={{ title: 'Node Sync' }}
        />
        <Stack.Screen 
          name="Alerts" 
          component={AlertsScreen} 
          options={{ title: 'Farm Alerts' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
