"""
Kafka Producer - Sends credit card transactions every 5 seconds
Simulates real-time transaction stream
"""
import csv
import json
import time
from kafka import KafkaProducer

def create_producer():
    """Create Kafka producer instance"""
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer

def send_transactions(csv_file='credit_card_transactions.csv'):
    """Read CSV and send transactions every 5 seconds"""
    producer = create_producer()
    topic = 'credit-card-transactions'
    
    print("Starting to send transactions...")
    print(f"Sending one transaction every 5 seconds to topic: {topic}\n")
    
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            # Convert row to dictionary and send
            transaction = {
                'transaction_id': row['transaction_id'],
                'amount': float(row['amount']),
                'time': row['time'],
                'merchant_category': row['merchant_category'],
                'distance_from_home': float(row['distance_from_home']),
                'transaction_count_1h': int(row['transaction_count_1h'])
            }
            
            producer.send(topic, value=transaction)
            print(f"Sent: {transaction['transaction_id']} - Amount: ${transaction['amount']}")
            
            time.sleep(5)  # Wait 5 seconds before next transaction
    
    producer.flush()
    producer.close()
    print("\nAll transactions sent successfully!")

if __name__ == '__main__':
    try:
        send_transactions()
    except Exception as e:
        print(f"Error: {e}")
