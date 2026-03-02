import streamlit as st
import datetime
import requests

# --- THE "BRAIN" SETTINGS ---
# PASTE YOUR KEY FROM NEWSAPI.ORG BETWEEN THE QUOTES BELOW
API_KEY = "62cab657679f4ba5b6ef931c884320c2" 

st.set_page_config(page_title="The Dorch's Daily", page_icon="🗞️")

# --- ADMIN TICKER ---
with st.sidebar:
    st.header("🛠️ Lead Dev Dashboard")
    st.metric("Today's Spend", "$0.08")
    st.error("Circuit Breaker: ACTIVE ($1.00)")

st.title("🗞️ The Dorch's Daily")

# --- STEP 1: THE INTERVIEW ---
if 'setup_complete' not in st.session_state:
    with st.form("onboarding"):
        paper_name = st.text_input("Name your Daily Edition:", "The Laine Ledger")
        topics = st.multiselect("Pillars:", ["Oilers", "Blue Jays", "Iran War", "Alberta Politics"])
        tone = st.selectbox("Pick your Voice:", ["Witty Friend", "Straight Shooter", "Deep Analyst"])
        submit = st.form_submit_button("Build My Edition")
        
        if submit:
            st.session_state.setup_complete = True
            st.session_state.paper_name = paper_name
            st.rerun()

# --- STEP 2: THE NEWS FEED ---
else:
    st.header(f"✨ {st.session_state.paper_name}")
    st.write(f"Generated for your 6:45 AM Coffee | {datetime.date.today()}")

    # This "Pipe" goes and grabs a real headline for you
    if API_KEY != "YOUR_API_KEY_HERE":
        url = f'https://newsapi.org/v2/everything?q=Oilers&sortBy=publishedAt&apiKey={API_KEY}'
        response = requests.get(url).json()
        
        if response.get('articles'):
            top_story = response['articles'][0]
            st.subheader("🏒 Latest Oilers Update")
            st.write(f"**{top_story['title']}**")
            st.write(top_story['description'])
            st.caption(f"Source: {top_story['source']['name']} | [Read Original]({top_story['url']})")
    else:
        st.warning("⚠️ Boss, you forgot to paste your API Key in the code!")

    if st.button("Reset & Re-Tune"):
        del st.session_state.setup_complete
        st.rerun()
