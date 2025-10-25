# Bash Script Usage Guide

## 📝 Available Bash Scripts

### 1. `train.sh` - Train the ML Model
**Purpose:** Trains the Mahout Random Forest model on historical fraud data

**Usage:**
```bash
cd ~/BIG_DATA_PROJECT
./train.sh
```

**What it does:**
- ✓ Checks/creates virtual environment
- ✓ Activates venv
- ✓ Installs dependencies if needed
- ✓ Runs `train_model.py`
- ✓ Shows next steps

**Output:**
```
======================================================================
            MAHOUT RANDOM FOREST MODEL TRAINING
======================================================================

Activating virtual environment...
Checking dependencies...
Starting training...

✓ Loaded 100 transactions
  - Fraudulent: 30
  - Legitimate: 70

Training Random Forest with 4 decision trees...
✓ Training Accuracy: 95.00%
✓ Model saved to: mahout-model/random_forest_model.pkl

======================================================================
Training complete!
======================================================================
```

---

### 2. `reset.sh` - Complete Project Reset
**Purpose:** Clears all data and resets Kafka for fresh demo

**Usage:**
```bash
cd ~/BIG_DATA_PROJECT
./reset.sh
```

**What it does:**
- ✓ Deletes both SQLite databases
- ✓ Deletes Kafka topic (removes old messages)
- ✓ Recreates fresh empty topic
- ✓ Deletes consumer group (clears offset cache)
- ✓ Verifies topic is empty

**Output:**
```
======================================================================
           COMPLETE PROJECT RESET - FRESH DEMO START
======================================================================

Step 1: Deleting SQLite databases...
  ✓ Deleted legitimate_transactions.db
  ✓ Deleted fraudulent_transactions.db

Step 2: Checking Kafka connection...
  ✓ Kafka is running

Step 3: Deleting Kafka topic...
  ✓ Topic deleted (waiting 3 seconds for cleanup...)

Step 4: Creating fresh Kafka topic...
  ✓ Fresh topic created

Step 5: Deleting consumer group...
  ✓ Consumer group deleted (offset cache cleared)

Step 6: Verifying topic is empty...
  ✓ Messages in topic: 0 (should be 0)

======================================================================
                      RESET COMPLETE!
======================================================================

✅ Databases cleared
✅ Kafka topic reset
✅ Consumer group cleared
```

---

## 🚀 Complete Demo Workflow Using Bash Scripts

### Before Demo:

```bash
# 1. Reset everything (clean slate)
cd ~/BIG_DATA_PROJECT
./reset.sh

# 2. Train model (if not already trained)
./train.sh
```

### During Demo:

```bash
# Terminal 1: Start Zookeeper
cd ~/kafka
bin/zookeeper-server-start.sh config/zookeeper.properties

# Terminal 2: Start Kafka
cd ~/kafka
bin/kafka-server-start.sh config/server.properties

# Terminal 3: Start Consumer
cd ~/BIG_DATA_PROJECT
source venv/bin/activate
python3 kafka_consumer.py

# Terminal 4: Start Producer
cd ~/BIG_DATA_PROJECT
source venv/bin/activate
python3 kafka_producer.py

# Terminal 5: View Results (after some transactions)
cd ~/BIG_DATA_PROJECT
source venv/bin/activate
python3 view_results.py
```

---

## 🔄 Python vs Bash Scripts

### Training:
- **Bash:** `./train.sh` - Handles venv activation automatically
- **Python:** `python3 train_model.py` - Requires manual venv activation

### Reset:
- **Bash:** `./reset.sh` - Single command, handles everything
- **Python:** `python3 full_reset.py` - Needs Python/venv activated

### Recommendation:
- **Use bash scripts** for quick demo setup (easier, less typing)
- **Use Python scripts** if you want more control or debugging

---

## 💡 Quick Commands Reference

```bash
# Make scripts executable (if not already)
chmod +x train.sh reset.sh

# Train model
./train.sh

# Reset before each demo
./reset.sh

# Check if scripts are executable
ls -lh *.sh
# Should show: -rwxr-xr-x (x means executable)
```

---

## ⚠️ Troubleshooting

### Script permission denied:
```bash
chmod +x train.sh reset.sh
```

### Kafka not running (for reset.sh):
```bash
# Start Kafka first:
cd ~/kafka
bin/zookeeper-server-start.sh config/zookeeper.properties &
bin/kafka-server-start.sh config/server.properties &

# Wait 10 seconds, then run reset
cd ~/BIG_DATA_PROJECT
./reset.sh
```

### Python dependencies missing:
```bash
# Manually install
source venv/bin/activate
pip install -r requirements.txt
```

---

## ✅ Benefits of Bash Scripts

1. **Faster:** One command instead of multiple steps
2. **Automatic:** Handles venv activation for you
3. **Cleaner:** Better output formatting
4. **Safer:** Checks before executing
5. **Professional:** Shows you know bash scripting

Perfect for your demo tonight! 🚀
