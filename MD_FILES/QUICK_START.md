# Quick Start Guide - For Tonight's Demo

## Prerequisites
1. Download Kafka: https://kafka.apache.org/downloads
2. Extract to a simple path like `C:\kafka`

## Installation (5 minutes)

```powershell
cd C:\fraud-detection-bigdata
pip install kafka-python
```

## Running the Demo (3 Terminals)

### Terminal 1: Start Kafka
```powershell
# Start Zookeeper
cd C:\kafka
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

Wait 10 seconds, then open Terminal 2:

### Terminal 2: Start Kafka Server
```powershell
cd C:\kafka
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

Wait 10 seconds, then open Terminal 3:

### Terminal 3: Run the Application
```powershell
cd C:\fraud-detection-bigdata

# Create topic
python setup_kafka.py

# Start consumer (keep this running)
python kafka_consumer.py
```

Open Terminal 4:

### Terminal 4: Start Producer
```powershell
cd C:\fraud-detection-bigdata

# Start sending transactions
python kafka_producer.py
```

## View Results
After some transactions are processed:

```powershell
python view_results.py
```

## What You'll See

**Producer sends every 5 seconds:**
```
Sent: TXN001 - Amount: $45.50
Sent: TXN002 - Amount: $1250.00
```

**Consumer classifies in real-time:**
```
📊 Processing: TXN001
   Amount: $45.50
  ✓  LEGITIMATE - Stored in legitimate database

📊 Processing: TXN002
   Amount: $1250.00
  ⚠️  FRAUD DETECTED - Stored in fraud database (score: 0.70)
```

## Architecture Explained
- **CSV File** → Sample credit card transactions
- **Kafka Producer** → Sends 1 transaction every 5 seconds (real-time simulation)
- **Kafka** → Message broker for streaming data
- **Consumer with ML** → Fraud detection rules (simulating Mahout classifier)
- **2 SQLite Databases** → Separate storage for legitimate and fraud transactions

That's it! Simple and ready for demo.
