# A2A Protocol — Agent-to-Agent Communication Demo

This mini project demonstrates the **Agent-to-Agent (A2A) Protocol** with Google ADK,
showing how agents built on **different frameworks** can communicate seamlessly.

## Architecture

```
User
 │
 ▼
Travel Concierge (Google ADK)          ← Port 8000 (adk web)
 ├──[A2A Protocol]──► Weather Agent    ← Port 8001 (Google ADK)
 └──[A2A Protocol]──► Travel Facts Agent  ← Port 8002 (LangGraph 🔥)
```

The key insight: **The Travel Concierge doesn't know or care that Travel Facts is LangGraph!**
A2A makes cross-framework communication transparent.

## What Each Agent Does

| Agent | Framework | Port | Capability |
|-------|-----------|------|------------|
| `weather_agent` | Google ADK | 8001 | Real-time weather via Open-Meteo API |
| `joke_agent` (Travel Facts) | **LangGraph** | 8002 | Fun destination facts & travel tips |
| `travel_concierge` | Google ADK | 8000 | Orchestrates both → complete travel brief |

## Setup

### 1. Install dependencies
```bash
cd adk-course/a2a
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

## Running the Project

You need **3 terminals** running simultaneously:

### Terminal 1 — Start the Weather Agent (ADK → A2A)
```bash
cd adk-course
adk api_server --a2a --port 8001 a2a/remote_agents
```

Verify it's running:
```bash
curl http://localhost:8001/a2a/weather_agent/.well-known/agent-card.json
```

### Terminal 2 — Start the Travel Facts Agent (LangGraph → A2A)
> Note: run from INSIDE `a2a/` to avoid package name conflict with `a2a-sdk`
```bash
cd adk-course/a2a
python -m joke_agent
```

Verify it's running:
```bash
curl http://localhost:8002/.well-known/agent-card.json
```

### Terminal 3 — Start the Travel Concierge (ADK root agent)
```bash
cd adk-course
adk web a2a/travel_concierge
```

Open **http://localhost:8000** in your browser and chat!

## Example Conversations

Try these prompts in the Travel Concierge chat:

**Single agent delegation:**
- `"What's the weather like in Tokyo right now?"`  → delegates to Weather Agent
- `"Tell me interesting facts about Paris"` → delegates to Travel Facts Agent

**Multi-agent orchestration (the best demo!):**
- `"I'm planning a trip to Barcelona next week. Give me a full travel brief!"`
- `"Help me decide between visiting Iceland or Morocco"`
- `"Plan a trip to New York — weather and things to know"`

## How A2A Works — Key Concepts

### 1. Agent Card (Agent Discovery)
Every A2A agent publishes a JSON "business card" at `/.well-known/agent.json`:
```json
{
  "name": "Travel Facts Agent",
  "description": "Provides travel facts for destinations worldwide",
  "url": "http://localhost:8002/",
  "skills": [...],
  "capabilities": {"streaming": true}
}
```

### 2. Exposing an ADK Agent via A2A
```bash
# ADK CLI automatically wraps your agent and starts an A2A server
adk api_server --a2a --port 8001 a2a/weather_agent
```

### 3. Exposing a LangGraph Agent via A2A
```python
# Use the a2a-sdk to wrap any framework
from a2a.server.apps import A2AStarletteApplication
from a2a.server.agent_execution import AgentExecutor

class MyExecutor(AgentExecutor):
    async def execute(self, context, event_queue):
        # Bridge your LangGraph agent to A2A here
        ...
```

### 4. Consuming Remote Agents in ADK
```python
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

remote = RemoteA2aAgent(
    name="my_remote_agent",
    description="What this agent does",
    agent_card="http://localhost:8001/a2a/my_agent/.well-known/agent.json",
)

root_agent = Agent(
    ...
    sub_agents=[remote],  # Remote agent feels like a local sub-agent!
)
```

## Project Structure

```
a2a/
├── README.md
├── requirements.txt
├── .env.example
│
├── weather_agent/              # Google ADK Agent → exposed via A2A
│   ├── __init__.py
│   └── agent.py               # Defines root_agent with get_weather tool
│
├── joke_agent/                 # LangGraph Agent → exposed via a2a-sdk
│   ├── __init__.py
│   ├── agent.py               # TravelFactsAgent (LangGraph StateGraph)
│   ├── agent_executor.py      # A2A adapter (AgentExecutor pattern)
│   └── __main__.py            # Starts the A2A server on port 8002
│
└── travel_concierge/           # Root ADK Agent → consumes both via A2A
    ├── __init__.py
    └── agent.py               # RemoteA2aAgent consuming weather + facts
```

## References

- [Google ADK A2A Documentation](https://adk.dev/a2a/)
- [A2A Protocol Specification](https://a2a-protocol.org/latest/)
- [A2A Python SDK](https://github.com/a2aproject/a2a-python)
- [A2A Sample Agents](https://github.com/a2aproject/a2a-samples)
