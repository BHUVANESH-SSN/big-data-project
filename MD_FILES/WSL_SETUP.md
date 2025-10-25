# Quick Start Guide - WSL/Linux Version

## Running in WSL

### STEP 1: Install Python Package
```bash
cd ~/fraud-detection-bigdata
pip install kafka-python
```

### STEP 2: Start Zookeeper (Terminal 1)
```bash
cd ~/kafka  # or wherever you installed Kafka
bin/zookeeper-server-start.sh config/zookeeper.properties
```
**Keep this terminal running!**

### STEP 3: Start Kafka Server (Terminal 2)
Open new WSL terminal:
```bash
cd ~/kafka
bin/kafka-server-start.sh config/server.properties
```
**Keep this terminal running!**

### STEP 4: Setup Kafka Topic (Terminal 3)
Open new WSL terminal:
```bash
cd ~/fraud-detection-bigdata
python3 setup_kafka.py
```

### STEP 5: Start Consumer (Same Terminal 3)
```bash
python3 kafka_consumer.py
```
**Keep this terminal running!**

### STEP 6: Start Producer (Terminal 4)
Open new WSL terminal:
```bash
cd ~/fraud-detection-bigdata
python3 kafka_producer.py
```

### STEP 7: View Results (Terminal 5)
```bash
cd ~/fraud-detection-bigdata
python3 view_results.py
```

## Quick Commands Summary:

**Terminal 1:** `bin/zookeeper-server-start.sh config/zookeeper.properties`
**Terminal 2:** `bin/kafka-server-start.sh config/server.properties`
**Terminal 3:** `python3 kafka_consumer.py`
**Terminal 4:** `python3 kafka_producer.py`
**Terminal 5:** `python3 view_results.py`

That's it! 🚀
