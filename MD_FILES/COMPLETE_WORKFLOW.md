# Complete ML Workflow - Training to Deployment

## 🎓 Understanding the Workflow

### Phase 1: Training (Offline)
**Input:** `training_fraud_data.csv` (100 transactions WITH labels)
**Process:** Train Mahout Random Forest model
**Output:** `mahout-model/random_forest_model.pkl` (trained model)

### Phase 2: Deployment (Real-time)
**Input:** `credit_card_transactions.csv` (20 transactions WITHOUT labels)
**Process:** Stream through Kafka → Classify with trained model
**Output:** Separate databases (fraud vs legitimate)

---

## 📋 Step-by-Step Instructions

### STEP 1: Install Dependencies
```bash
cd ~/fraud-detection-bigdata  # or /mnt/c/fraud-detection-bigdata
source venv/bin/activate
pip install kafka-python pandas
```

### STEP 2: Train the Model (FIRST!)
```bash
python3 train_model.py
```

**You'll see:**
```
======================================================================
MAHOUT RANDOM FOREST TRAINING
======================================================================

Loading training data...
✓ Loaded 100 transactions
  - Fraudulent: 30
  - Legitimate: 70

Training Random Forest with 4 decision trees...
✓ Tree 1 - Amount threshold: $1000
✓ Tree 1 - Distance threshold: 380.5 km
✓ Tree 2 - Frequency threshold: 4 transactions
✓ Tree 3 - High-risk categories: [2, 5, 8]
✓ Tree 4 - Very high amount: $2800.00

✓ Training Accuracy: 95.00%

✓ Model saved to: mahout-model/random_forest_model.pkl
✓ Model info saved to: mahout-model/model_info.txt

======================================================================
TRAINING COMPLETE!
======================================================================
```

**This creates:**
- `mahout-model/random_forest_model.pkl` ← Trained model
- `mahout-model/model_info.txt` ← Model metadata

### STEP 3: Start Kafka Infrastructure
```bash
# Terminal 1 - Zookeeper
cd ~/kafka
bin/zookeeper-server-start.sh config/zookeeper.properties

# Terminal 2 - Kafka
cd ~/kafka
bin/kafka-server-start.sh config/server.properties

# Terminal 3 - Create Topic
cd ~/kafka
bin/kafka-topics.sh --create --topic credit-card-transactions \
  --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### STEP 4: Run Consumer (Loads Trained Model)
```bash
cd ~/fraud-detection-bigdata
source venv/bin/activate
python3 kafka_consumer.py
```

**You'll see:**
```
✓ Loaded trained Mahout Random Forest model
  Model parameters: 6 decision tree thresholds
Fraud Detection Consumer Started
Waiting for Kafka connection...
Listening for transactions on topic: credit-card-transactions
```

### STEP 5: Run Producer (Sends Unlabeled Data)
```bash
# New terminal
cd ~/fraud-detection-bigdata
source venv/bin/activate
python3 kafka_producer.py
```

**Producer sends unlabeled transactions:**
```
Sent: TXN001 - Amount: $45.50
Sent: TXN002 - Amount: $1250.00
...
```

**Consumer classifies using trained model:**
```
📊 Processing Transaction #1: TXN001
   Amount: $45.50
   Category: grocery
   Distance from home: 2.5 km
  ✓  LEGITIMATE - Stored in legitimate database
----------------------------------------------------------------------
📊 Processing Transaction #2: TXN002
   Amount: $1250.00
   Category: electronics
   Distance from home: 450.0 km
  ⚠️  FRAUD DETECTED - Stored in fraud database (score: 0.70)
----------------------------------------------------------------------
```

### STEP 6: View Results
```bash
python3 view_results.py
```

---

## 🔗 The Complete Linkage

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 1: TRAINING                            │
└─────────────────────────────────────────────────────────────────┘

training_fraud_data.csv (labeled)
    ↓
    ↓ [100 transactions with fraud labels]
    ↓
train_model.py
    ↓
    ↓ [Learns patterns: thresholds, categories, scores]
    ↓
mahout-model/random_forest_model.pkl (trained model)


┌─────────────────────────────────────────────────────────────────┐
│                PHASE 2: REAL-TIME DEPLOYMENT                    │
└─────────────────────────────────────────────────────────────────┘

credit_card_transactions.csv (unlabeled)
    ↓
    ↓ [20 transactions WITHOUT labels]
    ↓
kafka_producer.py (sends to Kafka every 5 sec)
    ↓
    ↓ [Kafka streaming]
    ↓
kafka_consumer.py
    ↓
    ↓ [Loads trained model: random_forest_model.pkl]
    ↓
    ↓ [Applies learned thresholds to classify]
    ↓
    ├─→ legitimate_transactions.db (predicted as legit)
    └─→ fraudulent_transactions.db (predicted as fraud)
```

---

## 🎯 Key Points for Your Professor

1. **Two separate datasets:**
   - `training_fraud_data.csv` = labeled (for training)
   - `credit_card_transactions.csv` = unlabeled (for testing)

2. **Training happens FIRST:**
   - Model learns patterns from historical data
   - Saves learned parameters (thresholds, categories)

3. **Consumer loads trained model:**
   - Reads `random_forest_model.pkl`
   - Uses learned parameters for classification
   - NO hardcoded thresholds!

4. **Real-time classification:**
   - New unlabeled data → Kafka → Trained model → Prediction
   - Results stored in separate databases

---

## 🧪 To Retrain Model

If you get new fraud data:
```bash
# Add more rows to training_fraud_data.csv
# Then retrain:
python3 train_model.py

# Restart consumer (it will load the new model):
python3 kafka_consumer.py
```

---

## ✅ This is the CORRECT ML Workflow!

Training data (labeled) → Train model → Save model → Load model → Classify new data (unlabeled) → Store predictions

Perfect for your demo! 🎯
