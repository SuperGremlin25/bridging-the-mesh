
# How to Use the Node-RED Flow JSON (For Beginners)

This guide walks you through how to load the included Node-RED flow file `mesh-alert-dashboard-flow.json` and connect it to your MQTT broker. This process requires no programming and can be done in your browser.

---

## ✅ Prerequisites

Before you begin, make sure:

- Node-RED is installed and running on your Raspberry Pi
- Your MQTT broker (Mosquitto) is running on the same Pi
- Your Pi is connected to your local network

---

## 🚀 Step-by-Step Instructions

### 1. Open Node-RED in Your Browser

From a device on your network, go to:
```
http://<your-pi-ip>:1880
```

For example:
```
http://192.168.1.42:1880
```

---

### 2. Import the Flow JSON

1. In Node-RED, click the **☰ (menu icon)** in the top-right corner
2. Select **Import**
3. Click **Upload**, and choose the file:  
   `mesh-alert-dashboard-flow.json`
4. Click **Import**

You should now see a flow that includes:

- An MQTT Input node
- A function node to check if the message contains "HELP"
- A UI display and a debug node

---

### 3. Deploy the Flow

Click the **red "Deploy"** button in the top-right corner of the editor.  
Your flow is now live and listening for MQTT messages.

---

### 4. View the Dashboard

In your browser, visit:
```
http://<your-pi-ip>:1880/ui
```

You’ll see a simple dashboard.  
When a message with the word `HELP` comes through, it will trigger an alert.

---

## 🧪 Testing the Flow

If your Python bridge is running and a message like `"HELP FLOOD"` comes through from Meshtastic:

- It will be flagged by the AI (TinyLLaMA)
- The message will be published to MQTT topic: `alerts/emergency`
- The Node-RED flow will display it on your dashboard

---

## 💡 Customize Later

You can expand this flow to:

- Add more keyword filters
- Forward messages via email or SMS
- Display maps or charts using GPS/location data

This file (`mesh-alert-dashboard-flow.json`) is just a starting point.

