"""
A2A Agent Executor for the TravelFactsAgent
============================================
This file bridges the LangGraph agent and the A2A protocol.

The AgentExecutor is the adapter layer:
  A2A Request → AgentExecutor.execute() → LangGraph Agent → A2A Response

This pattern works for ANY framework (LangChain, CrewAI, custom code, etc.)
"""

import logging
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import new_agent_text_message

from joke_agent.agent import TravelFactsAgent

logger = logging.getLogger(__name__)


class TravelFactsAgentExecutor(AgentExecutor):
    """
    Wraps TravelFactsAgent (LangGraph) to work with the A2A protocol.

    This is the KEY integration point:
    - Receives incoming A2A task requests
    - Passes them to the LangGraph agent
    - Streams results back via the A2A EventQueue
    """

    def __init__(self):
        self.agent = TravelFactsAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """
        Called by the A2A server when a new task arrives.
        Streams agent responses back via event_queue.
        """
        # Extract the user's text message from the A2A request
        query = context.get_user_input()

        # Use context.task_id and context.context_id directly —
        # context.current_task may be None for brand-new requests
        task_id = context.task_id
        context_id = context.context_id

        # TaskUpdater manages the task lifecycle (submitted → working → complete)
        updater = TaskUpdater(event_queue, task_id, context_id)

        # Submit the task first (creates it in the task store)
        await updater.submit()
        await updater.start_work()

        try:
            # Stream responses from the LangGraph agent
            async for chunk in self.agent.stream(query, context_id):

                if chunk["is_task_complete"]:
                    # Final answer — add as artifact and mark complete
                    await updater.add_artifact(
                        parts=[TextPart(text=chunk["content"])],
                        name="travel_facts",
                    )
                    await updater.complete()
                    break

                elif chunk["require_user_input"]:
                    # Agent needs clarification from the user
                    await updater.requires_input(
                        message=new_agent_text_message(
                            chunk["content"], context_id, task_id
                        )
                    )
                    break

                else:
                    # Intermediate "working" status update
                    await updater.update_status(
                        TaskState.working,
                        message=new_agent_text_message(
                            chunk["content"], context_id, task_id
                        ),
                    )

        except Exception as e:
            logger.error(f"TravelFactsAgentExecutor error: {e}")
            await updater.failed(
                message=new_agent_text_message(
                    f"Error: {str(e)}", context_id, task_id
                ),
            )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancellation is not supported by this agent."""
        raise UnsupportedOperationError(message="TravelFactsAgent does not support cancellation.")
