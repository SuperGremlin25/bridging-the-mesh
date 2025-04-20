import time
import paho.mqtt.client as mqtt
import meshtastic
import meshtastic.serial_interface
import requests

# MQTT Configuration
MQTT_BROKER = "localhost"
TOPIC_FROM_MESH = "from_meshtastic"
TOPIC_FROM_AREDN = "from_aredn"
TOPIC_ALERTS = "alerts/emergency"

# Connect to Meshtastic device
iface = meshtastic.serial_interface.SerialInterface()

# Connect to MQTT broker
client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

# 🧠 Optional: Use local AI to classify messages
def classify_with_ai(message):
    try:
        res = requests.post("http://localhost:8000/completion", json={
            "prompt": f"Classify this message: {message}",
            "max_tokens": 30
        }, timeout=3)
        if res.status_code == 200:
            return res.json().get("content", "").lower()
        return ""
    except Exception as e:
        print("[AI ERROR]", e)
        return ""

# Callback: incoming messages from Meshtastic
def onReceive(packet):
    msg = packet.get("decoded", {}).get("text")
    if msg:
        print("[LoRa > MQTT]:", msg)
        classification = classify_with_ai(msg)
        if "emergency" in classification or "alert" in classification:
            print("⚠️ AI FLAGGED:", msg)
            client.publish(TOPIC_ALERTS, msg)
        client.publish(TOPIC_FROM_MESH, msg)

iface.onReceive = onReceive

# Callback: incoming messages from AREDN → send to LoRa
def on_aredn_msg(client, userdata, message):
    try:
        decoded = message.payload.decode()
        print("[AREDN > LoRa]:", decoded)
        iface.sendText(decoded)
    except Exception as e:
        print("[ERROR forwarding AREDN message]", e)

client.subscribe(TOPIC_FROM_AREDN)
client.on_message = on_aredn_msg

# Start MQTT loop and keep script running
print("📡 MQTT-LoRa-AI Bridge is running...")
client.loop_start()

while True:
    time.sleep(1)
