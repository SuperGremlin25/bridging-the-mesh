
# AI Assistant Integration (TinyLLaMA on Hailo-8)

This guide explains how to deploy a lightweight AI language model for real-time message classification in the Bridging the Mesh project.

## 🧠 Goal

Flag high-priority messages like:

- `HELP`
- `FLOOD`
- `FIRE`
- `TRAPPED`

## 🧰 Installation

### On Pi or reComputer:
```bash
pip3 install llama-cpp-python
wget https://huggingface.co/johnsmith0031/tiny-llama-v0-GGUF/resolve/main/tiny-llama.gguf
python3 -m llama_cpp.server --model tiny-llama.gguf --port 8000
```

## 🧪 Test the AI

```bash
curl http://localhost:8000/completion \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Classify: HELP FLOOD", "max_tokens":50}'
```

## 🔁 Python Integration

Add to `mqtt_bridge.py`:

```python
def classify_with_ai(message):
    res = requests.post("http://localhost:8000/completion", json={
        "prompt": f"Classify: {message}", "max_tokens": 30
    }, timeout=3)
    return res.json().get("content", "")
```

Use inside message handler to flag messages as emergency.
