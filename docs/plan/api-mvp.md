# AI Voice Agent - API MVP Setup Guide

**Version:** 1.0
**Last Updated:** December 22, 2025
**Purpose:** Minimal viable API scaffold to validate structure and endpoints

## Overview

This guide focuses on setting up the **minimal API scaffold** to validate the structure works. We'll use:
- **FastAPI** for the web framework
- **SQLite** for local development (no Supabase yet)
- **uv** for modern Python package management
- **SQLModel** for database models
- **Retell SDK** for API integration (structure only, no implementation)
- **No authentication/security** (MVP only)

## Goals

- ✅ Production-like folder structure
- ✅ All API endpoints scaffolded (no implementation)
- ✅ Database models defined
- ✅ Basic CRUD operations working
- ✅ Server running and testable
- ❌ No authentication
- ❌ No actual Retell integration (just structure)
- ❌ No LLM post-processing (just structure)

---

## Technology Stack (MVP)

```bash
# Core
fastapi[standard]>=0.115.0    # Web framework with uvicorn
sqlmodel>=0.0.22              # Database ORM + Pydantic
pydantic-settings>=2.7.0      # Environment configuration

# API Integration (structure only)
httpx>=0.28.0                 # Async HTTP client
retell-sdk>=4.3.0             # Retell AI SDK

# Development
ruff>=0.8.0                   # Linting and formatting
```

---

## Project Structure

```
ai-voice-agent/
├── api/                          # Backend API
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Settings management
│   │   ├── database.py          # Database connection
│   │   │
│   │   ├── models/              # SQLModel database models
│   │   │   ├── __init__.py
│   │   │   ├── agent_config.py
│   │   │   ├── call.py
│   │   │   └── call_result.py
│   │   │
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   ├── agent_config.py
│   │   │   ├── call.py
│   │   │   └── call_result.py
│   │   │
│   │   ├── api/                 # API routes
│   │   │   ├── __init__.py
│   │   │   ├── deps.py          # Shared dependencies
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       ├── agent_configs.py
│   │   │       ├── calls.py
│   │   │       └── webhooks.py
│   │   │
│   │   └── services/            # Business logic (structure only)
│   │       ├── __init__.py
│   │       ├── retell.py        # Retell API integration
│   │       └── post_processing.py  # LLM processing
│   │
│   ├── pyproject.toml           # Project dependencies
│   ├── .env.example             # Environment variables template
│   ├── .env                     # Local environment (gitignored)
│   └── dev.db                   # SQLite database (gitignored)
│
├── frontend/                     # (Future - not in this guide)
└── docs/
    └── plan/
        ├── plan.md
        ├── phase-1-be.md
        └── api-mvp.md            # This document
```

---

## Setup Instructions

### Prerequisites

- **Python 3.11+** installed
- **uv** package manager

### Step 1: Install uv

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

### Step 2: Initialize Project

```bash
# Navigate to project root
cd /Users/gchahm/dev/e3/ai-voice-agent

# Create api directory if it doesn't exist
mkdir -p api
cd api

# Initialize uv project
uv init --name ai-voice-agent-api --app

# This creates:
# - pyproject.toml
# - .python-version (defaults to current Python)
# - hello.py (we'll delete this)
```

### Step 3: Configure pyproject.toml

Replace the generated `pyproject.toml` with:

```toml
[project]
name = "ai-voice-agent-api"
version = "0.1.0"
description = "AI Voice Agent API for logistics call automation"
requires-python = ">=3.11"
dependencies = [
    "fastapi[standard]>=0.115.0",
    "sqlmodel>=0.0.22",
    "pydantic-settings>=2.7.0",
    "httpx>=0.28.0",
    "retell-sdk>=4.3.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.8.0",
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Step 4: Install Dependencies

```bash
# Install all dependencies
uv sync

# This creates:
# - .venv/ directory with virtual environment
# - uv.lock file for reproducible builds
```

### Step 5: Create Folder Structure

```bash
# Remove auto-generated file
rm hello.py

