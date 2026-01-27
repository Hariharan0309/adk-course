from mcp.server.fastmcp import FastMCP
import psutil

# 1. Define the server
mcp = FastMCP("My Computer Agent")

# 2. Add the tool
@mcp.tool()
def get_system_stats() -> str:
    """Returns the current CPU usage and Memory usage of the local machine."""
    # Get CPU usage (blocks for 0.5s to get an accurate reading)
    cpu = psutil.cpu_percent(interval=0.5)
    
    # Get Memory usage
    memory = psutil.virtual_memory()
    used_gb = memory.used / (1024**3)
    total_gb = memory.total / (1024**3)
    
    return (f"🖥️ System Status:\n"
            f"- CPU Usage: {cpu}%\n"
            f"- RAM Usage: {memory.percent}% ({used_gb:.1f} GB / {total_gb:.1f} GB)")

# 3. Run with STDIO transport
if __name__ == "__main__":
    # This keeps the script running and listening to stdin
    mcp.run(transport="stdio")