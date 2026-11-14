import requests
import streamlit as st

st.set_page_config(page_title="UPI Fraud Detector", page_icon="🛡️")
st.title("🛡️ UPI Fraud Detector")
st.write("Enter the transaction details and click **Check Fraud**.")

col1, col2 = st.columns(2)
with col1:
    amount = st.number_input("Amount (₹)", min_value=1.0, value=500.0)
    txn_type = st.selectbox("Transaction type", ["P2P", "P2M", "QR_scan", "collect_request"])
    hour = st.slider("Hour of day", 0, 23, 15)
    device = st.selectbox("Device", ["Android", "iOS", "Web"])
    day = st.selectbox("Day of week (0 = Monday)", list(range(7)), index=2)
    sender_city = st.selectbox("Sender city", ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata",
                                               "Pune", "Jaipur", "Lucknow", "Hyderabad", "Noida"])
with col2:
    receiver_city = st.selectbox("Receiver city", ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata",
                                                   "Pune", "Jaipur", "Lucknow", "Hyderabad", "Noida"])
    new_receiver = st.selectbox("Is this a new receiver?", ["No", "Yes"])
    acc_age = st.number_input("Receiver account age (days)", min_value=0, value=1500)
    txn_24h = st.number_input("Sender transactions in last 24h", min_value=0, value=1)
    avg_amt = st.number_input("Sender's average amount (₹)", min_value=1.0, value=500.0)
    failed = st.number_input("Failed attempts before", min_value=0, value=0)

if st.button("Check Fraud"):
    payload = {
        "amount": amount, "transaction_type": txn_type, "hour_of_day": hour,
        "device_type": device, "sender_city": sender_city, "receiver_city": receiver_city,
        "is_new_receiver": 1 if new_receiver == "Yes" else 0,
        "receiver_account_age_days": int(acc_age), "sender_txn_count_24h": int(txn_24h),
        "sender_avg_amount": avg_amt, "failed_attempts_before": int(failed), "day_of_week": day,
    }
    try:
        result = requests.post("http://127.0.0.1:8000/predict", json=payload, timeout=10).json()
        prob = result["fraud_probability"]
        level = result["risk_level"]
        if level == "HIGH":
            st.error(f"🚨 HIGH RISK: fraud probability {prob:.1%}")
        elif level == "MEDIUM":
            st.warning(f"⚠️ MEDIUM RISK: fraud probability {prob:.1%}")
        else:
            st.success(f"✅ LOW RISK: fraud probability {prob:.1%}")
    except Exception as e:
        st.error(f"Could not reach the API. Is the API window still running? ({e})")
