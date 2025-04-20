
# Contributing to Bridging the Mesh

Thank you for your interest in improving this hybrid Meshtastic + AREDN gateway project. This system is designed to be modular, transparent, and community-driven.

---

## 🧭 Project Overview

This project builds a decentralized communications relay using:
- Meshtastic (LoRa, sensor, GPS)
- AREDN (IP backbone over ham radio)
- MQTT (for message transport)
- Node-RED (for dashboards and automations)
- Local AI (LLM text classification using TinyLLaMA or Phi2)

The Raspberry Pi-based MeshBridging Unit (MBU) sits between these layers.

---

## 💡 How You Can Contribute

### 🔍 Testing
- Run the Python bridge and verify end-to-end flow
- Validate Node-RED flow alert triggering
- Test AI classification accuracy (TinyLLaMA or other models)
- Try the deployment guide from scratch — look for pain points

### 🛠️ Development
- Improve the Python MQTT bridge (logging, error handling, reconnections)
- Extend Node-RED dashboard for maps, status boards, GPS tracking
- Add support for MQTT message logging or storage
- Refactor code to allow plug-and-play modules

### 🤖 AI Contributions
- Swap in Phi-2 or other lightweight models
- Improve classification prompts and keyword detection
- Add NLP summaries for high-traffic events

---

## 🧪 Local Testing (Recommended)

Set up your environment:
```bash
git clone https://github.com/Supergremlin25/bridging-the-mesh.git
cd bridging-the-mesh
pip3 install -r requirements.txt  # or install manually
```

Run the bridge:
```bash
python3 mqtt_bridge.py
```

---

## 🔥 Want to Help? Start Here

- Fork the repo
- Try the deployment guide or AI flow
- Open a GitHub issue for any bugs or enhancement ideas
- Or suggest new directions in Discussions

---

## 📫 Communication

You can also get in touch through:
- Oklahoma Meshtastic Telegram Channel - https://t.me/OKMeshtastic
- OK DMR and Digital - https//t.me/OK_DMR_digital
- GitHub Issues & Discussions

---

Let's build the next-gen emergency network together.
