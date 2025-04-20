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
