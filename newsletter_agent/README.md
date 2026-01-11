# Newsletter Agent

This agent acts as an automated editorial team that researches, drafts, and edits a weekly developer newsletter. It leverages the Google ADK to coordinate multiple specialized AI agents.

## 🤖 Architecture

The `newsletter_root_agent` orchestrates a two-stage process using a **SequentialAgent**:

1.  **Research Phase (`research_squad`)**:
    *   **Type**: `ParallelAgent`
    *   **Description**: Runs two specialized research agents simultaneously to gather content.
    *   **Sub-agents**:
        *   `ai_news_agent`: Uses Google Search to find 3 major AI headlines from the last 7 days.
        *   `hackathon_agent`: Uses Google Search to find 3 upcoming global or online coding hackathons.

2.  **Editorial Phase (`editorial_process`)**:
    *   **Type**: `LoopAgent`
    *   **Description**: A collaborative loop between a writer and an editor to refine the content.
    *   **Sub-agents**:
        *   `newsletter_writer`: Combines the research findings into a "Weekly Developer Update" formatted with emojis, bullet points, and links.
        *   `editor_agent`: Reviews the draft. If it meets quality standards (links present, good formatting), it approves the draft by calling the `exit_loop` tool. Otherwise, it provides feedback for a rewrite.
    *   **Max Iterations**: 2

## 🛠️ Tools Used

*   **Google Search**: Used by the research agents to find real-time information.
*   **FunctionTool (`exit_loop`)**: Used by the `editor_agent` to signal final approval and terminate the editorial loop.

## 🧠 Models

All agents in this team use the **Gemini 2.5 Flash Lite** model for efficient and fast processing, configured with robust retry logic for reliability.

## 📂 File Structure

*   `agent.py`: Defines the `root_agent` and assembles the team.
*   `sub_agents/researchers.py`: Contains the `ai_news_agent` and `hackathon_agent`.
*   `sub_agents/editors.py`: Contains the `newsletter_writer` and `editor_agent` (plus the `exit_loop` tool).

## 🚀 Usage

## How to Run

Ensure you have the Google ADK installed and configured.

1. Navigate to the project root directory (`adk-course`).

2. Run the agent using the ADK web interface:
   ```bash
   adk web
   ```
