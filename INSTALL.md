
# 🛠️ Installation Guide – Bridging the Mesh

This guide walks you through setting up the development environment and running the Bridging the Mesh gateway.

---

## ✅ 1. Clone the Repository

```bash
git clone https://github.com/SuperGremlin25/bridging-the-mesh.git
cd bridging-the-mesh
```

---

## ✅ 2. Set Up Python Environment

We recommend using a virtual environment to avoid dependency issues.

```bash
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

---

## ✅ 3. Install Required Python Dependencies

Install required packages from the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install manually:

```bash
pip install paho-mqtt meshtastic flask weasyprint
```

> Note: You may need to install additional libraries for LLM support depending on your AI model (e.g., TinyLLaMA or local transformer).

---

## ✅ 4. Configure Your Hardware

Ensure the following hardware is connected and powered on:

- Raspberry Pi (or test machine)
- Meshtastic Node (via USB or UART)
- AREDN Router (via Ethernet or Tunnel)
- MQTT Broker (local or external)
- Optional: Node-RED and sensor devices

---

## ✅ 5. Run the Gateway Script

Run the Python bridge that connects Meshtastic <-> AREDN via MQTT.

```bash
python mqtt_bridge.py
```

---

## 🧪 Testing Setup

Once running, test the flow:

- Send a message from your Meshtastic device
- Check if it appears on the AREDN side (e.g., dashboard or message log)
- Try the reverse flow from AREDN → MQTT → Meshtastic

---

## 📎 Optional Tools

- [Node-RED](https://nodered.org) for live dashboards
- [Mosquitto](https://mosquitto.org) for your MQTT broker
- [AREDN Firmware](https://www.arednmesh.org/software) for flashing routers
- [TinyLLaMA](https://github.com/jzhang38/TinyLLaMA) for AI assistance (if using)

---

If you run into trouble, check the Deployment Guide or open an issue.
