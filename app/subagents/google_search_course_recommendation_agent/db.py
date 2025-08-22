import sqlite3
import json
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "database.db")

class DatabaseSessionService:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self._create_table()

    
    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees(
                EmployeeId INTEGER PRIMARY KEY,
                Name TEXT,
                CurrentRole TEXT,
                Team TEXT,
                CareerGoal TEXT,
                TimeAllocated INTEGER,
                Skills TEXT,
                TimeStamp TEXT DEFAULT (DATETIME('now'))
            )
        ''')
        self.conn.commit()

    def employee_exists(self, employee_id: int) -> bool:
        self.cursor.execute("SELECT 1 FROM employees where EmployeeId = ?", (employee_id,))
        return self.cursor.fetchone() is not None 
    
    def get_employee(self, employee_id: int) -> dict:
        self.cursor.execute("SELECT * FROM employees where EmployeeId = ?", (employee_id, ))
        row = self.cursor.fetchone()
        if row:
            return {
                "EmployeeId" : row[0], 
                "Name" : row[1],
                "CurrentRole" : row[2], 
                "Team" : row[3],
                "CareerGoal" : row[4],
                "TimeAllocated" : row[5], 
                "Skills" : json.loads(row[6]),
                "TimeStamp": row[7]
            }
        return {}
    

    def insert_employee(self, employee: dict):
        self.cursor.execute('''
            INSERT INTO employees (EmployeeId, Name, CurrentRole, Team, CareerGoal, TimeAllocated, Skills, TimeStamp) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            employee['EmployeeId'],
            employee['Name'],
            employee['CurrentRole'],
            employee['Team'],
            employee['CareerGoal'],
            employee['TimeAllocated'],
            json.dumps(employee['Skills']),
            employee['TimeStamp']
        ))
        self.conn.commit()


    def update_employee(self, employee:dict):
        skills_json = json.dumps(employee['Skills'])  # Convert dict to JSON string
        self.cursor.execute('''
            UPDATE employees SET
                Name = ?,
                CurrentRole = ?,
                Team = ?, 
                CareerGoal = ?,
                TimeAllocated = ?,
                Skills = ?,
                TimeStamp = ?
            WHERE EmployeeID = ?
        ''', (
            employee['Name'],
            employee['CurrentRole'],
            employee['Team'],
            employee['CareerGoal'],
            employee['TimeAllocated'],
            skills_json,
            employee['TimeStamp'],
            employee['EmployeeId']
        ))
        self.conn.commit()


    def get_employee(self, employee_id: int) -> dict:
        self.cursor.execute("SELECT * FROM employees WHERE EmployeeId = ?", (employee_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "EmployeeId": row[0],
                "Name": row[1],
                "CurrentRole": row[2],
                "Team": row[3],
                "CareerGoal": row[4],
                "TimeAllocated": row[5],
                "Skills": json.loads(row[6]),
                "TimeStamp": row[7]
            }
        return {}