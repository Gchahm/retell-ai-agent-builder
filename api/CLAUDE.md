# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Voice Agent API for logistics call automation using Retell AI. This is a FastAPI-based backend that manages agent configurations, test calls, and call results for voice interactions with truck drivers. The project is in MVP stage with scaffolded endpoints and database models.

## Development Commands

### Running the Server

```bash
# Development server with auto-reload
uv run fastapi dev app/main.py

# Alternative: Run with uvicorn directly
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server runs at http://localhost:8000 with interactive docs at http://localhost:8000/docs

### Package Management

```bash
# Install dependencies
uv sync

# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name
```

### Code Quality

```bash
# Format code
uv run ruff format .

# Lint and auto-fix issues
uv run ruff check . --fix

# Lint without fixing
uv run ruff check .
```

## Architecture

### Project Structure

```
api/
├── app/
│   ├── main.py              # FastAPI app entry point, lifespan events, CORS, router registration
│   ├── config.py            # Pydantic Settings with env var loading
│   ├── database.py          # SQLModel engine, session factory
│   │
│   ├── models/              # SQLModel database models (table=True)
│   │   ├── agent_config.py  # AgentConfig with JSON retell_settings
│   │   ├── call.py          # Call with status tracking
│   │   └── call_result.py   # CallResult with transcript and structured_data
│   │
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── agent_config.py  # Create, Update, Response schemas
│   │   ├── call.py          # CallCreate, CallResponse
│   │   └── call_result.py   # CallResultResponse
│   │
│   ├── api/
│   │   ├── deps.py          # Shared dependencies (SessionDep)
│   │   └── routes/          # API endpoint handlers
│   │       ├── agent_configs.py  # CRUD for agent configurations
│   │       ├── calls.py          # Trigger and list calls
│   │       └── webhooks.py       # Retell webhook receiver (TODO)
│   │
│   └── services/            # Business logic layer (scaffolded)
│       ├── retell.py        # Retell AI SDK integration (TODO)
│       └── post_processing.py  # LLM transcript processing (TODO)
│
├── pyproject.toml           # uv project config, dependencies, ruff config
├── .env                     # Local environment variables (gitignored)
└── dev.db                   # SQLite database (gitignored)
```

### Key Architectural Patterns

**Separation of Concerns:**
- `models/`: Database table definitions using SQLModel
- `schemas/`: API request/response validation using Pydantic (local data only)
  - `schemas/call.py`: Call request/response schemas (uses retell_agent_id)
- `routes/`: HTTP endpoint handlers, thin controllers
  - Agent routes use types directly from `retell.types` (AgentResponse, AgentListResponse)
- `services/`: Business logic and external API integration
  - `services/retell.py`: Retell AI SDK integration (list_agents implemented)

**Agent Configuration Pattern:**
Agent configurations are managed directly in Retell AI, not stored locally. The `/api/agent-configs` endpoints fetch agents from Retell's API in real-time and return types directly from the Retell SDK (`AgentResponse`, `AgentListResponse`). The `RetellService` class wraps the Retell SDK and provides methods like `list_agents()`.

**Database Pattern:**
SQLModel combines SQLAlchemy ORM with Pydantic validation. Models use `table=True` and can be directly serialized. The `SessionDep` annotated dependency in `api/deps.py` provides database sessions to route handlers.

**Configuration:**
Settings are loaded from `.env` using `pydantic-settings`. The `get_settings()` function is cached with `@lru_cache` for performance.

**Application Lifecycle:**
Database tables are created automatically on startup via the `lifespan` async context manager in `main.py`.

### Database Schema

**test_calls:**
- Tracks individual calls with driver info and status
- `retell_agent_id` (string): References agent in Retell AI, not a foreign key
- Status values: "pending", "in-progress", "completed", "failed"

**call_results:**
- Stores call transcripts and extracted structured data
- Foreign key to `test_calls`
- `structured_data` is a JSON column that varies by scenario type

## API Endpoints

### Agent Configurations (Managed in Retell AI)
- `POST /api/agent-configs` - Create new agent (light wrapper, only requires prompt text)
  - Request body: `{"prompt": "...", "agent_name": "..." (optional)}`
  - Returns: `AgentResponse` from Retell SDK
  - Our API handles all configuration (voice, model, responsiveness, etc.)
- `GET /api/agent-configs` - List all agent configurations from Retell AI
  - Query params: `limit` (1-1000, default 1000), `pagination_key` (string, optional)
- `GET /api/agent-configs/{agent_id}` - Get specific agent (501 Not Implemented - use list endpoint)
- `PATCH /api/agent-configs/{agent_id}` - Update existing agent
  - Request body: `{"prompt": "..." (optional), "agent_name": "..." (optional)}`
  - At least one field required
  - Updating prompt creates a new LLM and updates the agent's response_engine
- Delete agents should be done through Retell's dashboard or API directly

### Calls
- `POST /api/calls/trigger` - Trigger new call (creates pending record, no actual Retell integration yet)
- `GET /api/calls` - List all calls (supports `skip` and `limit` query params)
- `GET /api/calls/{id}` - Get specific call

### Webhooks
- `POST /api/webhooks/retell` - Retell webhook receiver
  - Handles events: `call_started`, `call_ended`, `call_analyzed`
  - Updates Call status in database
  - Stores transcript in CallResult when analysis complete
  - Saves all payloads to `webhook_logs/` directory as JSON files
  - Returns 204 No Content
  - Note: Signature verification not yet implemented

### System
- `GET /` - Root endpoint with API info
- `GET /health` - Health check

## Current State & TODOs

The API scaffold is complete with working CRUD operations, but core integrations are pending:

**COMPLETED - Agent Configuration:**
- ✅ `list_agents()` implemented in `services/retell.py`
- ✅ `create_agent()` implemented as light wrapper (only requires prompt)
- ✅ `update_agent()` implemented as light wrapper (updates prompt and/or name)
- ✅ `POST /api/agent-configs` endpoint creates agents in Retell AI
- ✅ `PATCH /api/agent-configs/{agent_id}` endpoint updates agents in Retell AI
- ✅ `GET /api/agent-configs` endpoint fetches from Retell AI
- ✅ Removed local AgentConfig model and schemas completely
- ✅ Updated Call model to use `retell_agent_id` instead of foreign key
- ✅ Uses Retell SDK types directly (no custom schemas)

**TODO - Retell Integration (`services/retell.py`):**
- Implement `get_agent(agent_id)` for fetching a single agent
- Implement `create_call()` using retell-sdk
- Implement `get_call_details()` for call status
- Update `routes/calls.py` to call Retell API when triggering calls

**COMPLETED - Webhook Processing:**
- ✅ Handle call lifecycle events (call_started, call_ended, call_analyzed)
- ✅ Update Call status based on events
- ✅ Store transcript in CallResult on call_analyzed
- ✅ Automatically extract structured data using OpenAI GPT-4o-mini

**COMPLETED - Post-Processing:**
- ✅ OpenAI integration for transcript analysis
- ✅ Structured data extraction with validation
- ✅ Schema: call_outcome, driver_status, current_location, eta, delay_reason, unloading_status, pod_reminder_acknowledged
- ✅ Error handling with sensible defaults

**TODO - Webhook Security:**
- Implement webhook signature verification (x-retell-signature header)

## Environment Configuration

The `.env` file contains:
```bash
DATABASE_URL=sqlite:///./dev.db
RETELL_API_KEY=your_retell_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
HOST=0.0.0.0
PORT=8000
RELOAD=true
WEBHOOK_BASE_URL=http://localhost:8000  # Use ngrok URL for local dev
```

## Important Notes

- Agent creation is fully implemented as a light wrapper around Retell SDK
- When creating agents, only the prompt is required - all other config uses sensible defaults:
  - Voice: `11labs-Adrian` (professional male, English)
  - Model: `gpt-4o-mini` (fast and cost-effective)
  - Voice Model: `eleven_turbo_v2` (high quality, low latency)
  - Responsiveness: 0.7, Interruption sensitivity: 0.5
  - Webhook URL: Automatically configured from `WEBHOOK_BASE_URL` env var
  - End Call Function: Agent can automatically end calls when user says goodbye or conversation is complete
- No authentication/authorization is currently implemented
- SQLite is used for local development; production will use PostgreSQL (likely Supabase)
- CORS is configured for `localhost:5173` and `localhost:3000` (Vite/React dev servers)
- SQL query logging is enabled via `echo=True` in database engine (disable in production)
