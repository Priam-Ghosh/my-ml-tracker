# 🎯 Personal ML Learning Tracker

A Python-based productivity tool to track your 6-month Machine Learning journey. Built with **Streamlit** (Frontend) and **SQLite** (Database).

## ✨ Features
- **Daily Log**: Track what you learned and your confidence level.
- **Dynamic Roadmap**: Automated 24-week schedule with weekly goals.
- **Daily Quiz**: 15 auto-generated questions (Easy/Medium/Hard) based on your weekly topic.
- **Project Portfolio**: Kanban-style board for your ML projects.
- **Analytics**: Visualize your consistency and confidence trends.

## 🚀 How to Run (For You & Friends)

### Prerequisites
- Python 3.8 or higher installed.

### Installation
1.  **Download** this folder/repo.
2.  Open your terminal/command prompt in this folder.
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Running the App
Execute this command:
```bash
streamlit run app.py
```
The app will open in your browser at `http://localhost:8501`.

## 🤝 Sharing with Friends
This app is designed as a **Personal** tracker.
- **Do not** host this single instance for multiple people (everyone would overwrite each other's data!).
- **Instead**, send this code to your friends. When they run it on their computer, it creates their own private `tracker.db` database.

## 🛠️ specific Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite3 (Local file `tracker.db`)
- **Data Viz**: Pandas + Streamlit Charts
