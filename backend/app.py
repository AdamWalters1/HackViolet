import json
from pathlib import Path

DATA_FILE = Path("daily_data.json")

from datetime import date

current_day = date.today()
daily_lux_sum = 0
current_plant = "medium"

PLANT_PROFILES = {
    "low": {
        "min": 20_000_000,
        "max": 40_000_000
    },
    "medium": {
        "min": 40_000_000,
        "max": 80_000_000
    },
    "high": {
        "min": 80_000_000,
        "max": 150_000_000
    }
}

@app.route("/data", methods=["POST"])
def receive_data():
    global daily_lux_sum, current_day

    data = request.json
    lux = data["lux"]
    interval = data["interval_seconds"]

    today = date.today()

    # Reset daily total at midnight
    if today != current_day:
        current_day = today
        daily_lux_sum = 0

    with open(DATA_FILE, "w") as f:
        json.dump({
            "date": str(current_day),
            "daily_lux_sum": daily_lux_sum,
            "status": status,
            "plant": current_plant
    }, f)

    daily_lux_sum += lux * interval

    profile = PLANT_PROFILES[current_plant]

    if daily_lux_sum < profile["min"]:
        status = "low"
    elif daily_lux_sum > profile["max"]:
        status = "high"
    else:
        status = "ok"

    response = {
        "daily_lux_sum": daily_lux_sum,
        "status": status,
        "plant": current_plant
    }

    print("Status:", response)

    return jsonify(response)


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "HappyPlant backend running"

@app.route("/data", methods=["POST"])
def receive_data():
    data = request.json
    print("Received data:", data)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