# Create directory structure
mkdir -p app/{models,schemas,api/routes,services}

# Create __init__.py files
touch app/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/api/__init__.py
touch app/api/routes/__init__.py
touch app/services/__init__.py
```

### Step 6: Environment Configuration

Create `.env.example`:

```bash
cat > .env.example << 'EOF'
# Database
DATABASE_URL=sqlite:///./dev.db

# API Keys (not used in MVP, but structure ready)
RETELL_API_KEY=your_retell_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Server
HOST=0.0.0.0
PORT=8000
RELOAD=true
EOF
```

Create `.env` for local development:

```bash
cp .env.example .env
```

Add to `.gitignore`:

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
env/

# uv
uv.lock
.python-version

# Database
*.db
*.db-journal

# Environment
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
```

---

## Core Files Implementation

### 1. Configuration (`app/config.py`)

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str = "sqlite:///./dev.db"

    # API Keys (structure only for MVP)
    retell_api_key: str = "mock_key"
    openai_api_key: str = "mock_key"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
```

### 2. Database Setup (`app/database.py`)

```python
from sqlmodel import SQLModel, create_engine, Session
from app.config import get_settings

settings = get_settings()

# SQLite engine (use check_same_thread=False for FastAPI)
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=True,  # Log SQL queries (disable in production)
)


def create_db_and_tables():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session
```

### 3. Database Models

#### `app/models/agent_config.py`

```python
from sqlmodel import SQLModel, Field, Column, JSON
from datetime import datetime
from typing import Optional


