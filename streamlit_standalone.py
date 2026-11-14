import joblib
import pandas as pd
import streamlit as st

# ---------- Load model ----------
@st.cache_resource
def load_model():
    saved = joblib.load("fraud_model.joblib")
    return saved["model"], saved["columns"]

model, COLUMNS = load_model()

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

# ---------- Page ----------
st.set_page_config(page_title="UPI Fraud Detector", page_icon="🛡️")
st.title("🛡️ UPI Fraud Detector")
st.write("Enter the transaction details and click **Check Fraud**.")
st.caption("Demo project trained on a synthetic dataset of 10,000 UPI transactions.")

CITIES = ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata",
          "Pune", "Jaipur", "Lucknow", "Hyderabad", "Noida"]

col1, col2 = st.columns(2)
with col1:
    amount = st.number_input("Amount (₹)", min_value=1.0, value=500.0)
    txn_type = st.selectbox("Transaction type", ["P2P", "P2M", "QR_scan", "collect_request"])
    hour = st.slider("Hour of day", 0, 23, 15)
    device = st.selectbox("Device", ["Android", "iOS", "Web"])
    day = st.selectbox("Day of week (0 = Monday)", list(range(7)), index=2)
    sender_city = st.selectbox("Sender city", CITIES)
with col2:
    receiver_city = st.selectbox("Receiver city", CITIES)
    new_receiver = st.selectbox("Is this a new receiver?", ["No", "Yes"])
    acc_age = st.number_input("Receiver account age (days)", min_value=0, value=1500)
    txn_24h = st.number_input("Sender transactions in last 24h", min_value=0, value=1)
    avg_amt = st.number_input("Sender's average amount (₹)", min_value=1.0, value=500.0)
    failed = st.number_input("Failed attempts before", min_value=0, value=0)

if st.button("Check Fraud"):
    row = {
        "amount": amount, "transaction_type": txn_type, "hour_of_day": hour,
        "device_type": device, "sender_city": sender_city, "receiver_city": receiver_city,
        "is_new_receiver": 1 if new_receiver == "Yes" else 0,
        "receiver_account_age_days": int(acc_age), "sender_txn_count_24h": int(txn_24h),
        "sender_avg_amount": avg_amt, "failed_attempts_before": int(failed), "day_of_week": day,
    }
    prob = float(model.predict_proba(prepare(pd.DataFrame([row])))[0][1])
    if prob >= 0.7:
        st.error(f"🚨 HIGH RISK: fraud probability {prob:.1%}")
    elif prob >= 0.3:
        st.warning(f"⚠️ MEDIUM RISK: fraud probability {prob:.1%}")
    else:
        st.success(f"✅ LOW RISK: fraud probability {prob:.1%}")
