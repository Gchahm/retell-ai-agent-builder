# Phase 1 Backend Implementation Guide (Days 1-2)

**Version:** 1.0
**Last Updated:** December 20, 2025
**Target:** AI Voice Agent - FastAPI Backend Setup

## Document Overview

This document provides actionable, library-specific guidance for implementing the FastAPI backend for the AI Voice Agent application. All recommendations are based on 2025 best practices and active maintenance status.

---

## 1. FastAPI Backend Setup

### 1.1 Core FastAPI Libraries

#### FastAPI Framework
```bash
pip install "fastapi[standard]>=0.115.0"
```

**Purpose:** Core web framework for building the API
**Justification:** The `[standard]` extra includes uvicorn, pydantic-settings, and other recommended dependencies. FastAPI provides automatic OpenAPI documentation, built-in validation via Pydantic, and excellent async support.
**Alternatives:** Flask with async extensions (less modern), Django REST Framework (heavier, more opinionated)

#### Pydantic v2
```bash
pip install "pydantic>=2.10.0"
```

**Purpose:** Data validation and serialization
**Justification:** Comes with FastAPI but pinning version ensures consistency. Pydantic v2 offers significant performance improvements over v1 and is the standard for FastAPI applications.
**Key Features:** Type hints validation, JSON schema generation, settings management

### 1.2 API Structure and Routing

#### Recommended Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Pydantic Settings
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── agent_config.py
│   │   │   ├── calls.py
│   │   │   └── webhooks.py
│   │   └── dependencies.py  # Shared dependencies
│   ├── models/              # SQLModel database models
│   ├── schemas/             # Pydantic schemas for API
│   ├── services/            # Business logic
│   │   ├── retell.py
│   │   ├── llm.py
│   │   └── post_processing.py
│   └── core/
│       ├── database.py
│       └── security.py
├── alembic/                 # Database migrations
├── tests/
└── pyproject.toml
```

#### APIRouter Organization
```bash
# No additional installation needed - built into FastAPI
```

**Purpose:** Modular route organization
**Justification:** APIRouter allows separating routes into logical modules while maintaining a single OpenAPI schema. Improves maintainability and testability.

**Implementation Pattern:**
```python
# app/api/routes/calls.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/call", tags=["calls"])

@router.post("/trigger")
async def trigger_call(...):
    pass
