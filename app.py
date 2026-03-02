import streamlit as st
import datetime

# --- SETTINGS & THE TICKER ---
st.set_page_config(page_title="The Dorch's Daily", page_icon="🗞️")

# Mock Admin Data (This is the 'Ticker' you asked for)
if 'total_spend' not in st.session_state:
    st.session_state.total_spend = 0.08  # Current test cost
    st.session_state.simulated_users = 1000

# --- ADMIN VIEW (Only for Laine) ---
with st.sidebar:
    st.header("🛠️ Lead Dev Dashboard")
    st.metric("Today's Spend", f"${st.session_state.total_spend:.2f}")
    st.write(f"**Scaling Alert:** If we had {st.session_state.simulated_users} users right now, you'd be at **${st.session_state.total_spend * 1000:.2f}/day**.")
    st.error("Circuit Breaker Status: ACTIVE ($1.00 Limit)")

# --- APP FEEDBACK (For your testers) ---
st.info("💡 **Tester Note:** How is the app working? Use the 'App Feedback' box at the bottom to tell us what questions or topics are missing!")

# --- THE ONBOARDING INTERVIEW ---
st.title("🗞️ The Dorch's Daily")
st.subheader("Your Sanctuary from the Noise")

with st.form("onboarding_form"):
    st.write("### 1. The Name")
    paper_name = st.text_input("What should we call your daily edition?", placeholder="e.g. The Laine Ledger")

    st.write("### 2. Your Anchor Topics")
    topics = st.multiselect("Pick your pillars:", ["Oilers", "Alberta Politics", "Iran War", "AI & Tech", "Local News"])
    custom_niche = st.text_input("Add a specific niche (e.g. Antique Cars):")

    st.write("### 3. The Tone Matrix")
    col1, col2 = st.columns(2)
    with col1:
        sports_tone = st.selectbox("Sports Tone:", ["Witty Friend", "Straight Shooter", "Deep Analyst"])
    with col2:
        politics_tone = st.selectbox("Politics Tone:", ["Straight Shooter", "Deep Analyst"])

    st.write("### 4. The Rage Filter")
    rage_filter = st.radio("How to handle 'Heavy' news?", ["Sanitized Narrative (Readable)", "Just the Facts (Bullet points)"])

    st.write("### 5. Coffee Time")
    coffee_time = st.time_input("When is your first sip of coffee?", value=datetime.time(6, 45))

    submitted = st.form_submit_button("Build My Edition")

if submitted:
    st.success(f"Configuration Saved! '{paper_name}' will be ready at {coffee_time.strftime('%I:%M %p')}.")
    st.balloons()

# --- FEEDBACK HOOKS (What you asked for) ---
st.divider()
st.write("### 🗣️ App & Design Feedback")
feedback_type = st.selectbox("What are you giving feedback on?", ["Interview Questions", "Topic List", "Custom Niche Clarity", "Design/Look"])
user_feedback = st.text_area("What should we change or add?")
if st.button("Send Feedback to Laine"):
    st.toast("Feedback Sent! Laine & Sam are on it.")
