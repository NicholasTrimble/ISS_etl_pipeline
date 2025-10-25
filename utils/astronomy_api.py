import os
from requests.auth import HTTPBasicAuth
import requests
from datetime import datetime

ASTRO_BASE = "https://api.astronomyapi.com/api/v2/studio"

def generate_star_chart(latitude: float, longitude: float, date: str = None):
    app_id = os.getenv("ASTRONOMY_APP_ID")
    app_secret = os.getenv("ASTRONOMY_APP_SECRET")
    if not app_id or not app_secret:
        raise RuntimeError("Astronomy API credentials not set in environment")

    if date is None:
        date = datetime.utcnow().date().isoformat()

    # payload for a clearer, zoomed-in view
    payload = {
        "style": "navy",  # "inverted" or "red" also look good at night
        "observer": {
            "latitude": float(latitude),
            "longitude": float(longitude),
            "date": date
        },
        "view": {
    "type": "constellation",
    "parameters": {
        "constellation": "ori"  # Orion
    }
},
                "zoom": 5  # 1 = wide, 10 = close zoom — try 5 to 8 for clarity
            }
        
    

    url = f"{ASTRO_BASE}/star-chart"
    resp = requests.post(url, json=payload, auth=HTTPBasicAuth(app_id, app_secret), timeout=30)
    resp.raise_for_status()
    return resp.json()["data"]["imageUrl"]
