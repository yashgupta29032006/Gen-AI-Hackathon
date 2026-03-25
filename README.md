# FlowOS – Multi-Agent Productivity Brain

FlowOS is a COMPLETE, production-ready, secure multi-agent AI system designed to help users manage tasks, schedules, and information through coordinated agents, tools, and memory.

## 🏗️ Architecture

FlowOS follows a modular, scalable architecture:
- **Primary Agent (Orchestrator)**: Parses user input, breaks it into structured tasks, and delegates to sub-agents.
- **Sub-Agents**:
    - **Task Agent**: Handles CRUD operations for tasks (Stored in SQLite).
    - **Scheduler Agent**: Manages time slots and handles scheduling conflicts.
    - **Notes Agent**: Stores and retrieves notes with context memory.
    - **Tool Agent (MCP Layer)**: Modular interface for executing database operations and external API calls.
- **Memory Layer**: SQLite database using SQLAlchemy ORM for persistence.
- **Workflow Engine**: Orchestrates execution chains with retry and fail-safe logic.
- **API Layer**: FastAPI powerhouses the system's endpoints.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Google Gemini API Key

### Installation

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

### Running the App

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

## 🛠️ API Endpoints

- `POST /ask`: Send a natural language query to the orchestrator.
- `GET /tasks`: List all tasks.
- `POST /execute`: Manually trigger a workflow step.
- `GET /logs`: Retrieve system execution logs.

## 🧪 Testing

Run tests using pytest:
```bash
pytest tests/
```

