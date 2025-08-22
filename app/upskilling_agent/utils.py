from .db import DatabaseSessionService

TAXONOMY_SKILL_MAP = {
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "ds": "Data Science",
    "data science": "Data Science",
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",
    "sql": "SQL",
    "python": "Python",
    "llm": "Large Language Models",
    "llms": "Large Language Models",
    "nlp": "Natural Language Processing",
    "data eng": "Data Engineering",
    "data engineering": "Data Engineering",
    "cv": "Computer Vision",
    "c++": "C++",
    "deep_learning": "Deep Learning",
}

def map_skills_to_taxonomy(user_skills: dict) -> dict:
    mapped_skills = {}
    for skill, years in user_skills.items():
        cleaned = skill.strip().lower()
        canonical = TAXONOMY_SKILL_MAP.get(cleaned, skill.title())  # Default to title-cased original if not mapped
        mapped_skills[canonical] = years
    return mapped_skills


def check_employee_and_route(employee_id: int) -> dict:
    db = DatabaseSessionService()
    if db.employee_exists(employee_id):
        return {
            "exists": True,
            "message":  f"Employee ID {employee_id} found. Would you like to:\n1. Take Skill Test\n2. Get Course Recommendations Again?"
        }
    else:
        return {
            "exists": False,
            "message": f"New Employee Detected. Please provide the skills, experience(per skill), team, role, career goal, and time allocated for learning."
        }
    

def store_employee_details(employee: dict) -> str:
    db = DatabaseSessionService()
    employee["Skills"] = map_skills_to_taxonomy(employee["Skills"])
    db.insert_employee(employee)
    return f"Details saved successfully for Employee ID"# {employee["EmployeeId"]}."

def update_employee_details(employee: dict) -> str:
    db = DatabaseSessionService()
    employee["Skills"] = map_skills_to_taxonomy(employee["Skills"])
    db.update_employee(employee)
    return f"Details updated successfully for Employee ID"# {employee["EmployeeId"]}."