class AgentConfig(SQLModel, table=True):
    """Agent configuration for voice calls."""

    __tablename__ = "agent_configurations"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    system_prompt: str
    scenario_type: str  # "check-in" or "emergency"

    # Retell settings stored as JSON
    retell_settings: dict = Field(default_factory=dict, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

#### `app/models/call.py`

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Call(SQLModel, table=True):
    """Test call metadata."""

    __tablename__ = "test_calls"

    id: Optional[int] = Field(default=None, primary_key=True)
    agent_config_id: int = Field(foreign_key="agent_configurations.id")

    # Call details
    driver_name: str
    phone_number: str
    load_number: str

    # Status tracking
    status: str  # "pending", "in-progress", "completed", "failed"
    retell_call_id: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

#### `app/models/call_result.py`

```python
from sqlmodel import SQLModel, Field, Column, JSON
from datetime import datetime
from typing import Optional


class CallResult(SQLModel, table=True):
    """Call results and structured data."""

    __tablename__ = "call_results"

    id: Optional[int] = Field(default=None, primary_key=True)
    call_id: int = Field(foreign_key="test_calls.id")

    # Raw data
    transcript: str

    # Structured data (varies by scenario)
    structured_data: dict = Field(default_factory=dict, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=datetime.utcnow)
```

#### `app/models/__init__.py`

```python
from app.models.agent_config import AgentConfig
from app.models.call import Call
from app.models.call_result import CallResult

__all__ = ["AgentConfig", "Call", "CallResult"]
```

### 4. API Schemas (Request/Response)

#### `app/schemas/agent_config.py`

```python
from pydantic import BaseModel
from datetime import datetime


class AgentConfigCreate(BaseModel):
    """Schema for creating agent configuration."""

    name: str
    system_prompt: str
    scenario_type: str
    retell_settings: dict = {}


class AgentConfigUpdate(BaseModel):
    """Schema for updating agent configuration."""

    name: str | None = None
    system_prompt: str | None = None
    scenario_type: str | None = None
    retell_settings: dict | None = None


class AgentConfigResponse(BaseModel):
    """Schema for agent configuration response."""

    id: int
    name: str
    system_prompt: str
    scenario_type: str
    retell_settings: dict
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

#### `app/schemas/call.py`

```python
from pydantic import BaseModel
from datetime import datetime


class CallCreate(BaseModel):
    """Schema for triggering a call."""

    agent_config_id: int
    driver_name: str
    phone_number: str
    load_number: str


class CallResponse(BaseModel):
    """Schema for call response."""

    id: int
    agent_config_id: int
    driver_name: str
    phone_number: str
    load_number: str
    status: str
    retell_call_id: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

#### `app/schemas/call_result.py`

```python
from pydantic import BaseModel
from datetime import datetime


class CallResultResponse(BaseModel):
    """Schema for call result response."""

    id: int
    call_id: int
    transcript: str
    structured_data: dict
    created_at: datetime

    model_config = {"from_attributes": True}
```

#### `app/schemas/__init__.py`

```python
from app.schemas.agent_config import (
    AgentConfigCreate,
    AgentConfigUpdate,
    AgentConfigResponse,
)
from app.schemas.call import CallCreate, CallResponse
from app.schemas.call_result import CallResultResponse

__all__ = [
    "AgentConfigCreate",
    "AgentConfigUpdate",
    "AgentConfigResponse",
    "CallCreate",
    "CallResponse",
    "CallResultResponse",
]
```

### 5. API Dependencies (`app/api/deps.py`)

```python
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from app.database import get_session

# Reusable dependency for database sessions
SessionDep = Annotated[Session, Depends(get_session)]
```

### 6. API Routes

#### `app/api/routes/agent_configs.py`

```python
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.api.deps import SessionDep
from app.models import AgentConfig
from app.schemas import AgentConfigCreate, AgentConfigUpdate, AgentConfigResponse

router = APIRouter(prefix="/api/agent-configs", tags=["agent-configs"])


@router.post("", response_model=AgentConfigResponse, status_code=201)
def create_agent_config(config: AgentConfigCreate, session: SessionDep):
    """Create a new agent configuration."""
    db_config = AgentConfig.model_validate(config)
    session.add(db_config)
    session.commit()
    session.refresh(db_config)
    return db_config


@router.get("", response_model=list[AgentConfigResponse])
def list_agent_configs(session: SessionDep):
    """List all agent configurations."""
    configs = session.exec(select(AgentConfig)).all()
    return configs


@router.get("/{config_id}", response_model=AgentConfigResponse)
def get_agent_config(config_id: int, session: SessionDep):
    """Get a specific agent configuration."""
    config = session.get(AgentConfig, config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Agent configuration not found")
    return config


@router.patch("/{config_id}", response_model=AgentConfigResponse)
def update_agent_config(config_id: int, updates: AgentConfigUpdate, session: SessionDep):
    """Update an agent configuration."""
    config = session.get(AgentConfig, config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Agent configuration not found")

    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(config, key, value)

    session.add(config)
    session.commit()
    session.refresh(config)
    return config


@router.delete("/{config_id}", status_code=204)
def delete_agent_config(config_id: int, session: SessionDep):
    """Delete an agent configuration."""
    config = session.get(AgentConfig, config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Agent configuration not found")

    session.delete(config)
    session.commit()
    return None
```

#### `app/api/routes/calls.py`

```python
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.api.deps import SessionDep
from app.models import Call
from app.schemas import CallCreate, CallResponse

router = APIRouter(prefix="/api/calls", tags=["calls"])


@router.post("/trigger", response_model=CallResponse, status_code=201)
def trigger_call(call_data: CallCreate, session: SessionDep):
    """
    Trigger a new call via Retell AI.

    TODO: Implement actual Retell API integration
    """
    # Create call record
    db_call = Call(
        agent_config_id=call_data.agent_config_id,
        driver_name=call_data.driver_name,
        phone_number=call_data.phone_number,
        load_number=call_data.load_number,
        status="pending",
    )

    session.add(db_call)
    session.commit()
    session.refresh(db_call)

    # TODO: Call Retell API to actually trigger the call
    # retell_response = retell_service.create_call(...)
    # db_call.retell_call_id = retell_response.call_id
    # db_call.status = "in-progress"
    # session.commit()

    return db_call


@router.get("", response_model=list[CallResponse])
def list_calls(session: SessionDep, skip: int = 0, limit: int = 100):
    """List all calls."""
    statement = select(Call).offset(skip).limit(limit)
    calls = session.exec(statement).all()
    return calls


@router.get("/{call_id}", response_model=CallResponse)
def get_call(call_id: int, session: SessionDep):
    """Get a specific call."""
    call = session.get(Call, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call
```

#### `app/api/routes/webhooks.py`

```python
from fastapi import APIRouter, Request, BackgroundTasks

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


@router.post("/retell")
async def retell_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Receive webhooks from Retell AI.

    TODO: Implement webhook signature verification
    TODO: Process webhook events
    TODO: Extract and store transcript
    TODO: Trigger post-processing
    """
    payload = await request.json()

    # TODO: Verify webhook signature
    # verify_retell_signature(request.headers, payload)

    # TODO: Process different webhook events
    # - call.started
    # - call.ended
    # - call.analyzed

    # Acknowledge immediately (webhooks have 10s timeout)
    return {"status": "received"}


def process_webhook_background(payload: dict):
    """
    Process webhook in background.

    TODO: Implement background processing
    TODO: Update call status
    TODO: Store transcript
    TODO: Trigger LLM post-processing
    """
    pass
```

#### `app/api/routes/__init__.py`

```python
from app.api.routes import agent_configs, calls, webhooks

__all__ = ["agent_configs", "calls", "webhooks"]
```

### 7. Service Layer (Structure Only)

#### `app/services/retell.py`

```python
from retell import Retell
from app.config import get_settings

settings = get_settings()


class RetellService:
    """Service for interacting with Retell AI API."""

    def __init__(self):
        self.client = Retell(api_key=settings.retell_api_key)

    def create_call(self, phone_number: str, agent_config: dict):
        """
        Create a phone call via Retell AI.

        TODO: Implement using retell-sdk
        See: https://github.com/RetellAI/retell-python-sdk/blob/main/api.md
        """
        pass

    def get_call_details(self, call_id: str):
        """
        Get call details from Retell AI.

        TODO: Implement using retell-sdk
        """
        pass
```

#### `app/services/post_processing.py`

```python
class PostProcessingService:
    """Service for LLM-based transcript post-processing."""

    def __init__(self):
        pass

    def extract_structured_data(self, transcript: str, scenario_type: str):
        """
        Extract structured data from transcript using LLM.

        TODO: Implement using OpenAI/Anthropic API
        TODO: Use different schemas based on scenario_type
        """
        pass
```

#### `app/services/__init__.py`

```python
from app.services.retell import RetellService
from app.services.post_processing import PostProcessingService

__all__ = ["RetellService", "PostProcessingService"]
```

### 8. Main Application (`app/main.py`)

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.api.routes import agent_configs, calls, webhooks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)


