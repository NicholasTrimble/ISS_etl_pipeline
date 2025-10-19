import sqlite3

DB_NAME = "iss_pipeline.db"


def init_db():
    """Create tables if they don't exist."""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # ISS data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS iss_data (
            timestamp TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL,
            overhead BOOLEAN,
            is_night BOOLEAN
        )
    """)

    # Users for notifications
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            latitude REAL DEFAULT 51.507351,
            longitude REAL DEFAULT -0.127758
        )
    """)

    conn.commit()
    conn.close()


def save_to_db(data):
    """Save ISS data entry."""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO iss_data (timestamp, latitude, longitude, overhead, is_night)
        VALUES (?, ?, ?, ?, ?)
    """, (str(data["timestamp"]), data["latitude"], data["longitude"], data["overhead"], data["is_night"]))
    conn.commit()
    conn.close()





def add_user(email, latitude=51.507351, longitude=-0.127758):
    """Add a new user for notifications."""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (email, latitude, longitude)
        VALUES (?, ?, ?)
    """, (email, latitude, longitude))
    conn.commit()
    conn.close()


def get_all_users():
    """Return list of all users."""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT email, latitude, longitude FROM users")
    users = [{"email": row[0], "latitude": row[1], "longitude": row[2]} for row in cursor.fetchall()]
    conn.close()
    return users


def remove_user(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()
    conn.close()