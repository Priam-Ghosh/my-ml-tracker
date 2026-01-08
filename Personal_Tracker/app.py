import streamlit as st
import database as db
import datetime
import roadmap
import pandas as pd
import roadmap
import pandas as pd
import quiz_engine
import json

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
    # Clear existing goals if needed? user handles via reset usually.
    # We will just append if not careful, but the DB init doesn't clear.
    # Ideally we should clear old goals for the Roadmap weeks.
    # But for now, let's just add the new ones.
    
    for week_num, content in roadmap.ML_ROADMAP.items():
        week_start = start_date + datetime.timedelta(weeks=week_num-1)
        week_str = week_start.strftime("%Y-%m-%d")
        
        # New Structure: goals are Day Titles
        # content['days'] is a dict {day_num: {...}}
        # We sort by day_num just in case
        for day_num in sorted(content['days'].keys()):
            day_data = content['days'][day_num]
            # Goal text concept: "Day X: Title"
            goal_text = f"Day {day_num}: {day_data['title']}"
            db.add_weekly_goal(week_str, goal_text)
            
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

    # Fetch existing log
    existing_log = db.get_daily_log(date_str)
    # Indices: 0=date, 1=plan(old), 2=actual(old), 3=conf, 4=created, 5=topics(new), 6=revision(new)
    
    default_topics = []
    default_revision = ""
    default_confidence = 3
    
    if existing_log:
        default_confidence = existing_log[3]
        if len(existing_log) > 5 and existing_log[5]:
             try:
                 default_topics = json.loads(existing_log[5])
             except:
                 pass
        if len(existing_log) > 6 and existing_log[6]:
            default_revision = existing_log[6]

    # Roadmap / Goals Logic
    roadmap_start = db.get_setting("roadmap_start_date")
    current_day_topics = []
    
    if roadmap_start:
        start_date = datetime.datetime.strptime(roadmap_start, "%Y-%m-%d").date()
        # Find which Day Number (1-based)
        days_diff = (selected_date - start_date).days
        day_num = days_diff + 1
        
        if 1 <= day_num <= 168:
            # Find Week
            week_idx = (day_num - 1) // 7 + 1
            
            # Fetch topics for this specific day from roadmap.py
            # roadmap.ML_ROADMAP[week][days][day_num]
            week_data = roadmap.ML_ROADMAP.get(week_idx)
            if week_data and 'days' in week_data:
                day_data = week_data['days'].get(day_num)
                if day_data:
                     # Add Day Title as first item or header?
                     # User wants topics.
                     current_day_topics = day_data['topics']
                     st.caption(f"**Day {day_num}: {day_data['title']}**")
        else:
            if day_num < 1:
                st.info("Selected date is before the roadmap start.")
            else:
                st.info("Congratulations! You have passed the 168-day roadmap.")

    with st.form("daily_log_form"):
        st.markdown("### 📚 Daily Learning")
        
        selected_topics = []
        if current_day_topics:
            st.caption("Select topics learned today:")
            for i, topic in enumerate(current_day_topics):
                # Check if this topic is in default_topics
                is_checked = topic in default_topics
                if st.checkbox(topic, value=is_checked, key=f"topic_{i}"):
                    selected_topics.append(topic)
        else:
            if not roadmap_start:
                st.info("Roadmap not initialized. Go to Settings.")
            else:
                 st.info("No specific topics found for this day (Rest day or outside range).")

        st.markdown("### 🔄 Topics to Revise")
        revision_notes = st.text_area("Enter topics/sub-topics to revise", value=default_revision, height=100)
        
        # --- SATURDAY SPECIAL SLOT ---
        # Check if it is Day 6 of the week
        if 1 <= day_num <= 168 and (day_num % 7 == 6):
            st.markdown("---")
            st.markdown("### 🔁 Saturday Weekly Revision")
            st.info("It's Saturday! Time to review everything you learned this week.")
            
            # Fetch logs for Day 1 to Day 5 of this week
            # Current date is Day 6. Day 1 is 5 days ago.
            topics_to_review = []
            
            for i in range(1, 6):
                 # d = selected_date - timedelta(days=i) ? 
                 # day_num is 6. day_num-1=5 (Friday), day_num-5=1 (Monday)
                 # So we look back 1 to 5 days.
                 lookback_date = selected_date - datetime.timedelta(days=i)
                 lookback_str = lookback_date.strftime("%Y-%m-%d")
                 l = db.get_daily_log(lookback_str)
                 if l and len(l) > 5 and l[5]:
                     try:
                         day_topics = json.loads(l[5])
                         topics_to_review.extend(day_topics)
                     except:
                         pass
            
            if topics_to_review:
                with st.expander("� Topics added this week", expanded=True):
                    for t in set(topics_to_review): # unique topics
                        st.markdown(f"- {t}")
                st.caption("Use the 'Topics to Revise' box above to note down any struggles.")
            else:
                st.warning("No learning logs found for this week yet.")

        st.markdown("### �🔋 Energy")
        confidence_score = st.slider("", 1, 5, value=default_confidence)
        
        if st.form_submit_button("Save Entry"):
            db.add_daily_log(date_str, json.dumps(selected_topics), revision_notes, confidence_score)
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
                
                # Style enhancement for Special Days
                # text format "Day X: Title"
                icon = "📄"
                extra_style = ""
                if "Day " in text:
                    try:
                        d_num_part = text.split(":")[0].replace("Day ", "")
                        d_n = int(d_num_part)
                        if d_n % 7 == 6:
                            icon = "🔁" # Revision
                            extra_style = "border-left: 3px solid #d29922;"
                        elif d_n % 7 == 0:
                            icon = "🛠️" # Project
                            extra_style = "border-left: 3px solid #8957e5;"
                    except:
                        pass

                col1, col2 = st.columns([0.1, 9])
                with col1:
                    is_checked = st.checkbox("", value=bool(is_done), key=f"goal_{g_id}")
                    if is_checked != bool(is_done):
                        db.toggle_goal_complete(g_id, is_done)
                        st.rerun()
                with col2:
                    content_html = f"<span>{icon} {text}</span>"
                    if is_done:
                        content_html = f"<span style='color: #8b949e; text-decoration: line-through;'>{icon} {text}</span>"
                    
                    if extra_style:
                         st.markdown(f"<div style='padding-left: 10px; {extra_style}'>{content_html}</div>", unsafe_allow_html=True)
                    else:
                         st.markdown(content_html, unsafe_allow_html=True)
        else:
            st.info("No goals found for this week.")
            
    st.markdown("---")
    with st.expander("📅 Daily Learning History (Special Section)", expanded=True):
        st.write("Recent daily logs:")
        all_logs = db.get_all_logs()
        # Filter logs that have new structure? Or show all.
        if all_logs:
            for log in all_logs[:7]: # Show last 7
                # 0=date, 5=topics, 6=revise
                date = log[0]
                topics = []
                revision = ""
                # Handle potential missing columns for old logs if query returned *
                if len(log) > 5 and log[5]:
                    try:
                        topics = json.loads(log[5])
                    except:
                        pass
                if len(log) > 6 and log[6]:
                    revision = log[6]
                    
                st.markdown(f"**{date}**")
                if topics:
                    st.markdown("*Learned:*")
                    for t in topics:
                        st.markdown(f"- {t}")
                if revision:
                    st.markdown(f"*To Revise:* {revision}")
                st.divider()
        else:
            st.info("No logs yet.")

