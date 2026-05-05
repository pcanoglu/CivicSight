import streamlit as st
import pandas as pd

st.set_page_config(page_title="CivicSight", layout="wide")

st.title("CivicSight")
st.subheader("Nonprofit Donor Intelligence Dashboard")

st.write(
    "CivicSight helps nonprofit organizations identify at-risk donors, understand donor behavior, "
    "and make better fundraising decisions using simple data analytics."
)

st.divider()

uploaded_file = st.file_uploader("Upload donor CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.read_csv("data/donations.csv")
    st.info("Using sample donor data. Upload your own CSV to analyze real donor records.")

required_columns = ["donor_id", "donation_amount", "last_donation_days", "donation_frequency"]

missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    st.error(f"Missing required columns: {missing_columns}")
    st.stop()

# Donor scoring logic
data["risk_score"] = (
    (data["last_donation_days"] * 0.5)
    - (data["donation_frequency"] * 10)
    - (data["donation_amount"] * 0.05)
)

def classify_donor(score):
    if score >= 80:
        return "High Risk"
    elif score >= 40:
        return "Medium Risk"
    else:
        return "Low Risk"

data["risk_level"] = data["risk_score"].apply(classify_donor)

def recommendation(row):
    if row["risk_level"] == "High Risk":
        return "Contact immediately with personalized re-engagement message."
    elif row["risk_level"] == "Medium Risk":
        return "Send campaign update or donor appreciation message."
    else:
        return "Maintain regular communication."

data["recommended_action"] = data.apply(recommendation, axis=1)

# Metrics
total_donations = data["donation_amount"].sum()
average_donation = data["donation_amount"].mean()
high_risk_count = (data["risk_level"] == "High Risk").sum()
total_donors = len(data)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Donations", f"${total_donations:,.0f}")
col2.metric("Average Donation", f"${average_donation:,.0f}")
col3.metric("Total Donors", total_donors)
col4.metric("High-Risk Donors", high_risk_count)

st.divider()

st.subheader("Donor Risk Overview")
risk_counts = data["risk_level"].value_counts()
st.bar_chart(risk_counts)

st.subheader("Priority Outreach List")
priority = data.sort_values(by="risk_score", ascending=False)

st.dataframe(
    priority[
        [
            "donor_id",
            "donation_amount",
            "last_donation_days",
            "donation_frequency",
            "risk_level",
            "recommended_action",
        ]
    ],
    use_container_width=True,
)

st.subheader("Export Action Plan")

csv = priority.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download donor action plan",
    data=csv,
    file_name="civicsight_donor_action_plan.csv",
    mime="text/csv",
)
