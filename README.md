# 🛡️ UPI Fraud Detection

A machine learning project which detects fraudulent UPI transactions.
Link to live demo: https://upi-fraud-detector-ankit.streamlit.app/

## Overview

Given information about a UPI transaction (amount, type, timing, device, cities, history of sender) a probability of whether it is fraudulent will be returned with a LOW/MEDIUM/HIGH risk rating.

## Pipeline

Data -> EDA -> Feature Engineering -> ML Model Training -> Evaluation -> FastAPI - Streamlit App - Deployed to Cloud.

## Dataset

10,000 UPI Transactions between Jan - Jun 2026. 3% (300) were fraudulent. This is a synthetic dataset.

## Feature Engineering

amount_ratio = Amount relative to senders average amount.

is_night = Transaction between 10pm - 4am.

is_cross_city = Sender and Receiver in different cities.

is_new_account = Recievers account is less than 30 days old.

day_of_week =

## Modelling

Time based train-test split. First 80% of transactions were used to train and the last 20% to test. This replicates how it would be used in practice.

Used class_weight='balanced' to account for the class imbalance.

Dummy Model, Logistic Regression and Random Forest models were used.

Precision, Recall and PR-AUC scores were calculated. Accuracy was misleading as a model which always predicts Legit has a score of 97%.

## Results

| Model | Fraud Precision | Fraud Recall | PR AUC |

|---|---|---|---|

| Dummy (Always Legit) | 0% | 0% | 0.03 |

| Logistic Regression | 100% | 100% | 1.00 |

| Random Forest | 100% | 100% | 1.00 |

Most important features were transactions in the past 24 hours, previous failed attempts and relative amount to senders average.

After removing the top 4 features, the Random Forest still had a HIGH PR-AUC score of 0.989.

## Limitations

These incredibly HIGH results are due to the synthetic dataset having very clear patterns of fraud. In reality fraud is much harder to identify and will have lower precision and recall. This project shows the whole pipeline but does not achieve state of the art accuracy.

## Technologies Used

Python, Pandas, Scikit Learn, FastAPI, Streamlit, Streamlit Community Cloud.

## Files

UPI_fraud_Detection3.ipynb - EDA, Features, Model Training.

app.py - FastAPI endpoint to predict. (/predict).

streamlit_app.py - Streamlit application to call the API. (Local).

streamlit_standalone.py - Deployed Streamlit app. (Model loaded in).

fraud_model.joblib - Trained Model.

## How to Run Locally

```

pip install -r requirements.txt

python -m streamlit run streamlit_standalone.py

```