```

### 1.3 Middleware Recommendations

#### CORS Middleware
```bash
# Built into FastAPI
from fastapi.middleware.cors import CORSMiddleware
```

**Purpose:** Handle Cross-Origin Resource Sharing for React frontend
**Justification:** Essential for development and production when frontend is on different domain/port. Built-in solution is production-ready.

**Configuration:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Timing Middleware (Optional but Recommended)
```bash
pip install asgi-correlation-id>=4.3.0
```

**Purpose:** Request ID tracking and timing
**Justification:** Helps with debugging and monitoring. Adds correlation IDs to logs for tracking requests across services.

#### Security Headers
```bash
pip install secure>=0.3.0
```

**Purpose:** Add security headers to responses
**Justification:** Production-ready security headers (CSP, X-Frame-Options, etc.) with minimal configuration.

---

## 2. Database Integration (Supabase/PostgreSQL)

### 2.1 ORM Selection - SQLModel (Recommended)

```bash
pip install sqlmodel>=0.0.22
```

**Purpose:** Combine SQLAlchemy and Pydantic for database models
**Justification:** Created by FastAPI's author specifically for FastAPI applications. Single class definition serves as both database model and Pydantic schema. Reduces code duplication and ensures type safety throughout the stack.

**Key Benefits:**
- Same models for DB and API validation
- Built on SQLAlchemy (mature, production-ready)
- Native FastAPI integration
- Type hints work seamlessly

**Alternatives:**
- **SQLAlchemy 2.0** (more verbose but more control) - `pip install sqlalchemy>=2.0.0`
- **Tortoise ORM** (Django-like async ORM) - Less mature, smaller community

### 2.2 Database Driver

```bash
pip install psycopg2-binary>=2.9.9  # For development
pip install psycopg[binary,pool]>=3.2.0  # For production (psycopg3)
```

**Purpose:** PostgreSQL database adapter
**Justification:** psycopg2-binary is perfect for development. For production, psycopg3 offers better async support and performance.

**Note:** Use `psycopg2-binary` for development/testing, switch to `psycopg[binary,pool]` for production deployment.

### 2.3 Async Database Support

```bash
pip install asyncpg>=0.29.0
```

**Purpose:** Async PostgreSQL driver
**Justification:** Best performance for async FastAPI applications. Native async/await support, faster than psycopg for high-concurrency scenarios.

**Usage with SQLModel:**
```python
from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine("postgresql+asyncpg://...")
```

### 2.4 Migration Tools - Alembic

```bash
pip install alembic>=1.14.0
```

**Purpose:** Database schema migrations
**Justification:** Industry standard for SQLAlchemy-based projects. Version control for database schema changes. Auto-generates migrations from SQLModel model changes.

**Setup:**
```bash
alembic init alembic
```

**Best Practices:**
- Never use `Base.metadata.create_all()` in production
- Use Alembic exclusively after initial migration
- Set `target_metadata = SQLModel.metadata` in `env.py`
- Store connection string in environment variables

### 2.5 Supabase Python Client

```bash
pip install supabase>=2.9.0
```

**Purpose:** Interact with Supabase services (Auth, Storage, Realtime)
**Justification:** While SQLAlchemy handles database queries, Supabase client provides access to authentication, file storage, and real-time subscriptions if needed.

**Note:** For this project, primarily using direct PostgreSQL connection via SQLModel. Supabase client is optional unless using Supabase Auth.

### 2.6 Connection Pooling

```bash
# Built into SQLAlchemy - configuration only
```

**Purpose:** Manage database connection lifecycle
**Justification:** Essential for production performance. SQLAlchemy's built-in pooling is production-ready.

**Configuration for Supabase:**
```python
from sqlalchemy.pool import NullPool  # For serverless
from sqlalchemy.ext.asyncio import create_async_engine

# Transaction mode (port 6543) with NullPool for serverless
engine = create_async_engine(
    database_url,
    poolclass=NullPool,  # Recommended for Supabase serverless
    echo=True  # Disable in production
)

# Or for stationary servers (direct connection):
engine = create_async_engine(
    database_url,
    pool_size=20,  # Max permanent connections
    max_overflow=15,  # Additional temporary connections
    pool_pre_ping=True  # Verify connections before use
)
```

**Key Settings:**
- Use `NullPool` for Supabase transaction mode (port 6543)
- Limit to 40% of available connections with REST client active
- Can increase to 80% if only using direct SQL connection

### 2.7 Query Optimization

```bash
# No additional libraries - use SQLModel/SQLAlchemy features
```

**Tools:**
- **Eager Loading:** `selectinload()`, `joinedload()` to prevent N+1 queries
- **Indexes:** Define in SQLModel with `Field(index=True)`
- **Query Debugging:** Enable SQLAlchemy echo for development

---

## 3. Retell AI Integration

### 3.1 HTTP Client Library - HTTPX (Recommended)

```bash
pip install httpx>=0.28.0
```

**Purpose:** Async HTTP client for Retell AI API calls
**Justification:** Modern, async-first HTTP client with HTTP/2 support. Both sync and async APIs. Better integration with FastAPI than requests. Official Retell SDK uses httpx under the hood.

**Key Features:**
- Async/await native support
- HTTP/2 support for better performance
- Connection pooling built-in
- Same API as requests (easy migration)

**Alternatives:**
- **aiohttp** (faster for extreme concurrency, but async-only) - `pip install aiohttp>=3.10.0`
- **requests** (sync-only, legacy) - Not recommended for FastAPI async applications

### 3.2 Retell AI Official SDK

```bash
pip install retell-sdk>=4.3.0
```

**Purpose:** Official Python SDK for Retell AI
**Justification:** Provides typed interfaces, automatic retries, webhook signature verification, and both sync/async clients. Highly recommended over manual API calls.

**Key Features:**
- Async support with httpx backend
- TypedDict support for webhook payloads
- Built-in webhook signature verification
- Automatic retries and error handling

**Basic Usage:**
```python
from retell import Retell
client = Retell(api_key=settings.retell_api_key)

