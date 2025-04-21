#!/bin/bash

echo "🔧 Setting up Bridging the Mesh environment..."

# Step 1: Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3 before continuing."
    exit 1
fi

# Step 2: Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv

# Step 3: Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Step 4: Install dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 5: Offer to start AI assistant
read -p "🤖 Start Flask AI assistant server? (y/n): " start_ai
if [[ $start_ai == "y" ]]; then
    echo "⚙️  Starting AI assistant server..."
    python3 -m flask --app ai_assistant_integration run --port=8000 &
fi

# Step 6: Offer to start MQTT bridge
read -p "🔁 Start MQTT Bridge now? (y/n): " start_bridge
if [[ $start_bridge == "y" ]]; then
    echo "🚀 Launching mqtt_bridge.py..."
    python mqtt_bridge.py
else
    echo "✅ Setup complete. Run the bridge later using:"
    echo "    source venv/bin/activate && python mqtt_bridge.py"
fi
