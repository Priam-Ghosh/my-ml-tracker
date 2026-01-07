import sqlite3
import datetime

DB_NAME = "tracker.db"

def init_db():
    """Initializes the database tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Daily Logs
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_logs (
            date TEXT PRIMARY KEY,
            planned_tasks TEXT,
            actual_learning TEXT,
            confidence_score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Weekly Goals
    c.execute('''
        CREATE TABLE IF NOT EXISTS weekly_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            week_start_date TEXT,
            goal_text TEXT,
            is_completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Projects
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            status TEXT, -- 'Not Started', 'In Progress', 'Done'
            github_link TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Settings
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # Monthly Assessments
    c.execute('''
        CREATE TABLE IF NOT EXISTS monthly_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month_str TEXT,
            reflection_text TEXT,
            rating INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # NEW: Quiz Results
    c.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            date TEXT PRIMARY KEY,
            score INTEGER,
            total_questions INTEGER,
            topic_covered TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# --- Daily Logs ---
def add_daily_log(date, planned, actual, confidence):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO daily_logs (date, planned_tasks, actual_learning, confidence_score)
        VALUES (?, ?, ?, ?)
    ''', (date, planned, actual, confidence))
    conn.commit()
    conn.close()

def get_daily_log(date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM daily_logs WHERE date = ?', (date,))
    data = c.fetchone()
    conn.close()
    return data

def get_all_logs():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM daily_logs ORDER BY date DESC')
    data = c.fetchall()
    conn.close()
    return data

# --- Weekly Goals ---
def add_weekly_goal(week_date, goal_text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO weekly_goals (week_start_date, goal_text, is_completed) VALUES (?, ?, 0)', (week_date, goal_text))
    conn.commit()
    conn.close()

def get_weekly_goals(week_date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM weekly_goals WHERE week_start_date = ?', (week_date,))
    data = c.fetchall()
    conn.close()
    return data

def toggle_goal_complete(goal_id, current_status):
    new_status = not current_status
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE weekly_goals SET is_completed = ? WHERE id = ?', (new_status, goal_id))
    conn.commit()
    conn.close()

def delete_goal(goal_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM weekly_goals WHERE id = ?', (goal_id,))
    conn.commit()
    conn.close()

# --- Projects ---
def add_project(name, description, status, link):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO projects (name, description, status, github_link)
        VALUES (?, ?, ?, ?)
    ''', (name, description, status, link))
    conn.commit()
    conn.close()

def get_projects():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM projects ORDER BY created_at DESC')
    data = c.fetchall()
    conn.close()
    return data

def update_project_status(project_id, new_status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE projects SET status = ? WHERE id = ?', (new_status, project_id))
    conn.commit()
    conn.close()

def delete_project(project_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    conn.commit()
    conn.close()

# --- Settings ---
def set_setting(key, value):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()

def get_setting(key):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT value FROM settings WHERE key = ?', (key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# --- Monthly Assessments ---
def add_monthly_assessment(month_str, reflection, rating):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id FROM monthly_assessments WHERE month_str = ?', (month_str,))
    exist = c.fetchone()
    if exist:
        c.execute('UPDATE monthly_assessments SET reflection_text = ?, rating = ? WHERE id = ?', (reflection, rating, exist[0]))
    else:
        c.execute('INSERT INTO monthly_assessments (month_str, reflection_text, rating) VALUES (?, ?, ?)', (month_str, reflection, rating))
    conn.commit()
    conn.close()

def get_monthly_assessments():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM monthly_assessments ORDER BY month_str DESC')
    data = c.fetchall()
    conn.close()
    return data

# --- Quiz Results ---
def add_quiz_result(date, score, total, topic):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO quiz_results (date, score, total_questions, topic_covered)
        VALUES (?, ?, ?, ?)
    ''', (date, score, total, topic))
    conn.commit()
    conn.close()

def get_quiz_result(date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM quiz_results WHERE date = ?', (date,))
    data = c.fetchone()
    conn.close()
    return data

# --- Analytics Queries ---
def get_analytics_stats():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Total Logs
    c.execute('SELECT COUNT(*) FROM daily_logs')
    total_logs = c.fetchone()[0]
    
    # Average Confidence
    c.execute('SELECT AVG(confidence_score) FROM daily_logs')
    avg_confidence = c.fetchone()[0] or 0.0
    
    # Projects Completed
    c.execute("SELECT COUNT(*) FROM projects WHERE status = 'Done'")
    projects_done = c.fetchone()[0]
    
    # Calculate Streak
    c.execute('SELECT DISTINCT date FROM daily_logs ORDER BY date DESC')
    dates = [row[0] for row in c.fetchall()]
    
    streak = 0
    today = datetime.date.today()
    
    # Simple streak logic
    current_streak = 0
    if dates:
        last_log = datetime.datetime.strptime(dates[0], "%Y-%m-%d").date()
        diff = (today - last_log).days
        if diff <= 1:
            current_streak = 1
            previous_date = last_log
            for i in range(1, len(dates)):
                d = datetime.datetime.strptime(dates[i], "%Y-%m-%d").date()
                if (previous_date - d).days == 1:
                    current_streak += 1
                    previous_date = d
                else:
                    break
        else:
            current_streak = 0
            
    conn.close()
    
    return {
        "total_logs": total_logs,
        "avg_confidence": round(avg_confidence, 1),
        "projects_done": projects_done,
        "current_streak": current_streak
    }
