import sqlite3
import json
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "kisan_eye.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Telemetry Nodes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            id TEXT PRIMARY KEY,
            farm_id TEXT,
            status TEXT,
            battery_mv INTEGER,
            last_seen TIMESTAMP
        )
    ''')

    # Raw Telemetry Data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_id TEXT,
            timestamp TIMESTAMP,
            lat REAL,
            lng REAL,
            temp REAL,
            humidity REAL,
            soil_moisture REAL,
            ph_level REAL,
            battery_mv INTEGER,
            synced BOOLEAN DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

def insert_telemetry(node_id, data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO telemetry (node_id, timestamp, lat, lng, temp, humidity, soil_moisture, ph_level, battery_mv)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        node_id, 
        datetime.fromtimestamp(data.get('timestamp', datetime.now().timestamp())),
        data.get('lat', 0.0),
        data.get('lng', 0.0),
        data.get('temp', 0.0),
        data.get('humidity', 0.0),
        data.get('soil_moisture', 0.0),
        data.get('ph_level', 0.0),
        data.get('battery_mv', 0)
    ))
    conn.commit()
    conn.close()

def get_latest_telemetry(node_id=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if node_id:
        cursor.execute('SELECT * FROM telemetry WHERE node_id=? ORDER BY timestamp DESC LIMIT 100', (node_id,))
    else:
        cursor.execute('SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT 100')
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    print("Telemetry database initialized.")
