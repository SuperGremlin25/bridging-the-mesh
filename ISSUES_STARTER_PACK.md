## 1. [BUG] Meshtastic message not forwarded to AREDN reliably

Sometimes messages received from Meshtastic don't appear to make it to the AREDN MQTT topic. Possibly a rate-limiting, serial, or message buffer issue?

**Steps to Reproduce:**
1. Send repeated messages via Meshtastic CLI or app
2. Monitor AREDN mesh interface via MQTT
3. Check for dropped or delayed messages

Expected behavior: Messages consistently appear on `from_meshtastic` topic and get routed to AREDN.

Please test and log any pattern or failure condition you discover.

---
## 2. [ENHANCEMENT] Add GPS coordinate handling to MQTT bridge

Meshtastic packets include GPS data which could be parsed and published to a separate topic like `gps/position`.

This would allow dashboarding in Node-RED or third-party map viewers.

**Possible approach:**
- Extract `position` field from the decoded packet
- Format as JSON or NMEA-like string
- Publish to `gps/position` or `location/<device_id>`

---
## 3. [TASK] Document how to replace TinyLLaMA with Phi-2

Phi-2 is a more performant model that may run on-device or via LAN server.

Create a new markdown file (`ai_model_swap.md`) with:
- Setup instructions for running Phi-2 using llama-cpp-python or Ollama
- Model download links
- How to update `classify_with_ai()` to use new endpoint

Tag as `documentation` and `ai`.

---
## 4. [QUESTION] Can we add Node-RED alerts via SMS or email?

If a user has cell service, an emergency alert coming from the mesh could be escalated to SMS or email.

Requesting help from someone with Twilio/email experience to integrate this into Node-RED.

Bonus: Add a toggle in dashboard UI to activate/deactivate notifications.

---
## 5. [FEATURE] Create install.sh for one-command Raspberry Pi setup

Create a simple bash script that installs:
- Mosquitto
- Node-RED
- Python requirements
- Sets up systemd service for `mqtt_bridge.py`

Goal: make this plug-and-play for newcomers deploying MBUs.

---
