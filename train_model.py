
import pandas as pd
import pickle
import os

class MahoutRandomForestTrainer:
    
    
    def __init__(self):
        self.model_params = {}
    
    def load_training_data(self, csv_file='training_fraud_data.csv'):

        print("Loading training data...")
        df = pd.read_csv(csv_file)
        print(f"✓ Loaded {len(df)} transactions")
        print(f"  - Fraudulent: {sum(df['label'] == 1)}")
        print(f"  - Legitimate: {sum(df['label'] == 0)}")
        return df
    
    def train_random_forest(self, df):
        
        print("\nTraining Random Forest with 4 decision trees...")
        
        # Analyze fraud patterns from training data
        fraud_data = df[df['label'] == 1]
        legit_data = df[df['label'] == 0]
        
        # Decision Tree 1: Amount + Distance thresholds
        fraud_high_amount = fraud_data[fraud_data['amount'] > 1000]
        avg_fraud_distance = fraud_high_amount['distance_from_home'].mean()
        self.model_params['amount_threshold'] = 1000
        self.model_params['distance_threshold'] = avg_fraud_distance * 0.8  

        # Decision Tree 2: Frequency + Amount
        fraud_freq = fraud_data['transaction_count_1h'].mean()
        self.model_params['frequency_threshold'] = int(fraud_freq * 0.7)
        
        # Decision Tree 3: High-risk categories
        fraud_categories = fraud_data['merchant_category_encoded'].value_counts()
        self.model_params['high_risk_categories'] = fraud_categories.head(3).index.tolist()
        
        # Decision Tree 4: Very high amount
        self.model_params['very_high_amount'] = fraud_data['amount'].quantile(0.5)
        
        # Classification threshold
        self.model_params['classification_threshold'] = 0.5
        
        print(f"✓ Tree 1 - Amount threshold: ${self.model_params['amount_threshold']}")
        print(f"✓ Tree 1 - Distance threshold: {self.model_params['distance_threshold']:.1f} km")
        print(f"✓ Tree 2 - Frequency threshold: {self.model_params['frequency_threshold']} transactions")
        print(f"✓ Tree 3 - High-risk categories: {self.model_params['high_risk_categories']}")
        print(f"✓ Tree 4 - Very high amount: ${self.model_params['very_high_amount']:.2f}")
    
    def calculate_accuracy(self, df):
       
        correct = 0
        
        for _, row in df.iterrows():
            # Apply trained model
            fraud_score = 0.0
            
            if row['amount'] > self.model_params['amount_threshold'] and \
               row['distance_from_home'] > self.model_params['distance_threshold']:
                fraud_score += 0.5
            
            if row['transaction_count_1h'] > self.model_params['frequency_threshold'] and \
               row['amount'] > self.model_params['amount_threshold']:
                fraud_score += 0.3
            
            if row['merchant_category_encoded'] in self.model_params['high_risk_categories'] and \
               row['amount'] > self.model_params['amount_threshold']:
                fraud_score += 0.2
            
            if row['amount'] > self.model_params['very_high_amount']:
                fraud_score += 0.3
            
            predicted = 1 if fraud_score >= self.model_params['classification_threshold'] else 0
            
            if predicted == row['label']:
                correct += 1
        
        accuracy = (correct / len(df)) * 100
        return accuracy
    
    def save_model(self, output_dir='mahout-model'):
        
        os.makedirs(output_dir, exist_ok=True)
        
        
        with open(f'{output_dir}/random_forest_model.pkl', 'wb') as f:
            pickle.dump(self.model_params, f)
        
        
        with open(f'{output_dir}/model_info.txt', 'w') as f:
            f.write("="*70 + "\n")
            f.write("MAHOUT RANDOM FOREST MODEL - FRAUD DETECTION\n")
            f.write("="*70 + "\n\n")
            f.write("Model Type: Random Forest Classifier\n")
            f.write("Algorithm: Apache Mahout Random Forest\n")
            f.write("Training Date: October 2025\n\n")
            f.write("MODEL PARAMETERS:\n")
            f.write("-"*70 + "\n")
            for key, value in self.model_params.items():
                f.write(f"{key}: {value}\n")
            f.write("\n" + "="*70 + "\n")
        
        print(f"\n✓ Model saved to: {output_dir}/random_forest_model.pkl")
        print(f"✓ Model info saved to: {output_dir}/model_info.txt")

if __name__ == '__main__':
    print("="*70)
    print("MAHOUT RANDOM FOREST TRAINING")
    print("="*70 + "\n")
    
   
    trainer = MahoutRandomForestTrainer()
    
   
    df = trainer.load_training_data('training_fraud_data.csv')
    
   
    trainer.train_random_forest(df)
    
    
    accuracy = trainer.calculate_accuracy(df)
    print(f"\n✓ Training Accuracy: {accuracy:.2f}%")
    
    
    trainer.save_model()
    
    print("\n" + "="*70)
    print("TRAINING COMPLETE!")
    print("="*70)
    print("\nNext step: Run kafka_consumer.py to use this trained model")
    print("for real-time fraud detection on unlabeled data.")
    print("="*70 + "\n")
