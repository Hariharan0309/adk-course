"""
Travel Facts Agent — LangGraph Agent
======================================
This agent is built with LangGraph (not Google ADK!) and wrapped with
the a2a-sdk to expose it via the A2A protocol.

This is the KEY demo of cross-framework A2A communication:
  LangGraph Agent ←→ A2A Protocol ←→ Google ADK Agent
"""

import os
from typing import Annotated, AsyncIterable
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


# ─── LangGraph State ──────────────────────────────────────────────────────────
class State(TypedDict):
    messages: Annotated[list, add_messages]


# ─── LangGraph Agent ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a fun and enthusiastic travel facts expert! 🌍

When someone mentions a travel destination or asks about a place, you:
1. Share 2-3 fascinating, surprising, or little-known facts about that destination
2. Include one fun travel tip for visitors
3. Keep it engaging, conversational, and full of personality

If the query is not about a travel destination, politely redirect and ask them
to ask about a place they'd like to visit.

Always respond with interesting and accurate facts that would make someone excited to visit!"""


class TravelFactsAgent:
    """
    A LangGraph-based agent that provides fun travel facts.
    This will be wrapped and exposed as an A2A server.
    """

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.environ.get("GOOGLE_API_KEY"),
        )

        # Build the LangGraph workflow
        builder = StateGraph(State)
        builder.add_node("chatbot", self._chatbot_node)
        builder.add_edge(START, "chatbot")
        builder.add_edge("chatbot", END)
        self.graph = builder.compile()

    def _chatbot_node(self, state: State) -> dict:
        """The main LangGraph node — calls the LLM with the system prompt."""
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
        response = self.llm.invoke(messages)
        return {"messages": [response]}

    async def stream(self, user_message: str, session_id: str) -> AsyncIterable[dict]:
        """
        Stream responses from the LangGraph agent.
        Yields dicts with:
          - is_task_complete: bool
          - require_user_input: bool
          - content: str
        """
        # Show a "thinking" message first
        yield {
            "is_task_complete": False,
            "require_user_input": False,
            "content": "✈️ Researching travel facts...",
        }

        try:
            # Run the LangGraph workflow
            result = await self.graph.ainvoke(
                {"messages": [HumanMessage(content=user_message)]},
                config={"configurable": {"thread_id": session_id}},
            )

            # Extract the final response
            final_message = result["messages"][-1].content

            yield {
                "is_task_complete": True,
                "require_user_input": False,
                "content": final_message,
            }

        except Exception as e:
            yield {
                "is_task_complete": True,
                "require_user_input": False,
                "content": f"Sorry, I couldn't fetch travel facts: {str(e)}",
            }
