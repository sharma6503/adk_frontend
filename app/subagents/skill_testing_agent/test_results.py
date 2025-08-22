import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("RESUTLS_DB_NAME", "skill_test_results.db")

class SkillTestResultsDB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS skill_test_results (
                employee_id INTEGER,
                domain TEXT,
                quiz_score INTEGER,
                scenario_score INTEGER,
                total_score INTEGER,
                timestamp TEXT DEFAULT (DATETIME('now'))
            )
        ''')
        self.conn.commit()

    def insert_result(self, employee_id: int, domain: str, quiz_score: int, scenario_score: str, total_score: int, timestamp: str):
        self.cursor.execute('''
            INSERT INTO skill_test_results (employee_id, domain, quiz_score, scenario_score, total_score, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (employee_id, domain, quiz_score, scenario_score, total_score, timestamp))
        self.conn.commit()

    def insert_bulk_results(self, employee_id: int, results: dict):
        for domain, result in results.items():
            self.insert_result(
                employee_id,
                domain,
                result["quiz_score"],
                result["scenario_score"],
                result["total_score"],
                result["timestamp"]
            )

    def get_results_by_employee(self, employee_id: int) -> list:
        self.cursor.execute("SELECT * FROM skill_test_results WHERE employee_id = ?", (employee_id,))
        rows = self.cursor.fetchall()
        return [
            {
                "employee_id": row[0],
                "domain": row[1],
                "quiz_score": row[2],
                "scenario_score": row[3],
                "total_score": row[4],
                "timestamp": row[5]
            }
            for row in rows
        ]

    def delete_results_by_employee(self, employee_id: int):
        self.cursor.execute("DELETE FROM skill_test_results WHERE employee_id = ?", (employee_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()