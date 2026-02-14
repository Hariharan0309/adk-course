import asyncio
import vertexai

# --- CONFIGURATION ---
PROJECT_ID = "valued-mediator-461216-k7"
LOCATION = "us-central1"
RESOURCE_ID = "projects/valued-mediator-461216-k7/locations/us-central1/reasoningEngines/7301622524083699712"
USER_ID = "weather_enthusiast_05"

async def main():
    print(f"🔌 Connecting to Vertex AI Client...")
    
    # 1. Initialize Client
    client = vertexai.Client(project=PROJECT_ID, location=LOCATION)
    adk_app = client.agent_engines.get(name=RESOURCE_ID)
    print(f"✅ Connected to ADK App: {RESOURCE_ID}")

    # 2. Session Management
    session_id = None
    
    print(f"🔍 Checking existing sessions for: {USER_ID}...")
    try:
        # returns a Dictionary, e.g. {"sessions": [...], "next_page_token": ...}
        response = await adk_app.async_list_sessions(user_id=USER_ID)
        
        # FIX: Use .get() for dictionary access
        sessions = response.get('sessions', [])
        
        if sessions:
            # Pick the most recent session
            existing_session = sessions[0]
            # FIX: The ID is usually in the 'name' field of the dict
            session_id = existing_session.get('name')
            print(f"🔄 Found existing session. Resuming: {session_id}")
        else:
            print("⚪ No sessions found.")

    except Exception as e:
        print(f"⚠️ Note: Could not list sessions: {e}")

    # 3. Create New Session (If none found)
    if not session_id:
        print(f"🆕 Creating new session...")
        try:
            # returns a Dictionary representing the session
            new_session = await adk_app.async_create_session(user_id=USER_ID)
            # FIX: Access 'name' from dict
            session_id = new_session.get('name')
            print(f"✅ Created Session: {session_id}")
        except Exception as e:
            print(f"❌ Error creating session: {e}")
            return

    # 4. Stream the Query
    query_text = "What is the weather like in New York today?"
    print(f"\n🗣️ User: {query_text}")
    print("🤖 Agent: ", end="", flush=True)

    try:
        async for event in adk_app.async_stream_query(
            user_id=USER_ID,
            session_id=session_id,
            message=query_text,
        ):
            # FIX: Handle event as Dictionary OR Object (Robustness)
            if hasattr(event, "output_text"):
                print(event.output_text, end="", flush=True)
            elif isinstance(event, dict):
                # Check for common keys in ADK response dicts
                if "output_text" in event:
                    print(event["output_text"], end="", flush=True)
                elif "text" in event:
                    print(event["text"], end="", flush=True)
                else:
                    # Fallback
                    print(str(event), end="", flush=True)
            else:
                print(str(event), end="", flush=True)

    except Exception as e:
        print(f"\n❌ Error during streaming: {e}")

    print("\n" + "-"*40)

if __name__ == "__main__":
    asyncio.run(main())