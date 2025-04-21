# 🧰 Bridging the Mesh – Installation Guide

This guide helps you get the MQTT bridge, Meshtastic/AREDN integration, and AI assistant up and running.

---

## 🚀 Quick Setup (Recommended)

If you're using Linux or Raspberry Pi, use the `setup.sh` script:

```bash
chmod +x setup.sh
./setup.sh
```

This script will:
- ✅ Set up a virtual Python environment
- 📦 Install all required dependencies
- ⚙️ Offer to launch the AI assistant (Flask server)
- 🔁 Start the MQTT bridge if you choose

---

## 🛠️ Manual Setup (Advanced)

### 1. Clone the Repository

```bash
git clone https://github.com/SuperGremlin25/bridging-the-mesh.git
cd bridging-the-mesh
```

### 2. Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Edit the Configuration File

Edit `mqtt_bridge.conf` to match your environment:

- MQTT broker (e.g. Mosquitto)
- Meshtastic serial device (e.g. /dev/ttyUSB0)
- AI endpoint URL
- Topics and alerts

---

## 🧠 Start AI Assistant (Optional)

If you're using local classification:

```bash
python3 -m flask --app ai_assistant_integration run --port=8000
```

Make sure your `.conf` file points to that port.

---

## 🔁 Run the Bridge

```bash
python mqtt_bridge.py
```

This connects to your Meshtastic radio, your MQTT broker, and starts listening for bidirectional messages.

---

## 🧪 Testing

- Send a message from a Meshtastic node and watch it flow to MQTT.
- Use keywords like “HELP” or “FIRE” to test AI classification (if enabled).
- Watch console logs or your dashboard (Node-RED or Grafana) for routing activity.

---

## 📚 Related Docs

- `ai_assistant_integration.md` – Guide to AI module
- `mqtt_bridge.conf` – Required configuration settings
- `requirements.txt` – Dependency list
- `README.md` – Project overview