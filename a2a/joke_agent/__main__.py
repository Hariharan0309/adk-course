"""
Travel Facts Agent — A2A Server Startup
=========================================
This file starts the A2A-compatible HTTP server for the LangGraph agent.

This is what makes a non-ADK agent discoverable and callable via A2A:
  1. Define an AgentCard  (who am I? what can I do?)
  2. Wrap the executor   (how do I handle requests?)
  3. Start the server    (listen on a port)

Run:
    cd adk-course/a2a
    python -m joke_agent

Agent card will be at:
    http://localhost:8002/.well-known/agent-card.json
"""

import logging
import os
import sys
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from dotenv import load_dotenv

from joke_agent.agent_executor import TravelFactsAgentExecutor

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST = "localhost"
PORT = 8002


def main():
    # Validate environment
    if not os.environ.get("GOOGLE_API_KEY"):
        logger.error("Missing GOOGLE_API_KEY environment variable.")
        sys.exit(1)

    # ── 1. Define the Agent Card ─────────────────────────────────────────────
    # The AgentCard is like a "business card" for your agent.
    # Other agents discover your capabilities by fetching this JSON.
    skill = AgentSkill(
        id="travel_facts",
        name="Travel Facts & Tips",
        description=(
            "Provides fascinating facts, hidden gems, and travel tips "
            "for any destination in the world."
        ),
        tags=["travel", "facts", "destinations", "tips"],
        examples=[
            "Tell me interesting facts about Tokyo",
            "What should I know before visiting Paris?",
            "Give me fun facts about Brazil",
        ],
    )

    agent_card = AgentCard(
        name="Travel Facts Agent",
        description=(
            "A LangGraph-powered agent that shares fascinating travel facts "
            "and insider tips about destinations worldwide. "
            "Built with LangGraph, exposed via A2A protocol."
        ),
        url=f"http://{HOST}:{PORT}/",
        skills=[skill],
        capabilities=AgentCapabilities(streaming=True),
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
    )

    # ── 2. Wire up the executor and request handler ──────────────────────────
    executor = TravelFactsAgentExecutor()
    handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=InMemoryTaskStore(),
    )

    # ── 3. Build and start the A2A Starlette server ──────────────────────────
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=handler,
    )

    logger.info(f"🚀 Travel Facts Agent (LangGraph) starting on http://{HOST}:{PORT}")
    logger.info(f"📋 Agent card: http://{HOST}:{PORT}/.well-known/agent-card.json")

    uvicorn.run(server.build(), host=HOST, port=PORT)


if __name__ == "__main__":
    main()
