import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "kisan_eye.db")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "firebase_export.json")

def export_to_json():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row['name'] for row in cursor.fetchall()]

    firebase_data = {}

    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        
        table_data = {}
        for row in rows:
            row_dict = dict(row)
            # Use 'id' as the document key if it exists
            doc_id = row_dict.get('id') or row_dict.get('farmer_id') or str(len(table_data))
            table_data[str(doc_id)] = row_dict
            
        firebase_data[table] = table_data

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(firebase_data, f, indent=2)

    print(f"Successfully exported database to {OUTPUT_PATH}")
    print("This JSON can be imported into Firebase Firestore or Realtime Database.")

if __name__ == "__main__":
    export_to_json()
