# app/db.py
import sqlite3
from datetime import datetime

DB = "results.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS evaluations
                 (id INTEGER PRIMARY KEY, filename TEXT, jd_title TEXT, score REAL,
                  verdict TEXT, missing_skills TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_result(filename, jd_title, score, verdict, missing_skills):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO evaluations (filename,jd_title,score,verdict,missing_skills,timestamp) VALUES (?,?,?,?,?,?)",
              (filename, jd_title, score, verdict, ",".join(missing_skills), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
