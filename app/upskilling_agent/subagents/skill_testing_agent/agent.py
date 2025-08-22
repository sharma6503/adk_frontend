import sqlite3
from google.adk.agents import Agent, LlmAgent
from .test_results import SkillTestResultsDB
from .courses_db import CourseRecommendationDatabase

from datetime import datetime, timedelta
from ...dd_module.dd_config import load_config
from ...dd_module.dd_trace import llm_obs

load_config()

@llm_obs(name="skill_testing_agent", model="gemini-2.5-pro", component_type='agent')
def display_courses(employee_id: int) -> str:
    cdb = CourseRecommendationDatabase()
    course_level_map = cdb.get_courses_and_levels_for_employee(employee_id)
    if not course_level_map:
        return f"No recommended domains found for Employee ID {employee_id}."
    return f"Recommended Domains for Employee ID {employee_id}:" + "\n".join([
        f"- {course} ({level})" for course, level in course_level_map.items()
    ])

skill_testing_agent = Agent(
    name="skill_testing_agent",
    model="gemini-2.5-pro",
    description="Agent to test employees after upskilling",
    instruction="""
    You are a Skill Testing Agent. Your task is to send the user selected skill and associated level to the skill_collector_agent.

    1. First show the recommended courses and their levels using the `display_courses` tool.
    2. Wait for the employee to select a skill to test.
    3. For the selected skill, determine the associated level.
    4. return the selected skill and associated level to the 'skill_collector_agent'
    """,
    tools=[display_courses]
)