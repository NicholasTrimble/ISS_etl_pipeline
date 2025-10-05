import sqlite3

DB_NAME = "iss_pipeline.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS iss_data (
            timestamp TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL,
            overhead BOOLEAN,
            is_night BOOLEAN
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO iss_data (timestamp, latitude, longitude, overhead, is_night)
        VALUES (?, ?, ?, ?, ?)
    """, (str(data["timestamp"]), data["latitude"], data["longitude"], data["overhead"], data["is_night"]))
    conn.commit()
    conn.close()