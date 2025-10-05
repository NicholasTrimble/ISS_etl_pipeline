from flask import Flask
import sqlite3

DB_NAME = "iss_pipeline.db"
app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>ISS ETL Dashboard</title>
        <style>
            body {
                background-color: #000;
                color: #fff;
                font-family: 'Open Sans', Open Sans;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            h1 {
                font-size: 4.5em;
                margin-bottom: 20px;
            }
            a {
                color: #1e90ff;
                text-decoration: none;
                font-size: 1.2em;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>ISS ETL Dashboard</h1>
        <p>Go to <a href="/data">/data</a> to see the latest ISS entries.</p>
    </body>
    </html>
    """

@app.route("/data")
def show_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM iss_data ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    # Build a simple readable string
    output = ""
    for row in rows:
        output += f"Timestamp: {row[0]}, Latitude: {row[1]}, Longitude: {row[2]}, Overhead: {row[3]}, Is Night: {row[4]}\n"

    return f"""
    <html>
    <head>
        <title>Latest ISS Data</title>
        <style>
            body {{
                background-color: #000;
                color: #fff;
                font-family: 'Arial', sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }}
            h1 {{
                font-size: 2em;
                margin-bottom: 20px;
            }}
            pre {{
                background-color: #111;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 2px 2px 8px #444;
            }}
        </style>
    </head>
    <body>
        <h1>Latest ISS Entries</h1>
        <pre>{output}</pre>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
