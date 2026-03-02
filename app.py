import streamlit as st
import datetime
import requests

# --- THE "BRAIN" SETTINGS ---
API_KEY = "62cab657679f4ba5b6ef931c884320c2"

st.set_page_config(page_title="The Dorch's Daily", page_icon="🗞️")

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
    
    # LOCKDOWN: clear_on_submit=False keeps the data safe if they hit enter
    with st.form(key="onboarding_form_final", clear_on_submit=False):
        st.write("### 1. The Soul")
        paper_name = st.text_input("Name your Daily Edition:", "The Laine Ledger")
        
        st.write("### 2. The Pillars")
        topics = st.multiselect("Pick your anchor topics:", ["Oilers", "Blue Jays", "F1", "Iran War", "Alberta Politics", "AI & Tech"])
        custom_niche = st.text_input("Add a specific niche (e.g. Ballet):")
        
        st.write("### 3. The Tone Matrix")
        tone = st.selectbox("Pick your Voice:", ["Witty Friend", "Straight Shooter", "Deep Analyst"])
        
        st.write("### 4. The Rage Filter")
        rage_filter = st.radio("How to handle 'Heavy' news?", ["Sanitized Narrative", "Just the Facts"])
        
        st.write("### 5. Coffee Time")
        coffee_time = st.time_input("When is your first sip of coffee?", value=datetime.time(6, 45))
        
        # This is the ONLY button that will now submit the form
        submit = st.form_submit_button("Build My Edition")
        
        if submit:
            if not topics and not custom_niche:
                st.error("Wait! You didn't pick any topics.")
            else:
                st.session_state.paper_name = paper_name
                st.session_state.topics = topics
                st.session_state.custom_niche = custom_niche
                st.session_state.tone = tone
                st.session_state.rage_filter = rage_filter
                st.session_state.setup_complete = True
                st.rerun()

# --- STEP 2: THE DAILY EDITION ---
else:
    st.header(f"✨ {st.session_state.paper_name}")
    st.caption(f"Tone: {st.session_state.tone} | Filter: {st.session_state.rage_filter}")
    st.divider()

    all_topics = st.session_state.topics.copy()
    if st.session_state.custom_niche:
        all_topics.append(st.session_state.custom_niche)

    for topic in all_topics:
        url = f'https://newsapi.org/v2/everything?q={topic}&language=en&sortBy=publishedAt&apiKey={API_KEY}'
        try:
            r = requests.get(url).json()
            if r.get('articles'):
                st.subheader(f"📍 {topic} Update")
                for i in range(min(2, len(r['articles']))):
                    story = r['articles'][i]
                    st.write(f"**{story['title']}**")
                    # COMING NEXT: Gemini will replace this raw description with a 1,000-word story
                    st.write(story['description'] if story['description'] else "Scanning for details...")
                    st.caption(f"Source: {story['source']['name']} | [Read Original]({story['url']})")
                    st.write("---")
        except:
            st.error(f"The 'Pipe' for {topic} is currently clogged.")
    
    if st.button("Reset & Re-Tune"):
        st.session_state.setup_complete = False
        st.rerun()
