#!/bin/bash

# Train Mahout Random Forest Model
# This script trains the fraud detection model on historical data

echo "======================================================================"
echo "            MAHOUT RANDOM FOREST MODEL TRAINING"
echo "======================================================================"
echo ""

# Navigate to project directory
cd ~/BIG_DATA_PROJECT

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "Checking dependencies..."
pip show pandas > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip install -r requirements.txt
fi

echo ""
echo "Starting training..."
echo "======================================================================"
echo ""

# Run training script
python3 train_model.py

echo ""
echo "======================================================================"
echo "Training complete!"
echo "======================================================================"
echo ""
echo "Next steps:"
echo "  1. Start Kafka infrastructure (Zookeeper + Kafka)"
echo "  2. Run consumer: python3 kafka_consumer.py"
echo "  3. Run producer: python3 kafka_producer.py"
echo ""
echo "======================================================================"
