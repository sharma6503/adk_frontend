from ddtrace.llmobs import LLMObs
from dotenv import load_dotenv  
import os

load_dotenv()

def load_config():
    LLMObs.enable(
        ml_app='upskilling-agent-aug21',
        api_key=os.getenv("DD_API_KEY"),
        agentless_enabled=True,
        site=os.getenv("DD_SITE"),
    )