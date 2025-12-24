# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Voice Agent API for logistics call automation using Retell AI. This is a FastAPI-based backend that manages agent configurations, test calls, and call results for voice interactions with truck drivers. The project uses Retell AI's **Conversation Flow** feature with a fixed node architecture.

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
│   │   ├── call.py          # Call with status tracking
│   │   └── call_result.py   # CallResult with transcript and structured_data
│   │
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── agent.py         # AgentCreateRequest, AgentUpdateRequest, AgentGetResponse
│   │   ├── call.py          # CallCreate, CallResponse
│   │   └── call_result.py   # CallResultResponse
│   │
│   ├── api/
│   │   ├── deps.py          # Shared dependencies (SessionDep, RetellServiceDep)
│   │   └── routes/          # API endpoint handlers
│   │       ├── agent_configs.py  # CRUD for agent configurations
│   │       ├── calls.py          # Trigger and list calls
│   │       └── webhooks.py       # Retell webhook receiver
│   │
│   └── services/            # Business logic layer
│       ├── retell.py            # Retell AI SDK integration
│       ├── conversation_flow.py # Fixed node architecture for all agents
│       ├── call_analysis.py     # Shared call analysis field definitions
│       └── post_processing.py   # Extract structured data from calls
│
├── pyproject.toml           # uv project config, dependencies, ruff config
├── .env                     # Local environment variables (gitignored)
└── dev.db                   # SQLite database (gitignored)
```

### Conversation Flow Architecture

All agents use the same **Conversation Flow** with this node structure:

```
                    ┌──────────────────────┐
                    │   EMERGENCY NODE     │
                    │     (Global)         │
                    │ Trigger: accident,   │
                    │ breakdown, medical   │
                    └──────────┬───────────┘
                               │
                               ▼
┌─────────────┐     ┌──────────────────────┐
│   START     │────▶│  GREETING/STATUS     │
│             │     │  CHECK NODE          │
└─────────────┘     └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │  IN-TRANSIT     │ │  ARRIVAL        │ │  UNCOOPERATIVE  │
    │  DETAILS        │ │  DETAILS        │ │  HANDLING       │
    └────────┬────────┘ └────────┬────────┘ └────────┬────────┘
             │                   │                   │
             ▼                   ▼                   ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │ EXTRACT: ETA,   │ │ EXTRACT:        │ │  END CALL       │
    │ location, delay │ │ unloading, POD  │ │                 │
    └────────┬────────┘ └────────┬────────┘ └─────────────────┘
             │                   │
             ▼                   ▼
    ┌─────────────────┐ ┌─────────────────┐
    │  END CALL       │ │  END CALL       │
    └─────────────────┘ └─────────────────┘
```

The flow is defined in `app/services/conversation_flow.py`.

### Key Architectural Patterns

**Conversation Flow (Not Single-Prompt LLM):**
- Agents use Retell's `conversation-flow` response engine type
- All agents get the same node architecture - no customization needed
- Structured data is extracted during the call via `extract_dynamic_variable` nodes
- Emergency handling is a global node that can be triggered from any state

**Database Pattern:**
SQLModel combines SQLAlchemy ORM with Pydantic validation. Models use `table=True` and can be directly serialized.

**Configuration:**
Settings are loaded from `.env` using `pydantic-settings`. The `get_settings()` function is cached with `@lru_cache` for performance.

### Database Schema

**calls:**
- `id` (string): Retell call ID (primary key)
- `agent_id` (string): References agent in Retell AI
- `driver_name`, `phone_number`, `load_number`: Call metadata
- `status`: "pending", "in-progress", "completed", "failed"

**call_results:**
- Foreign key to `calls`
- `transcript`: Full call transcript
- `structured_data`: JSON with extracted data (varies by call outcome)

## API Endpoints

### Agent Configurations
- `POST /api/agent-configs` - Create new agent with standard conversation flow
  - Request body: `{"agent_name": "..." (optional)}`
  - Returns: `AgentResponse` from Retell SDK
- `GET /api/agent-configs` - List all agents from Retell AI
  - Query params: `limit` (1-1000), `pagination_key` (optional)
- `GET /api/agent-configs/{agent_id}` - Get specific agent
  - Returns: `{agent_id, name, flow_id}`
- `PATCH /api/agent-configs/{agent_id}` - Update agent
  - Request body: `{"agent_name": "...", "recreate_flow": true/false}`
- Delete agents via Retell's dashboard

### Calls
- `POST /api/calls/trigger` - Trigger new call
- `GET /api/calls` - List all calls
- `GET /api/calls/{id}` - Get specific call

### Webhooks
- `POST /api/webhooks/retell` - Retell webhook receiver
  - Handles: `call_started`, `call_ended`, `call_analyzed`
  - Returns 204 No Content

### System
- `GET /` - Root endpoint with API info
- `GET /health` - Health check

## Dynamic Variables

When creating calls, pass these variables to personalize the conversation:

```python
dynamic_variables = {
    "driver_name": "Mike",
    "load_number": "7891-B",
    "agent_name": "Alex",
    "dispatcher_phone": "+18005551234"
}
```

## Extracted Data

Data is extracted during the call via flow nodes:

**In-Transit:**
- `call_outcome`: "In-Transit Update"
- `driver_status`: Driving, Delayed
- `current_location`: Highway, city, mile marker
- `eta`: Expected arrival time
- `delay_reason`: None, Traffic, Weather, Mechanical, Other

**Arrival:**
- `call_outcome`: "Arrival Confirmation"
- `driver_status`: Arrived, Unloading
- `unloading_status`: Door number, lumper status
- `pod_reminder_acknowledged`: boolean

**Emergency:**
- `call_outcome`: "Emergency"
- `emergency_type`: Accident, Breakdown, Medical, Other
- `safety_status`: Driver's safety confirmation
- `injury_status`: Any injuries
- `emergency_location`: Location details
- `load_secure`: boolean

## Environment Configuration

```bash
DATABASE_URL=sqlite:///./dev.db
RETELL_API_KEY=your_retell_api_key_here
HOST=0.0.0.0
PORT=8000
RELOAD=true
WEBHOOK_BASE_URL=http://localhost:8000  # Use ngrok URL for local dev
```

## Agent Configuration Defaults

All agents use these sensible defaults:
- Voice: `11labs-Adrian` (professional male)
- Voice Model: `eleven_turbo_v2` (high quality, low latency)
- Model: `gpt-4o-mini` (via conversation flow)
- Responsiveness: 0.8, Interruption sensitivity: 0.6
- Backchannel: Enabled with frequency 0.5
- Ambient sound: `call-center` at 0.3 volume
- Denoising: `noise-cancellation` mode
- STT: `accurate` mode for noisy environments
- Boosted keywords: POD, BOL, lumper, detention, ETA, mile marker, etc.
