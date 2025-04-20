# Bridging the Mesh

**Hybrid Meshtastic + AREDN Gateway** powered by Raspberry Pi and Edge AI  
Built for resilient communications, off-grid sensor monitoring, and local mesh automation.

---

## 🔥 Features

- 🔄 MQTT-based message bridging (LoRa ↔ AREDN)
- 🧠 Local AI assistant with TinyLLaMA or Phi-2 for keyword detection
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

## 🚀 Quick Start

See full setup instructions in  
📄 [`Bridging_The_Mesh_Deployment_Guide.md`](Bridging_The_Mesh_Deployment_Guide.md)

---

## ⚙️ Python Bridge Script

- Located in: [`mqtt_bridge.py`](mqtt_bridge.py)
- Bridges MQTT traffic between AREDN (IP) and Meshtastic (LoRa)
- Compatible with the Meshtastic Python API and paho-mqtt

---

## 🧰 Node-RED Alert Flow

File: [`mesh-alert-dashboard-flow.json`](mesh-alert-dashboard-flow.json)

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

## 🔐 Compliance

This project follows FCC Part 97 guidelines by:
- Broadcasting only unencrypted or publicly shared-key messages
- Identifying ham-band AREDN traffic by callsign at gateway level
- Filtering and alerting locally (not altering RF packets)

---

## 🤝 Contribute

This is an evolving prototype. We’re inviting developers, hams, and tinkerers to get involved in testing, expanding, and building out use cases.

---

## 📄 License

MIT License – see `LICENSE` for details.

---

## 🌐 Project Page (Coming Soon)

To be hosted on GitHub Pages or project site.  
Use this repo to track updates, submit ideas, and collaborate.

