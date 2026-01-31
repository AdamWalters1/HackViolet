# HackViolet
A repository to host our groups code for HackViolet hackathon

import paho.mqtt.client as mqtt
import json

# --- CONFIGURATION ---
MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "HackViolet/YOUR_TEAM/sensors" # <--- MUST MATCH ESP32 CODE EXACTLY

def on_connect(client, userdata, flags, rc):
    print(f"✅ Connected to Cloud! Listening for: {MQTT_TOPIC}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        
        # THIS IS WHERE THE DATA LANDS ON HIS LAPTOP
        print(f"📥 RECEIVED: {data}")
        
        # If he wants to save it to a file/database, do it here:
        # with open("data.csv", "a") as f:
        #    f.write(f"{data['soil']},{data['temp']}\n")
            
    except Exception as e:
        print(f"Error: {e}")

# --- MAIN LOOP ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, 1883, 60)
client.loop_forever()