# Async client
from retell import AsyncRetell
async_client = AsyncRetell(api_key=settings.retell_api_key)
```

### 3.3 Webhook Handling

#### Webhook Signature Verification
```bash
# Built into retell-sdk
from retell.webhook import verify_signature
```

**Purpose:** Verify webhook authenticity
**Justification:** Security best practice. Ensures webhooks are actually from Retell AI.

**Implementation:**
```python
@router.post("/webhook/retell")
async def retell_webhook(
    request: Request,
    x_retell_signature: str = Header(...)
):
    body = await request.body()
    if not verify_signature(body, x_retell_signature, settings.retell_api_key):
        raise HTTPException(status_code=403, detail="Invalid signature")
    # Process webhook...
```

#### Background Task Processing
```bash
# Built into FastAPI
from fastapi import BackgroundTasks
```

**Purpose:** Process webhooks asynchronously
**Justification:** Webhooks have 10-second timeout with 3 retries. Acknowledge immediately, process heavy work in background.

**Pattern:**
```python
@router.post("/webhook/retell")
async def retell_webhook(background_tasks: BackgroundTasks, payload: dict):
    background_tasks.add_task(process_transcript, payload)
    return {"status": "accepted"}  # Return within 3 seconds
```

### 3.4 Real-time Communication

#### Server-Sent Events (SSE) - For Call Status Updates
```bash
pip install sse-starlette>=2.1.0
```

**Purpose:** Push call status updates to frontend
**Justification:** Lightweight alternative to WebSockets for one-way server-to-client communication. Perfect for status updates.

**Alternatives:**
- **WebSockets** with `websockets>=13.0` - For bidirectional communication (overkill for this use case)
- **Polling** - Simpler but less efficient

#### Task Queue for Heavy Processing (Optional)
```bash
pip install celery>=5.4.0
pip install redis>=5.0.0  # For Celery broker
```

**Purpose:** Offload LLM post-processing to background workers
**Justification:** If post-processing takes >10 seconds, use Celery to avoid webhook timeouts.

**Note:** Likely not needed for Day 1-2. Start with FastAPI BackgroundTasks, migrate to Celery if needed.

---

## 4. Post-Processing & LLM Integration

### 4.1 OpenAI API Client

```bash
pip install openai>=1.57.0
```

**Purpose:** Call OpenAI API for transcript post-processing
**Justification:** Official SDK with async support. Used for extracting structured data from call transcripts.

**Usage:**
```python
from openai import AsyncOpenAI
client = AsyncOpenAI(api_key=settings.openai_api_key)

response = await client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": f"Extract data: {transcript}"}],
    response_format={"type": "json_object"}
)
```

### 4.2 Anthropic API Client

```bash
pip install anthropic>=0.42.0
```

**Purpose:** Call Claude API for transcript analysis
**Justification:** Alternative to OpenAI, excellent for structured data extraction. Async support built-in.

**Usage:**
```python
from anthropic import AsyncAnthropic
client = AsyncAnthropic(api_key=settings.anthropic_api_key)

response = await client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1024
)
```

### 4.3 JSON Schema Validation

#### Pydantic for Schema Definition
```bash
# Already installed with FastAPI
```

**Purpose:** Define and validate structured data schemas
**Justification:** Already part of the stack. Use for defining expected output structure for each scenario.

**Pattern:**
```python
from pydantic import BaseModel, Field

class CheckInData(BaseModel):
    call_outcome: str = Field(..., description="Call result")
    driver_status: str = Field(..., description="In-Transit or Arrived")
    location: str | None = None
    eta: str | None = None
    delays: str | None = None
    pod_acknowledged: bool = False
