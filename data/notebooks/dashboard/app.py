import streamlit as st
import pandas as pd

st.set_page_config(page_title="CivicSight", layout="wide")

st.title("CivicSight")
st.subheader("Nonprofit Sustainability & Impact Intelligence Platform")

st.write(
    "CivicSight helps nonprofits and mission-driven organizations improve fundraising, "
    "donor retention, operational capacity, and impact reporting through accessible analytics."
)

st.divider()

uploaded_file = st.file_uploader("Upload donor CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.read_csv("data/donations.csv")
    st.info("Using sample data. Upload your own donor CSV to analyze real nonprofit records.")

required_columns = ["donor_id", "donation_amount", "last_donation_days", "donation_frequency"]
missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    st.error(f"Missing required columns: {missing_columns}")
    st.stop()

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

def donor_segment(row):
    if row["donation_amount"] >= 250 and row["donation_frequency"] >= 5:
        return "Core Supporter"
    elif row["donation_amount"] >= 100:
        return "Growth Donor"
    elif row["last_donation_days"] >= 120:
        return "Lapsed Donor"
    else:
        return "Emerging Donor"

data["donor_segment"] = data.apply(donor_segment, axis=1)

def recommendation(row):
    if row["risk_level"] == "High Risk":
        return "Send personalized re-engagement message within 7 days."
    elif row["donor_segment"] == "Core Supporter":
        return "Invite to recurring giving or leadership donor circle."
    elif row["donor_segment"] == "Growth Donor":
        return "Send impact story and ask for upgraded contribution."
    elif row["donor_segment"] == "Lapsed Donor":
        return "Send win-back campaign with recent program outcomes."
    else:
        return "Maintain regular updates and donor appreciation."

data["recommended_action"] = data.apply(recommendation, axis=1)

total_donations = data["donation_amount"].sum()
average_donation = data["donation_amount"].mean()
total_donors = len(data)
high_risk_count = (data["risk_level"] == "High Risk").sum()
retention_health = max(0, 100 - (high_risk_count / total_donors * 100))

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Donations", f"${total_donations:,.0f}")
col2.metric("Average Donation", f"${average_donation:,.0f}")
col3.metric("Total Donors", total_donors)
col4.metric("Fundraising Health Score", f"{retention_health:.0f}/100")

st.divider()

st.subheader("Donor Risk Overview")
st.bar_chart(data["risk_level"].value_counts())

st.subheader("Donor Segments")
st.bar_chart(data["donor_segment"].value_counts())

st.subheader("Priority Outreach Action Plan")
priority = data.sort_values(by="risk_score", ascending=False)

st.dataframe(
    priority[
        [
            "donor_id",
            "donation_amount",
            "last_donation_days",
            "donation_frequency",
            "risk_level",
            "donor_segment",
            "recommended_action",
        ]
    ],
    use_container_width=True,
)

st.divider()

st.subheader("Grant Readiness Checklist")
st.write("Use this section to assess whether the organization is prepared for grant applications.")

grant_items = {
    "Clear mission statement": st.checkbox("Clear mission statement"),
    "Program impact metrics available": st.checkbox("Program impact metrics available"),
    "Annual budget prepared": st.checkbox("Annual budget prepared"),
    "Donor/funding history organized": st.checkbox("Donor/funding history organized"),
    "Measurable outcomes documented": st.checkbox("Measurable outcomes documented"),
}

grant_score = sum(grant_items.values()) / len(grant_items) * 100
st.metric("Grant Readiness Score", f"{grant_score:.0f}/100")

if grant_score >= 80:
    st.success("Strong grant readiness. The organization appears prepared to pursue funding opportunities.")
elif grant_score >= 50:
    st.warning("Moderate readiness. Improve documentation before applying to major grants.")
else:
    st.error("Low readiness. Build stronger financial and impact documentation first.")

st.divider()

st.subheader("Program Impact Tracker")

people_served = st.number_input("People served this period", min_value=0, value=100)
program_cost = st.number_input("Program cost this period ($)", min_value=0, value=5000)
volunteer_hours = st.number_input("Volunteer hours contributed", min_value=0, value=50)

cost_per_person = program_cost / people_served if people_served > 0 else 0
volunteer_value = volunteer_hours * 33

col5, col6, col7 = st.columns(3)
col5.metric("Cost Per Person Served", f"${cost_per_person:,.2f}")
col6.metric("Estimated Volunteer Value", f"${volunteer_value:,.0f}")
col7.metric("People Served", people_served)

st.divider()

st.subheader("Executive Summary")

summary = f"""
CivicSight analyzed {total_donors} donor records and identified {high_risk_count} high-risk donors.
The organization has a fundraising health score of {retention_health:.0f}/100 and a grant readiness score of {grant_score:.0f}/100.
Recommended next step: prioritize donor re-engagement, strengthen impact documentation, and use program metrics to support fundraising and grant applications.
"""

st.write(summary)

csv = priority.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download donor action plan",
    data=csv,
    file_name="civicsight_donor_action_plan.csv",
    mime="text/csv",
)
