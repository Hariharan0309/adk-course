from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters, StreamableHTTPConnectionParams
import os

#uv run main.py --tools drive --tool-tier core --transport streamable-http

LOCAL_SERVER_SCRIPT = "server.py"
LOCAL_SERVER_DIR = "/home/hariharan-r/PROJECTS/ContentCreationProjects/adk-course/mcp_tutorial/local_mcp_server"

SERVER_DIR = "/home/hariharan-r/PROJECTS/ContentCreationProjects/adk-course/mcp_tutorial/google_workspace_mcp"

# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='''You are an intelligent Drive Assistant connected to Google Drive via the Model Context Protocol (MCP). 

# Your goal is to help the user find, summarize, and extract information from their documents.

# Follow this strictly sequential process for every query:
# 1.  **SEARCH**: Always start by using the `drive_search` tool to find relevant files. Do not guess filenames.
# 2.  **VERIFY**: If multiple files are found, list them and ask the user to confirm which one to use. If one clear match is found, proceed.
# 3.  **READ**: Use the `drive_read_file` tool to inspect the content of the selected file.
# 4.  **ANSWER**: Provide a clear, concise answer based *strictly* on the file content.

# Constraint: If you cannot find the file or the information is missing, explicitly state "I could not find that information in your Drive" rather than hallucinating an answer.''',
# tools=[
#         MCPToolset(
#     connection_params=StreamableHTTPConnectionParams(
#         url="http://0.0.0.0:8020/mcp")
#     ),
#     ],
# )

# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='''You are an intelligent Drive Assistant connected to Google Drive via the Model Context Protocol (MCP). 

# Your goal is to help the user find, summarize, and extract information from their documents.

# Follow this strictly sequential process for every query:
# 1.  **SEARCH**: Always start by using the `drive_search` tool to find relevant files. Do not guess filenames.
# 2.  **VERIFY**: If multiple files are found, list them and ask the user to confirm which one to use. If one clear match is found, proceed.
# 3.  **READ**: Use the `drive_read_file` tool to inspect the content of the selected file.
# 4.  **ANSWER**: Provide a clear, concise answer based *strictly* on the file content.

# Constraint: If you cannot find the file or the information is missing, explicitly state "I could not find that information in your Drive" rather than hallucinating an answer.''',
# # ... inside your root_agent definition ...

# tools=[
#     MCPToolset(
#         connection_params=StdioServerParameters(
#             command="uv",
#             args=["run", "main.py","--tools", "drive", "--tool-tier", "complete"],
#             cwd=SERVER_DIR,
            
#             # 👇 CHANGE THE EMAIL HERE
#             env={
#                 "GOOGLE_CLIENT_SECRET_PATH": "/home/hariharan-r/Documents/Google_Credentials/gdrive-credentials.json",
                
#                 # Replace 'my_email@gmail.com' with your actual email
#                 "USER_GOOGLE_EMAIL": "hariharan2002psg@gmail.com", 
#                 "WORKSPACE_MCP_BASE_URI": "http://localhost",
#                 "WORKSPACE_MCP_PORT": "8010",
#                 "OAUTHLIB_INSECURE_TRANSPORT": "1",
                
#             }
#         )
#     ),
# ],
# )

root_agent = Agent(
    model='gemini-2.5-flash',
    name='System_Monitor_Agent',
    instruction="""
    You are a System Administrator Agent.
    Use the `get_system_stats` tool to check the computer's health (CPU/RAM) whenever asked.
    """,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                # Use the python executable directly
                command="python",
                
                # Just run the script filename
                args=[LOCAL_SERVER_SCRIPT],
                
                # We still set cwd so Python knows where to look
                cwd=LOCAL_SERVER_DIR,
            )
        ),
    ],
)