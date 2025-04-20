# 🛰️ Bridging the Mesh – Project Overview

**What if we could merge low-power LoRa messaging and high-speed ham radio mesh into one seamless, AI-powered network?**

Bridging the Mesh is an open-source initiative to unify **Meshtastic** and **AREDN** using MQTT, edge AI, and Raspberry Pi-based gateways.

---

## 🚀 What It Does

- Connects **Meshtastic LoRa nodes** to **AREDN IP networks**
- Bridges messages in real time via MQTT
- Uses on-device **AI (TinyLLaMA)** to classify emergency messages
- Displays alerts in **Node-RED dashboards**
- All fully **offline-capable** (solar-ready)

---

## 📡 How It Works

1. A message is sent over LoRa (e.g. “HELP at Elm & 5th”)
2. The Pi receives it via USB and classifies it using a local LLM
3. If flagged urgent, it publishes to a shared MQTT broker
4. AREDN relays it to other areas or displays it in Node-RED

---

## 🧱 Hardware Stack

- Raspberry Pi 5 or reComputer R2130-12
- Meshtastic node (FemtoFox, T-Beam, RAK4631)
- AREDN node (MikroTik hAP ac2 or Ubiquiti)
- Solar + LiFePO₄ (optional)

---

## 🧠 AI Assistant

Runs offline on-device:
- Classifies messages like “TRAPPED”, “FLOOD”, “911”
- Publishes alerts to: `alerts/emergency`
- Future: multi-message summarization, NLP triage

---

## 🧰 Tools Used

| Component | Role |
|----------|------|
| MQTT (Mosquitto) | Real-time message broker |
| Node-RED | Dashboard & automations |
| llama-cpp-python | LLM backend |
| Meshtastic Python API | LoRa input/output |
| AREDN | High-speed RF/IP mesh backbone |

---

## 💡 Why It Matters

This project brings **true hybrid mesh networking** to life:
- Leverages both license-free and Part 97 bands
- Enables city-wide alerting with pocket-sized radios
- Prepares for emergency use when internet and cell fail
- Scales from hobbyist projects to CERT and SAR teams

---

## 🙋‍♂️ Get Involved

- Clone or fork this repo:  
  `https://github.com/Supergremlin25/bridging-the-mesh`
- Try the [Deployment Guide](../../wiki/Deployment-Guide)
- Contribute code, test setups, or hardware feedback
- Join the OKC Mesh community on Facebook or GitHub

Together, we’re building resilient comms for the next generation.

---

## 👨‍🔧 Maintainer

Project created and maintained by **KJ5IUL**  
Oklahoma City-based amateur radio operator and mesh enthusiast.  
GitHub: [Supergremlin25](https://github.com/Supergremlin25)
