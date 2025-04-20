
# Bridging the Mesh: Full Deployment Guide (Beginner-Friendly)

This guide walks you through setting up the Bridging the Mesh project—linking AREDN and Meshtastic networks using a Raspberry Pi-based AI gateway. You’ll build a device that listens to both networks, routes messages via MQTT, and uses AI to flag urgent events.

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
5. Boot Pi and connect via SSH: `ssh pi@raspberrypi.local` (default password: `raspberry`)

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

Access Node-RED at: `http://<pi-ip>:1880`

---

## 🔌 STEP 5: Connect Meshtastic Device

Plug your Meshtastic node (e.g. FemtoFox) into the Pi via USB.

Check it’s recognized:
```bash
ls /dev/ttyUSB*
```

---

## 📜 STEP 6: Setup Python Bridge Script

1. Copy `mqtt_bridge.py` from this repo
2. Make sure it's executable:
```bash
chmod +x mqtt_bridge.py
```
3. Run it:
```bash
python3 mqtt_bridge.py
```

---

## 🧠 STEP 7: Add AI Assistant

1. Download the TinyLLaMA model:
```bash
wget https://huggingface.co/johnsmith0031/tiny-llama-v0-GGUF/resolve/main/tiny-llama.gguf
```

2. Start the LLM server:
```bash
python3 -m llama_cpp.server --model tiny-llama.gguf --port 8000
```

3. The script will now query this AI over REST for incoming messages and flag any containing critical terms (e.g. “HELP”, “FIRE”) to a special topic.

---

## 🧪 STEP 8: Test End-to-End

- Use Meshtastic app or CLI to send a message like: `HELP FLOOD`
- Watch it get flagged by the Pi’s AI and published to MQTT topic: `alerts/emergency`
- Send MQTT messages from AREDN to topic `from_aredn` and confirm delivery to LoRa
- Observe Node-RED dashboard updates at: `http://<pi-ip>:1880/ui`

---

## 📡 STEP 9: Optional Mesh Expansion

Deploy additional MeshBridging Units (MBUs) at high elevation points with:

- reComputer R2130-12 + Hailo-8
- AREDN 2.4/5 GHz radios (MikroTik)
- Meshtastic radio over LoRa
- Solar + LiFePO₄ for off-grid power

Suggested test deployments:
- Strata Tower (OKC)
- OU Science Bldg (Norman)
- Grain elevator (Edmond)

---

## 📚 Summary

You’ve now built a decentralized radio gateway that:
- Bridges IP and LoRa mesh messaging
- Classifies messages locally using offline AI
- Publishes alerts in real time via MQTT
- Can be monitored and automated via Node-RED

This architecture enables hyper-resilient mesh communications for emergency, sensor, and public service use.

