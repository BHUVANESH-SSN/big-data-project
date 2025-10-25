# Complete Reset - Clear All Cache and Data

## 🚨 Problem: Old messages appear when running consumer/producer

**Reason:** Kafka stores messages and consumer offsets. When you restart, old messages are still in the topic!

---

## ✅ Solution 1: Automated Reset Script (EASIEST!)

### Run the Python reset script:
```bash
cd ~/fraud-detection-bigdata  # or /mnt/c/fraud-detection-bigdata
python3 full_reset.py
```

**This clears:**
- ✓ Both SQLite databases
- ✓ Kafka topic (deletes old messages)
- ✓ Consumer group (clears offset cache)
- ✓ Verifies everything is clean

---

## ✅ Solution 2: Bash Script (WSL/Linux)

```bash
cd ~/fraud-detection-bigdata
chmod +x reset_everything.sh
bash reset_everything.sh
```

---

## ✅ Solution 3: Manual Commands (Step by Step)

### Step 1: Delete Databases
```bash
cd ~/fraud-detection-bigdata
rm -f legitimate_transactions.db fraudulent_transactions.db
```

### Step 2: Delete Kafka Topic
```bash
cd ~/kafka
bin/kafka-topics.sh --delete \
  --topic credit-card-transactions \
  --bootstrap-server localhost:9092
```

Wait 5 seconds, then:

### Step 3: Recreate Fresh Topic
```bash
bin/kafka-topics.sh --create \
  --topic credit-card-transactions \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1
```

### Step 4: Delete Consumer Group (Clear Offset Cache)
```bash
bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --delete \
  --group fraud-detection-group
```

### Step 5: Verify Topic is Empty
```bash
bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic credit-card-transactions \
  --from-beginning \
  --timeout-ms 2000
```
Should show nothing (empty topic)!

---

## 🎬 Complete Demo Workflow (Fresh Start)

```bash
# 1. RESET EVERYTHING (run this FIRST!)
cd ~/fraud-detection-bigdata
python3 full_reset.py

# 2. Start Kafka (if not running)
# Terminal 1: Zookeeper
cd ~/kafka
bin/zookeeper-server-start.sh config/zookeeper.properties

# Terminal 2: Kafka Server
cd ~/kafka
bin/kafka-server-start.sh config/server.properties

# 3. Start Consumer (fresh, no old messages)
cd ~/fraud-detection-bigdata
source venv/bin/activate
python3 kafka_consumer.py

# 4. Start Producer (sends fresh data)
# New terminal
cd ~/fraud-detection-bigdata
source venv/bin/activate
python3 kafka_producer.py
```

---

## 🔍 How to Check if Reset Worked

### Check databases don't exist:
```bash
ls -la *.db
# Should show: No such file or directory
```

### Check topic is empty:
```bash
cd ~/kafka
bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic credit-card-transactions \
  --from-beginning \
  --timeout-ms 2000
# Should show: nothing (timeout after 2 seconds)
```

### Check consumer group is deleted:
```bash
bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --list
# Should NOT show: fraud-detection-group
```

---

## 💡 Why This Happens

**Kafka behavior:**
- Stores all messages in topics (persistent)
- Remembers where each consumer stopped reading (offset)
- When consumer restarts, it continues from last position OR reads all old messages

**Solution:**
- Delete topic = removes all old messages
- Delete consumer group = resets offset tracking
- Create fresh topic = start completely clean

---

## ⚡ Quick Reset (One Command)

```bash
cd ~/fraud-detection-bigdata && python3 full_reset.py
```

That's it! Run this before EVERY demo to ensure clean start! 🎯

---

## 📋 Before Each Demo Checklist:

- [ ] Run `python3 full_reset.py`
- [ ] Verify databases deleted
- [ ] Verify topic is empty
- [ ] Start consumer FIRST
- [ ] Then start producer
- [ ] Watch fresh transactions flow!

✅ No more old cached data! 🚀
