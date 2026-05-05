import streamlit as st
import pandas as pd

st.set_page_config(page_title="CivicSight", page_icon="📊", layout="wide")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("CivicSight")
st.sidebar.caption("Nonprofit Intelligence Platform")

page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Donor Analytics",
        "Donor Message Generator",
        "Grant Readiness",
        "Impact Tracker",
        "Executive Summary",
        "Workspace Links",
    ],
)

st.sidebar.divider()
st.sidebar.subheader("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload donor CSV", type=["csv"])

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

# -----------------------------
# Load Data
# -----------------------------
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.read_csv("data/donations.csv")
    st.sidebar.info("Using sample data.")

required_columns = ["donor_id", "donation_amount", "last_donation_days", "donation_frequency"]
missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    st.error(f"Missing required columns: {missing_columns}")
    st.stop()

# -----------------------------
# Donor Analytics Logic
# -----------------------------
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

priority = data.sort_values(by="risk_score", ascending=False)

# -----------------------------
# Pages
# -----------------------------
if page == "Dashboard":
    st.title("CivicSight")
    st.subheader("Nonprofit Sustainability & Impact Intelligence Platform")

    st.write(
        "CivicSight helps nonprofits track donor retention, fundraising health, "
        "grant readiness, impact metrics, and team workspace tools in one simple dashboard."
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Donations", f"${total_donations:,.0f}")
    col2.metric("Average Donation", f"${average_donation:,.0f}")
    col3.metric("Total Donors", total_donors)
    col4.metric("Fundraising Health", f"{fundraising_health:.0f}/100")

    st.divider()

    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Donor Risk Overview")
        st.bar_chart(data["risk_level"].value_counts())

    with col6:
        st.subheader("Donor Segments")
        st.bar_chart(data["donor_segment"].value_counts())

    st.divider()
    st.subheader("Top Priority Donors")
    st.dataframe(
        priority[
            [
                "donor_id",
                "donation_amount",
                "last_donation_days",
                "risk_level",
                "donor_segment",
                "recommended_action",
            ]
        ].head(10),
        use_container_width=True,
    )

elif page == "Donor Analytics":
    st.title("Donor Analytics")

    st.write(
        "Analyze donor behavior, identify at-risk donors, and generate a priority outreach plan."
    )

    st.subheader("Full Donor Dataset")
    st.dataframe(data, use_container_width=True)

    st.subheader("Priority Outreach Action Plan")
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

elif page == "Donor Message Generator":
    st.title("Donor Message Generator")

    st.write(
        "Generate simple donor outreach messages based on donor status and campaign goals."
    )

    organization_name = st.text_input("Organization name", "Your Organization")

    donor_type = st.selectbox(
        "Choose donor type",
        [
            "High-Risk Donor",
            "Lapsed Donor",
            "Core Supporter",
            "Growth Donor",
            "New Donor",
        ],
    )

    campaign_goal = st.text_input(
        "Campaign goal",
        "Re-engage donors and encourage continued support"
    )

    tone = st.selectbox(
        "Message tone",
        ["Warm", "Professional", "Urgent", "Grateful"]
    )

    if st.button("Generate Message"):
        if donor_type == "High-Risk Donor":
            message = f"""
Dear Supporter,

We wanted to personally reconnect with you and thank you for the role you have played in supporting {organization_name}. Your past contribution helped move our mission forward, and we would be grateful to share how your support continues to make a difference.

As we work toward {campaign_goal}, your renewed involvement would help us continue serving our community with greater impact.

With gratitude,  
{organization_name}
"""
        elif donor_type == "Lapsed Donor":
            message = f"""
Dear Supporter,

It has been some time since we last connected, and we wanted to reach out with appreciation for your past support of {organization_name}. Your generosity has been part of our story, and we would love to welcome you back into our mission.

Your renewed support would help us continue working toward {campaign_goal}.

Warmly,  
{organization_name}
"""
        elif donor_type == "Core Supporter":
            message = f"""
Dear Supporter,

Thank you for being one of the valued supporters of {organization_name}. Your continued generosity helps sustain our work and expand our impact.

As we focus on {campaign_goal}, we would be honored to have your continued partnership in this mission.

With sincere appreciation,  
{organization_name}
"""
        elif donor_type == "Growth Donor":
            message = f"""
Dear Supporter,

Thank you for your meaningful support of {organization_name}. Your generosity has already helped create progress, and we believe your continued involvement can help expand that impact even further.

As we work toward {campaign_goal}, we invite you to stay connected and consider deepening your support.

With appreciation,  
{organization_name}
"""
        else:
            message = f"""
Dear Supporter,

Thank you for your interest in {organization_name}. We are grateful for every person who believes in our mission.

As we continue working toward {campaign_goal}, your support can help create meaningful impact in the community.

Thank you,  
{organization_name}
"""

        st.text_area("Generated donor message", message, height=300)

elif page == "Grant Readiness":
    st.title("Grant Readiness")

    st.write(
        "Assess whether the organization is prepared to apply for grants and funding opportunities."
    )

    checks = [
        "Clear mission statement",
        "Program impact metrics available",
        "Annual budget prepared",
        "Donor/funding history organized",
        "Measurable outcomes documented",
        "Board or leadership support documented",
        "Program budget available",
        "Community need clearly explained",
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

    st.write(
        "Track program reach, cost efficiency, volunteer contribution, and community impact."
    )

    people_served = st.number_input("People served this period", min_value=0, value=100)
    program_cost = st.number_input("Program cost this period ($)", min_value=0, value=5000)
    volunteer_hours = st.number_input("Volunteer hours contributed", min_value=0, value=50)
    programs_delivered = st.number_input("Programs delivered", min_value=0, value=5)

    cost_per_person = program_cost / people_served if people_served > 0 else 0
    volunteer_value = volunteer_hours * 33
    cost_per_program = program_cost / programs_delivered if programs_delivered > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Cost Per Person Served", f"${cost_per_person:,.2f}")
    col2.metric("Estimated Volunteer Value", f"${volunteer_value:,.0f}")
    col3.metric("Cost Per Program", f"${cost_per_program:,.2f}")

elif page == "Executive Summary":
    st.title("Executive Summary")

    summary = f"""
CivicSight analyzed {total_donors} donor records and identified {high_risk_count} high-risk donors.

The organization has a fundraising health score of {fundraising_health:.0f}/100.

Recommended next steps:
1. Prioritize high-risk donor re-engagement.
2. Strengthen impact documentation for grant applications.
3. Use donor segmentation to personalize fundraising outreach.
4. Track program outcomes to improve reporting and funding readiness.
"""

    st.text_area("Generated Executive Summary", summary, height=300)

    st.download_button(
        "Download executive summary",
        data=summary,
        file_name="civicsight_executive_summary.txt",
        mime="text/plain",
    )

elif page == "Workspace Links":
    st.title("Workspace Links")

    st.write(
        "Quick access to common platforms used by nonprofit teams."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.link_button("Open Slack", "https://slack.com/signin")
        st.link_button("Open Microsoft Teams", "https://teams.microsoft.com")
        st.link_button("Open Gmail / Google Workspace", "https://mail.google.com")
        st.link_button("Open Mailchimp", "https://login.mailchimp.com")

    with col2:
        st.link_button("Open Canva", "https://www.canva.com")
        st.link_button("Open Instagram", "https://www.instagram.com")
        st.link_button("Open Facebook", "https://www.facebook.com")
        st.link_button("Open LinkedIn", "https://www.linkedin.com")
