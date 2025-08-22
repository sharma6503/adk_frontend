import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

COURSE_DB_NAME = os.getenv("COURSE_DB_NAME", "serp_course_recommendations.db")

class CourseRecommendationDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(COURSE_DB_NAME)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS serp_course_recommendations (
                EmployeeId INTEGER,
                CourseName TEXT,
                Level TEXT,
                Platform TEXT,
                Description TEXT,
                Link TEXT,
                Skill TEXT
            )
        ''')
        self.conn.commit()

    def insert_recommendation(self, recommendation: dict):
        self.cursor.execute('''
            INSERT INTO serp_course_recommendations (EmployeeId, CourseName, Level, Platform, Description, Link, Skill)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            recommendation['EmployeeId'],
            recommendation['CourseName'],
            recommendation['Level'],
            recommendation['Platform'],
            recommendation['Description'],
            recommendation['Link'],
            recommendation['Skill']
        ))
        self.conn.commit()

    def get_recommendations_for_employee(self, employee_id: int) -> list:
        self.cursor.execute("SELECT * FROM serp_course_recommendations WHERE EmployeeId = ?", (employee_id,))
        rows = self.cursor.fetchall()
        return [
            {
                "EmployeeId": row[0],
                "CourseName": row[1],
                "Level": row[2],
                "Platform": row[3],
                "Description": row[4],
                "Link": row[5],
                "Skill": row[6]
            }
            for row in rows
        ]
    
    def delete_employee_courses(self, employee_id: int):
        self.cursor.execute("DELETE FROM serp_course_recommendations WHERE EmployeeId = ?", (employee_id,))
        self.conn.commit()


    # Function to extract courses and their levels for skill testing
    def get_courses_and_levels_for_employee(self, employee_id: int) -> dict:
        self.cursor.execute(
            "SELECT CourseName, Level FROM serp_course_recommendations WHERE EmployeeId = ?", (employee_id,)
        )
        rows = self.cursor.fetchall()
        course_level_map = {}
        for course, level in rows:
            course_level_map[course] = level
        return course_level_map