import time
import signal
import sys
import json
import logging
import os
from queue import Queue, Full
import paho.mqtt.client as mqtt
import meshtastic
import meshtastic.serial_interface
import requests
from configparser import ConfigParser

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("mqtt_bridge.log")
    ]
)
logger = logging.getLogger("mqtt_bridge")

# Configuration with defaults
CONFIG_FILE = "mqtt_bridge.conf"
config = ConfigParser()

# Default configuration
default_config = {
    "mqtt": {
        "broker": "localhost",
        "port": 1883,
        "keepalive": 60,
        "username": "",
        "password": "",
        "topic_from_mesh": "from_meshtastic",
        "topic_from_aredn": "from_aredn",
        "topic_alerts": "alerts/emergency"
    },
    "meshtastic": {
        "device": "",
        "reconnect_attempts": 5,
        "reconnect_delay": 10
    },
    "ai_service": {
        "url": "http://localhost:8000/completion",
        "timeout": 5,
        "enabled": True
    },
    "general": {
        "queue_size": 100,
        "retry_interval": 30
    }
}

# Load configuration
def load_config():
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        logger.info(f"Configuration loaded from {CONFIG_FILE}")
    else:
        for section, options in default_config.items():
            if not config.has_section(section):
                config.add_section(section)
            for key, value in options.items():
                config.set(section, key, str(value))
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
        logger.info(f"Default configuration created at {CONFIG_FILE}")

load_config()

MQTT_BROKER = config.get("mqtt", "broker")
MQTT_PORT = config.getint("mqtt", "port")
MQTT_KEEPALIVE = config.getint("mqtt", "keepalive")
MQTT_USERNAME = config.get("mqtt", "username")
MQTT_PASSWORD = config.get("mqtt", "password")
TOPIC_FROM_MESH = config.get("mqtt", "topic_from_mesh")
TOPIC_FROM_AREDN = config.get("mqtt", "topic_from_aredn")
TOPIC_ALERTS = config.get("mqtt", "topic_alerts")

MESHTASTIC_DEVICE = config.get("meshtastic", "device")
MESH_RECONNECT_ATTEMPTS = config.getint("meshtastic", "reconnect_attempts")
MESH_RECONNECT_DELAY = config.getint("meshtastic", "reconnect_delay")

AI_SERVICE_URL = config.get("ai_service", "url")
AI_TIMEOUT = config.getint("ai_service", "timeout")
AI_ENABLED = config.getboolean("ai_service", "enabled")

QUEUE_SIZE = config.getint("general", "queue_size")
RETRY_INTERVAL = config.getint("general", "retry_interval")

iface = None
client = None
running = True
message_queue = Queue(maxsize=QUEUE_SIZE)

def connect_meshtastic():
    global iface
    for attempt in range(MESH_RECONNECT_ATTEMPTS):
        try:
            logger.info(f"Connecting to Meshtastic device (attempt {attempt+1}/{MESH_RECONNECT_ATTEMPTS})...")
            iface = meshtastic.serial_interface.SerialInterface(devPath=MESHTASTIC_DEVICE) if MESHTASTIC_DEVICE else meshtastic.serial_interface.SerialInterface()
            iface.onReceive = onReceive
            logger.info("Successfully connected to Meshtastic device")
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            time.sleep(MESH_RECONNECT_DELAY)
    return False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")
        client.subscribe(TOPIC_FROM_AREDN)
    else:
        logger.error(f"Failed to connect to MQTT broker: {rc}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.warning("Unexpected MQTT disconnection")
        while running and not client.is_connected():
            try:
                client.reconnect()
            except Exception as e:
                logger.error(f"MQTT reconnection failed: {e}")
                time.sleep(RETRY_INTERVAL)

def setup_mqtt_client():
    client = mqtt.Client()
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_aredn_msg
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        return client
    except Exception as e:
        logger.error(f"MQTT connect error: {e}")
        return None

def classify_with_ai(message):
    if not AI_ENABLED:
        return ""
    try:
        res = requests.post(AI_SERVICE_URL, json={"prompt": f"Classify this message: {message}", "max_tokens": 30}, timeout=AI_TIMEOUT)
        return res.json().get("content", "").lower() if res.status_code == 200 else ""
    except Exception as e:
        logger.warning(f"AI classification error: {e}")
        return ""

def onReceive(packet):
    if not running:
        return
    try:
        msg = packet.get("decoded", {}).get("text")
        if not msg:
            return
        logger.info(f"[LoRa > MQTT]: {msg}")
        classification = classify_with_ai(msg)
        if client and client.is_connected():
            client.publish(TOPIC_FROM_MESH, msg)
            if "emergency" in classification or "alert" in classification:
                logger.warning(f"⚠️ AI FLAGGED: {msg}")
                client.publish(TOPIC_ALERTS, msg)
        else:
            enqueue_message("to_mqtt", msg, "emergency" in classification or "alert" in classification)
    except Exception as e:
        logger.error(f"Error onReceive: {e}")

def on_aredn_msg(client, userdata, message):
    if not running:
        return
    try:
        decoded = message.payload.decode()
        logger.info(f"[AREDN > LoRa]: {decoded}")
        if iface:
            iface.sendText(decoded)
        else:
            enqueue_message("to_mesh", decoded)
    except Exception as e:
        logger.error(f"Error forwarding AREDN message: {e}")

def enqueue_message(msg_type, payload, is_alert=False):
    try:
        message_queue.put_nowait({
            "type": msg_type,
            "payload": payload,
            "is_alert": is_alert
        })
    except Full:
        logger.warning("Queue full, discarding oldest message")
        message_queue.get()
        message_queue.put({
            "type": msg_type,
            "payload": payload,
            "is_alert": is_alert
        })

def process_queue():
    if message_queue.empty():
        return
    for _ in range(min(10, message_queue.qsize())):
        try:
            message = message_queue.get_nowait()
            if message["type"] == "to_mqtt" and client and client.is_connected():
                client.publish(TOPIC_FROM_MESH, message["payload"])
                if message.get("is_alert"):
                    client.publish(TOPIC_ALERTS, message["payload"])
            elif message["type"] == "to_mesh" and iface:
                iface.sendText(message["payload"])
            message_queue.task_done()
        except Exception as e:
            logger.error(f"Queue processing error: {e}")

def cleanup():
    global running
    running = False
    if client:
        client.loop_stop()
        client.disconnect()
    if iface:
        try:
            iface.close()
        except:
            pass
    logger.info("Shutdown complete")

def signal_handler(sig, frame):
    logger.info("Interrupt received, shutting down...")
    cleanup()
    sys.exit(0)

def main():
    global client, iface
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    logger.info("Starting MQTT-Meshtastic bridge...")
    if not connect_meshtastic():
        return
    client = setup_mqtt_client()
    if not client:
        return
    client.loop_start()
    while running:
        process_queue()
        time.sleep(1)
    cleanup()

if __name__ == "__main__":
    main()
