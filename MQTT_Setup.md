
# Setting Up the MQTT Server on the Raspberry Pi

This guide explains how to install, configure, and test the Mosquitto MQTT broker on your MeshBridging Unit (MBU), typically a Raspberry Pi 5 or reComputer R2130-12.

---

## ✅ Why Run MQTT on the Pi?

- Keeps all services local and offline
- Allows your Python script, Node-RED, and AI engine to talk together
- Reduces complexity and increases resilience

---

## 🔧 Step-by-Step: Install Mosquitto on the Pi

### 1. Update and install Mosquitto
```bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
```

### 2. Enable and start the service
```bash
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

This runs Mosquitto in the background on port 1883 (default).

---

## 🧪 Test the Broker Locally

### Open two terminal windows:

**Terminal 1: Listen for messages**
```bash
mosquitto_sub -t "test/topic"
```

**Terminal 2: Send a message**
```bash
mosquitto_pub -t "test/topic" -m "Hello from MQTT!"
```

✅ You should see the message appear in the first terminal.

---

## 🧠 Using in the Python Bridge Script

In `mqtt_bridge.py`, this is how we connect:
```python
MQTT_BROKER = "localhost"
```

No further setup needed — your script and AI assistant can now publish/subscribe to topics on this local broker.

---

## 📊 Using in Node-RED

1. Open Node-RED at `http://<pi-ip>:1880`
2. Add an MQTT input or output node
3. Set the broker address to:
```
localhost:1883
```

You can now bridge traffic from Meshtastic, AREDN, and AI alerts through MQTT!

---

## 🔐 Optional: Add Security (Later)

If you expose your Pi to other users or the internet, consider:
- Adding a username/password file
- Enabling TLS encryption
- Restricting topics via access control

Let us know when you want to add those — they're not needed for local mesh use.

