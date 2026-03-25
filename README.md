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
- `GET /auth/login`: Initialize Google OAuth flow.

## 🎨 Frontend (Next.js)

The project now includes a modern dashboard built with Next.js and Tailwind CSS.

### Setup Frontend
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`
4. Access the UI at `http://localhost:3000`.

## 🔗 Google Calendar Integration

FlowOS can now schedule real events on your Google Calendar.

### Prerequisites
1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Google Calendar API**.
3. Create **OAuth 2.0 Client IDs** (Web application).
4. Add `http://localhost:8000/auth/callback` to the **Authorized redirect URIs**.

### Environment Variables
Add the following to your `.env` file in the root:
```env
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://localhost:8000/auth/callback
```

## 🧪 Testing

Run tests using pytest:
```bash
pytest tests/
```