app = FastAPI(
    title="AI Voice Agent API",
    description="API for managing AI voice agent calls for logistics",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent_configs.router)
app.include_router(calls.router)
app.include_router(webhooks.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "AI Voice Agent API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
```

---

## Running the Application

### Development Server

```bash
# Activate virtual environment (if not using uv run)
source .venv/bin/activate

# Run with uv (recommended)
uv run fastapi dev app/main.py

# Or run with uvicorn directly
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Testing Endpoints

#### Using FastAPI Docs (http://localhost:8000/docs)

1. Navigate to http://localhost:8000/docs
2. Try the endpoints interactively

#### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Create agent configuration
curl -X POST http://localhost:8000/api/agent-configs \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Agent",
    "system_prompt": "You are a helpful assistant",
    "scenario_type": "check-in",
    "retell_settings": {
      "voice": "en-US-Neural2-A",
      "backchanneling": true
    }
  }'

# List agent configurations
curl http://localhost:8000/api/agent-configs

# Trigger a call (will create pending call, no actual Retell call yet)
curl -X POST http://localhost:8000/api/calls/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "agent_config_id": 1,
    "driver_name": "John Doe",
    "phone_number": "+1234567890",
    "load_number": "LOAD-123"
  }'

# List calls
curl http://localhost:8000/api/calls
```

---

## API Endpoints Summary

### Agent Configurations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/agent-configs` | Create new agent configuration |
| GET | `/api/agent-configs` | List all agent configurations |
| GET | `/api/agent-configs/{id}` | Get specific agent configuration |
| PATCH | `/api/agent-configs/{id}` | Update agent configuration |
| DELETE | `/api/agent-configs/{id}` | Delete agent configuration |

