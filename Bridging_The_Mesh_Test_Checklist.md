
# 🧪 Bridging the Mesh - Demo & Testing Checklist

Use this checklist to verify your full mesh bridging system works from end to end. This is ideal for live demos, dry runs, or validating your deployment.

---

## ✅ 1. Hardware Setup

- [ ] Raspberry Pi 5 or reComputer is powered on and accessible via SSH
- [ ] Meshtastic node is connected to Pi via USB and recognized as `/dev/ttyUSB0`
- [ ] AREDN node is reachable (tunneled or RF)
- [ ] Ethernet or WiFi network is active
- [ ] MQTT broker is installed (Mosquitto) and running on the Pi
- [ ] Node-RED is installed and accessible at `http://<pi-ip>:1880`

---

## ✅ 2. Software & Scripts

- [ ] `mqtt_bridge.py` is present and updated with latest version
- [ ] Script runs without error (`python3 mqtt_bridge.py`)
- [ ] You see terminal output showing incoming Meshtastic messages
- [ ] Python dependencies are installed: `paho-mqtt`, `requests`, `meshtastic`, `pyserial`

---

## ✅ 3. MQTT Communication

- [ ] Mosquitto broker is active (`sudo systemctl status mosquitto`)
- [ ] `mosquitto_pub` and `mosquitto_sub` work locally
- [ ] Message published to `from_aredn` appears in LoRa network
- [ ] Message received from Meshtastic is published to `from_meshtastic`

---

## ✅ 4. AI Message Classification

- [ ] TinyLLaMA is downloaded and running with:
```bash
python3 -m llama_cpp.server --model tiny-llama.gguf --port 8000
```

- [ ] `curl` test returns valid output from local AI endpoint
- [ ] Messages like `"HELP FLOOD"` are flagged and published to:
  ```
  alerts/emergency
  ```

---

## ✅ 5. Node-RED Dashboard

- [ ] Node-RED flow is imported from `mesh-alert-dashboard-flow.json`
- [ ] Flow is deployed without errors
- [ ] UI is visible at `http://<pi-ip>:1880/ui`
- [ ] Messages flagged by AI appear in the dashboard

---

## ✅ 6. Live Simulation Test

- [ ] Use Meshtastic app to send: `"HELP I’m trapped under tree"`
- [ ] Message appears in terminal from `mqtt_bridge.py`
- [ ] AI classifies it → Flagged as emergency
- [ ] Message appears on MQTT topic `alerts/emergency`
- [ ] Node-RED dashboard shows alert in UI

---

## 🧠 Optional Expansions

- [ ] Attach GPS-enabled Meshtastic node → track positions
- [ ] Use `mosquitto_pub` to simulate AREDN alerts
- [ ] Add second MBU node at remote site
- [ ] Add local web dashboard or info portal

---

## 🏁 Final Check

- [ ] End-to-end path confirmed:
  - LoRa → MQTT → AI → MQTT → Node-RED → UI
  - AREDN → MQTT → LoRa

Print this checklist or save as a PDF before demo day.
