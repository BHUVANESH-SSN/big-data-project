#!/bin/bash

# Complete Reset Script - Clean Everything Before Demo
# Clears databases, Kafka topics, and consumer groups

echo "======================================================================"
echo "           COMPLETE PROJECT RESET - FRESH DEMO START"
echo "======================================================================"
echo ""

# Set paths
PROJECT_DIR=~/BIG_DATA_PROJECT
KAFKA_DIR=~/kafka

# Navigate to project directory
cd $PROJECT_DIR

# Step 1: Delete databases
echo "Step 1: Deleting SQLite databases..."
if [ -f "legitimate_transactions.db" ]; then
    rm -f legitimate_transactions.db
    echo "  ✓ Deleted legitimate_transactions.db"
else
    echo "  - legitimate_transactions.db doesn't exist"
fi

if [ -f "fraudulent_transactions.db" ]; then
    rm -f fraudulent_transactions.db
    echo "  ✓ Deleted fraudulent_transactions.db"
else
    echo "  - fraudulent_transactions.db doesn't exist"
fi
echo ""

# Step 2: Check if Kafka is running
echo "Step 2: Checking Kafka connection..."
$KAFKA_DIR/bin/kafka-broker-api-versions.sh --bootstrap-server localhost:9092 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "  ✓ Kafka is running"
    
    # Step 3: Delete Kafka topic
    echo ""
    echo "Step 3: Deleting Kafka topic..."
    $KAFKA_DIR/bin/kafka-topics.sh --delete \
      --topic credit-card-transactions \
      --bootstrap-server localhost:9092 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "  ✓ Topic deleted (waiting 3 seconds for cleanup...)"
        sleep 3
    else
        echo "  - Topic might not exist (that's ok)"
    fi
    
    # Step 4: Recreate fresh topic
    echo ""
    echo "Step 4: Creating fresh Kafka topic..."
    $KAFKA_DIR/bin/kafka-topics.sh --create \
      --topic credit-card-transactions \
      --bootstrap-server localhost:9092 \
      --partitions 1 \
      --replication-factor 1 2>&1 | grep -q "Created topic"
    
    if [ $? -eq 0 ]; then
        echo "  ✓ Fresh topic created"
    else
        echo "  ⚠️  Topic creation had issues (might already exist)"
    fi
    
    # Step 5: Delete consumer group
    echo ""
    echo "Step 5: Deleting consumer group..."
    $KAFKA_DIR/bin/kafka-consumer-groups.sh \
      --bootstrap-server localhost:9092 \
      --delete \
      --group fraud-detection-group 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "  ✓ Consumer group deleted (offset cache cleared)"
    else
        echo "  - Consumer group might not exist (that's ok)"
    fi
    
    # Step 6: Verify topic is empty
    echo ""
    echo "Step 6: Verifying topic is empty..."
    MESSAGE_COUNT=$($KAFKA_DIR/bin/kafka-console-consumer.sh \
      --bootstrap-server localhost:9092 \
      --topic credit-card-transactions \
      --from-beginning \
      --timeout-ms 2000 2>/dev/null | wc -l)
    
    echo "  ✓ Messages in topic: $MESSAGE_COUNT (should be 0)"
    
else
    echo "  ⚠️  Kafka is not running!"
    echo ""
    echo "  Please start Kafka first:"
    echo "    Terminal 1: cd ~/kafka && bin/zookeeper-server-start.sh config/zookeeper.properties"
    echo "    Terminal 2: cd ~/kafka && bin/kafka-server-start.sh config/server.properties"
    echo ""
    echo "  Then run this reset script again."
fi

echo ""
echo "======================================================================"
echo "                      RESET COMPLETE!"
echo "======================================================================"
echo ""
echo "✅ Databases cleared"
if [ $? -eq 0 ]; then
    echo "✅ Kafka topic reset"
    echo "✅ Consumer group cleared"
fi
echo ""
echo "Everything is now clean and fresh. Ready for demo!"
echo ""
echo "Next steps:"
echo "  1. Start consumer: python3 kafka_consumer.py"
echo "  2. Start producer: python3 kafka_producer.py"
echo ""
echo "======================================================================"