```

#### JSON Schema Generation
```bash
# Built into Pydantic
```

**Purpose:** Generate JSON schemas for LLM function calling
**Justification:** Pydantic v2 can generate JSON schemas compatible with OpenAI function calling and structured outputs.

```python
schema = CheckInData.model_json_schema()
# Use in OpenAI function calling or prompt
```

### 4.4 LLM Prompt Management

#### LiteLLM (Optional - Multi-Provider Abstraction)
```bash
pip install litellm>=1.54.0
```

**Purpose:** Unified interface for OpenAI, Anthropic, and other LLM providers
**Justification:** Allows switching between providers without code changes. Useful if testing different models for extraction quality.

**Alternatives:** Just use official SDKs directly (simpler, more control)

### 4.5 Instructor for Structured Outputs

```bash
pip install instructor>=1.7.0
```

**Purpose:** Get structured Pydantic objects from LLMs
**Justification:** Wraps OpenAI/Anthropic clients to automatically return validated Pydantic models. Reduces boilerplate for structured extraction.

**Usage:**
```python
import instructor
from openai import AsyncOpenAI

client = instructor.from_openai(AsyncOpenAI())

result = await client.chat.completions.create(
    model="gpt-4o",
    response_model=CheckInData,
    messages=[{"role": "user", "content": transcript}]
)
# result is automatically a CheckInData instance
```

**Alternatives:** Manual JSON parsing with Pydantic validation (more explicit)

---

## 5. Authentication & Security

### 5.1 JWT Handling - PyJWT (2025 Recommendation)

```bash
pip install pyjwt>=2.10.0
pip install cryptography>=44.0.0  # For RSA/ECDSA algorithms
```

**Purpose:** Create and verify JWT tokens
**Justification:** **IMPORTANT:** FastAPI documentation now recommends PyJWT over python-jose. python-jose is abandoned and incompatible with Python 3.10+. PyJWT is actively maintained, more secure, and lightweight.

**Migration Note:** If following older tutorials using python-jose:
- Replace `from jose import jwt, JWTError` with `import jwt` and `from jwt.exceptions import InvalidTokenError`
- API is nearly identical

**Usage:**
```python
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### 5.2 Password Hashing

```bash
pip install passlib[bcrypt]>=1.7.4
```

**Purpose:** Hash and verify passwords
**Justification:** Industry standard. bcrypt algorithm recommended for password storage.

**Usage:**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed = pwd_context.hash("plain_password")
is_valid = pwd_context.verify("plain_password", hashed)
```

### 5.3 Environment Variable Management - Pydantic Settings

```bash
pip install pydantic-settings>=2.7.0
```

**Purpose:** Type-safe environment variable loading
**Justification:** Validates environment variables at startup. Supports .env files. Integrates perfectly with FastAPI.

**Configuration Pattern:**
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # Database
    database_url: str

    # APIs
    retell_api_key: str
    openai_api_key: str
    anthropic_api_key: str | None = None

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

@lru_cache
def get_settings():
    return Settings()
```

**Best Practice:** Use `@lru_cache` to load settings only once (performance optimization).

### 5.4 API Key Security

#### Python-dotenv (Included with pydantic-settings)
```bash
# Automatically installed with pydantic-settings
```

**Purpose:** Load .env files
**Justification:** Already included with pydantic-settings. Ensures secrets never committed to git.

**.env.example:**
```
DATABASE_URL=postgresql://user:pass@localhost/dbname
RETELL_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
SECRET_KEY=your_secret_key_here
```

#### Secrets Management (Production)
```bash
# No library needed - use environment variables
```

**Options:**
- Docker secrets
- Kubernetes secrets
- Cloud provider secret managers (AWS Secrets Manager, GCP Secret Manager)
- **HashiCorp Vault** - `pip install hvac>=2.3.0` (enterprise-grade)

**Recommendation:** Start with .env for development, use cloud secrets in production.

---

## 6. Testing & Quality

### 6.1 Testing Framework - Pytest

```bash
pip install pytest>=8.3.0
pip install pytest-asyncio>=0.24.0  # For async tests
pip install pytest-cov>=6.0.0       # Coverage reporting
```

**Purpose:** Test framework for backend
**Justification:** Industry standard for Python testing. Excellent async support with pytest-asyncio. FastAPI documentation uses pytest exclusively.

