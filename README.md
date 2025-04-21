
# 🛰️ Bridging the Mesh

**A Hybrid Emergency Gateway for LoRa + AREDN + AI**  
Created by: **KJ5IUL (Supergremlin25)** | Oklahoma City

---

## 🌐 Overview

Bridging the Mesh is a beta-stage open-source project designed to connect **Meshtastic LoRa mesh networks** with **AREDN high-speed IP mesh nodes**, enhanced with lightweight **AI classification** and **Node-RED dashboards**.

This system enables **offline, resilient communication** during emergencies or infrastructure outages using low-cost, repurposed gear.

---

## 🔧 Features

- 🔁 MQTT-based message bridging: LoRa <-> AREDN
- 🧠 AI assistant (TinyLLaMA): Flags terms like "HELP", "FIRE", "EMERGENCY"
- 📊 Node-RED dashboard: Displays real-time messages and alerts
- 🔋 Fully off-grid deployable: Solar + LiFePO₄ + field-ready Pi units
- 🧰 Tested on Raspberry Pi, FemtoFox, MikroTik hAP ac, Ubiquiti nodes
- 📡 Extends LoRa range using AREDN backbone
- 💬 Designed for hams, preppers, educators & civic mesh deployments

---

## 📥 Getting Started

Use the resources below to clone, configure, and run your first MeshBridging Unit (MBU).

- 📄 [Installation Guide](./INSTALL.md) — How to clone, install, and run everything  
- 📦 [Python Dependencies](./requirements.txt) — Required packages  
- 🧭 [Deployment Guide (Wiki)](https://github.com/SuperGremlin25/bridging-the-mesh/wiki/Deployment-Guide)

---

## 🚀 Quick Start

```bash
git clone https://github.com/SuperGremlin25/bridging-the-mesh.git
cd bridging-the-mesh
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python mqtt_bridge.py
```

---

## 🛠 Hardware Reference

**MeshBridging Unit (MBU)**
- Raspberry Pi 4 or Seeed reComputer R2130-12 (Pi 5 + Hailo-8)
- Meshtastic LoRa Node (T-Beam or FemtoFox)
- AREDN node (MikroTik hAP ac2 or Ubiquiti NanoStation)
- LiFePO₄ Battery + Solar Panel (optional)
- MQTT Broker (on Pi or external)
- Node-RED server (optional dashboard)

---

## 🧪 Testing Goals (Beta Phase)

- Validate LoRa → MQTT → AREDN routing
- Confirm AI classifier detects alerts correctly
- Monitor stability on low-power setups (Raspberry Pi)
- Test bidirectional communication and map routing

---

## 📘 Documentation & Extras

- 🧾 [AREDN Flashing Guide (PDF)](./AREDN_Flashing_Field_Guide.pdf)
- 🧠 [AI Assistant Integration Notes](./ai_assistant_integration.md)
- 📄 [Printable Test Checklist](./Test_Checklist.md)
- 📊 Node-RED JSON Flows available in `/nodered_flows/`

---

## 🧠 Project Status

This is a **beta prototype** designed to show what’s possible — not a polished consumer system. We're calling on radio experts, coders, and tinkerers to help test, refine, and scale this across Oklahoma and beyond.

---

## 📣 Get Involved

Pull requests, issues, and forks welcome!

- 🤝 Collaborator Onboarding → See CONTRIBUTING.md (coming soon)
- 🗨️ Join the discussion: Facebook / Discord / Reddit (share links here)
- 🛠️ Project built by: [SuperGremlin25](https://github.com/SuperGremlin25)

---

## 🔖 License

This project is released under the MIT License. See [LICENSE](./LICENSE) for details.

## Visual Diagram of Repo

<pre>
```text
bridging-the-mesh/
├── mqtt_bridge.py                  # Main bridge script
├── mqtt_bridge.conf                # Configuration file for MQTT, AI, and LoRa
├── requirements.txt                # Python package dependencies
├── INSTALL.md                      # Installation instructions
├── README.md                       # Project overview and usage
├── ai_assistant_integration.md     # Guide for integrating the AI assistant
├── Bridging_The_Mesh_Deployment_Guide.md
├── Bridging_The_Mesh_Test_Checklist.md
├── Project_Overview_OnePager.md
├── NodeRED_Flow_Setup.md
├── MQTT_Setup.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── ISSUES_STARTER_PACK.md
├── mesh-alert-dashboard-flow.json  # Node-RED dashboard flow export
├── wiki/                            # GitHub Wiki pages
│   └── (multiple .md files)



