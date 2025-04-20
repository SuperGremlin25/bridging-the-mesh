# Bridging the Mesh

This project bridges Meshtastic and AREDN networks using a Raspberry Pi running MQTT, Node-RED, and lightweight AI. It enables message routing, emergency keyword flagging, and offline dashboards for amateur radio operators.

## Features
- MQTT-based message bridging between Meshtastic and AREDN
- Local AI assistant using TinyLLaMA for offline message classification
- Node-RED dashboards and automation flows
- FCC Part 97 compliant communication using public shared-key encryption or unencrypted channels

## Hardware Required
- Raspberry Pi 5 or reComputer R2130-12
- Meshtastic device (e.g. FemtoFox, T-Beam, RAK4631)
- MikroTik hAP ac2 (running AREDN)
- Power supply, Ethernet cable, optional solar + battery

## Setup Instructions
See the [Deployment Guide](Bridging_The_Mesh_Deployment_Guide.md)

## 🧰 Node-RED Alert Flow

Included in this repo is a file called `mesh-alert-dashboard-flow.json`.

### What it does:
- Listens on the MQTT topic `from_meshtastic`
- Filters messages containing the word `HELP`
- Displays an alert on the Node-RED Dashboard (`/ui`)
- Logs all messages in the debug tab

### How to use:
1. Open your Node-RED editor at `http://<pi-ip>:1880`
2. Click the top-right menu → **Import**
3. Upload the file `mesh-alert-dashboard-flow.json`
4. Click **Import** and then **Deploy**
5. Open your dashboard at `http://<pi-ip>:1880/ui`