**Basic Test Structure:**
```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_agent_config():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/agent-config", json={...})
        assert response.status_code == 200
```

### 6.2 Test Client for FastAPI

```bash
# Built into FastAPI - uses httpx under the hood
from fastapi.testclient import TestClient  # Sync
from httpx import AsyncClient  # Async (recommended)
```

**Purpose:** Simulate HTTP requests to FastAPI app
**Justification:** No need to run server. Tests execute in milliseconds.

**Recommendation:** Use `httpx.AsyncClient` for async tests (more realistic), `TestClient` for simple sync tests.

### 6.3 Database Testing

```bash
pip install pytest-postgresql>=6.1.0  # Managed PostgreSQL for tests
```

**Purpose:** Spin up temporary PostgreSQL databases for tests
**Justification:** Isolated, reproducible test database. Automatic cleanup.

**Alternative Pattern:**
```python
# Use SQLite in-memory for faster tests
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def test_db():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
```

### 6.4 Mocking External APIs

```bash
pip install respx>=0.21.0  # Mock httpx calls
pip install pytest-mock>=3.14.0  # General mocking utilities
```

**Purpose:** Mock Retell AI, OpenAI, Anthropic API calls
**Justification:** Tests shouldn't make real API calls. respx integrates seamlessly with httpx.

**Usage:**
```python
import respx
from httpx import Response

@pytest.mark.asyncio
@respx.mock
async def test_retell_call():
    respx.post("https://api.retellai.com/v1/calls").mock(
        return_value=Response(200, json={"call_id": "123"})
    )
    # Test code that calls Retell API
```

### 6.5 Code Quality Tools

#### Ruff - Linting and Formatting (2025 Standard)

```bash
pip install ruff>=0.8.0
```

**Purpose:** Fast Python linter and formatter (replaces Black, Flake8, isort, and more)
**Justification:** Written in Rust, 10-100x faster than traditional tools. Consolidates multiple tools into one. Now the recommended standard for 2025.

**Configuration in pyproject.toml:**
```toml
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
    "UP",  # pyupgrade
]

[tool.ruff.format]
quote-style = "double"
```

**Usage:**
```bash
ruff check . --fix      # Lint and auto-fix
ruff format .           # Format code
```

**Alternatives:**
- **Black** (formatting only) - `pip install black>=24.0.0` - Still valid but Ruff can replace it
- **Flake8** - Legacy, slower

#### Mypy - Type Checking

```bash
pip install mypy>=1.14.0
```

**Purpose:** Static type checker
**Justification:** Catches type errors before runtime. Essential for large projects. Works perfectly with Pydantic and SQLModel.

**Configuration:**
```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
plugins = ["pydantic.mypy"]

[[tool.mypy.overrides]]
module = "retell.*"
ignore_missing_imports = true
```

**Usage:**
```bash
mypy app/
```

**Note:** Ruff handles linting/formatting, Mypy handles type checking. Use both together for comprehensive code quality.

#### Pre-commit Hooks (Recommended)

```bash
pip install pre-commit>=4.0.0
```

**Purpose:** Run Ruff and Mypy automatically before commits
**Justification:** Ensures code quality standards before code reaches repository.

**.pre-commit-config.yaml:**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.14.0
    hooks:
      - id: mypy
```

### 6.6 Logging

#### Structlog (Recommended for Production)

```bash
pip install structlog>=24.4.0
```

**Purpose:** Structured logging with context
**Justification:** JSON logs for production. Human-readable for development. Attaches context (request IDs, user IDs) to all log entries. Excellent for distributed systems.

**Configuration:**
```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer() if production else structlog.dev.ConsoleRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()
logger.info("call_triggered", call_id="123", driver="John")
```

**Alternatives:**
- **Loguru** - `pip install loguru>=0.7.0` - Simpler, pre-configured, excellent for small-medium projects
- **Standard logging** - Built-in, less features

**Recommendation:**
- Use **Loguru** for Day 1-2 (simpler setup)
- Migrate to **Structlog** if deploying to production with log aggregation

#### Loguru (Simpler Alternative)

```bash
pip install loguru>=0.7.0
```

**Purpose:** Production-ready logging with minimal configuration
**Justification:** Pre-configured with rotation, compression, and formatting. Simpler than structlog for smaller projects.

**Usage:**
```python
from loguru import logger

