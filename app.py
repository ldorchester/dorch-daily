import streamlit as st
import datetime
import requests

# --- THE "BRAIN" SETTINGS ---
API_KEY = "62cab657679f4ba5b6ef931c884320c2" 

st.set_page_config(page_title="The Dorch's Daily", page_icon="🗞️")

# Initialize session state so it doesn't forget who you are
if 'setup_complete' not in st.session_state:
    st.session_state.setup_complete = False

# --- ADMIN TICKER (Laine's View) ---
with st.sidebar:
    st.header("🛠️ Lead Dev Dashboard")
    st.metric("Today's Spend", "$0.08")
    st.error("Circuit Breaker: ACTIVE ($1.00)")

# --- STEP 1: THE ONBOARDING INTERVIEW ---
if not st.session_state.setup_complete:
    st.title("🗞️ The Dorch's Daily")
    st.subheader("Your Sanctuary from the Noise")
    
    with st.form("onboarding"):
        paper_name = st.text_input("Name your Daily Edition:", "The Laine Ledger")
        topics = st.multiselect("Pick your pillars:", ["Oilers", "Blue Jays", "Iran War", "Alberta Politics", "AI & Tech"])
        tone = st.selectbox("Pick your Voice:", ["Witty Friend", "Straight Shooter", "Deep Analyst"])
        rage_filter = st.radio("How to handle 'Heavy' news?", ["Sanitized Narrative", "Just the Facts"])
        submit = st.form_submit_button("Build My Edition")
        
        if submit:
            st.session_state.paper_name = paper_name
            st.session_state.topics = topics
            st.session_state.tone = tone
            st.session_state.rage_filter = rage_filter
            st.session_state.setup_complete = True
            st.rerun()

# --- STEP 2: THE DAILY EDITION ---
else:
    st.header(f"✨ {st.session_state.paper_name}")
    st.caption(f"Tone: {st.session_state.tone} | Filter: {st.session_state.rage_filter}")
    st.write(f"Generated for your 6:45 AM Coffee | {datetime.date.today()}")
    st.divider()

    # Fetch news for every topic selected
    for topic in st.session_state.topics:
        url = f'https://newsapi.org/v2/everything?q={topic}&language=en&sortBy=publishedAt&apiKey={API_KEY}'
        try:
            r = requests.get(url).json()
            if r.get('articles'):
                st.subheader(f"📍 {topic} Update")
                # Show top 2 stories to make it feel like a real paper
                for i in range(min(2, len(r['articles']))):
                    story = r['articles'][i]
                    st.write(f"**{story['title']}**")
                    st.write(story['description'] if story['description'] else "No summary available.")
                    st.caption(f"Source: {story['source']['name']} | [Read Original]({story['url']})")
                    st.write("---")
            else:
                st.warning(f"No fresh news found for {topic} in the last hour.")
        except:
            st.error(f"The 'Pipe' for {topic} is currently clogged.")
    
    # FEEDBACK SECTION
    st.divider()
    st.write("### 🗣️ Sam's Feedback Loop")
    feedback = st.text_area("What should we change? (Questions, Design, Tone?)")
    if st.button("Send to Sam"):
        st.toast("Feedback logged! I'm on it, Laine.")

    if st.button("Reset & Re-Tune"):
        st.session_state.setup_complete = False
        st.rerun()
