import sqlite3
from google.adk.agents import Agent, LlmAgent
from ...dd_module.dd_config import load_config
from ...dd_module.dd_trace import llm_obs

load_config()


question_generation_agent = llm_obs(name="question_generation_agent", model="gemini-2.5-pro", component_type='agent')(LlmAgent)(
    name="question_generation_agent",
    model="gemini-2.5-pro",
    description="Generates quiz and scenario questions based on skill and level, hiding answers from the user output.",
    instruction="""
    You are a Question Generation Agent.

    Inputs:
    - skill: A technical skill (e.g., Python, SQL, Machine Learning)
    - level: One of [intermediate, advanced, expert]

    Your responsibilities:
    1. Generate 5 multiple-choice quiz questions:
        - Each should include 4 options labeled A, B, C, D.
    2. Generate 5 scenario-based questions:
        - Open-ended questions designed to test real-world understanding.
    3. Output in the following formats:
        - `display_text`: A plain-text formatted string showing only the questions and options (to show the user), like this:

    Quiz Questions:
    1. What is X in Python?
    Options:
    A. Option A
    B. Option B
    C. Option C
    D. Option D

    Scenario Questions:
    1. Describe a scenario where...

    Answers should **not** appear in `display_text`.

    Finally, instruct the user to submit their responses in the following format:

    Answers should be in the following format:
    Quiz Answers:
    1. X
    2. Y
    3. Z
    4. X
    5. Y

    Scenario Answers:
    1. [Answer to scenario 1]
    2. [Answer to scenario 2]
    3. [Answer to scenario 3]
    4. [Answer to scenario 4]
    5. [Answer to scenario 5]


    *** Display the questions to the user.
    *** After user answering the questions, if the responses are not in the specified format which we mentioned, then ask the user to answer in the specified format
    *** Send both the questions and the responses to the 'Skill_Collector_agent'
    """
)