logger.add("logs/app.log", rotation="500 MB", retention="10 days")
logger.info("Call triggered: {call_id}", call_id="123")
logger.bind(request_id="abc").info("Processing webhook")
```

---

## 7. Deployment & Infrastructure

### 7.1 ASGI Server - Uvicorn

```bash
pip install "uvicorn[standard]>=0.34.0"
```

**Purpose:** ASGI server to run FastAPI
**Justification:** Built for async applications. Includes uvloop and httptools for performance. Standard choice for FastAPI.

**Development:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production (with workers):**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 7.2 Process Manager - Gunicorn with Uvicorn Workers

```bash
pip install gunicorn>=23.0.0
```

**Purpose:** Production-grade process manager
**Justification:** Manages multiple Uvicorn worker processes. Handles worker crashes, load balancing, and graceful shutdowns.

**Production Command:**
```bash
gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --keep-alive 5
```

**Worker Calculation:** `(2 x CPU cores) + 1`

**Kubernetes Note:** If deploying to Kubernetes, run single Uvicorn process per container (no Gunicorn needed).

### 7.3 Docker

#### Dockerfile for FastAPI
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

#### Docker Compose for Local Development
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - RETELL_API_KEY=${RETELL_API_KEY}
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --reload --host 0.0.0.0

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ai_voice_agent
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
```

### 7.4 Environment Management

#### Poetry (Modern Dependency Management)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Purpose:** Modern Python dependency management
**Justification:** Deterministic builds, better dependency resolution than pip. Replaces requirements.txt with pyproject.toml.

**Usage:**
```bash
poetry init
poetry add fastapi sqlmodel uvicorn
poetry add --group dev pytest ruff mypy
poetry install
poetry run uvicorn app.main:app
```

**Alternatives:**
- **pip + requirements.txt** - Simple, works everywhere (good for Day 1-2)
- **pipenv** - Older alternative to Poetry

**Recommendation:** Use pip for Days 1-2, migrate to Poetry if project grows.

#### pyproject.toml Structure
```toml
[project]
name = "ai-voice-agent"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi[standard]>=0.115.0",
    "sqlmodel>=0.0.22",
    "asyncpg>=0.29.0",
    "alembic>=1.14.0",
    "httpx>=0.28.0",
    "retell-sdk>=4.3.0",
    "openai>=1.57.0",
    "pyjwt>=2.10.0",
    "cryptography>=44.0.0",
    "passlib[bcrypt]>=1.7.4",
    "pydantic-settings>=2.7.0",
    "structlog>=24.4.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=6.0.0",
    "ruff>=0.8.0",
    "mypy>=1.14.0",
    "pre-commit>=4.0.0",
]

[tool.ruff]
line-length = 100

[tool.mypy]
python_version = "3.11"
```

---

## 8. Complete Dependency List for Days 1-2

### Core Backend (Minimal for Day 1)
```bash
pip install fastapi[standard]>=0.115.0
pip install sqlmodel>=0.0.22
pip install asyncpg>=0.29.0
pip install alembic>=1.14.0
pip install httpx>=0.28.0
pip install retell-sdk>=4.3.0
pip install openai>=1.57.0
pip install pyjwt>=2.10.0
pip install cryptography>=44.0.0
pip install pydantic-settings>=2.7.0
pip install loguru>=0.7.0
```

### Development Tools
```bash
pip install pytest>=8.3.0
pip install pytest-asyncio>=0.24.0
pip install ruff>=0.8.0
pip install mypy>=1.14.0
```

### Optional but Recommended
```bash
pip install instructor>=1.7.0  # Structured LLM outputs
pip install respx>=0.21.0      # HTTP mocking for tests
pip install sse-starlette>=2.1.0  # Server-sent events
```