### Calls

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/calls/trigger` | Trigger a new call (TODO: implement Retell) |
| GET | `/api/calls` | List all calls |
| GET | `/api/calls/{id}` | Get specific call |

### Webhooks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/webhooks/retell` | Receive Retell AI webhooks (TODO: implement) |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API info |
| GET | `/health` | Health check |

---

## Database Schema

### Tables Created

1. **agent_configurations**
   - id (primary key)
   - name
   - system_prompt
   - scenario_type
   - retell_settings (JSON)
   - created_at
   - updated_at

2. **test_calls**
   - id (primary key)
   - agent_config_id (foreign key)
   - driver_name
   - phone_number
   - load_number
   - status
   - retell_call_id
   - created_at
   - updated_at

3. **call_results**
   - id (primary key)
   - call_id (foreign key)
   - transcript
   - structured_data (JSON)
   - created_at

---

## Using Docker (Alternative to SQLite)

If you prefer PostgreSQL in Docker instead of SQLite:

### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ai_voice_agent
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Update .env

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_voice_agent
```

### Install PostgreSQL driver

```bash
uv add asyncpg
```

### Update database.py

```python
from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

# For PostgreSQL
engine = create_async_engine(
    settings.database_url,
    echo=True,
)
```

---

## Code Quality

### Format code with Ruff

```bash
uv run ruff format .
```

### Lint code with Ruff

```bash
uv run ruff check . --fix
```

---

## Next Steps

Once the scaffold is validated:

1. **Implement Retell Integration**
   - Use retell-sdk to create actual phone calls
   - Handle webhook events properly
   - Verify webhook signatures

2. **Implement Post-Processing**
   - Integrate OpenAI/Anthropic for transcript analysis
   - Create scenario-specific extraction schemas
   - Store structured data

3. **Add Frontend**
   - React application for UI
   - Call triggering interface
   - Results viewer

4. **Add Authentication**
   - JWT tokens with PyJWT
   - User management
   - Secure endpoints

5. **Switch to Supabase**
   - Migrate from SQLite to Supabase PostgreSQL
   - Use Alembic for migrations
   - Connection pooling

6. **Testing**
   - Write pytest tests
   - Mock external APIs
   - Integration tests

---

## Validation Checklist

- [ ] uv project initialized
- [ ] Dependencies installed
- [ ] Folder structure created
- [ ] Database models defined
- [ ] API schemas created
- [ ] Routes scaffolded
- [ ] Server runs without errors
- [ ] Can create agent configuration via API
- [ ] Can list agent configurations
- [ ] Can trigger call (creates pending record)
- [ ] Database persists data (dev.db created)
- [ ] Interactive docs accessible at /docs
- [ ] Health check endpoint works

---

## Troubleshooting

### Issue: SQLite database not created

**Solution**: Check that `create_db_and_tables()` is called in the lifespan event. Verify `DATABASE_URL` in `.env`.

### Issue: Import errors

**Solution**: Ensure you're running commands with `uv run` or have activated the virtual environment with `source .venv/bin/activate`.

### Issue: Port already in use

**Solution**: Change port in `.env` or kill the process using port 8000:
```bash
lsof -ti:8000 | xargs kill -9
```

### Issue: CORS errors from frontend

**Solution**: Add frontend URL to `allow_origins` in CORS middleware in `app/main.py`.

---

## Summary

This MVP scaffold provides:
- ✅ Production-like structure
- ✅ All endpoint routes defined
- ✅ Database models and schemas
- ✅ Working CRUD operations
- ✅ Ready for Retell SDK integration
- ✅ Ready for LLM post-processing

**The API is now ready for implementation of the actual business logic!**
