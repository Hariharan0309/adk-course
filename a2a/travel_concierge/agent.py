"""
Travel Concierge — Root ADK Agent (A2A Consumer)
=================================================
This is the MAIN agent the user talks to. It orchestrates two remote agents
via the A2A protocol:

  User
   │
   ▼
Travel Concierge (ADK, port 8000)
   ├──[A2A]──► Weather Agent      (ADK, port 8001)
   └──[A2A]──► Travel Facts Agent (LangGraph, port 8002)

Key concept: RemoteA2aAgent makes remote agents feel like local sub-agents.
The orchestrator doesn't know (or care) what framework the remote agents use!

Prerequisites:
    Terminal 1: adk api_server --a2a --port 8001 a2a/weather_agent
    Terminal 2: python -m a2a.joke_agent
    Terminal 3: adk web a2a/travel_concierge  (or adk run)
"""

from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# ─── Remote Agent 1: Weather Agent (Google ADK, port 8001) ───────────────────
# This is an ADK agent running as a separate service.
# AGENT_CARD_WELL_KNOWN_PATH = "/.well-known/agent.json"
weather_remote_agent = RemoteA2aAgent(
    name="weather_remote_agent",
    description=(
        "A remote weather agent that provides real-time weather information "
        "for any city. Call this when the user asks about weather, temperature, "
        "or climate conditions."
    ),
    # ADK exposes agents at: /a2a/{agent_name}/.well-known/agent-card.json
    agent_card="http://localhost:8001/a2a/weather_agent/.well-known/agent-card.json",
)

# ─── Remote Agent 2: Travel Facts Agent (LangGraph, port 8002) ───────────────
# This is a LangGraph agent — a completely different framework!
# The A2A protocol makes it work seamlessly as a sub-agent.
travel_facts_remote_agent = RemoteA2aAgent(
    name="travel_facts_remote_agent",
    description=(
        "A remote travel facts agent that provides fascinating facts, "
        "hidden gems, and travel tips for any destination. Call this when "
        "the user wants to learn about a place or needs travel inspiration."
    ),
    # a2a-sdk exposes agents at: /.well-known/agent-card.json
    agent_card="http://localhost:8002/.well-known/agent-card.json",
)

# ─── Root Orchestrator Agent ─────────────────────────────────────────────────
# This agent decides which remote agent to call based on the user's request.
# Both remote agents are treated exactly like local sub-agents!
root_agent = Agent(
    model="gemini-2.0-flash",
    name="travel_concierge",
    instruction="""You are a friendly and knowledgeable Travel Concierge.

You help users plan amazing trips by combining real-time weather information
with fascinating destination facts.

You have two specialist agents available:

1. **weather_remote_agent** — Use this for any weather-related questions.
   Example triggers: "What's the weather like?", "Is it cold in Tokyo?",
   "Should I pack an umbrella for London?"

2. **travel_facts_remote_agent** — Use this for destination facts and travel tips.
   Example triggers: "Tell me about Paris", "What's interesting about Japan?",
   "Fun facts about Brazil"

For the BEST travel advice, combine both! When a user mentions a destination:
- First get the current weather from weather_remote_agent
- Then get fascinating facts from travel_facts_remote_agent
- Combine the information into a helpful, engaging travel brief

Always be enthusiastic, warm, and helpful. Make travel planning exciting!""",
    sub_agents=[weather_remote_agent, travel_facts_remote_agent],
)
