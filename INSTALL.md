
# 🧰 Installation Guide – Bridging the Mesh

This guide walks you through installing and running the Bridging the Mesh project on Linux or Raspberry Pi.

---

## 🚀 Quick Setup (Recommended)

For most users, the easiest way to get started is with our automated setup script:

```bash
chmod +x setup.sh
./setup.sh
```

This script will:
- ✅ Create a Python virtual environment
- 📦 Install all required dependencies (`requirements.txt`)
- 🤖 Optionally launch the Flask AI assistant
- 🔁 Optionally run the MQTT-Meshtastic bridge script

This method is ideal for Raspberry Pi or any Linux system.

---

## 🛠️ Manual Setup (Advanced / Alternate Option)

If you prefer manual installation, follow the steps below:

### 1. Clone the Repository

```bash
git clone https://github.com/SuperGremlin25/bridging-the-mesh.git
cd bridging-the-mesh
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Your `.conf` File

Edit `mqtt_bridge.conf` to set your:

- MQTT broker address and credentials
- Meshtastic device port
- AI assistant settings (URL, timeout, enable/disable)

### 5. Start the MQTT Bridge

```bash
python mqtt_bridge.py
```

### 6. (Optional) Start AI Classifier Flask Server

You can run a local Flask API to handle message classification:

```bash
python3 -m flask --app ai_assistant_integration run --port=8000
```

Make sure the `ai_service.url` in your `.conf` file points to this port.

---

## 🧪 Test Your Setup

- Send a message from a Meshtastic node.
- Watch it appear in your MQTT broker or AREDN dashboard.
- Try triggering alerts with keywords like "HELP" or "FIRE".

---

## 📚 Additional Resources

- [`ai_assistant_integration.md`](./ai_assistant_integration.md)
- [`mqtt_bridge.conf`](./mqtt_bridge.conf)
- [Project Wiki](https://github.com/SuperGremlin25/bridging-the-mesh/wiki)

---

Happy bridging!
