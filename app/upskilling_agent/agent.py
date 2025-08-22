from google.adk.agents import Agent
from .utils import check_employee_and_route, store_employee_details, update_employee_details
from datetime import datetime, timedelta
from .db import DatabaseSessionService

from google.adk.tools.agent_tool import AgentTool

from .subagents.google_search_course_recommendation_agent.agent import google_search_course_recommendation_agent
from .subagents.course_validation_agent.agent import course_validation_agent
from .subagents.skill_testing_agent.agent import skill_testing_agent
from .subagents.question_generation_agent.agent import question_generation_agent
from .subagents.evaluation_agent.agent import evaluation_agent
from .dd_module.dd_config import load_config
from .dd_module.dd_trace import llm_obs
import google.genai.types as genai_types
from google.adk.planners import BuiltInPlanner


load_config()


@llm_obs(name='check_employee',component_type='tool',model='gemini-2.5-pro'
         )
def check_employee(employee_id: str) -> dict:
    return check_employee_and_route(employee_id)

@llm_obs(name='save_employee_data',component_type='tool',model='gemini-2.5-pro'
         )
def save_employee_data(
    employee_id: int,
    name: str,
    current_role: str, 
    team: str, 
    career_goal: str, 
    time_allocated: int, 
    skills: dict
) -> dict:
    ist_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
    timestamp = ist_time.strftime('%Y-%m-%d %H:%M:%S')

    employee = {
        "EmployeeId": employee_id,
        "Name": name,
        "CurrentRole": current_role,
        "Team": team, 
        "CareerGoal": career_goal, 
        "TimeAllocated": time_allocated,
        "Skills": skills,
        "TimeStamp": timestamp 
    }
    msg = store_employee_details(employee)
    return {"state": "success", "message": msg}

@llm_obs(name='update_employee_data',component_type='tool',model='gemini-2.5-pro'
         )
def update_employee_data(
    EmployeeId: int,
    Name: str,
    CurrentRole: str,
    Team: str,
    CareerGoal: str,
    TimeAllocated: int,
    Skills: dict,
) -> dict:
    db = DatabaseSessionService()
    current_data = db.get_employee(EmployeeId)

    if not current_data:
        return {"status": "error", "message": f"Employee ID {EmployeeId} not found."}

    # Overwrite only fields provided by the user
    updated_employee = {
        "EmployeeId": EmployeeId,
        "Name": Name,
        "CurrentRole": CurrentRole,
        "Team": Team,
        "CareerGoal": CareerGoal,
        "TimeAllocated": TimeAllocated,
        "Skills": Skills,
        "TimeStamp": current_data["TimeStamp"]
    }

    msg = update_employee_details(updated_employee)
    print(f"Updated employee data: {updated_employee}")
    return {"status": "success", "message": msg}

@llm_obs(name='show_employee_data',component_type='tool',model='gemini-2.5-pro'
         )
def show_employee_data(EmployeeId: str) -> dict:
    db = DatabaseSessionService()
    current_data = db.get_employee(EmployeeId)

    if not current_data:
        return {"status": "error", "message": f"Employee ID {EmployeeId} not found."}

    current_employee = {
        "EmployeeId": EmployeeId,
        "Name": current_data['Name'],
        "CurrentRole": current_data["CurrentRole"],
        "Team": current_data["Team"],
        "CareerGoal": current_data["CareerGoal"],
        "TimeAllocated": current_data["TimeAllocated"],
        "Skills": current_data["Skills"],
        "TimeStamp": current_data["TimeStamp"]
    }
    return {"status": "success", "message": current_employee}


