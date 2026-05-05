import streamlit as st
import pandas as pd

st.set_page_config(page_title="CivicSight", page_icon="📊", layout="wide")

# Sidebar
st.sidebar.title("CivicSight")
st.sidebar.caption("Nonprofit Intelligence Platform")

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Donor Analytics",
        "Grant Readiness",
        "Impact Tracker",
        "Executive Summary",
        "Workspace Links",
    ],
)

st.sidebar.divider()
st.sidebar.subheader("Quick Access")
st.sidebar.link_button("Slack", "https://slack.com/signin")
st.sidebar.link_button("Microsoft Teams", "https://teams.microsoft.com")
st.sidebar.link_button("Gmail / Google Workspace", "https://mail.google.com")
st.sidebar.link_button("Mailchimp", "https://login.mailchimp.com")
st.sidebar.link_button("Canva", "https://www.canva.com")
st.sidebar.link_button("Instagram", "https://www.instagram.com")
st.sidebar.link_button("Facebook", "https://www.facebook.com")
st.sidebar.link_button("LinkedIn", "https://www.linkedin.com")

# Load data
uploaded_file = st.sidebar.file_uploader("Upload donor CSV", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.read_csv("data/donations.csv")

required_columns = ["donor_id", "donation_amount", "last_donation_days", "donation_frequency"]
missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    st.error(f"Missing required columns: {missing_columns}")
    st.stop()

# Analytics logic
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
    return "Low Risk"

data["risk_level"] = data["risk_score"].apply(classify_donor)

def donor_segment(row):
    if row["donation_amount"] >= 250 and row["donation_frequency"] >= 5:
        return "Core Supporter"
    elif row["donation_amount"] >= 100:
        return "Growth Donor"
    elif row["last_donation_days"] >= 120:
        return "Lapsed Donor"
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
    return "Maintain regular updates and donor appreciation."

data["recommended_action"] = data.apply(recommendation, axis=1)

total_donations = data["donation_amount"].sum()
average_donation = data["donation_amount"].mean()
total_donors = len(data)
high_risk_count = (data["risk_level"] == "High Risk").sum()
fundraising_health = max(0, 100 - (high_risk_count / total_donors * 100))

# Pages
if page == "Dashboard":
    st.title("CivicSight")
    st.subheader("Nonprofit Sustainability & Impact Intelligence Platform")
    st.write("A simple workspace for fundraising, donor retention, grant readiness, impact tracking, and organizational tools.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Donations", f"${total_donations:,.0f}")
    col2.metric("Average Donation", f"${average_donation:,.0f}")
    col3.metric("Total Donors", total_donors)
    col4.metric("Fundraising Health", f"{fundraising_health:.0f}/100")

    st.divider()
    st.subheader("Priority Overview")
    st.bar_chart(data["risk_level"].value_counts())

elif page == "Donor Analytics":
    st.title("Donor Analytics")
    st.dataframe(data, use_container_width=True)

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

    csv = priority.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download donor action plan",
        data=csv,
        file_name="civicsight_donor_action_plan.csv",
        mime="text/csv",
    )

elif page == "Grant Readiness":
    st.title("Grant Readiness")

    checks = [
        "Clear mission statement",
        "Program impact metrics available",
        "Annual budget prepared",
        "Donor/funding history organized",
        "Measurable outcomes documented",
    ]

    completed = 0
    for item in checks:
        if st.checkbox(item):
            completed += 1

    grant_score = completed / len(checks) * 100
    st.metric("Grant Readiness Score", f"{grant_score:.0f}/100")

    if grant_score >= 80:
        st.success("Strong readiness. The organization appears prepared to pursue funding opportunities.")
    elif grant_score >= 50:
        st.warning("Moderate readiness. Improve documentation before applying to major grants.")
    else:
        st.error("Low readiness. Build stronger financial and impact documentation first.")

elif page == "Impact Tracker":
    st.title("Impact Tracker")

    people_served = st.number_input("People served this period", min_value=0, value=100)
    program_cost = st.number_input("Program cost this period ($)", min_value=0, value=5000)
    volunteer_hours = st.number_input("Volunteer hours contributed", min_value=0, value=50)

    cost_per_person = program_cost / people_served if people_served > 0 else 0
    volunteer_value = volunteer_hours * 33

    col1, col2, col3 = st.columns(3)
    col1.metric("Cost Per Person Served", f"${cost_per_person:,.2f}")
    col2.metric("Estimated Volunteer Value", f"${volunteer_value:,.0f}")
    col3.metric("People Served", people_served)

elif page == "Executive Summary":
    st.title("Executive Summary")

    summary = f"""
    CivicSight analyzed {total_donors} donor records and identified {high_risk_count} high-risk donors.
    
    The organization has a fundraising health score of {fundraising_health:.0f}/100.
    
    Recommended next step: prioritize donor re-engagement, strengthen impact documentation, and use program metrics to support fundraising and grant applications.
    """

    st.write(summary)

elif page == "Workspace Links":
    st.title("Workspace Links")
    st.write("Quick access to the platforms nonprofit teams commonly use.")

    col1, col2 = st.columns(2)

    with col1:
        st.link_button("Open Slack", "https://slack.com/signin")
        st.link_button("Open Microsoft Teams", "https://teams.microsoft.com")
        st.link_button("Open Gmail", "https://mail.google.com")
        st.link_button("Open Mailchimp", "https://login.mailchimp.com")

    with col2:
        st.link_button("Open Canva", "https://www.canva.com")
        st.link_button("Open Instagram", "https://www.instagram.com")
        st.link_button("Open Facebook", "https://www.facebook.com")
        st.link_button("Open LinkedIn", "https://www.linkedin.com")
