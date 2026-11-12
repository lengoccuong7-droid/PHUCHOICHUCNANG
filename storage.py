"""Lưu hồ sơ và lần khám cục bộ bằng SQLite. Không lưu ảnh tải lên."""
import sqlite3, json
from pathlib import Path
from datetime import datetime
DB_PATH = Path(__file__).resolve().parent / "data" / "phcn_ai.db"

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con=sqlite3.connect(DB_PATH)
    con.row_factory=sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    return con

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, phone TEXT NOT NULL UNIQUE,
            birth_year INTEGER, job TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)""")
        con.execute("""CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER NOT NULL,
            region TEXT NOT NULL, input_json TEXT NOT NULL, summary_text TEXT,
            analysis_json TEXT, report_text TEXT, created_at TEXT NOT NULL,
            FOREIGN KEY(patient_id) REFERENCES patients(id))""")
        con.execute("CREATE INDEX IF NOT EXISTS idx_visits_patient ON visits(patient_id, created_at DESC)")

def save_visit(patient, region, payload, summary_text, analysis, report):
    now=datetime.now().isoformat(timespec="seconds")
    with connect() as con:
        row=con.execute("SELECT id FROM patients WHERE phone=?",(str(patient.get('phone','')).strip(),)).fetchone()
        if row:
            pid=row['id']
            con.execute("UPDATE patients SET name=?, birth_year=?, job=?, updated_at=? WHERE id=?",
                        (patient.get('name',''), patient.get('age'), patient.get('job',''), now, pid))
        else:
            cur=con.execute("INSERT INTO patients(name,phone,birth_year,job,created_at,updated_at) VALUES(?,?,?,?,?,?)",
                (patient.get('name',''),str(patient.get('phone','')).strip(),patient.get('age'),patient.get('job',''),now,now))
            pid=cur.lastrowid
        cur=con.execute("INSERT INTO visits(patient_id,region,input_json,summary_text,analysis_json,report_text,created_at) VALUES(?,?,?,?,?,?,?)",
            (pid,region,json.dumps(payload,ensure_ascii=False),summary_text,
             json.dumps(analysis,ensure_ascii=False),report,now))
        return cur.lastrowid

def list_visits(limit=100):
    with connect() as con:
        return con.execute("""SELECT v.id, p.name, p.phone, v.region, v.created_at
            FROM visits v JOIN patients p ON p.id=v.patient_id
            ORDER BY v.created_at DESC LIMIT ?""",(limit,)).fetchall()
