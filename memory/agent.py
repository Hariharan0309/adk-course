import asyncio
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.sessions import  InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from utils import run_interactive_session
import vertexai
from google.adk.memory import VertexAiMemoryBankService
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

# 1. Load environment variables (Fixes the ValueError)
load_dotenv()

PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

client = vertexai.Client(project=PROJECT, location=LOCATION)

AGENT_ENGINE_ID = os.getenv("AGENT_ENGINE_ID")

if AGENT_ENGINE_ID:
    print(f"Using existing Agent Engine ID: {AGENT_ENGINE_ID}")
    agent_engine_id = AGENT_ENGINE_ID
else:
    print("Creating new Agent Engine...")
    agent_engine = client.agent_engines.create(
        config={
            "context_spec": {
                "memory_bank_config": {
                    "generation_config": {
                        "model": f"projects/{PROJECT}/locations/{LOCATION}/publishers/google/models/gemini-2.5-flash"
                    }
                }
            }
        }
    )
    agent_engine_id = agent_engine.api_resource.name.split("/")[-1]
    print(f"✅ Created new Agent Engine ID: {agent_engine_id}")
    print("Please add AGENT_ENGINE_ID=<ID> to your .env file to reuse it.")

memory_bank_service = VertexAiMemoryBankService(
    agent_engine_id=agent_engine_id,
    project=PROJECT,
    location=LOCATION,
)

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

async def auto_save_session_to_memory_callback(callback_context):
    # Use the invocation context to access the conversation history that should
    # be used as the data source for memory generation.
    await memory_bank_service.add_session_to_memory(
        callback_context._invocation_context.session
    )

APP_NAME = "default"
USER_ID = "default"
# Use a valid model name
MODEL_NAME = "gemini-2.5-flash-lite" 
SESSION_NAME = "interactive-session"


# --- Agent Setup ---
root_agent = Agent(
    model=Gemini(model=MODEL_NAME, retry_options=retry_config),
    name="AutoMemoryAgent",
    instruction="Answer user questions.",
    tools=[PreloadMemoryTool()],
    after_agent_callback=auto_save_session_to_memory_callback
)

session_service = InMemorySessionService()

runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service, 
                memory_service=memory_bank_service)

print("✅ Agent initialized and ready for input!")

# --- Main Execution ---
async def main():
    search_results = await memory_bank_service.search_memory(
            app_name=APP_NAME,
            user_id=USER_ID,
            query="What is my friend name ?",
    )
    print(f"Search Results: {search_results}")
    await run_interactive_session(user_id=USER_ID, 
                                  runner_instance=runner, 
                                  session_service=session_service, 
                                  session_name=SESSION_NAME, 
                                )

if __name__ == "__main__":
    asyncio.run(main())