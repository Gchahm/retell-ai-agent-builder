# AI Voice Agent API

FastAPI backend for managing AI voice agent calls for logistics scenarios using Retell AI.

## Quick Start

```bash
# Install dependencies
uv sync

# Run development server
uv run fastapi dev app/main.py
```

Visit http://localhost:8000/docs for interactive API documentation.

---

## Prerequisites

- **Python 3.13+**
- **uv** package manager ([install guide](https://docs.astral.sh/uv/getting-started/installation/))

### Installing uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

---

## Development Setup

### 1. Clone and Navigate

```bash
cd /path/to/ai-voice-agent/api
```

### 2. Install Dependencies

```bash
# Install all dependencies and create virtual environment
uv sync

# This creates:
# - .venv/ directory with virtual environment
# - Installs all packages from pyproject.toml
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings (optional for MVP)
# nano .env
```

Environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQLite database path | `sqlite:///./dev.db` |
| `RETELL_API_KEY` | Retell AI API key | `your_retell_api_key_here` |
| `OPENAI_API_KEY` | OpenAI API key | `your_openai_api_key_here` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `RELOAD` | Auto-reload on changes | `true` |

### 4. Run Development Server

```bash
# Option 1: Using fastapi CLI (recommended for dev)
uv run fastapi dev app/main.py

# Option 2: Using uvicorn directly
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option 3: Activate venv first (if you prefer)
source .venv/bin/activate
fastapi dev app/main.py
```

```bash
ngrok http http://localhost:8000
```

The server will start at:
- **API Base**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## Project Structure

```
api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings management (Pydantic)
│   ├── database.py          # Database connection and session
│   │
│   ├── models/              # SQLModel database models
│   │   ├── __init__.py
│   │   ├── agent_config.py  # AgentConfig table
│   │   ├── call.py          # Call table
│   │   └── call_result.py   # CallResult table
│   │
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── agent_config.py  # AgentConfig schemas
│   │   ├── call.py          # Call schemas
│   │   └── call_result.py   # CallResult schemas
│   │
│   ├── api/                 # API layer
│   │   ├── __init__.py
│   │   ├── deps.py          # Shared dependencies (DB session)
│   │   └── routes/          # API route handlers
│   │       ├── __init__.py
│   │       ├── agent_configs.py  # Agent CRUD endpoints
│   │       ├── calls.py          # Call trigger endpoints
│   │       └── webhooks.py       # Retell webhook handler
│   │
│   └── services/            # Business logic
│       ├── __init__.py
│       ├── retell.py        # Retell AI integration
│       └── post_processing.py  # LLM post-processing
│
├── .env                     # Environment variables (gitignored)
├── .env.example             # Environment template
├── .gitignore
├── pyproject.toml           # Project dependencies and config
├── uv.lock                  # Dependency lock file
└── README.md                # This file
```

---

## API Endpoints

### System Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |

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
| POST | `/api/calls/trigger` | Trigger a new call |
| GET | `/api/calls` | List all calls (paginated) |
| GET | `/api/calls/{id}` | Get specific call details |

### Webhooks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/webhooks/retell` | Receive Retell AI webhooks |

---

## Testing the API

### Using Interactive Docs (Recommended)

1. Start the server: `uv run fastapi dev app/main.py`
2. Open http://localhost:8000/docs
3. Click "Try it out" on any endpoint
4. Fill in the request body and click "Execute"

### Using curl

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Create Agent Configuration
```bash
curl -X POST http://localhost:8000/api/agent-configs \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Check-In Agent",
    "system_prompt": "You are a helpful logistics assistant conducting driver check-ins.",
    "scenario_type": "check-in",
    "retell_settings": {
      "voice": "en-US-Neural2-A",
      "backchanneling": true,
      "filler_words": true
    }
  }'
```

#### List Agent Configurations
```bash
curl http://localhost:8000/api/agent-configs
```

#### Get Specific Agent Configuration
```bash
curl http://localhost:8000/api/agent-configs/1
```

#### Update Agent Configuration
```bash
curl -X PATCH http://localhost:8000/api/agent-configs/1 \
  -H "Content-Type: application/json" \
  -d '{
    "system_prompt": "Updated prompt text"
  }'
```

#### Trigger a Call
```bash
curl -X POST http://localhost:8000/api/calls/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "agent_config_id": 1,
    "driver_name": "John Doe",
    "phone_number": "+1234567890",
    "load_number": "LOAD-12345"
  }'
```

#### List Calls
```bash
curl http://localhost:8000/api/calls
```

### Using HTTPie (Alternative)

```bash
# Install httpie
brew install httpie  # macOS
# or
pip install httpie

# Create agent config
http POST localhost:8000/api/agent-configs \
  name="Test Agent" \
  system_prompt="You are helpful" \
  scenario_type="check-in" \
  retell_settings:='{"voice": "en-US-Neural2-A"}'

# List configs
http GET localhost:8000/api/agent-configs
```

---

## Database

### SQLite (Default)

The application uses SQLite by default for local development. The database file (`dev.db`) is created automatically when you first run the server.

#### Database Location
```
api/dev.db
```

#### View Database (Optional)

```bash
# Install sqlite3 CLI (usually pre-installed on macOS/Linux)
sqlite3 dev.db

# View tables
.tables

# View schema
.schema agent_configurations

# Query data
SELECT * FROM agent_configurations;

# Exit
.quit
```

#### Reset Database

```bash
# Delete database file
rm dev.db

# Restart server (will recreate tables)
uv run fastapi dev app/main.py
```

### Switching to PostgreSQL (Docker)

If you prefer PostgreSQL:

1. **Create `docker-compose.yml`** in the `api/` directory:

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

2. **Update `.env`**:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_voice_agent
```

3. **Install PostgreSQL driver**:

```bash
uv add asyncpg
```

4. **Start PostgreSQL**:

```bash
docker-compose up -d
```

---

## Code Quality

### Formatting

Format code with Ruff:

```bash
# Format all files
uv run ruff format .

# Check formatting without changes
uv run ruff format --check .
```

### Linting

Lint code with Ruff:

```bash
# Lint and auto-fix issues
uv run ruff check . --fix

# Check without fixing
uv run ruff check .
```

### Pre-commit Setup (Optional)

Run linting and formatting automatically before commits:

```bash
# Install pre-commit
uv add --dev pre-commit

# Install git hooks
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files
```

---

## Common Tasks

### Add New Dependency

```bash
# Add production dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Examples
uv add anthropic
uv add --dev pytest
```

### Update Dependencies

```bash
# Update all dependencies
uv sync --upgrade

# Update specific package
uv add package-name@latest
```

### Run Python Shell with Context

```bash
# Start Python shell with venv activated
uv run python

# Or activate venv first
source .venv/bin/activate
python
```

### View Installed Packages

```bash
uv pip list
```

---

## Development Workflow

### Typical Development Cycle

1. **Start the server**:
   ```bash
   uv run fastapi dev app/main.py
   ```

2. **Make code changes** - The server auto-reloads on file changes

3. **Test in browser**:
   - Interactive docs: http://localhost:8000/docs
   - Test endpoints directly

4. **Format and lint**:
   ```bash
   uv run ruff format .
   uv run ruff check . --fix
   ```

5. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

### Adding a New Endpoint

1. **Define database model** (if needed) in `app/models/`
2. **Create request/response schemas** in `app/schemas/`
3. **Add route handler** in `app/api/routes/`
4. **Include router** in `app/main.py` (if new router file)
5. **Test at** http://localhost:8000/docs

---

## Troubleshooting

### Server won't start

**Error**: `Address already in use`

**Solution**: Port 8000 is already in use. Either:
```bash
# Option 1: Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Option 2: Use different port
uv run fastapi dev app/main.py --port 8001
```

### Import errors

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**: Ensure you're in the `api/` directory and using `uv run`:
```bash
cd api/
uv run fastapi dev app/main.py
```

### Database errors

**Error**: `no such table: agent_configurations`

**Solution**: Delete and recreate database:
```bash
rm dev.db
uv run fastapi dev app/main.py
```

### uv command not found

**Solution**: Install uv or use full path:
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use python -m
python -m uv run fastapi dev app/main.py
```

### Virtual environment issues

**Solution**: Remove and recreate:
```bash
rm -rf .venv
uv sync
```

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | No | `sqlite:///./dev.db` | Database connection string |
| `RETELL_API_KEY` | For production | `mock_key` | Retell AI API key |
| `OPENAI_API_KEY` | For production | `mock_key` | OpenAI API key (for post-processing) |
| `HOST` | No | `0.0.0.0` | Server bind host |
| `PORT` | No | `8000` | Server port |
| `RELOAD` | No | `true` | Auto-reload on code changes |

---

## Next Steps

Now that the API scaffold is working:

1. **Implement Retell Integration** - Complete `app/services/retell.py`
2. **Add Webhook Processing** - Implement `app/api/routes/webhooks.py`
3. **LLM Post-Processing** - Complete `app/services/post_processing.py`
4. **Add Tests** - Create `tests/` directory with pytest
5. **Frontend Integration** - Build React UI to consume this API

---

## Useful Links

- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com
- **Retell AI SDK**: https://github.com/RetellAI/retell-python-sdk
- **uv Documentation**: https://docs.astral.sh/uv/

---

## Support

For issues or questions:
1. Check the [troubleshooting section](#troubleshooting)
2. Review API docs at http://localhost:8000/docs
3. Check logs in terminal where server is running

---

## License

[Add your license here]