elif page == "Projects":
    st.title("🚀 Portfolio Projects")
    
    # 1. Fetch Key Data
    roadmap_start = db.get_setting("roadmap_start_date")
    current_day_num = 0
    if roadmap_start:
        start_date = datetime.datetime.strptime(roadmap_start, "%Y-%m-%d").date()
        today = datetime.date.today()
        current_day_num = (today - start_date).days + 1

    # 2. defined projects
    defined_projects = roadmap.ML_PROJECTS
    
    # 3. existing db projects
    db_projects = db.get_projects() 
    # db_projects tuple structure: id, name, desc, status, link, created, roadmap_day
    
    # helper to find db match
    def find_db_match(r_day, r_title):
        for p in db_projects:
            # Check ID match if available (new schema) or Name match (legacy)
            # p[6] is roadmap_project_day (might be None for old records)
            if len(p) > 6 and p[6] == r_day:
                return p
            if p[1] == r_title:
                return p
        return None

    st.caption("Track your hands-on journey. Projects are unlocked as you progress.")
    
    sorted_days = sorted(defined_projects.keys())
    
    # Display Logic
    for r_day in sorted_days:
        p_def = defined_projects[r_day]
        title = p_def["title"]
        desc = p_def["description"]
        features = p_def["features"]
        
        db_match = find_db_match(r_day, title)
        
        # Determine Status
        status = "Upcoming"
        link = ""
        p_id = None
        
        if db_match:
            p_id = db_match[0]
            status = db_match[3]
            link = db_match[4]
        else:
            # Logic for Missing vs Upcoming
            if current_day_num > r_day + 7: # Allow 1 week grace period?
                 status = "Missing"
            elif current_day_num >= r_day:
                 status = "Not Started"
            else:
                 status = "Upcoming"

        # Badge Colors
        color_map = {
            "Done": "#238636", # Green
            "In Progress": "#d29922", # Yellow
            "Not Started": "#8b949e", # Grey
            "Missing": "#da3633", # Red
            "Upcoming": "#1b1f24" # Dark
        }
        badge_color = color_map.get(status, "#8b949e")
        
        # UI Rendering
        with st.expander(f"{title}  [{status}]", expanded=(status in ["In Progress", "Missing"])):
            st.markdown(f"**Goal (Day {r_day})**: {desc}")
            
            st.markdown("#### 🔑 Key Features to Build")
            for f in features:
                st.markdown(f"- {f}")
            
            st.markdown("---")
            
            # Interactive Section
            if p_id:
                # Update Existing
                col1, col2 = st.columns([3, 1])
                with col1:
                    new_link = st.text_input("Project Link (GitHub/Demo)", value=link, key=f"lnk_{r_day}")
                with col2:
                    new_status = st.selectbox("Status", ["Not Started", "In Progress", "Done"], index=["Not Started", "In Progress", "Done"].index(status) if status in ["Not Started", "In Progress", "Done"] else 0, key=f"st_{r_day}")
                
                if st.button("Update Project", key=f"btn_{r_day}"):
                    db.update_project_status(p_id, new_status)
                    db.update_project_link(p_id, new_link)
                    st.toast("Project updated!")
                    st.rerun()
            else:
                # Create New Entry Logic
                if status == "Upcoming":
                    st.info(f"This project is scheduled for Day {r_day}. You are on Day {current_day_num}.")
                else:
                    st.warning("You haven't tracked this project yet.")
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        new_link = st.text_input("Project Link (GitHub/Demo)", key=f"lnk_{r_day}")
                    with col2:
                        new_status = st.selectbox("Status", ["Not Started", "In Progress", "Done"], key=f"st_{r_day}")
                        
                    if st.button("Start Tracking", key=f"btn_new_{r_day}"):
                         db.add_project(title, desc, new_status, new_link, r_day)
                         st.toast("Project created!")
                         st.rerun()

    # Generic/Custom Projects Section
    st.markdown("---")
    with st.expander("➕ Add Custom Project (Extra Credit)"):
        with st.form("new_custom_project"):
            c_name = st.text_input("Project Name")
            c_desc = st.text_area("Description")
            c_link = st.text_input("Link")
            c_stat = st.selectbox("Status", ["Not Started", "In Progress", "Done"])
            if st.form_submit_button("Add Custom Project"):
                db.add_project(c_name, c_desc, c_stat, c_link)
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
