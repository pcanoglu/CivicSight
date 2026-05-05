import streamlit as st
import pandas as pd

st.set_page_config(page_title="CivicSight Dashboard", layout="wide")

st.title("CivicSight Nonprofit Donor Dashboard")

st.write(
    "CivicSight helps nonprofits understand donor behavior, identify at-risk donors, "
    "and improve fundraising decisions through simple analytics."
)

data = pd.read_csv("data/donations.csv")

st.subheader("Donor Data")
st.dataframe(data)

total_donations = data["donation_amount"].sum()
average_donation = data["donation_amount"].mean()
retention_rate = data["will_donate_again"].mean() * 100

col1, col2, col3 = st.columns(3)

col1.metric("Total Donations", f"${total_donations:,.0f}")
col2.metric("Average Donation", f"${average_donation:,.0f}")
col3.metric("Predicted Retention Rate", f"{retention_rate:.1f}%")

st.subheader("Donor Risk Segments")

data["donor_status"] = data["will_donate_again"].apply(
    lambda x: "Likely to Donate Again" if x == 1 else "At-Risk Donor"
)

st.bar_chart(data["donor_status"].value_counts())

st.subheader("Recommended Action List")

at_risk = data[data["will_donate_again"] == 0]

if len(at_risk) > 0:
    st.write("These donors may need re-engagement:")
    st.dataframe(at_risk[["donor_id", "donation_amount", "last_donation_days", "donation_frequency"]])
else:
    st.write("No at-risk donors identified.")
