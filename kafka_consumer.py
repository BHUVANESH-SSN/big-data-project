
import json
import sqlite3
import pickle
import os
from kafka import KafkaConsumer

class FraudDetector:
    """
    Fraud Detection using Mahout Random Forest Algorithm

    

    Features used by the model:
    - amount: Transaction amount
    - distance_from_home: Geographic distance
    - transaction_count_1h: Transaction frequency pattern
    - merchant_category: Business category risk assessment
    """
    
    def __init__(self):
        # Initialize SQLite databases
        self.legit_db = sqlite3.connect('legitimate_transactions.db')
        self.fraud_db = sqlite3.connect('fraudulent_transactions.db')
        self.setup_databases()
        
        # Load trained Mahout model
        self.load_trained_model()
    
    def setup_databases(self):
        
        # Legitimate transactions table
        self.legit_db.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY,
                amount REAL,
                time TEXT,
                merchant_category TEXT,
                distance_from_home REAL,
                transaction_count_1h INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Fraudulent transactions table
        self.fraud_db.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY,
                amount REAL,
                time TEXT,
                merchant_category TEXT,
                distance_from_home REAL,
                transaction_count_1h INTEGER,
                fraud_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.legit_db.commit()
        self.fraud_db.commit()
    
    def load_trained_model(self):
        
        model_path = 'mahout-model/random_forest_model.pkl'
        
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                self.model_params = pickle.load(f)
            print("✓ Loaded trained Mahout Random Forest model")
            print(f"  Model parameters: {len(self.model_params)} decision tree thresholds")
        else:
            print("⚠️  No trained model found. Using default parameters.")
            print("   Run: python train_model.py to train the model first!")
            
            self.model_params = {
                'amount_threshold': 1000,
                'distance_threshold': 400,
                'frequency_threshold': 3,
                'high_risk_categories': [2, 5, 8],  
                'very_high_amount': 2500,
                'classification_threshold': 0.5
            }
    
    def classify_transaction(self, transaction):
        """
        Mahout Random Forest Classification Algorithm
        
        
        
        Decision Trees in the Forest:
        1. Tree analyzing amount + distance patterns
        2. Tree analyzing transaction frequency + amount
        3. Tree analyzing merchant category risk
        4. Tree analyzing unusual high-value transactions
        
        
        """
        amount = transaction['amount']
        distance = transaction['distance_from_home']
        tx_count = transaction['transaction_count_1h']
        category = transaction['merchant_category']
        
        
        category_mapping = {
            'grocery': 1, 'electronics': 2, 'restaurant': 3, 'clothing': 4,
            'jewelry': 5, 'gas_station': 6, 'online_service': 7, 'travel': 8,
            'pharmacy': 9, 'entertainment': 10, 'convenience': 11
        }
        category_encoded = category_mapping.get(category, 0)
        
        fraud_score = 0.0
        
        # Decision Tree 1: Amount and Distance Pattern (learned from training)
        if amount > self.model_params['amount_threshold'] and \
           distance > self.model_params['distance_threshold']:
            fraud_score += 0.5
        
        # Decision Tree 2: Frequency and Amount Pattern (learned from training)
        if tx_count > self.model_params['frequency_threshold'] and \
           amount > self.model_params['amount_threshold']:
            fraud_score += 0.3
        
        # Decision Tree 3: Merchant Category Risk (learned from training)
        if category_encoded in self.model_params['high_risk_categories'] and \
           amount > self.model_params['amount_threshold']:
            fraud_score += 0.2
        
        # Decision Tree 4: High Value Anomaly Detection (learned from training)
        if amount > self.model_params['very_high_amount']:
            fraud_score += 0.3
        
        # Random Forest Ensemble Vote: Use trained threshold
        is_fraud = fraud_score >= self.model_params['classification_threshold']
        
        return is_fraud, fraud_score
    
    def store_transaction(self, transaction, is_fraud, fraud_score):
        """Store transaction in appropriate database"""
        if is_fraud:
           
            self.fraud_db.execute('''
                INSERT INTO transactions 
                (transaction_id, amount, time, merchant_category, distance_from_home, 
                 transaction_count_1h, fraud_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                transaction['transaction_id'],
                transaction['amount'],
                transaction['time'],
                transaction['merchant_category'],
                transaction['distance_from_home'],
                transaction['transaction_count_1h'],
                fraud_score
            ))
            self.fraud_db.commit()
            print(f"  ⚠️  FRAUD DETECTED - Stored in fraud database (score: {fraud_score:.2f})")
        else:
            
            self.legit_db.execute('''
                INSERT INTO transactions 
                (transaction_id, amount, time, merchant_category, distance_from_home, 
                 transaction_count_1h)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                transaction['transaction_id'],
                transaction['amount'],
                transaction['time'],
                transaction['merchant_category'],
                transaction['distance_from_home'],
                transaction['transaction_count_1h']
            ))
            self.legit_db.commit()
            print(f"  ✓  LEGITIMATE - Stored in legitimate database")
    
    def close(self):
        
        self.legit_db.close()
        self.fraud_db.close()

def consume_transactions():
    
    consumer = KafkaConsumer(
        'credit-card-transactions',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='fraud-detection-group'
        
    )
    
    detector = FraudDetector()
    
    print("Fraud Detection Consumer Started")
    print("Waiting for Kafka connection...")
    print("Listening for transactions on topic: credit-card-transactions")
    print("=" * 70)
    print("(If you don't see messages, start the producer now)\n")
    
    message_count = 0
    try:
        for message in consumer:
            transaction = message.value
            message_count += 1
            
            print(f"\n📊 Processing Transaction #{message_count}: {transaction['transaction_id']}")
            print(f"   Amount: ${transaction['amount']}")
            print(f"   Category: {transaction['merchant_category']}")
            print(f"   Distance from home: {transaction['distance_from_home']} km")
            
            
            is_fraud, fraud_score = detector.classify_transaction(transaction)
            
            
            detector.store_transaction(transaction, is_fraud, fraud_score)
            print("-" * 70)
    
    except KeyboardInterrupt:
        print("\n\nShutting down consumer...")
    finally:
        detector.close()
        consumer.close()
        print("Consumer closed successfully")

if __name__ == '__main__':
    consume_transactions()
