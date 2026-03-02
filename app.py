import streamlit as st
import datetime
import requests

# --- THE "BRAIN" SETTINGS ---
API_KEY = "62cab657679f4ba5b6ef931c884320c2" 

st.set_page_config(page_title="The Dorch's Daily", page_icon="🗞️")

# Initialize session state keys to prevent the "AttributeError"
if 'setup_complete' not in st.session_state:
    st.session_state.setup_complete = False

# --- ADMIN TICKER ---
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
    st.divider()

    if API_KEY != "62cab657679f4ba5b6ef931c884320c2":
        for topic in st.session_state.topics:
            url = f'https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&apiKey={API_KEY}'
            try:
                r = requests.get(url).json()
                if r.get('articles'):
                    story = r['articles'][0]
                    st.subheader(f"📍 {topic}")
                    st.write(f"**{story['title']}**")
                    st.write(story['description'])
                    st.caption(f"[Read Original]({story['url']})")
                    st.divider()
            except:
                st.error(f"Error fetching {topic}")
    
    if st.button("Reset & Re-Tune"):
        st.session_state.setup_complete = False
        st.rerun()