### requirements.txt
```
# Core
fastapi[standard]>=0.115.0
sqlmodel>=0.0.22
asyncpg>=0.29.0
alembic>=1.14.0

# HTTP & APIs
httpx>=0.28.0
retell-sdk>=4.3.0
openai>=1.57.0

# Security
pyjwt>=2.10.0
cryptography>=44.0.0
passlib[bcrypt]>=1.7.4
pydantic-settings>=2.7.0

# Logging
loguru>=0.7.0

# Server
uvicorn[standard]>=0.34.0
gunicorn>=23.0.0

# Dev Tools
pytest>=8.3.0
pytest-asyncio>=0.24.0
pytest-cov>=6.0.0
ruff>=0.8.0
mypy>=1.14.0
```

---

## 9. Day 1-2 Implementation Checklist

### Day 1: Foundation
- [ ] Initialize project structure
- [ ] Install core dependencies (FastAPI, SQLModel, Uvicorn)
- [ ] Set up Pydantic Settings for environment variables
- [ ] Create SQLModel database models (agent_configurations, test_calls, call_results)
- [ ] Initialize Alembic and create first migration
- [ ] Set up FastAPI app with CORS middleware
- [ ] Create basic API routes structure
- [ ] Test database connection with Supabase

### Day 2: Core Integration
- [ ] Implement Retell AI SDK integration
- [ ] Create webhook endpoint with signature verification
- [ ] Implement call trigger endpoint
- [ ] Set up OpenAI client for post-processing
- [ ] Create Pydantic schemas for structured data extraction
- [ ] Implement background task processing for webhooks
- [ ] Add basic logging with Loguru
- [ ] Write basic tests for endpoints
- [ ] Set up Ruff for code formatting
- [ ] Test end-to-end flow: trigger call → webhook → post-process → store results

---

## 10. Key Design Decisions

### Why SQLModel over Raw SQLAlchemy?
- **Single source of truth:** Same class for DB and API
- **Reduced boilerplate:** No duplicate Pydantic models
- **Type safety:** Full mypy support across stack
- **FastAPI integration:** Created specifically for FastAPI by same author

### Why HTTPX over Aiohttp?
- **Sync + Async:** Same API for both (more flexible)
- **HTTP/2 support:** Better performance
- **Requests compatibility:** Easier migration
- **Retell SDK uses it:** Consistency in stack

### Why PyJWT over python-jose?
- **Active maintenance:** python-jose is abandoned
- **Python 3.10+ compatibility:** python-jose broken on newer Python
- **Security:** More actively patched
- **Official FastAPI recommendation (2025)**

### Why Ruff over Black + Flake8 + isort?
- **Speed:** 10-100x faster (written in Rust)
- **Consolidation:** One tool instead of 4+
- **Better defaults:** Modern Python conventions built-in
- **Active development:** Most momentum in Python ecosystem

---

## 11. Critical Files for Implementation

Based on this implementation plan, here are the most critical files to create:

1. **backend/app/config.py** - Pydantic Settings for environment configuration
2. **backend/app/models/database.py** - SQLModel models for all database tables
3. **backend/app/main.py** - FastAPI app initialization with middleware and routers
4. **backend/app/api/routes/webhooks.py** - Retell webhook handler
5. **backend/app/services/post_processing.py** - LLM integration for transcript analysis
6. **backend/alembic/env.py** - Alembic configuration for migrations
7. **backend/.env.example** - Environment variable template
8. **backend/requirements.txt** - Dependency list
9. **backend/pyproject.toml** - Project configuration with Ruff/Mypy settings

---

## Conclusion

This document provides a complete, production-ready backend setup for Days 1-2 of the AI Voice Agent project. All library recommendations are based on:

1. **2025 best practices** (PyJWT over python-jose, Ruff over Black)
2. **Active maintenance** (avoiding abandoned projects)
3. **FastAPI ecosystem compatibility**
4. **Production readiness**

Focus on the minimal dependency set for Day 1-2, then expand with optional libraries as needed. Prioritize getting the core flow working:

**Trigger Call → Retell Webhook → Post-Process → Store → Retrieve**
