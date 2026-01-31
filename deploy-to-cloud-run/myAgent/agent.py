from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A weather agent that provides real-time weather information.',
    instruction='Answer user questions about the weather using the get_weather tool.',
    tools=[
        MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://weather-mcp-server-673680613234.us-central1.run.app/mcp")
    ),
    ],
)
