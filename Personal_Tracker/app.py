import streamlit as st
import database as db
import datetime
import roadmap
import pandas as pd
import quiz_engine

# --- Configuration ---
st.set_page_config(page_title="Personal ML Tracker", page_icon="✨", layout="centered")

# Initialize Database
db.init_db()

# --- Aesthetic & Minimal Design (CSS) ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
        width: 250px;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #E6EDF3 !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }
    
    /* Input Areas */
    .stTextArea textarea, .stTextInput input, .stRadio label {
        color: #C9D1D9;
    }
    .stRadio div[role='radiogroup'] {
        background-color: #0D1117;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #30363D;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #2EA043;
        transform: translateY(-1px);
    }
    
    /* Custom Badge for Difficulty */
    .badge-easy { background-color: #238636; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; }
    .badge-medium { background-color: #d29922; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; }
    .badge-hard { background-color: #da3633; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; }
    
</style>
""", unsafe_allow_html=True)

# --- Logic for Roadmap ---
def initialize_roadmap(start_date):
    for week_num, content in roadmap.ML_ROADMAP.items():
        week_start = start_date + datetime.timedelta(weeks=week_num-1)
        week_str = week_start.strftime("%Y-%m-%d")
        for goal in content["goals"]:
            db.add_weekly_goal(week_str, f"Week {week_num} [{content['title']}]: {goal}")
    db.set_setting("roadmap_start_date", start_date.strftime("%Y-%m-%d"))

# --- Sidebar ---
st.sidebar.markdown("### 🧭 Navigation")
page = st.sidebar.radio("", ["Dashboard", "Log Progress", "Daily Quiz", "Goals", "Projects", "Analytics", "Settings"], label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 Motivation")
st.sidebar.info("\"The best way to predict the future is to invent it.\"")

# --- Main Logic ---

if page == "Dashboard":
    st.title("👋 Welcome Back")
    
    stats = db.get_analytics_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Streak", f"{stats['current_streak']} Days", "🔥")
    with col2:
        st.metric("Total Logs", stats['total_logs'])
    with col3:
        st.metric("Avg Confidence", f"{stats['avg_confidence']}/5")
        
    st.markdown("---")
    st.subheader("Recent Activity")
    logs = db.get_all_logs()
    if logs:
        for log in logs[:3]: 
            with st.container():
                st.markdown(f"""
                <div style="background-color: #161B22; padding: 15px; border-radius: 10px; border: 1px solid #30363D; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: #58A6FF;">{log[0]}</h4>
                        <span style="background-color: #238636; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px;">Score: {log[3]}/5</span>
                    </div>
                    <p style="color: #8B949E; margin-top: 5px; font-size: 14px;">{log[2][:100]}...</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No logs yet. Start your journey in the 'Log Progress' tab.")

elif page == "Log Progress":
    st.title("✍️ Daily Focus")
    selected_date = st.date_input("Date", datetime.date.today(), label_visibility="hidden")
    date_str = selected_date.strftime("%Y-%m-%d")

    existing_log = db.get_daily_log(date_str)
    default_planned = existing_log[1] if existing_log else ""
    default_actual = existing_log[2] if existing_log else ""
    default_confidence = existing_log[3] if existing_log else 3

    with st.form("daily_log_form"):
        st.markdown("### 🎯 Plan")
        planned_tasks = st.text_area("Objective", value=default_planned, height=100)
        st.markdown("### 🧠 Retrospective")
        actual_learning = st.text_area("What stuck?", value=default_actual, height=100)
        st.markdown("### 🔋 Energy")
        confidence_score = st.slider("", 1, 5, value=default_confidence)
        
        if st.form_submit_button("Save Entry"):
            db.add_daily_log(date_str, planned_tasks, actual_learning, confidence_score)
            st.toast(f"Entry saved!", icon="✅")

elif page == "Daily Quiz":
    st.title("🧩 Daily Knowledge Check")
    
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    
    # Check if we have determined a topic for today?
    # Logic: Get current week from roadmap or use a placeholder topic based on Day of Week or random
    # For now: Try to get the topic from current week in roadmap
    
    roadmap_start = db.get_setting("roadmap_start_date")
    topic_for_quiz = "Machine Learning" # Default
    
    if roadmap_start:
        start_date = datetime.datetime.strptime(roadmap_start, "%Y-%m-%d").date()
        today = datetime.date.today()
        days_diff = (today - start_date).days
        week_idx = max(0, min(days_diff // 7, 23))
        week_data = roadmap.ML_ROADMAP.get(week_idx+1)
        if week_data:
            topic_for_quiz = week_data["title"]

    st.markdown(f"**Today's Topic**: {topic_for_quiz}")
    
    # Check if quiz already taken
    past_result = db.get_quiz_result(today_str)
    
    if past_result:
        # Show results
        st.success(f"You have already completed today's quiz!")
        st.metric("Your Score", f"{past_result[1]} / {past_result[2]}")
        
    else:
        # Generate new quiz (store in session state so it doesn't reshuffle on re-render)
        if "quiz_data" not in st.session_state:
            st.session_state.quiz_data = quiz_engine.generate_quiz(topic_for_quiz)
            
        questions = st.session_state.quiz_data
        
        with st.form("quiz_form"):
            score = 0
            user_answers = {}
            
            # 5 Easy
            st.markdown("### Level 1: Foundations (Easy)")
            for i in range(5):
                q = questions[i]
                st.markdown(f"**{i+1}. {q['question']}**")
                user_answers[i] = st.radio(f"Select answer for Q{i+1}", q['options'], key=f"q{i}", label_visibility="collapsed")
                st.divider()

            # 5 Medium
            st.markdown("### Level 2: Application (Medium)")
            for i in range(5, 10):
                q = questions[i]
                st.markdown(f"**{i+1}. {q['question']}**")
                user_answers[i] = st.radio(f"Select answer for Q{i+1}", q['options'], key=f"q{i}", label_visibility="collapsed")
                st.divider()

            # 5 Hard
            st.markdown("### Level 3: Theory & Edge Cases (Hard)")
            for i in range(10, 15):
                q = questions[i]
                st.markdown(f"**{i+1}. {q['question']}**")
                user_answers[i] = st.radio(f"Select answer for Q{i+1}", q['options'], key=f"q{i}", label_visibility="collapsed")
                st.divider()
                
            submitted = st.form_submit_button("Submit Assessment")
            
            if submitted:
                # Calculate score
                for i in range(15):
                    if user_answers[i] == questions[i]['answer']:
                        score += 1
                
                db.add_quiz_result(today_str, score, 15, topic_for_quiz)
                st.session_state.quiz_score = score
                st.rerun()

elif page == "Goals":
    st.title("🎯 Weekly Targets")
    roadmap_start = db.get_setting("roadmap_start_date")
    if not roadmap_start:
        st.warning("Roadmap not initialized. Go to Settings.")
    else:
        start_date = datetime.datetime.strptime(roadmap_start, "%Y-%m-%d").date()
        today = datetime.date.today()
        week_options = []
        for i in range(24):
            w_start = start_date + datetime.timedelta(weeks=i)
            week_options.append(f"Week {i+1}: {w_start.strftime('%b %d')}")
        days_diff = (today - start_date).days
        current_week_idx = max(0, min(days_diff // 7, 23))
        
        selected_week_str = st.selectbox("Select Week", week_options, index=current_week_idx)
        selected_week_idx = week_options.index(selected_week_str)
        view_start_date = start_date + datetime.timedelta(weeks=selected_week_idx)
        view_start_str = view_start_date.strftime("%Y-%m-%d")
        
        st.markdown(f"**Focus**: {roadmap.ML_ROADMAP.get(selected_week_idx+1, {}).get('title', 'Unknown')}")
        goals = db.get_weekly_goals(view_start_str)
        
        if goals:
            completed_count = sum(1 for g in goals if g[3])
            progress = completed_count / len(goals)
            st.progress(progress, text=f"Progress: {int(progress*100)}%")
            for goal in goals:
                g_id, _, text, is_done, _ = goal
                col1, col2 = st.columns([0.1, 9])
                with col1:
                    is_checked = st.checkbox("", value=bool(is_done), key=f"goal_{g_id}")
                    if is_checked != bool(is_done):
                        db.toggle_goal_complete(g_id, is_done)
                        st.rerun()
                with col2:
                    if is_done:
                        st.markdown(f"<span style='color: #8b949e; text-decoration: line-through;'>{text}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span>{text}</span>", unsafe_allow_html=True)
        else:
            st.info("No goals found for this week.")

elif page == "Projects":
    st.title("🚀 Portfolio Projects")
    with st.expander("➕ Add New Project"):
        with st.form("new_project_form"):
            p_name = st.text_input("Project Name")
            p_desc = st.text_area("Description")
            p_link = st.text_input("GitHub/Demo Link")
            p_status = st.selectbox("Status", ["Not Started", "In Progress", "Done"])
            if st.form_submit_button("Create Project"):
                db.add_project(p_name, p_desc, p_status, p_link)
                st.rerun()

    st.markdown("---")
    projects = db.get_projects()
    if projects:
        for p in projects:
            p_id, name, desc, status, link, _ = p
            status_color = "#238636" if status == "Done" else "#d29922" if status == "In Progress" else "#8b949e"
            with st.container():
                st.markdown(f"""
                <div style="background-color: #161B22; border: 1px solid #30363D; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h3 style="margin: 0; color: #58A6FF;">{name}</h3>
                            <p style="color: #8B949E; margin-top: 5px; font-size: 14px;">{desc}</p>
                            {'<a href="' + link + '" target="_blank" style="color: #58A6FF; text-decoration: none;">🔗 Link</a>' if link else ''}
                        </div>
                        <span style="background-color: {status_color}; color: white; padding: 2px 10px; border-radius: 12px; font-size: 12px;">{status}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([2,1])
                with col1:
                    new_stat = st.selectbox("Status", ["Not Started", "In Progress", "Done"], index=["Not Started", "In Progress", "Done"].index(status), key=f"p_{p_id}", label_visibility="collapsed")
                    if new_stat != status:
                        db.update_project_status(p_id, new_stat)
                        st.rerun()

elif page == "Analytics":
    st.title("📊 Analytics & Reflections")
    tab1, tab2 = st.tabs(["Charts", "Monthly Assessment"])
    with tab1:
        st.subheader("Confidence Trend")
        logs = db.get_all_logs()
        if logs:
            df = pd.DataFrame(logs, columns=["date", "planned", "actual", "confidence", "created_at"])
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            st.line_chart(df.set_index('date')['confidence'], color="#58A6FF")
        else:
            st.info("Log some days to see your confidence trend.")
    with tab2:
        st.subheader("Monthly Reflection")
        today = datetime.date.today()
        current_month_str = today.strftime("%Y-%m")
        month_input = st.text_input("Month (YYYY-MM)", value=current_month_str)
        with st.form("assessment_form"):
            reflection = st.text_area("Big Picture: What went well? What didn't?", height=150)
            rating = st.slider("Overall Satisfaction", 1, 10, 5)
            if st.form_submit_button("Save Assessment"):
                db.add_monthly_assessment(month_input, reflection, rating)
                st.rerun()
        st.markdown("---")
        st.subheader("Past Assessments")
        assessments = db.get_monthly_assessments()
        if assessments:
            for a in assessments:
                with st.expander(f"{a[1]} - Rating: {a[3]}/10"):
                    st.write(a[2])

elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("Roadmap Automation")
    today = datetime.date.today()
    last_monday = today - datetime.timedelta(days=today.weekday())
    start_date_input = st.date_input("Course Start Date (Monday)", last_monday)
    if st.button("Generate/Reset Roadmap"):
        with st.spinner("Generating 24-week plan..."):
            initialize_roadmap(start_date_input)
        st.success("Roadmap generated! Check the 'Goals' tab.")
