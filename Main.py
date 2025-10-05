import requests
from datetime import datetime, timezone
import time
import schedule
from database import init_db, save_to_db

MY_LAT = 51.507351
MY_LONG = -0.127758

def fetch_iss_position():
    try:
        response = requests.get("http://api.open-notify.org/iss-now.json", timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "latitude": float(data["iss_position"]["latitude"]),
            "longitude": float(data["iss_position"]["longitude"]),
            "timestamp": datetime.now(timezone.utc)
        }
    except:
        # fallback dummy data
        return {
            "latitude": 51.5,
            "longitude": -0.1,
            "timestamp": datetime.now(timezone.utc)
        }

def check_overhead(lat, long, observer_lat=MY_LAT, observer_long=MY_LONG):
    return observer_lat - 5 <= lat <= observer_lat + 5 and observer_long - 5 <= long <= observer_long + 5

def check_night(observer_lat=MY_LAT, observer_long=MY_LONG):
    try:
        params = {"lat": observer_lat, "lng": observer_long, "formatted": 0}
        response = requests.get("https://api.sunrise-sunset.org/json", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
        sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
        hour_now = datetime.now(timezone.utc).hour
        return hour_now >= sunset or hour_now <= sunrise
    except:
        return False

def run_etl():
    iss_data = fetch_iss_position()
    iss_data["overhead"] = check_overhead(iss_data["latitude"], iss_data["longitude"])
    iss_data["is_night"] = check_night()
    save_to_db(iss_data)
    print(f"ETL run complete: {iss_data}")

if __name__ == "__main__":
    init_db()
    run_etl()
    schedule.every(10).minutes.do(run_etl)
    while True:
        schedule.run_pending()
        time.sleep(60)
