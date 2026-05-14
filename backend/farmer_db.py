"""
Kisan-Eye V6 — Farmer Database
SQLite-backed farmer profiles with face embeddings, farm data, and interaction history.
"""

import sqlite3
import json
import os
import numpy as np
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "kisan_eye.db"


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            father_name TEXT,
            village TEXT,
            district TEXT,
            state TEXT,
            pin_code TEXT,
            phone TEXT,
            language TEXT DEFAULT 'hi',
            latitude REAL,
            longitude REAL,
            land_acres REAL DEFAULT 0,
            crops TEXT DEFAULT '[]',
            soil_type TEXT,
            irrigation_type TEXT,
            aadhaar_last4 TEXT,
            face_embedding BLOB,
            financial_state TEXT DEFAULT 'stable',
            annual_income REAL DEFAULT 0,
            debt_amount REAL DEFAULT 0,
            family_members INTEGER DEFAULT 4,
            bpl_card INTEGER DEFAULT 0,
            token TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER REFERENCES farmers(id),
            query TEXT,
            response TEXT,
            query_lang TEXT,
            mode TEXT DEFAULT 'voice',
            satellite_data TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS yield_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER REFERENCES farmers(id),
            crop TEXT,
            season TEXT,
            year INTEGER,
            area_acres REAL,
            yield_quintals REAL,
            revenue REAL,
            expenses REAL,
            profit REAL,
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS scheme_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER REFERENCES farmers(id),
            scheme_id TEXT,
            status TEXT DEFAULT 'eligible',
            applied_at TEXT,
            approved_at TEXT,
            amount REAL,
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_farmers_village ON farmers(village, district, state);
        CREATE INDEX IF NOT EXISTS idx_interactions_farmer ON interactions(farmer_id);
        CREATE INDEX IF NOT EXISTS idx_yield_farmer ON yield_history(farmer_id);
    """)
    conn.commit()
    conn.close()


# ===== FARMER CRUD =====

def create_farmer(name, village, district, state, language="hi",
                   latitude=None, longitude=None, land_acres=0, crops=None,
                   face_embedding=None, phone=None, token=None, **kwargs):
    conn = get_db()
    embedding_blob = face_embedding.tobytes() if face_embedding is not None else None
    cursor = conn.execute("""
        INSERT INTO farmers (name, village, district, state, language, latitude, longitude,
                             land_acres, crops, face_embedding, phone,
                             father_name, aadhaar_last4, bpl_card, family_members,
                             irrigation_type, financial_state, token)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, village, district, state, language, latitude, longitude,
          land_acres, json.dumps(crops or []), embedding_blob, phone,
          kwargs.get('father_name'), kwargs.get('aadhaar_last4'),
          kwargs.get('bpl_card', 0), kwargs.get('family_members', 4),
          kwargs.get('irrigation_type'), kwargs.get('financial_state', 'stable'), token))
    farmer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return farmer_id


def get_farmer(farmer_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM farmers WHERE id=?", (farmer_id,)).fetchone()
    conn.close()
    if row:
        d = dict(row)
        d['crops'] = json.loads(d['crops']) if d['crops'] else []
        return d
    return None


def verify_token(farmer_id, token):
    if not token:
        return False
    conn = get_db()
    row = conn.execute("SELECT 1 FROM farmers WHERE id=? AND token=?", (farmer_id, token)).fetchone()
    conn.close()
    return row is not None


def get_all_farmers_with_embeddings():
    conn = get_db()
    rows = conn.execute("SELECT id, name, face_embedding FROM farmers WHERE face_embedding IS NOT NULL").fetchall()
    conn.close()
    result = []
    for row in rows:
        emb = np.frombuffer(row['face_embedding'], dtype=np.float32) if row['face_embedding'] else None
        result.append({'id': row['id'], 'name': row['name'], 'embedding': emb})
    return result


def update_farmer(farmer_id, **kwargs):
    conn = get_db()
    sets = []
    vals = []
    for k, v in kwargs.items():
        if k == 'face_embedding' and v is not None:
            v = v.tobytes()
        elif k == 'crops':
            v = json.dumps(v)
        sets.append(f"{k}=?")
        vals.append(v)
    sets.append("updated_at=datetime('now')")
    vals.append(farmer_id)
    conn.execute(f"UPDATE farmers SET {', '.join(sets)} WHERE id=?", vals)
    conn.commit()
    conn.close()


def log_interaction(farmer_id, query, response, lang="hi", mode="voice", sat_data=None):
    conn = get_db()
    conn.execute("""
        INSERT INTO interactions (farmer_id, query, response, query_lang, mode, satellite_data)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (farmer_id, query, response, lang, mode, json.dumps(sat_data) if sat_data else None))
    conn.commit()
    conn.close()


def get_farmer_history(farmer_id, limit=20):
    conn = get_db()
    rows = conn.execute("""
        SELECT query, response, query_lang, created_at FROM interactions
        WHERE farmer_id=? ORDER BY created_at DESC LIMIT ?
    """, (farmer_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_yield_record(farmer_id, crop, season, year, area, yield_q, revenue=0, expenses=0):
    conn = get_db()
    profit = revenue - expenses
    conn.execute("""
        INSERT INTO yield_history (farmer_id, crop, season, year, area_acres, yield_quintals, revenue, expenses, profit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (farmer_id, crop, season, year, area, yield_q, revenue, expenses, profit))
    conn.commit()
    conn.close()


def get_yield_history(farmer_id):
    conn = get_db()
    rows = conn.execute("""
        SELECT * FROM yield_history WHERE farmer_id=? ORDER BY year DESC, season
    """, (farmer_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Initialize DB on import
init_db()
