import time
import random
import requests
from datetime import datetime

BACKEND_URL = "http://localhost:5000/data"
DEVICE_ID = "happyplant-mock-01"
INTERVAL_SECONDS = 5  # send data every 5 seconds

daily_lux_sum = 0

print("🌱 Mock ESP32 started")

while True:
    # Simulate sunlight (lux)
    lux = random.randint(0, 60000)

    daily_lux_sum += lux * INTERVAL_SECONDS

    payload = {
        "device_id": DEVICE_ID,
        "timestamp": datetime.now().isoformat(),
        "lux": lux,
        "interval_seconds": INTERVAL_SECONDS,
        "daily_lux_sum": daily_lux_sum
    }

    try:
        response = requests.post(BACKEND_URL, json=payload)
        print(f"Sent: {payload} | Status: {response.status_code}")
    except Exception as e:
        print("Failed to send data:", e)

    time.sleep(INTERVAL_SECONDS)
