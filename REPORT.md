# Project Details – Credit Card Fraud Detection

## Team Members
- **Bhuvanesh S**  
- **Harishkanna R**

## Project Title
**Credit Card Fraud Detection**

---

## Big Data Features Used
- Data ingestion with **Apache Kafka** (streaming producer and consumer)  
- Offline batch datasets for training and evaluation  
- Model training and preprocessing in **Python**  
- **Apache Mahout** artifacts for scalable model export  
- Environment setup scripts (`reset.sh`, `full_reset.py`, `train.sh`)  
- Result visualization via `view_results.py`  
  

---

## Modules / Functionalities
- **kafka_producer.py** — Publishes transaction data to Kafka topic  
- **kafka_consumer.py** — Consumes and processes transaction stream  
- **train_model.py** — Preprocesses data, trains model, saves artifacts  
- **view_results.py** — Displays model output and evaluation metrics  
- **reset.sh / full_reset.py** — Resets or recreates environment  
- **mahout-model/** — Stores exported Mahout model and metadata  
- **MD_FILES/** — Contains documentation and setup guides  

---

## Suggestions for Improvement
1. Add distributed processing using **Apache Spark**  
2. Implement **schema validation** for streaming data  
3. Use modern scalable libraries like **Spark MLlib** or **XGBoost**  
4. Add **hyperparameter tuning** and **cross-validation**  
5. Create a **REST API** for real-time scoring (Flask/FastAPI)  
6. Implement **model monitoring** and **performance alerts**  
 

---

## Self-Evaluation Marks (Out of 40)
- **Bhuvanesh S – 35/40**  
  - Lead on Kafka streaming, model training, scripting, and documentation  

- **Harishkanna R – 35/40**  
  - Worked on preprocessing, visualization, and Kafka integration  

---

## Project Repository
🔗 [GitHub Link](https://github.com/BHUVANESH-SSN/big-data-project.git)

---

## Datasets Used
- `credit_card_transactions.csv`  
- `training_fraud_data.csv`

---

## Documentation
Available under the **MD_FILES/** directory in the repository.
