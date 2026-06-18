# Fraud Risk Intelligence Platform

A SQL-first fraud detection and risk analytics platform built with PostgreSQL, Python, and Streamlit.

The project simulates how modern fraud operations teams identify, prioritize, and investigate suspicious financial transactions using a combination of:

- Rule-based fraud detection
- SQL feature engineering
- Machine learning risk scoring
- Risk-based alert prioritization
- Interactive investigation dashboards

---

## Project Objective

Traditional fraud detection projects focus only on predicting whether a transaction is fraudulent.

This project focuses on a more realistic business problem:

>Investigators have limited time and cannot review every alert.

The platform therefore prioritizes transactions by expected financial risk and provides an investigation workflow rather than simply producing a binary fraud prediction.

---

## Tech Stack

### Database

- PostgreSQL 17
- SQL Views
- Window Functions
- Indexing
- Query Optimization

### Data Science

- Python
- Pandas
- NumPy
- Scikit-Learn
- XGBoost
- SHAP

### Dashboard

- Streamlit
- Plotly

### Development

- VS Code
- Git
- GitHub

---

## Planned Architecture

Raw Transactions  
-> PostgreSQL Database  
-> SQL Feature Engineering  
-> Rule-Based Detection Engine  
-> Machine Learning Risk Model   
-> Risk Scoring Layer  
-> Alert Prioritization Engine  
-> Streamlit Dashboard

---

## Key Features

### Fraud Detection

- Transaction risk scoring
- Fraud probability estimation
- High-risk alert generation

### Risk Analytics

- Fraud trends
- Risk exposure monitoring
- Transaction behavior analysis

### Investigation Queue

- Prioritized alert review
- Expected loss ranking
- Investigator workflow support

### Explainability

- Feature importance
- SHAP explanations
- Risk driver analysis

---

## Planned SQL Features

### Velocity Features

- Transactions in last hour
- Transactions in last 24 hours
- Transactions in last 7 days

### Behavioral Features

- New merchant detection
- Merchant risk profile
- Unusual transaction timing

### Amount Anomaly Features

- Rolling average comparison
- Rolling standard deviation comparison
- Transaction deviation score

---

## Planned Machine Learning Models

### Baseline

- Logistic Regression

### Tree Models

- Random Forest
- XGBoost

### Anomaly Detection

- Isolation Forest

---

## Evaluation Metrics

Because fraud datasets are highly imbalanced, accuracy is not a useful metric.

Primary metrics:

- Precision
- Recall
- PR-AUC
- Precision@K
- Expected Loss Prevented

---

## Repository Structure

```text
fraud-risk-intelligence-platform/
│
├── .streamlit/
│   └── config.toml                     # Streamlit configuration
│
├── data/
│   ├── raw/                            # Original unmodified source data
│   └── processed/                      # Cleaned and transformed datasets
│
├── models/                             # Saved trained ML models and artifacts
│
├── notebooks/ 
│   ├── 01_eda.ipynb                    # EDA and fraud pattern discovery
│   └── 02_model_dev.ipynb              # Model development and evaluation
│
├── sql/
│   ├── 01_schema.sql                   # Database schema and table creation
│   ├── 02_load.sql                     # Data loading and ingestion scripts
│   ├── 03_features.sql                 # SQL feature engineering pipeline
│   ├── 04_rules.sql                    # Rule-based fraud detection engine
│   └── 05_feature_matrix.sql           # Final ML-ready feature dataset
│
├── src/
│   ├── db.py                           # Database connection utilities
│   ├── features.py                     # Feature generation and processing
│   ├── train.py                        # Model training and evaluation pipeline
│   ├── risk.py                         # Risk scoring and alert prioritisation
│   └── theme.py                        # Shared dashboard styling and theme
│
├── screenshots/                        # Dashboard screenshots for documentation
│
├── app.py
├── .env.example                        # Example environment variables template
├── .gitignore
├── README.md
├── requirements.txt
└── presentation.pdf                    # Project presentation and summary
```

---

## Author

Nihira Sharma  
Bachelor of Advanced Computing Student  
Majors: Data Science & Business Analytics  
University of Sydney  

---