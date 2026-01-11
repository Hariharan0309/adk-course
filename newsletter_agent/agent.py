from google.adk.agents import SequentialAgent, ParallelAgent, LoopAgent

# IMPORT YOUR AGENTS
from .sub_agents.researchers import ai_news_agent, hackathon_agent
from .sub_agents.editors import newsletter_writer, editor_agent

# 1. Build the Parallel Team
research_squad = ParallelAgent(
    name="research_squad",
    sub_agents=[ai_news_agent, hackathon_agent],
    description="Fetches AI news and Hackathon events simultaneously."
)

editorial_process = LoopAgent(
    name="editorial_loop",
    sub_agents=[newsletter_writer, editor_agent],
    max_iterations=2
)

# 3. Connect it all
root_agent = SequentialAgent(
    name="newsletter_root_agent",
    sub_agents=[research_squad, editorial_process]
)


