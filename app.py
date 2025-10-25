from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from database import add_user, remove_user
from utils.weather_helpers import get_weather_data, calculate_visibility
import os
from dotenv import load_dotenv
import utils.astronomy_api as astronomy_api



load_dotenv()

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
        <h1>Interactive Map With Weather and ISS ETL Dashboard</h1>
        <p>Go to <a href="/data">ISS location</a> to see the latest ISS entries.</p>
        <p>Go to <a href="/map">Interactive map with Weather</a> to see the latest weather.</p>
        <form action="/subscribe" method="POST" style="margin-top: 20px;" onsubmit="showAlert()">
            <input type="email" name="email" placeholder="your_email@example.com" required
            style="padding: 10px; font-size: 1em;">
            <button type="submit" style="padding: 10px; font-size: 1em;">Subscribe</button>
        </form>

    </body>
    <script>
        function showAlert() {
        alert("Thank you! You are subscribed.");
        }
    </script>
    </html>
    """

@app.route("/map")
def show_map():
    return render_template("map.html")


@app.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email")
    if email:
        add_user(email)
    return redirect("/")


@app.route("/iss_position")
def iss_position():
    import requests
    from datetime import datetime, timezone

    try:
        response = requests.get("http://api.open-notify.org/iss-now.json", timeout=10)
        response.raise_for_status()
        data = response.json()
        latitude = float(data["iss_position"]["latitude"])
        longitude = float(data["iss_position"]["longitude"])
        timestamp = datetime.now(timezone.utc).isoformat()
    except:
        # fallback
        latitude = 51.5
        longitude = -0.1
        timestamp = datetime.now(timezone.utc).isoformat()

    return jsonify({
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": timestamp
    })


@app.route("/weather_info")
def weather_info_route():
    # Get latitude and longitude from query parameters
    lat = float(request.args.get("lat", 51.507351))  # default London
    lon = float(request.args.get("lon", -0.127758))

    # Determine if it’s night (optional, default True for now)
    is_night_time = True

    # Call weather helper to get full weather info
    weather_info = get_weather_data(lat, lon, is_night_time)

    # Return JSON for JS to read
    return jsonify(weather_info)


@app.route("/star_chart")
def star_chart():
    from flask import request, jsonify

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Missing lat/lon"}), 400

    try:
        # note the module prefix
        image_url = astronomy_api.generate_star_chart(float(lat), float(lon))
        return jsonify({"imageUrl": image_url})
    except Exception as e:
        print("Star chart error:", e)
        return jsonify({"error": str(e)}), 500



@app.route("/unsubscribe")
def unsubscribe():
    email = request.args.get("email")
    if email:
        remove_user(email)
        return f"Email {email} has been unsubscribed."
    return "No email provided."



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
