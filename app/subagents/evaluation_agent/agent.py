import sqlite3
from google.adk.agents import Agent, LlmAgent
from .test_results import SkillTestResultsDB
from .courses_db import CourseRecommendationDatabase

from datetime import datetime, timedelta
from ...dd_module.dd_config import load_config
from ...dd_module.dd_trace import llm_obs

load_config()
@llm_obs(name="evaluation_agent", model="gemini-2.5-pro", component_type='tool')
def store_results(employee_id:int, course: str, quiz_score: int, evaluated_score: int):
    total_score = round((quiz_score + evaluated_score)/2)
 
    ist_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
    timestamp = ist_time.strftime('%Y-%m-%d %H:%M:%S')

    db = SkillTestResultsDB()
    db.insert_result(employee_id, course, quiz_score, evaluated_score, total_score, timestamp)
    db.close()

evaluation_agent = Agent(
    name="evaluation_agent",
    model="gemini-2.5-pro",
    description="Evaluates quiz and scenario responses, assigns scores, and stores them in the database.",
    instruction="""
    You are an Evaluation Agent. You receive:
    - `employee_id`: the user's ID
    - `course`: the skill being tested
    - `question_data`: contains quiz questions with correct answers and scenario questions
    - `user_answers`: contains user's responses in this format:

    {
        "quiz_answers": {
            "1": "A",
            "2": "C",
            ...
        },
        "scenario_answers": {
            "1": "user's answer 1...",
            "2": "user's answer 2...",
            ...
        }
    }

    Your task:
    1. Compare each quiz answer (1 mark = 20 points). If correct, award 20, else 0.
    2. Evaluate each scenario answer qualitatively. Assign 0, 5, 10, 15 or 20 depending on relevance, completeness, and depth.
    3. Compute:
    - `quiz_score` = total quiz score out of 100
    - `evaluated_score` = total scenario score out of 100
    4. Call the tool `store_results(employee_id, course, quiz_score, evaluated_score)` to save results to DB.

    Return answers to the user. Confirm the evaluation is complete or failed.
    And display the results to the user and send the results to the 'skill_colletor_agent'
    """,
    tools=[store_results]
)