import time
import paho.mqtt.client as mqtt
import meshtastic
import meshtastic.serial_interface

# MQTT settings
MQTT_BROKER = "localhost"
TOPIC_FROM_MESH = "from_meshtastic"
TOPIC_FROM_AREDN = "from_aredn"

# Connect to Meshtastic
iface = meshtastic.serial_interface.SerialInterface()

# MQTT setup
client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

# Incoming Meshtastic message handler
def onReceive(packet):
    msg = packet.get("decoded", {}).get("text")
    if msg:
        print(f"LoRa > {msg}")
        client.publish(TOPIC_FROM_MESH, msg)

iface.onReceive = onReceive

# AREDN > MQTT handler
def on_aredn_msg(client, userdata, message):
    print(f"AREDN > {message.payload.decode()}")
    iface.sendText(message.payload.decode())

client.subscribe(TOPIC_FROM_AREDN)
client.on_message = on_aredn_msg

# Loop
client.loop_start()
while True:
    time.sleep(1)
