# 🔧 TROUBLESHOOTING: Consumer Not Receiving Messages

## Problem: Consumer shows "Listening..." but never processes transactions

### ✅ QUICK FIX - Try This First:

**Option 1: Start Producer FIRST, then Consumer**
```bash
# Terminal 1: Start producer first
source venv/bin/activate
python kafka_producer.py

# Wait 10 seconds, then in Terminal 2: Start consumer
source venv/bin/activate
python kafka_consumer.py
```

**Option 2: Reset Consumer Group**

If consumer was already running when producer sent messages, reset it:

```bash
# Stop consumer (Ctrl+C)

# Delete consumer group (this resets the offset)
cd ~/kafka
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --delete --group fraud-detection-group

# Now restart consumer
cd ~/fraud-detection-bigdata
source venv/bin/activate
python kafka_consumer.py
```

**Option 3: Use Troubleshooting Script**
```bash
source venv/bin/activate
python troubleshoot.py
```

This will show:
- Is Kafka running?
- Does the topic exist?
- Are there messages in the topic?

---

## Why This Happens:

Kafka consumers remember where they left off reading. If the consumer starts, it creates a "checkpoint" (offset). When producer sends messages BEFORE consumer starts, consumer might skip those old messages depending on its group ID.

## Best Practice for Demo:

**Order matters:**
1. Start Zookeeper
2. Start Kafka
3. Start Producer FIRST (let it send a few messages)
4. Then start Consumer (it will catch up and process all messages)

OR

1. Start Consumer FIRST
2. THEN start Producer
3. Consumer will process each message as it arrives

---

## Alternative: Always Read from Beginning

The consumer code already has `auto_offset_reset='earliest'` which should read from the beginning. If it's not working, the consumer group might have an existing offset stored.

**Solution:** Delete the consumer group offset (see Option 2 above)
