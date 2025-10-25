# Training Data Explanation

## File: `training_fraud_data.csv`

This is your **labeled historical dataset** for training the Mahout model.

### Structure:

```
amount,distance_from_home,transaction_count_1h,merchant_category_encoded,label
45.50,2.5,1,1,0
1250.00,450.0,1,2,1
```

### Features (Columns 1-4):

1. **`amount`** - Transaction amount in dollars
2. **`distance_from_home`** - Distance from home in kilometers
3. **`transaction_count_1h`** - Number of transactions in past hour
4. **`merchant_category_encoded`** - Numeric code for merchant type
   - 1 = grocery
   - 2 = electronics
   - 3 = restaurant
   - 4 = clothing
   - 5 = jewelry
   - 6 = gas_station
   - 7 = online_service
   - 8 = travel
   - 9 = pharmacy
   - 10 = entertainment
   - 11 = convenience

### Label (Column 5):

- **`label`** - Historical classification
  - 0 = Legitimate transaction
  - 1 = Fraudulent transaction

### Dataset Stats:

- **Total records:** 100 transactions
- **Fraudulent:** ~30 transactions (30%)
- **Legitimate:** ~70 transactions (70%)
- **Features:** 4 numeric features
- **Classes:** 2 (binary classification)

### Why This Data?

This labeled data is what you would use to **train** the Mahout model. In production:
1. Collect historical credit card transactions
2. Label them as fraud/legitimate (from investigations)
3. Use this data to train the Random Forest
4. Deploy the trained model for real-time classification

### How to Use:

```bash
cd ~/fraud-detection-bigdata

# Run the training script
bash train_mahout_model.sh
```

This creates the model that your `kafka_consumer.py` uses for classification!

---

## Important Note:

The **`credit_card_transactions.csv`** file (without label) is your **test/production data** that flows through Kafka.

The **`training_fraud_data.csv`** file (with label) is your **training data** used to build the model.

This is the correct approach! ✓
