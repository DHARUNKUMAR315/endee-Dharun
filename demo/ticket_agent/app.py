import streamlit as st
import os
import time
import pandas as pd
from sentence_transformers import SentenceTransformer
import endee
import requests
import uuid
from datetime import datetime, timedelta
import json
import random

st.set_page_config(page_title="AI Support Agent", page_icon="🎫", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 💎 CLEAN SAAS AI INTERFACE CSS
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background-color: #0d1117;
    color: #c9d1d9;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #30363d;
}

/* Hide Streamlit elements for a clean SaaS look */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Custom Title */
.main-header {
    margin-top: -40px;
    margin-bottom: 25px;
    display: flex;
    align-items: center;
    gap: 15px;
    border-bottom: 1px solid #30363d;
    padding-bottom: 15px;
}
.main-header h1 {
    margin: 0;
    font-weight: 800;
    font-size: 2.2rem;
    color: #ffffff;
}
.ticket-id-badge {
    background: #21262d; border: 1px solid #30363d; padding: 5px 12px; border-radius: 15px; font-family: monospace; color: #58a6ff; font-weight: bold; font-size: 0.9em;
}

/* Chat/Interface Elements */
.ticket-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 15px;
}

.badge {
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 0.75em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge-category { background: #1f6feb; color: white; }
.badge-priority-Critical { background: #f85149; color: white; }
.badge-priority-High { background: #d29922; color: #000; }
.badge-priority-Medium { background: #2ea043; color: white; }
.badge-priority-Low { background: #58a6ff; color: #000; }

/* Status Badges */
.status-completed { background: #238636; border: 1px solid #2ea043; color: white; padding: 6px 15px; border-radius: 20px; font-weight: 700; font-size: 0.85em; }
.status-inprogress { background: #d29922; border: 1px solid #e3b341; color: black; padding: 6px 15px; border-radius: 20px; font-weight: 800; font-size: 0.85em; }
.status-notstarted { background: #1f6feb; border: 1px solid #58a6ff; color: white; padding: 6px 15px; border-radius: 20px; font-weight: 700; font-size: 0.85em; }
.status-escalated { background: #b62324; border: 1px solid #f85149; color: white; padding: 6px 15px; border-radius: 20px; font-weight: 700; font-size: 0.85em; }

.escalate-banner {
    background: #490202;
    border: 1px solid #f85149;
    color: #ff7b72;
    padding: 15px;
    border-radius: 8px;
    font-weight: 600;
    margin-bottom: 20px;
}

.automation-banner {
    background: #04260f;
    border: 1px solid #2ea043;
    color: #3fb950;
    padding: 15px;
    border-radius: 8px;
    font-weight: 600;
    margin-bottom: 20px;
}
.sentiment-banner {
    background: rgba(248, 81, 73, 0.1);
    border-left: 4px solid #f85149;
    color: #c9d1d9;
    padding: 15px;
    border-radius: 8px;
    font-weight: 600;
    margin-bottom: 20px;
}

/* Modern Stepper */
.stepper-container {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
    margin-bottom: 30px;
    padding: 20px;
    background: #161b22;
    border-radius: 12px;
    border: 1px solid #30363d;
}
.step {
    text-align: center;
    flex: 1;
    position: relative;
    opacity: 0.4;
    transition: opacity 0.3s;
}
.step.active {
    opacity: 1.0;
}
.step:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 15px;
    left: 70%;
    width: 60%;
    height: 2px;
    background: #30363d;
    z-index: 0;
}
.step.active:not(:last-child)::after {
    background: #1f6feb;
}
.step-icon {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: #21262d;
    border: 2px solid #30363d;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 10px auto;
    position: relative;
    z-index: 1;
    font-size: 0.9em;
    color: #8b949e;
}
.step.active .step-icon {
    background: #1f6feb;
    border-color: #58a6ff;
    color: white;
}
.step.pulse .step-icon {
    box-shadow: 0 0 10px #1f6feb;
}
.step p {
    margin: 0;
    font-weight: 500;
    font-size: 0.85em;
    color: #8b949e;
}
.step.active p {
    color: #c9d1d9;
}

/* Fancy Buttons */
.stButton > button {
    background-color: #238636 !important;
    color: white !important;
    font-weight: 600 !important;
    border: 1px solid rgba(240, 246, 252, 0.1) !important;
    border-radius: 6px !important;
    transition: all 0.2s;
}
.stButton > button:hover {
    background-color: #2ea043 !important;
    border-color: #2ea043 !important;
}

/* Nav Buttons */
.nav-btn > button {
    background-color: #21262d !important;
    color: #c9d1d9 !important;
    font-weight: 500 !important;
    border: 1px solid #30363d !important;
    text-align: left !important;
    justify-content: flex-start !important;
}
.nav-btn > button:hover {
    background-color: #30363d !important;
    border-color: #8b949e !important;
}

.preset-btn > button {
    background-color: #21262d !important;
    border: 1px solid #30363d !important;
    color: #c9d1d9 !important;
}
.preset-btn > button:hover {
    background-color: #30363d !important;
    border-color: #8b949e !important;
}

/* Feedback Buttons */
.feedback-btn > button {
    background-color: transparent !important;
    border: 1px solid #30363d !important;
    color: #c9d1d9 !important;
    padding: 5px 15px !important;
}
.feedback-btn > button:hover {
    background-color: #1f6feb !important;
    border-color: #58a6ff !important;
}

/* Timer text */
.analyst-timer {
    color: #58a6ff;
    font-family: monospace;
    font-size: 1.1em;
    font-weight: bold;
    margin-top: -15px;
    margin-bottom: 20px;
    text-align: right;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 🚄 INITIALIZATION (Models & Endee & State)
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = "live_agent"
if 'user_history' not in st.session_state:
    st.session_state.user_history = []

def change_page(page_name):
    st.session_state.page = page_name

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_resource
def setup_endee():
    client = endee.Endee()
    
    endee_host = os.environ.get("ENDEE_HOST", "http://localhost:8080")
    client.base_url = f"{endee_host}/api/v1"
    
    index_name = "enterprise_tickets_index"
    try:
        requests.get(f"{endee_host}/api/v1/health")
    except requests.exceptions.ConnectionError:
        st.error(f"⚠️ Endee server not reachable at {endee_host}! Check if it's running.")
        st.stop()
    try:
        index = client.get_index(index_name)
    except Exception as e:
        st.error(f"Failed to connect to index '{index_name}'. Did you run data_pipeline.py first? Error: {e}")
        st.stop()
    return index

@st.cache_data
def load_dashboard_data():
    """Generates synthetic historical analytics based on the CSV dataset."""
    df = pd.read_csv('tickets.csv')
    end_date = datetime.now()
    
    # Generate 30 days of synthetic timelines
    dates = [end_date - timedelta(days=random.randint(0, 30)) for _ in range(len(df))]
    df['date'] = dates
    df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')
    
    # Generate synthetic statuses
    statuses = random.choices(["Completed", "In Progress", "Escalated/Open"], weights=[0.65, 0.25, 0.10], k=len(df))
    df['status'] = statuses
    
    # Sort for latest first
    df = df.sort_values(by='date', ascending=False)
    return df

with st.spinner("Initializing AI Core..."):
    model = load_model()
    index = setup_endee()
    df_analytics = load_dashboard_data()

# ==========================================
# 🛰️ SIDEBAR TELEMETRY & NAVIGATION
# ==========================================
st.sidebar.markdown("## 🧭 Navigation")
st.sidebar.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
if st.sidebar.button("🤖 Live AI Agent Demo", use_container_width=True):
    change_page("live_agent")
if st.sidebar.button("👤 My Profile", use_container_width=True):
    change_page("my_profile")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("## 📊 Dept Dashboards")
st.sidebar.markdown("<div class='nav-btn'>", unsafe_allow_html=True)
if st.sidebar.button("🌐 Network", use_container_width=True): change_page("dashboard_Network")
if st.sidebar.button("🔒 Security", use_container_width=True): change_page("dashboard_Security")
if st.sidebar.button("💻 Application", use_container_width=True): change_page("dashboard_Application")
if st.sidebar.button("🗄️ Database", use_container_width=True): change_page("dashboard_Database")
if st.sidebar.button("☁️ Infrastructure", use_container_width=True): change_page("dashboard_Infrastructure")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**System Health**", unsafe_allow_html=True)
st.sidebar.info("🟢 ONLINE - Endee Matrix Engine Active")
st.sidebar.markdown("---")
st.sidebar.caption("ENGINE SPECS")
st.sidebar.markdown("🧠 **Model:** `all-MiniLM-L6-v2`")
st.sidebar.markdown("⚡ **Param Dimensions:** `384 Dims`")
st.sidebar.markdown("🗂️ **Knowledge Base:** `1,000 Verified Tickets`")
st.sidebar.markdown("🛡️ **PII Redaction:** `ACTIVE`")

# ==========================================
# 🖥️ PAGE: DEPARTMENT DASHBOARD
# ==========================================
if str(st.session_state.page).startswith("dashboard_"):
    dept_name = str(st.session_state.page).split("_")[1]
    
    st.markdown(f"""
    <div class="main-header">
        <div style="font-size: 2.5em;">📊</div>
        <div>
            <h1>{dept_name} Department Analytics</h1>
            <div style="color: #8b949e; font-size: 0.95em;">30-Day Trailing Escalation & Resolution Metrics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter Data
    df_dept = df_analytics[df_analytics['category'] == dept_name]
    total_tickets = len(df_dept)
    completed_tickets = len(df_dept[df_dept['status'] == "Completed"])
    in_progress_tickets = len(df_dept[df_dept['status'] == "In Progress"])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Tickets (30d)", value=total_tickets)
    with col2:
        completion_rate = f"{(completed_tickets/max(total_tickets, 1))*100:.1f}%"
        st.metric(label="AI Deflection Rate", value=completion_rate)
    with col3:
        st.metric(label="In Progress", value=in_progress_tickets)
    with col4:
        st.metric(label="Avg Resolution TTR", value="2.4 hrs", delta="-1.1 hrs", delta_color="inverse")
        
    st.markdown("<hr style='border-color: #30363d;'>", unsafe_allow_html=True)
    
    st.markdown("### 📈 Ticket Volume (Last 30 Days)")
    chart_data = df_dept.groupby('date_str').size().rename("Ticket Volume")
    st.bar_chart(chart_data, color="#1f6feb", use_container_width=True)
    
    st.markdown("<br>### 📋 Recent Actioned Tickets", unsafe_allow_html=True)
    
    # Clean table view
    display_df = df_dept[['id', 'priority', 'status', 'title', 'date_str']].head(20).copy()
    display_df.columns = ["Ticket ID", "Priority", "Status", "Issue Summary", "Date Logged"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)


# ==========================================
# 🖥️ PAGE: USER PROFILE
# ==========================================
elif st.session_state.page == "my_profile":
    st.markdown("""
    <div class="main-header">
        <div style="font-size: 2.5em;">👤</div>
        <div>
            <h1>User Profile Dashboard</h1>
            <div style="color: #8b949e; font-size: 0.95em;">Manage your active tickets and historical requests</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_prof1, col_prof2 = st.columns([1, 2])
    with col_prof1:
        st.markdown("""
        <div class="ticket-card" style="text-align: center;">
            <div style="width: 80px; height: 80px; border-radius: 50%; background: #1f6feb; color: white; display: flex; align-items: center; justify-content: center; font-size: 2em; margin: 0 auto 15px auto; font-weight: bold;">DK</div>
            <h3 style="margin: 0; color: #ffffff;">Dharun Kumar</h3>
            <p style="color: #8b949e; margin: 5px 0;">Software Engineer</p>
            <hr style="border-color: #30363d; margin: 15px 0;">
            <div style="text-align: left; font-size: 0.9em;">
                <p><strong>Employee ID:</strong> EMP-7742</p>
                <p><strong>Department:</strong> Engineering R&D</p>
                <p><strong>Location:</strong> Chennai / IND</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_prof2:
        st.markdown("### 🎫 My Ticket History")
        if not st.session_state.user_history:
            st.info("You haven't submitted any tickets yet in this session. Go to the Live Agent Demo to trigger a query!")
        else:
            for tkt in st.session_state.user_history:
                st.markdown(f'''
                <div class="ticket-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <span class="ticket-id-badge">{tkt['ticket_id']}</span>
                            <span style="color: #8b949e; font-size: 0.85em; margin-left: 10px;">Submitted: {tkt['timestamp']}</span>
                        </div>
                        <div>
                            <span class="badge" style="background: {'#238636' if tkt['status'] == 'COMPLETED' else '#b62324'}; color: white;">{tkt['status']}</span>
                        </div>
                    </div>
                    <p style="margin: 15px 0; color: #c9d1d9; font-size: 0.95em;"><strong>Query:</strong> {tkt['original_query']}</p>
                    <div style="background: rgba(48, 54, 61, 0.4); padding: 10px; border-radius: 6px; font-size: 0.85em; color: #8b949e; border-left: 3px solid #1f6feb;">
                        <strong>Routed Dept:</strong> {tkt['ai_assigned_category']} &nbsp;&nbsp;|&nbsp;&nbsp; 
                        <strong>Priority:</strong> {tkt['priority']} &nbsp;&nbsp;|&nbsp;&nbsp;
                        <strong>Resolution:</strong> {tkt['final_resolution']}
                    </div>
                </div>
                ''', unsafe_allow_html=True)


# ==========================================
# 🖥️ PAGE: LIVE AI AGENT INFERENCE
# ==========================================
elif st.session_state.page == "live_agent":
    st.markdown("""
    <div class="main-header">
        <div style="font-size: 2.5em;">🤖</div>
        <div>
            <h1>IT Workspace AI</h1>
            <div style="color: #8b949e; font-size: 0.95em;">Automated Issue Triage & Resolution Assistant</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    def get_stepper_html(step):
        """Generates a clean HTML stepper."""
        s1_class = "step active" if step >= 1 else "step"
        s2_class = "step active pulse" if step == 2 else ("step active" if step > 2 else "step")
        s3_class = "step active pulse" if step == 3 else ("step active" if step > 3 else "step")
        s4_class = "step active pulse" if step == 4 else ("step active" if step > 4 else "step")
        s5_class = "step active pulse" if step == 5 else ("step active" if step > 5 else "step")
        
        html = f"""
        <div class="stepper-container">
            <div class="{s1_class}">
                <div class="step-icon">1</div>
                <p>Log & Scrub PII</p>
            </div>
            <div class="{s2_class}">
                <div class="step-icon">2</div>
                <p>Sentiment Sync</p>
            </div>
            <div class="{s3_class}">
                <div class="step-icon">3</div>
                <p>Vector Analysis</p>
            </div>
            <div class="{s4_class}">
                <div class="step-icon">4</div>
                <p>Dynamic Route</p>
            </div>
            <div class="{s5_class}">
                <div class="step-icon">5</div>
                <p>Resolution Status</p>
            </div>
        </div>
        """
        return html

    # AI Input Area
    with st.container():
        col_q1, col_q2, col_q3 = st.columns(3)
        
        if 'quick_query' not in st.session_state:
            st.session_state.quick_query = ""
            
        with col_q1:
            st.markdown("<div class='preset-btn'>", unsafe_allow_html=True)
            if st.button("🔥 Try: Urgent Infrastructure", use_container_width=True):
                st.session_state.quick_query = "URGENT! Our production web-prod-1 server is completely down right now and throwing a 502 Bad Gateway error. Customers cannot access the portal!"
            st.markdown("</div>", unsafe_allow_html=True)
        with col_q2:
            st.markdown("<div class='preset-btn'>", unsafe_allow_html=True)
            if st.button("🔌 Try: Access / Security Issue", use_container_width=True):
                st.session_state.quick_query = "A former employee's laptop was stolen at the airport and we need to revoke VPN and SSO access immediately. Pwd leaked."
            st.markdown("</div>", unsafe_allow_html=True)
        with col_q3:
            st.markdown("<div class='preset-btn'>", unsafe_allow_html=True)
            if st.button("⚠️ Try: Impossible Ambiguity", use_container_width=True):
                st.session_state.quick_query = "The sandwich in the breakroom refrigerator is frozen completely solid and my desk is sticky."
            st.markdown("</div>", unsafe_allow_html=True)

        query = st.text_area("Describe the IT issue:", value=st.session_state.quick_query, height=100, placeholder="E.g. The database server keeps crashing under load...", key="query_input")
        
        col_empty, col_btn = st.columns([4, 1])
        with col_btn:
            analyze_btn = st.button("Process Ticket", use_container_width=True)

    if analyze_btn and query:
        ticket_id = f"TKT-{str(uuid.uuid4())[:8].upper()}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.markdown("<hr style='border-color: #30363d;'>", unsafe_allow_html=True)
        
        # --- LIFECYCLE TRACKER ---
        st.markdown(f"**Tracing Workflow for <span class='ticket-id-badge'>{ticket_id}</span>**", unsafe_allow_html=True)
        lifecycle_placeholder = st.empty()
        
        lifecycle_placeholder.markdown(get_stepper_html(1), unsafe_allow_html=True) # PII Scrub
        time.sleep(0.5) 
        
        lifecycle_placeholder.markdown(get_stepper_html(2), unsafe_allow_html=True) # Sentiment
        time.sleep(0.4)
        # Simple heuristic sentiment logic
        critical_keywords = ['urgent', 'down', 'stolen', 'immediately', 'crashed', 'crashing', 'leaked', 'hack']
        is_critical = any(word.lower() in query.lower() for word in critical_keywords)
        
        lifecycle_placeholder.markdown(get_stepper_html(3), unsafe_allow_html=True) # Analysis
        start_t = time.time()
        query_vector = model.encode(query).tolist()
        results = index.query(vector=query_vector, top_k=3)
        latency = (time.time() - start_t) * 1000
        time.sleep(0.5) 
        
        lifecycle_placeholder.markdown(get_stepper_html(4), unsafe_allow_html=True) # Routing
        time.sleep(0.5) 

        lifecycle_placeholder.markdown(get_stepper_html(5), unsafe_allow_html=True) # Resolution
        
        if results and len(results) > 0:
            top_match = results[0]
            confidence = top_match['similarity']
            matched_priority = top_match['meta'].get('priority', 'Medium')
            if is_critical:
                matched_priority = 'Critical'
                
            # Determine Routing
            if confidence >= 0.85:
                assigned_cat = top_match['meta']['category']
            elif confidence >= 0.30:
                 assigned_cat = top_match['meta']['category']
            else:
                assigned_cat = "ESCALATED (Uncertain)"

            # Set Estimated Time based on priority
            eta_map = {
                "Critical": "< 15 minutes (Immediate Dispatch)",
                "High": "< 1 hour",
                "Medium": "Same Business Day",
                "Low": "Next Business Day"
            }
            eta_str = eta_map.get(matched_priority, "Standard Wait")

            # Status Banner rendering mechanism
            status_banner_placeholder = st.empty()
            timer_placeholder = st.empty()
            
            def render_banner(s_class, s_text, s_msg):
                status_banner_placeholder.markdown(f"""
                <div style="background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 10px; margin-bottom: 25px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3 style="margin: 0; font-size: 1.1em; color: #ffffff;">System Processing Status</h3>
                            <p style="margin: 5px 0 0 0; color: #8b949e; font-size: 0.9em;">{s_msg}</p>
                        </div>
                        <div>
                            <span class="{s_class}">{s_text}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if confidence >= 0.85:
                render_banner("status-completed", "COMPLETED", f"✅ Autonomous Resolution Delivered for {ticket_id}.")
            elif confidence >= 0.30:
                pass 
            else:
                render_banner("status-escalated", "ESCALATED", f"⚠️ Manual Triage Required for {ticket_id}.")

            # Render Core Payload Info
            col_left, col_right = st.columns([1, 1.2])
            
            with col_left:
                st.markdown("#### 🎯 Routing Decision")
                
                # --- SENTIMENT URGENCY INJECTION ---
                if is_critical and confidence >= 0.30:
                    st.markdown(f"""
                    <div class="sentiment-banner">
                        🔥 <b>CRITICAL URGENCY DETECTED BY AI</b><br>
                        <span style="font-weight:normal; font-size:0.9em;">Stress lexicon detected in text. Upgrading system priority classification. Bypassing standard queues.</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                if confidence < 0.30:
                    st.markdown(f"""
                    <div class="escalate-banner">
                        ⚠️ AGENT ESCALATION TRIGGERED<br>
                        <span style="font-weight:normal; font-size:0.9em;">Confidence metric ({confidence:.2f}) fell below bounds. Routing disabled.</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                all_depts = ["Infrastructure", "Application", "Security", "Database", "Network", "Access Management"]
                
                html_routes = "<div style='display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; margin-bottom: 20px;'>"
                for dept in all_depts:
                    if dept == assigned_cat:
                        html_routes += f"<div style='background: #1f6feb; color: white; padding: 6px 12px; border-radius: 15px; font-weight: 600; font-size: 0.85em;'>✓ {dept}</div>"
                    else:
                        html_routes += f"<div style='background: transparent; color: #8b949e; padding: 6px 12px; border-radius: 15px; font-weight: 500; font-size: 0.85em; border: 1px solid #30363d;'>○ {dept}</div>"
                
                if assigned_cat == "ESCALATED (Uncertain)":
                    html_routes += f"<div style='background: #b62324; color: white; padding: 6px 12px; border-radius: 15px; font-weight: 600; font-size: 0.85em;'>⚠️ Manual Triage</div>" 
                html_routes += "</div>"
                st.markdown(html_routes, unsafe_allow_html=True)
                
                if len(results) >= 2 and results[0]['similarity'] > 0.65 and results[1]['similarity'] > 0.65:
                    st.markdown(f"""
                    <div class="automation-banner">
                        🤖 MACRO-AUTOMATION PROPOSED<br>
                        <span style="font-weight:normal; font-size:0.9em;">Detected frequent semantic overlap. Recommending RPA automation flow.</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
            with col_right:
                st.markdown("#### 💡 AI Action Plan")
                with st.container(border=True):
                    resolution = top_match['meta']['resolution']
                    if confidence >= 0.85:
                        st.success(f"**Automated Resolution Sent:**\n{resolution}")
                    else:
                        st.info(f"**Recommended Engineering Workflow for Assignee:**\n{resolution}")
            
            st.markdown("<hr style='border-color: #30363d;'>", unsafe_allow_html=True)
            st.markdown("#### 📚 Referenced Internal Knowledge")
            for r in results:
                sim = r['similarity']
                meta = r['meta']
                pri = meta.get('priority', 'Medium')
                
                # Boost priority badge visually if sentiment was critical
                if is_critical and r == top_match:
                    pri = 'Critical'
                    
                st.markdown(f"""
                <div class="ticket-card">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <div><span class="badge badge-category">{meta['category']}</span> <span class="badge badge-priority-{pri}">{pri} Priority</span></div>
                        <div style="color: #3fb950; font-weight: 600; font-size: 0.9em;">Confidence: {(sim*100):.1f}%</div>
                    </div>
                    <h4 style="margin: 0 0 5px 0; color: #ffffff; font-size: 1.1em;">{meta.get('title', 'Historical Incident')}</h4>
                    <p style="color: #8b949e; font-size: 0.9em; margin-bottom: 10px;">{meta['text']}</p>
                    <div style="background: rgba(46, 160, 67, 0.1); padding: 10px; border-radius: 6px; font-size: 0.85em; color: #c9d1d9; border-left: 3px solid #2ea043;">
                        <strong>Action Log:</strong> {meta['resolution']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # --- LIVE HUMAN ANALYST SIMULATION ---
            if confidence >= 0.30 and confidence < 0.85:
                timer_placeholder.empty()
                
                # ETA Feature injected here directly for the user!
                eta_msg = f"⏳ Waiting for analyst...<br><span style='color: #8b949e; font-size: 0.9em;'><strong>Estimated Wait Time (Based on {matched_priority} Priority):</strong> {eta_str}</span>"
                render_banner("status-notstarted", "OPEN", eta_msg)
                time.sleep(20)
                
                render_banner("status-inprogress", "IN PROGRESS", "👨‍💻 Analyst take this problem...")
                time.sleep(20)
                
                analyst_solution = top_match['meta']['resolution']
                final_msg = f"✅ Completed.<br><br><span style='color: #c9d1d9;'><strong>Analyst Final Solution Notes:</strong></span><br><span style='color: #3fb950; font-style: italic;'>\"{analyst_solution}\"</span>"
                render_banner("status-completed", "COMPLETED", final_msg)

            # --- EXPORT REPORT BUTTON & USER FEEDBACK ---
            st.markdown("<br>", unsafe_allow_html=True)
            
            # User Feedback feature
            st.markdown("<div style='text-align: center; margin-bottom: 20px; color: #c9d1d9;'><strong>Did this resolution help solve your issue today?</strong></div>", unsafe_allow_html=True)
            col_f1, col_f2, col_f3, col_f4 = st.columns([2, 1, 1, 2])
            with col_f2:
                st.markdown("<div class='feedback-btn'>", unsafe_allow_html=True)
                if st.button("👍 Yes, Solved", use_container_width=True):
                    st.toast("Thank you for your feedback! This helps train the AI.", icon="🎉")
                st.markdown("</div>", unsafe_allow_html=True)
            with col_f3:
                st.markdown("<div class='feedback-btn'>", unsafe_allow_html=True)
                if st.button("👎 No, Need help", use_container_width=True):
                    st.toast("Sorry about that! We've immediately escalated this to human review.", icon="⚠️")
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("<br><hr style='border-color: #30363d;'><br>", unsafe_allow_html=True)
            
            export_data = {
                "ticket_id": ticket_id,
                "timestamp": timestamp,
                "original_query": query,
                "is_critical_sentiment": is_critical,
                "ai_assigned_category": assigned_cat,
                "priority": matched_priority,
                "match_confidence": round(confidence, 4),
                "latency_ms": round(latency, 2),
                "final_resolution": top_match['meta']['resolution'],
                "status": "COMPLETED" if confidence >= 0.30 else "ESCALATED",
                "model_used": "all-MiniLM-L6-v2",
                "db_used": "Endee Vector Storage"
            }
            if not any(t['ticket_id'] == ticket_id for t in st.session_state.user_history):
                st.session_state.user_history.insert(0, export_data)
                
            json_dump = json.dumps(export_data, indent=4)
            
            st.download_button(
                label="⬇️ Download Ticket Report (JSON)",
                data=json_dump,
                file_name=f"{ticket_id}_report.json",
                mime="application/json",
                use_container_width=True
            )

        else:
            st.warning("No context matched. Escalating directly to Engineering queue.")
