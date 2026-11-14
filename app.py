import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="UPI Fraud Detection API")
saved = joblib.load("fraud_model.joblib")
model, COLUMNS = saved["model"], saved["columns"]

FEATURES = ['amount', 'amount_ratio', 'hour_of_day', 'is_night', 'is_cross_city',
            'is_new_receiver', 'is_new_account', 'receiver_account_age_days',
            'sender_txn_count_24h', 'sender_avg_amount', 'failed_attempts_before',
            'day_of_week', 'transaction_type', 'device_type']

def build_features(d):
    d = d.copy()
    d['amount_ratio']   = d['amount'] / (d['sender_avg_amount'] + 1)
    d['is_night']       = d['hour_of_day'].apply(lambda h: 1 if (h >= 22 or h <= 4) else 0)
    d['is_cross_city']  = (d['sender_city'] != d['receiver_city']).astype(int)
    d['is_new_account'] = (d['receiver_account_age_days'] < 30).astype(int)
    return d

def prepare(d):
    d = build_features(d)[FEATURES]
    d = pd.get_dummies(d, columns=['transaction_type', 'device_type'])
    return d.reindex(columns=COLUMNS, fill_value=0)

class Transaction(BaseModel):
    amount: float
    transaction_type: str
    hour_of_day: int
    device_type: str
    sender_city: str
    receiver_city: str
    is_new_receiver: int
    receiver_account_age_days: int
    sender_txn_count_24h: int
    sender_avg_amount: float
    failed_attempts_before: int
    day_of_week: int

@app.get("/")
def home():
    return {"status": "UPI fraud API is running"}

@app.post("/predict")
def predict(txn: Transaction):
    df = pd.DataFrame([txn.model_dump()])
    prob = float(model.predict_proba(prepare(df))[0][1])
    return {
        "fraud_probability": round(prob, 4),
        "is_fraud": prob >= 0.5,
        "risk_level": "HIGH" if prob >= 0.7 else "MEDIUM" if prob >= 0.3 else "LOW",
    }
