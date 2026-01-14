from typing import Any, Dict
import sys
from google.adk.runners import Runner
from google.adk.tools import ToolContext, FunctionTool
from google.genai import types


# --- Interactive Session Logic ---
async def run_interactive_session(
    user_id: str,
    runner_instance: Runner,
    session_service,
    session_name: str = "default",
    session_state: Dict[str, Any] = {},
):
    print(f"\n### Starting Session: {session_name}")
    print("### Type 'exit' or 'quit' to stop the program.\n")

    app_name = runner_instance.app_name

    # 1. Initialize Session
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id, session_id=session_name, state=session_state
        )
    except Exception:
        # If session exists, retrieve it
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_name
        )

    # 2. Continuous Input Loop
    while True:
        try:
            # Get input from user (synchronous input is okay for simple CLI scripts)
            user_text = input("\nUser > ").strip()

            # Check for exit command
            if user_text.lower() in ["exit", "quit"]:
                print("Exiting chat. Goodbye!")
                sys.exit(0)
            
            # Skip empty inputs
            if not user_text:
                continue

            # Convert to ADK Content format
            query_content = types.Content(role="user", parts=[types.Part(text=user_text)])

            # 3. Stream Response
            # We use print(..., end="") to make streaming look natural, 
            # or just print chunks as they arrive.
            print(f"model > ", end="", flush=True)

            async for event in runner_instance.run_async(
                user_id=user_id, session_id=session.id, new_message=query_content
            ):
                if event.content and event.content.parts:
                    chunk_text = event.content.parts[0].text
                    # Simple check to avoid printing None or empty chunks
                    if chunk_text and chunk_text != "None":
                        print(chunk_text, end="", flush=True)
            
            # Print a newline at the end of the response
            print() 

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")


# --- TOOLS UTILITIES ---


def add_remainder(tool_context: ToolContext, remainder: str) -> str:
    """Adds a remainder to the session state."""
    remainders = tool_context.state.get("remainders", [])
    remainders.append(remainder)
    tool_context.state["remainders"] = remainders
    return {"status": "success", "updated_remainders": remainders}

def remove_remainder(tool_context: ToolContext, remainder: str) -> str:
    """Removes a remainder from the session state."""
    remainders = tool_context.state.get("remainders", [])
    if remainder in remainders:
        remainders.remove(remainder)
        tool_context.state["remainders"] = remainders
        return {"status": "success", "updated_remainders": remainders}
    else:
        return {"status": "failure", "message": "Remainder not found."}




