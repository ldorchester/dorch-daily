import streamlit as st
import datetime
import requests

# --- THE "BRAIN" SETTINGS ---
API_KEY = "YOUR_API_KEY_HERE" 

st.set_page_config(page_title="The Dorch's Daily", page_icon="🗞️")

# --- ADMIN TICKER (Laine's View) ---
with st.sidebar:
    st.header("🛠️ Lead Dev Dashboard")
    st.metric("Today's Spend", "$0.08")
    st.error("Circuit Breaker: ACTIVE ($1.00)")
    st.divider()
    st.info("💡 Tip: Use the feedback at the bottom to see what testers think.")

# --- STEP 1: THE ONBOARDING INTERVIEW ---
if 'setup_complete' not in st.session_state:
    st.title("🗞️ The Dorch's Daily")
    st.subheader("Your Sanctuary from the Noise")
    
    with st.form("onboarding"):
        st.write("### 1. The Soul")
        paper_name = st.text_input("What should we call your daily edition?", "The Laine Ledger")
        
        st.write("### 2. The Pillars")
        topics = st.multiselect("Pick your anchor topics:", ["Oilers", "Blue Jays", "Iran War", "Alberta Politics", "AI & Tech"])
        custom_niche = st.text_input("Add a specific niche (e.g. Antique Cars):", placeholder="Be specific!")
        
        st.write("### 3. The Tone Matrix")
        tone = st.selectbox("Pick your Voice:", ["Witty Friend", "Straight Shooter", "Deep Analyst"])
        
        st.write("### 4. The Rage Filter")
        rage_filter = st.radio("How to handle 'Heavy' news?", ["Sanitized Narrative (Readable)", "Just the Facts (Bullet points)"])
        
        st.write("### 5. Coffee Time")
        coffee_time = st.time_input("When is your first sip of coffee?", value=datetime.time(6, 45))
        
        submit = st.form_submit_button("Build My Edition")
        
        if submit:
            st.session_state.setup_complete = True
            st.session_state.paper_name = paper_name
            st.session_state.topics = topics
            st.session_state.tone = tone
            st.session_state.rage_filter = rage_filter
            st.rerun()

# --- STEP 2: THE DAILY EDITION ---
else:
    st.header(f"✨ {st.session_state.paper_name}")
    st.caption(f"Tone: {st.session_state.tone} | Filter: {st.session_state.rage_filter}")
    st.write(f"Generated for your 6:45 AM Coffee | {datetime.date.today()}")
    st.divider()

    # The Loop: Goes through every topic you picked
    if API_KEY != "YOUR_API_KEY_HERE":
        for topic in st.session_state.topics:
            url = f'https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&apiKey={API_KEY}'
            try:
                response = requests.get(url).json()
                if response.get('articles'):
                    story = response['articles'][0]
                    st.subheader(f"📍 {topic} Update")
                    st.write(f"**{story['title']}**")
                    # (In the final version, Gemini will rewrite this 'description' part)
                    st.write(story['description'])
                    st.caption(f"Source: {story['source']['name']} | [Read Original]({story['url']})")
                    st.divider()
            except:
                st.error(f"Could not fetch {topic}")
    else:
        st.warning("⚠️ Boss, put your API Key in the code!")

    # --- FEEDBACK BOXES (For your testers) ---
    st.write("### 🗣️ Thoughts on this Story?")
    st.text_area("Is this too much rage? Too boring? Tell us:", key="story_feedback")
    if st.button("Send Story Feedback"):
        st.toast("Sam is analyzing your feedback!")

    if st.button("Reset & Re-Tune"):
        del st.session_state.setup_complete
        st.rerun()