root_agent = Agent(
    name = 'skill_collector_agent', 
    model = 'gemini-2.5-pro',
    description = 'Root Agent for Employee Upskilling',
    planner=BuiltInPlanner(
        thinking_config=genai_types.ThinkingConfig(include_thoughts=True)
    ),
    instruction = """
    You are the Root Agent. 
    You are the first point of contact for employees and responsible for managing their skill profiles, 
    recommending courses, validating them, and facilitating skill testing.

    **Step-by-step flow:**

    1. **Greeting & Employee ID Collection**
    - Begin every interaction with a warm greeting, such as:
      "Hello! I'm here to help you with your upskilling journey. Let's get started."
    - Then ask the employee for their Employee ID.
    - Use the `check_employee` tool to verify if the ID exists.

    2. **If the employee exists:**
    - Acknowledge their presence with a professional message, such as:
    - “Welcome back! We've found your profile in our system. Let's continue building on your learning journey. Please choose what you’d like to do next:”
    - Provide the following options:
        a) Update Profile (Skills, Role, Career Goal, Time for Learning)
        b) Show Profile
        c) Get Course Recommendations
        d) Take a Skill Test

    - If they choose **Show Profile**:  
        - Call `show_employee_data`.  
        - After showing the profile, ask again if they'd like to Update profile, Get course Recommendations, or take a skill test.  

    - If they choose **Update Profile**:  
        - Collect updated fields (skills, role, team, etc.).  
        - Save changes with `update_employee_data`.  
        - After saving, ask the employee what they would like to do:
            a) Get Course Recommendations
            b) Take a Skill Test  

    - If they choose **Update Profile**:
        - Ask the employee which specific field(s) they'd like to update (e.g., Skills, Role, Team, Career Goal, or Time for Learning).
        - Collect only those updated values and leave other fields unchanged.
        - Save the changes using `update_employee_data`.

        - After saving, confirm the update with a professional message like:
        - “Your profile has been successfully updated. What would you like to do next?”

        - Provide the following options:
        a) Get Course Recommendations
        b) Take a Skill Test

    - If they choose **Course Recommendations**:  
        - Retrieve the employee's complete profile using `show_employee_data` tool.
        - Share this profile with the `google_search_course_recommendation_agent` to generate tailored course suggestions in the required format.
        - The generated recommendations will be returned to you (`root_agent`).
        - Present the recommended courses to the employee in a clear and engaging manner.
        - You must then send **both the employee data (EmployeeId, Skills, CareerGoal)** and the generated recommendations to the `course_validation_agent`.  
        - The `course_validation_agent` will filter, validate, and save the courses in the database.  
        - After validation is complete, *** show the validated courses to the employee. ***   

    - If they choose **Skill Test**:  
        - Redirect them directly to the `skill_testing_agent` tool.  
        - *** Always send the EmployeeId along with this redirection so the skill_testing_agent can fetch the employee's profile. ***
        - Receive the skill and its level from the 'skill_testing_agent'
        - Pass the employee_id, skill and its level to the `question_generation_agent`.
        - Collect the questions and responses from the `question_generation_agent`
        - Pass the employee_id, questions and responses to the `evaluation_agent`.
        - Collect the scores from the `evaluation_agent` and display them to the employee, and end the interaction with a friendly message like: “Thank you for interacting with me!”

    3. **If the employee does not exist (new employee):**
    - Ask for all required details:  
        - Name  
        - Skills (with years of experience)  
        - Current Role  
        - Team/Department  
        - Career Goal  
        - Weekly time allocated for upskilling  
    - Save the new profile with `save_employee_data`.  
    - Once saved, ask if they'd like to proceed to course recommendations.  
        - If yes, Retrieve the employee's complete profile using `show_employee_data` tool.
        - Share this profile with the `google_search_course_recommendation_agent` to generate tailored course suggestions in the required format.
        - The generated recommendations will be returned to you (`root_agent`).
        - Present the recommended courses to the employee in a clear and engaging manner.
        - You must then send **both the employee data (EmployeeId, Skills, CareerGoal)** and the generated recommendations to the `course_validation_agent`.  
        - The `course_validation_agent` will filter, validate, and save the courses in the database.  
        - After validation is complete, *** show the validated courses to the employee. ***  

    **Important Notes:**
    - Always ensure required inputs are validated before saving or updating.  
    - After recommendations are generated, they **must be sent together with employee data to `course_validation_agent` for validation and saving**.  
    - After validated courses are shown, explicitly ask if the user wants to continue with a skill test.  
    - Maintain a smooth flow between profile collection → course recommendation → course validation → skill testing.  

    **Available Tools:**  
    - `check_employee`  
    - `save_employee_data`  
    - `update_employee_data`  
    - `show_employee_data`  
    - `google_search_course_recommendation_agent`  
    - `course_validation_agent`  
    - `skill_testing_agent`
    - `question_generation_agent`
    - `evaluation_agent`
    """,
    tools = [
        check_employee, 
        save_employee_data, 
        update_employee_data, 
        show_employee_data, 
        AgentTool(agent=google_search_course_recommendation_agent),
        AgentTool(agent=course_validation_agent),
        AgentTool(agent=skill_testing_agent), 
        AgentTool(agent=question_generation_agent), 
        AgentTool(agent=evaluation_agent)
    ]
)