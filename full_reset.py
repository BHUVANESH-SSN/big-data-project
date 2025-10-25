"""
Complete Python Reset Script
Clears all databases, Kafka topics, and consumer groups
Run this before each demo to start fresh
"""
import os
import subprocess
import time

def clear_databases():
    """Delete SQLite database files"""
    print("\n🗑️  Step 1: Clearing databases...")
    databases = ['legitimate_transactions.db', 'fraudulent_transactions.db']
    
    for db in databases:
        if os.path.exists(db):
            os.remove(db)
            print(f"  ✓ Deleted {db}")
        else:
            print(f"  - {db} doesn't exist")
    print("  ✓ Databases cleared\n")

def reset_kafka_topic(kafka_dir):
    """Delete and recreate Kafka topic"""
    print("🔄 Step 2: Resetting Kafka topic...")
    
    # Delete topic
    try:
        subprocess.run([
            f"{kafka_dir}/bin/kafka-topics.sh",
            "--delete",
            "--topic", "credit-card-transactions",
            "--bootstrap-server", "localhost:9092"
        ], capture_output=True, timeout=10)
        print("  ✓ Deleted old topic")
        time.sleep(3)
    except Exception as e:
        print(f"  - Topic might not exist: {e}")
    
    # Create fresh topic
    try:
        result = subprocess.run([
            f"{kafka_dir}/bin/kafka-topics.sh",
            "--create",
            "--topic", "credit-card-transactions",
            "--bootstrap-server", "localhost:9092",
            "--partitions", "1",
            "--replication-factor", "1"
        ], capture_output=True, text=True, timeout=10)
        
        if "Created topic" in result.stdout or "already exists" in result.stderr:
            print("  ✓ Fresh topic created")
        else:
            print(f"  ⚠️  {result.stdout}")
    except Exception as e:
        print(f"  ✗ Error creating topic: {e}")
    
    print()

def reset_consumer_group(kafka_dir):
    """Delete consumer group to reset offsets"""
    print("🔄 Step 3: Resetting consumer group...")
    
    try:
        subprocess.run([
            f"{kafka_dir}/bin/kafka-consumer-groups.sh",
            "--bootstrap-server", "localhost:9092",
            "--delete",
            "--group", "fraud-detection-group"
        ], capture_output=True, timeout=10)
        print("  ✓ Consumer group deleted (offset cache cleared)")
    except Exception as e:
        print(f"  - Group might not exist: {e}")
    
    print()

def verify_clean(kafka_dir):
    """Verify topic is empty"""
    print("✅ Step 4: Verifying everything is clean...")
    
    try:
        result = subprocess.run([
            f"{kafka_dir}/bin/kafka-console-consumer.sh",
            "--bootstrap-server", "localhost:9092",
            "--topic", "credit-card-transactions",
            "--from-beginning",
            "--timeout-ms", "2000"
        ], capture_output=True, text=True, timeout=5)
        
        message_count = len([line for line in result.stdout.split('\n') if line.strip()])
        print(f"  ✓ Messages in topic: {message_count} (should be 0)")
        
        if message_count == 0:
            print("  ✓ Topic is empty and clean!")
        else:
            print("  ⚠️  Topic still has messages. Try running reset again.")
    except Exception as e:
        print(f"  - Could not verify: {e}")
    
    print()

if __name__ == '__main__':
    print("="*70)
    print("           COMPLETE PROJECT RESET - FRESH DEMO START")
    print("="*70)
    
    # Detect Kafka directory
    kafka_dirs = [
        os.path.expanduser("~/kafka"),
        "/mnt/c/kafka",
        os.path.expanduser("~/kafka_2.13-3.6.0")
    ]
    
    kafka_dir = None
    for kdir in kafka_dirs:
        if os.path.exists(kdir):
            kafka_dir = kdir
            break
    
    if not kafka_dir:
        print("\n⚠️  Kafka directory not found!")
        print("Please enter your Kafka installation path:")
        kafka_dir = input("Kafka path: ").strip()
    
    print(f"\nUsing Kafka: {kafka_dir}\n")
    
    # Run all cleanup steps
    clear_databases()
    reset_kafka_topic(kafka_dir)
    reset_consumer_group(kafka_dir)
    verify_clean(kafka_dir)
    
    print("="*70)
    print("                      RESET COMPLETE!")
    print("="*70)
    print("\n✅ Everything is now clean and fresh. Ready for demo!\n")
    print("Next steps:")
    print("  1. Start consumer: python3 kafka_consumer.py")
    print("  2. Start producer: python3 kafka_producer.py")
    print("\n" + "="*70 + "\n")
