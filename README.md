# HackViolet
A repository to host our groups code for HackViolet hackathon

import paho.mqtt.client as mqtt
import json
import time
import threading

# --- CONFIGURATION ---
MQTT_BROKER = "test.mosquitto.org"
# The topic the ESP32 writes to (Sensors)
MQTT_TOPIC_DATA = "HackViolet/YOUR_TEAM/sensors"  
# The topic the ESP32 listens to (Commands)
MQTT_TOPIC_CMD  = "HackViolet/YOUR_TEAM/commands" 

# --- CALLBACKS ---
def on_connect(client, userdata, flags, rc):
    print(f"✅ Connected! Listening to: {MQTT_TOPIC_DATA}")
    client.subscribe(MQTT_TOPIC_DATA)

def on_message(client, userdata, msg):
    try:
        # Don't print while user is typing
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        # Print nicely formatted data
        print(f"\n[SENSOR DATA] Soil: {data.get('soil')} | Light: {data.get('light')} | Valve: {data.get('valve')}")
        print("Type 'water' to open valve > ", end="", flush=True)
    except:
        pass

# --- SETUP MQTT ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)

# Start MQTT in a background thread so we can type commands
client.loop_start()

# --- MAIN COMMAND LOOP ---
print("--- COMMAND CENTER ---")
print("Type 'water' and hit ENTER to trigger the valve.")
print("Type 'close' and hit ENTER to close it.")

try:
    while True:
        # This waits for him to type something
        user_input = input("Type command > ")
        
        if user_input.strip().lower() == "water":
            print(f"🌊 Sending WATER_NOW command to {MQTT_TOPIC_CMD}...")
            client.publish(MQTT_TOPIC_CMD, "WATER_NOW")
            
        elif user_input.strip().lower() == "close":
            print(f"🛑 Sending CLOSE command...")
            # You might need to add handling for "CLOSE_NOW" in your ESP32 if you haven't yet
            # But for now, "WATER_NOW" toggles it or starts the timer.
            
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nDisconnecting...")
    client.loop_stop()
    client.disconnect()
