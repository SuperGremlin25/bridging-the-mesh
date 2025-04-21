
# 🧠 AI Assistant Integration – Bridging the Mesh

This document explains how the AI assistant is integrated into the MQTT-Meshtastic-AREDN bridge and how to customize or replace the model used for message classification.

---

## ✅ How It Works

The AI assistant acts as a lightweight alert classifier running locally on a Raspberry Pi or low-power edge device. It inspects messages coming from the **Meshtastic LoRa network** and attempts to flag high-priority messages like emergency alerts.

- Messages are sent to the AI as prompts via a local Flask API.
- The AI response is parsed to check for keywords like `"emergency"`, `"fire"`, `"help"`, etc.
- If flagged, the message is published to a special MQTT alert topic (e.g. `alerts/emergency`).

---

## 🧩 Configuration Overview

All AI integration settings live in `mqtt_bridge.conf` under the `[ai_service]` section:

```ini
[ai_service]
url = http://localhost:8000/completion
timeout = 5
enabled = True
```

- `url`: Your AI model’s local Flask server endpoint
- `timeout`: Max seconds before a request is aborted
- `enabled`: Set to `False` to disable AI entirely

---

## 🧪 Sample Local Classifier API

You can build a very basic Flask-based AI server to serve a local LLM (like TinyLLaMA or a quantized model). Here's a simplified version:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/completion", methods=["POST"])
def classify():
    data = request.json
    msg = data.get("prompt", "").lower()
    if any(kw in msg for kw in ["help", "emergency", "fire", "trapped", "flood"]):
        return jsonify({"content": "emergency"})
    return jsonify({"content": "normal"})

if __name__ == "__main__":
    app.run(port=8000)
```

---

## 📦 Requirements for AI API

- Python 3.7+
- Flask (`pip install flask`)
- Optional: TinyLLaMA or quantized LLM
- Optional: Hailo-8 setup with inference engine (requires separate integration)

---

## 📣 Customizing Keyword Detection

Edit the AI backend logic to support your own filters, e.g.:

- Prioritize based on sender (call sign or location)
- Classify by urgency, severity, or category
- Summarize incoming traffic with LLM

---

## 🔧 Advanced Suggestions

- Log AI decisions to a separate topic (`logs/ai`)
- Include confidence scores or categories
- Route critical messages via multiple MQTT paths

---

## 📍 Conclusion

The AI integration is modular and optional. It is designed to act as a field-based triage tool for human net control operators. Your Python backend can be replaced with any model or API capable of parsing incoming messages and returning a classification label.

