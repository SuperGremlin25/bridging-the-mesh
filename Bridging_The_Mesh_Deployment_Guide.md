
# Bridging the Mesh: Full Deployment Guide (Beginner-Friendly)

This guide walks you through setting up the Bridging the Mesh project—linking AREDN and Meshtastic networks with a Raspberry Pi-based AI gateway. You’ll build a device that listens to both networks, routes messages via MQTT, and uses AI to flag urgent events.

---

## 🧰 STEP 1: Hardware Checklist

- Raspberry Pi 5 or reComputer R2130-12
- Meshtastic device (e.g. FemtoFox, T-Beam, RAK4631)
- MikroTik hAP ac2 or hAP ac lite (running AREDN)
- microSD Card (32GB minimum, Class 10)
- Power supply (USB-C or PoE splitter)
- Optional: Solar + LiFePO₄ battery setup
- Ethernet cable

---

## 💻 STEP 2: Software Overview

- Raspberry Pi OS (Lite or Desktop)
- Python 3.11+
- Node-RED (installed via script)
- Mosquitto MQTT Broker
- llama-cpp-python (for running TinyLLaMA)
- Python Libraries: `paho-mqtt`, `pyserial`, `meshtastic`, `llama-cpp-python`

---

## 🔧 STEP 3: Flash Raspberry Pi OS

1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Select **Raspberry Pi OS Lite (64-bit)**
3. Write to microSD card
4. Enable SSH & WiFi using Imager's "Advanced Settings"
5. Boot Pi and connect via SSH: `ssh pi@raspberrypi.local` (password: `raspberry`)

---

## 📦 STEP 4: Install Required Packages

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip git mosquitto mosquitto-clients screen
pip3 install paho-mqtt pyserial meshtastic llama-cpp-python
```

Install Node-RED:
```bash
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
sudo systemctl enable nodered.service
```

Visit Node-RED at `http://<pi-ip>:1880`.

---

## 🔌 STEP 5: Connect Meshtastic Device

1. Plug Meshtastic device into Pi (via USB)
2. Confirm it shows up using: `ls /dev/ttyUSB*`

---

## 📜 STEP 6: Python Bridge Script

Save the following as `mqtt_bridge.py`:

```python
import time, paho.mqtt.client as mqtt, meshtastic, meshtastic.serial_interface

MQTT_BROKER = "localhost"
TOPIC_FROM_MESH = "from_meshtastic"
TOPIC_FROM_AREDN = "from_aredn"

iface = meshtastic.serial_interface.SerialInterface()
client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

def onReceive(packet):
    msg = packet.get("decoded", {}).get("text")
    if msg:
        print(f"LoRa > {msg}")
        client.publish(TOPIC_FROM_MESH, msg)

iface.onReceive = onReceive

def on_aredn_msg(client, userdata, message):
    print(f"AREDN > {message.payload.decode()}")
    iface.sendText(message.payload.decode())

client.subscribe(TOPIC_FROM_AREDN)
client.on_message = on_aredn_msg

client.loop_start()
while True:
    time.sleep(1)
```

Run it:
```bash
python3 mqtt_bridge.py
```

---

## 🧠 STEP 7: Add AI with TinyLLaMA

```bash
pip3 install llama-cpp-python
wget https://huggingface.co/johnsmith0031/tiny-llama-v0-GGUF/resolve/main/tiny-llama.gguf
python3 -m llama_cpp.server --model tiny-llama.gguf
```

---

## 🧪 STEP 8: Test

1. Send a message from Meshtastic → appears in MQTT broker
2. Send MQTT message to AREDN topic → appears on Meshtastic device

---

## 🌐 STEP 9: Access Dashboard from AREDN

- Assign Pi static IP via DHCP or manually
- Open Node-RED at `http://pi-ip:1880` from the mesh

---

## 📡 STEP 10: Supernode Strategy

Deploy this stack on high-value infrastructure points like:
- Strata Tower (OKC, 330’)
- OU Science Building (Norman)
- Downtown Edmond grain elevator

Equip with:
- Pi 5 + Hailo-8 AI module
- AREDN + Meshtastic radios
- Solar/LiFePO₄ for resiliency

---

You're now ready to prototype your own AI-assisted mesh gateway.
