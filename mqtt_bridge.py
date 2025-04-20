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
        "device": "",  # Empty for auto-detection
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

# Load configuration from file or create default
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

# Extract configuration values
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

# Global variables
iface = None
client = None
running = True
message_queue = Queue(maxsize=QUEUE_SIZE)

# Connect to Meshtastic device with retry
def connect_meshtastic():
    global iface
    
    for attempt in range(MESH_RECONNECT_ATTEMPTS):
        try:
            logger.info(f"Connecting to Meshtastic device (attempt {attempt+1}/{MESH_RECONNECT_ATTEMPTS})...")
            if MESHTASTIC_DEVICE:
                iface = meshtastic.serial_interface.SerialInterface(devPath=MESHTASTIC_DEVICE)
            else:
                iface = meshtastic.serial_interface.SerialInterface()
                
            iface.onReceive = onReceive
            logger.info("Successfully connected to Meshtastic device")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Meshtastic device: {e}")
            if attempt < MESH_RECONNECT_ATTEMPTS - 1:
                logger.info(f"Retrying in {MESH_RECONNECT_DELAY} seconds...")
                time.sleep(MESH_RECONNECT_DELAY)
    
    logger.critical("Could not connect to Meshtastic device after multiple attempts")
    return False

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")
        client.subscribe(TOPIC_FROM_AREDN)
        logger.info(f"Subscribed to {TOPIC_FROM_AREDN}")
    else:
        logger.error(f"Failed to connect to MQTT broker, return code: {rc}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.warning("Unexpected disconnection from MQTT broker")
        while running and not client.is_connected():
            try:
                logger.info("Attempting to reconnect to MQTT broker...")
                client.reconnect()
                time.sleep(1)
            except Exception as e:
                logger.error(f"Reconnection failed: {e}")
                time.sleep(RETRY_INTERVAL)

def setup_mqtt_client():
    client = mqtt.Client()
    
    # Set up authentication if provided
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_aredn_msg
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
        return client
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {e}")
        return None

def classify_with_ai(message):
    if not AI_ENABLED:
        return ""
        
    try:
        res = requests.post(
            AI_SERVICE_URL, 
            json={
                "prompt": f"Classify this message: {message}",
                "max_tokens": 30
            }, 
            timeout=AI_TIMEOUT
        )
        
        if res.status_code == 200:
            return res.json().get("content", "").lower()
        else:
            logger.warning(f"AI service returned status code: {res.status_code}")
        return ""
    except requests.exceptions.Timeout:
        logger.warning("AI classification request timed out")
        return ""
    except Exception as e:
        logger.error(f"AI classification error: {e}")
        return ""

def onReceive(packet):
    if not running:
        return
        
    try:
        msg = packet.get("decoded", {}).get("text")
        if not msg:
            return
            
        logger.info(f"[LoRa > MQTT]: {msg}")
        
        # Try AI classification
        classification = classify_with_ai(msg)
        
        # Publish to MQTT
        if client and client.is_connected():
            client.publish(TOPIC_FROM_MESH, msg)
            
            if "emergency" in classification or "alert" in classification:
                logger.warning(f"⚠️ AI FLAGGED: {msg}")
                client.publish(TOPIC_ALERTS, msg)
        else:
            # Queue message for later if MQTT is disconnected
            try:
                message_queue.put_nowait({
                    "type": "to_mqtt",
                    "payload": msg,
                    "is_alert": "emergency" in classification or "alert" in classification
                })
                logger.info("Message queued for later delivery")
            except Full:
                logger.warning("Message queue is full, discarding oldest message")
                message_queue.get()  # Remove oldest message
                message_queue.put({
                    "type": "to_mqtt",
                    "payload": msg,
                    "is_alert": "emergency" in classification or "alert" in classification
                })
    except Exception as e:
        logger.error(f"Error processing received message: {e}")

def on_aredn_msg(client, userdata, message):
    if not running:
        return
        
    try:
        decoded = message.payload.decode()
        logger.info(f"[AREDN > LoRa]: {decoded}")
        
        if iface:
            iface.sendText(decoded)
        else:
            # Queue message for later if Meshtastic is disconnected
            try:
                message_queue.put_nowait({
                    "type": "to_mesh",
                    "payload": decoded
                })
                logger.info("Message queued for later delivery to mesh")
            except Full:
                logger.warning("Message queue is full, discarding oldest message")
                message_queue.get()  # Remove oldest message
                message_queue.put({
                    "type": "to_mesh",
                    "payload": decoded
                })
    except Exception as e:
        logger.error(f"Error forwarding AREDN message: {e}")

def process_queue():
    """Process any queued messages"""
    if message_queue.empty():
        return
        
    # Process up to 10 messages per cycle to prevent blocking
    for _ in range(min(10, message_queue.qsize())):
        if message_queue.empty():
            break
            
        try:
            message = message_queue.get_nowait()
            
            if message["type"] == "to_mqtt" and client and client.is_connected():
                client.publish(TOPIC_FROM_MESH, message["payload"])
                if message.get("is_alert", False):
                    client.publish(TOPIC_ALERTS, message["payload"])
                logger.info("Delivered queued message to MQTT")
                message_queue.task_done()
                
            elif message["type"] == "to_mesh" and iface:
                iface.sendText(message["payload"])
                logger.info("Delivered queued message to mesh network")
                message_queue.task_done()
                
            else:
                # Put the message back in the queue
                message_queue.put(message)
                break
                
        except Exception as e:
            logger.error(f"Error processing queued message: {e}")
            # Put the message back in the queue
            try:
                message_queue.put(message)
            except Full:
                pass
            break

def cleanup():
    """Clean up connections before exiting"""
    global running
    logger.info("Shutting down...")
    running = False
    
    # Stop MQTT loop and disconnect
    if client:
        client.loop_stop()
        client.disconnect()
        
    # Close Meshtastic connection
    if iface:
        try:
            iface.close()
        except:
            pass
    
    logger.info("All connections closed")

def signal_handler(sig, frame):
    """Handle interrupt signals"""
    logger.info("Interrupt received, shutting down...")
    cleanup()
    sys.exit(0)

def main():
    global client, iface
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("Starting MQTT-Meshtastic bridge...")
    
    # Connect to Meshtastic
    if not connect_meshtastic():
        logger.error("Could not initialize Meshtastic interface. Exiting.")
        return
    
    # Connect to MQTT broker
    client = setup_mqtt_client()
    if not client:
        logger.error("Could not connect to MQTT broker. Exiting.")
        return
    
    # Start MQTT loop
    client.loop_start()
    
    logger.info("Bridge is running...")
    
    try:
        # Main processing loop
        while running:
            # Process any queued messages
            process_queue()
            
            # Check if connections are alive
            if not client.is_connected():
                logger.warning("MQTT connection lost, attempting to reconnect...")
                try:
                    client.reconnect()
                except Exception as e:
                    logger.error(f"MQTT reconnection failed: {e}")
            
            # Try to reconnect to Meshtastic if needed
            if not iface or not hasattr(iface, "_SpotInterface__consumer") or not iface._SpotInterface__consumer.is_alive():
                logger.warning("Meshtastic connection appears to be down, attempting to reconnect...")
                connect_meshtastic()
            
            time.sleep(1)
    except Exception as e:
        logger.critical(f"Unhandled exception in main loop: {e}")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
