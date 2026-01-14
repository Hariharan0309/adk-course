import asyncio
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.genai import types
from utils import run_interactive_session
from utils import add_remainder, remove_remainder
from google.adk.tools import FunctionTool


# 1. Load environment variables (Fixes the ValueError)
load_dotenv()

# Verify API Key exists
if not os.getenv("GOOGLE_API_KEY"):
    print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
    print("   Please create a .env file with GOOGLE_API_KEY=your_key_here")
    exit(1)

# --- Configuration ---
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

APP_NAME = "default"
USER_ID = "default"
# Use a valid model name
MODEL_NAME = "gemini-2.5-flash-lite" 
SESSION_NAME = "interactive-session"
SESSION_STATE = {"remainders" : []}

add_remainder_tool = FunctionTool(func=add_remainder)
remove_remainder_tool = FunctionTool(func=remove_remainder)



# --- Agent Setup ---
root_agent = Agent(
    model=Gemini(model=MODEL_NAME, retry_options=retry_config),
    name="remainder_agent",
    instruction=
    '''An agent that helps users manage and track their remainders effectively.
       The available remainders are {remainders}.
         Always confirm with the user before adding or removing a remainder.
         Use the tool add_remainder to add a new remainder.
         Use the tool remove_remainder to remove an existing remainder.
         while calling the tool remove_remainder, ensure that the remainder exists in the user's list.
         and also make sure the remainder text matches exactly.

         When listing remainders, provide them in a numbered format for clarity.
         If there are no remainders, inform the user that their list is empty.''',
    tools=[add_remainder_tool, remove_remainder_tool]
)

db_url = "sqlite+aiosqlite:///my_agent_data.db"  # Local SQLite file
session_service = DatabaseSessionService(db_url=db_url)

runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

print("✅ Agent initialized and ready for input!")

# --- Main Execution ---
async def main():
    await run_interactive_session(user_id=USER_ID, 
                                  runner_instance=runner, 
                                  session_service=session_service, 
                                  session_name=SESSION_NAME, 
                                  session_state=SESSION_STATE)

if __name__ == "__main__":
    asyncio.run(main())