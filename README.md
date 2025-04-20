# Bridging the Mesh

**Hybrid Meshtastic + AREDN Gateway** powered by Raspberry Pi and Edge AI  
Built for resilient communications, off-grid sensor monitoring, and local mesh automation.

---

## 🔥 Features

- 🔄 MQTT-based message bridging (LoRa ↔ AREDN)
- 🧠 Local AI assistant with TinyLLaMA for keyword detection
- 🧰 Node-RED dashboards for live message visualization
- 📡 FCC Part 97 compliant (via public shared key or open channel)
- 🌐 Fully offline-capable deployment (solar + LiFePO₄ supported)

---

## 🧱 Hardware Required

| Component | Example |
|----------|--------|
| MeshBridging Unit (MBU) | Raspberry Pi 5 / reComputer R2130-12 |
| LoRa Radio | FemtoFox / T-Beam / RAK4631 |
| AREDN Router | MikroTik hAP ac2 or ac lite |
| Power | USB-C or PoE splitter |
| Optional | Solar + LiFePO₄ battery, Ethernet switch |

---

## ⚙️ Python Bridge Script

- Located in: `mqtt_bridge.py`
- Bridges MQTT traffic between AREDN (IP) and Meshtastic (LoRa)
- Compatible with Meshtastic Python API and paho-mqtt

---

## 🧰 Node-RED Alert Flow

File: `mesh-alert-dashboard-flow.json`

### What it does:
- Subscribes to `from_meshtastic`
- Filters messages containing `"HELP"`
- Sends dashboard alerts
- Logs messages in debug

### How to use:
1. Visit `http://<pi-ip>:1880`
2. Menu > **Import** → Upload the JSON
3. Click **Deploy**
4. Open dashboard at `http://<pi-ip>:1880/ui`

---

## 🤖 AI Assistant

- TinyLLaMA model runs locally on Hailo-8 (or CPU fallback)
- REST API used by `mqtt_bridge.py` to classify message priority
- Publishes flagged messages to `alerts/emergency`

---

## 🔐 Compliance

This project follows FCC Part 97 guidelines by:
- Broadcasting only unencrypted or publicly shared-key messages
- Identifying ham-band AREDN traffic by callsign at gateway level
- Filtering and alerting locally (not altering RF packets)

---

## 📄 License

MIT License – see `LICENSE` for details.


## 📡 Project Lead  
Developed by **KJ5IUL** (Supergremlin25)  
Oklahoma City, OK  
Licensed Amateur Radio Operator

You can also get in touch through:
- Oklahoma Meshtastic Telegram - https://t.me/OKMeshtastic
- OK DMR & Digital - https://t.me/OK_DMR_digital
- OK 650 Discord Server - https://discord.gg/feVDqnVD
- GitHub Issues & Discussions
