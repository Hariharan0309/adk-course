from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

def exit_loop():
    """Call this function ONLY when the newsletter is approved and no more changes are needed."""
    return {"status": "approved", "message": "Story approved. Exiting refinement loop."}


# The Writer
newsletter_writer = Agent(
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    name="newsletter_writer",
    instruction="""You are a Developer Advocate.
    1. Combine the AI News and Hackathon list into a 'Weekly Developer Update'.
    2. Format it nicely with emojis and bullet points.
    3. Ensure every news item and hackathon has a URL link.
    """
)

# The Critic
editor_agent = Agent(
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    name="editor_agent",
    instruction="""You are the Editor in Chief.
    Check the newsletter.
    - If it is missing links or looks messy, reply: 'REWRITE: [Specific Issue]'.
    - If it looks perfect call the exit_loop tool.
    """,
    tools=[FunctionTool(exit_loop)]
)