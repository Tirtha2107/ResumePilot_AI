


# import os
# import sqlite3

# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# DB_DIR = os.path.join(PROJECT_ROOT, "database")
# os.makedirs(DB_DIR, exist_ok=True)

# DB_PATH = os.path.join(DB_DIR, "user.db")


# def get_connection():
#     return sqlite3.connect(DB_PATH, check_same_thread=False)


# def init_db():

#     conn = get_connection()
#     c = conn.cursor()

#     c.execute("""
#     CREATE TABLE IF NOT EXISTS users(

#         id INTEGER PRIMARY KEY AUTOINCREMENT,

#         full_name TEXT NOT NULL,

#         email TEXT UNIQUE NOT NULL,

#         password TEXT NOT NULL,

#         age INTEGER,

#         qualification TEXT,

#         branch TEXT,

#         college TEXT,

#         passing_year INTEGER,

#         contact TEXT

#     )
#     """)


#     c.execute("""
#     CREATE TABLE IF NOT EXISTS quiz_history(

#         id INTEGER PRIMARY KEY AUTOINCREMENT,

#         user_id INTEGER NOT NULL,

#         topic TEXT,

#         difficulty TEXT,

#         score INTEGER,

#         correct_answers INTEGER,

#         total_questions INTEGER,

#         quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

#         FOREIGN KEY(user_id) REFERENCES users(id)

#     )
#     """)


#     c.execute("""
#     CREATE TABLE IF NOT EXISTS mock_interview(

#         id INTEGER PRIMARY KEY AUTOINCREMENT,

#         user_id INTEGER,

#         score INTEGER,

#         feedback TEXT,

#         interview_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

#         FOREIGN KEY(user_id) REFERENCES users(id)

#     )
#     """)


#     c.execute("""
#     CREATE TABLE IF NOT EXISTS technical_round(

#         id INTEGER PRIMARY KEY AUTOINCREMENT,

#         user_id INTEGER,

#         topic TEXT,

#         score INTEGER,

#         feedback TEXT,

#         completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

#         FOREIGN KEY(user_id) REFERENCES users(id)

#     )
#     """)


#     c.execute("""
#     CREATE TABLE IF NOT EXISTS hr_round(

#         id INTEGER PRIMARY KEY AUTOINCREMENT,

#         user_id INTEGER,

#         question TEXT,

#         answer TEXT,

#         ai_feedback TEXT,

#         score INTEGER,

#         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

#         FOREIGN KEY(user_id) REFERENCES users(id)

#     )
#     """)


#     c.execute("""
#     CREATE TABLE IF NOT EXISTS interview_progress(

#         user_id INTEGER PRIMARY KEY,

#         roadmap_completed INTEGER DEFAULT 0,

#         aptitude_completed INTEGER DEFAULT 0,

#         technical_completed INTEGER DEFAULT 0,

#         hr_completed INTEGER DEFAULT 0,

#         mock_completed INTEGER DEFAULT 0,

#         overall_progress REAL DEFAULT 0,

#         last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

#         FOREIGN KEY(user_id) REFERENCES users(id)

#     )
#     """)

#     conn.commit()
#     conn.close()


# init_db()

# print("Database path:", DB_PATH)

import os
import sqlite3

# =========================
# Project & Database Path
# =========================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DB_DIR = os.path.join(PROJECT_ROOT, "database")
os.makedirs(DB_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "user.db")


# =========================
# Database Connection
# =========================

def get_connection():
    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )


# =========================
# Initialize Database
# =========================

def init_db():

    conn = get_connection()
    c = conn.cursor()

    # Users
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            age INTEGER,
            qualification TEXT,
            branch TEXT,
            college TEXT,
            passing_year INTEGER,
            contact TEXT
        )
    """)

    # Quiz History
    c.execute("""
        CREATE TABLE IF NOT EXISTS quiz_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            topic TEXT,
            difficulty TEXT,
            score INTEGER,
            correct_answers INTEGER,
            total_questions INTEGER,
            quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Mock Interview
    c.execute("""
        CREATE TABLE IF NOT EXISTS mock_interview (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER,
            feedback TEXT,
            interview_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Technical Round
    c.execute("""
        CREATE TABLE IF NOT EXISTS technical_round (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            topic TEXT,
            score INTEGER,
            feedback TEXT,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # HR Round
    c.execute("""
        CREATE TABLE IF NOT EXISTS hr_round (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            question TEXT,
            answer TEXT,
            ai_feedback TEXT,
            score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Interview Progress
    c.execute("""
        CREATE TABLE IF NOT EXISTS interview_progress (
            user_id INTEGER PRIMARY KEY,
            roadmap_completed INTEGER DEFAULT 0,
            aptitude_completed INTEGER DEFAULT 0,
            technical_completed INTEGER DEFAULT 0,
            hr_completed INTEGER DEFAULT 0,
            mock_completed INTEGER DEFAULT 0,
            overall_progress REAL DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# =========================
# Initialize Database
# =========================

init_db()

print("Database path:", DB_PATH)