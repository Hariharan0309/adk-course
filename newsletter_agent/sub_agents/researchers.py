from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

# Agent A: The AI Reporter
ai_news_agent = Agent(
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    name="ai_news_agent",
    instruction="Find 3 major headlines about Artificial Intelligence from the last 7 days.",
    tools=[google_search]
)

# Agent B: The Hackathon Scout
hackathon_agent = Agent(
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    name="hackathon_agent",
    instruction="Find 3 upcoming global or online coding hackathons scheduled for this month.",
    tools=[google_search]
)