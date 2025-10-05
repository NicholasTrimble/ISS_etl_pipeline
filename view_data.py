import sqlite3

DB_NAME = "iss_pipeline.db"

def print_all_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM iss_data")
    rows = cursor.fetchall()

    column_names = [description[0] for description in cursor.description]
    print("\t".join(column_names))  # prints: timestamp latitude longitude overhead is_night

    for row in rows:
        print("\t".join(map(str, row)))

    conn.close()

if __name__ == "__main__":
    print_all_data()
