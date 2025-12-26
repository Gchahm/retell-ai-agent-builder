# AI Voice Agent API

FastAPI backend for managing AI voice agent calls for logistics scenarios using Retell AI.

## Quick Start

```bash
# 1. Install dependencies
uv sync

# 2. Start Supabase locally
supabase start

# 3. Configure environment
cp .env.example .env
```

 Edit .env with values from `supabase status`

```bash

# 4. Run database migrations
uv run alembic upgrade head

# 5. Run development server
uv run fastapi dev app/main.py
```

Visit http://localhost:8000/docs for interactive API documentation.

---

## Prerequisites

- **Python 3.13+**
- **uv** package manager ([install guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Supabase CLI** ([install guide](https://supabase.com/docs/guides/local-development/cli/getting-started))
- **Docker** (required for local Supabase)

### Installing uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### Installing Supabase CLI

```bash
# macOS
brew install supabase/tap/supabase

# Windows (scoop)
scoop bucket add supabase https://github.com/supabase/scoop-bucket.git
scoop install supabase

# npm (cross-platform)
npm install -g supabase

# Verify installation
supabase --version
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

### 3. Start Supabase Locally

```bash
# Start local Supabase (requires Docker running)
supabase start

# This starts:
# - PostgreSQL on port 54322
# - Supabase API on port 54321
# - Auth, Storage, and other services
```

After starting, you'll see output with your local credentials:

```
API URL: http://127.0.0.1:54321
anon key: eyJ...
service_role key: eyJ...
DB URL: postgresql://postgres:postgres@127.0.0.1:54322/postgres
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env
```

Edit `.env` with values from `supabase status`:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@127.0.0.1:54322/postgres` |
| `SUPABASE_URL` | Supabase API URL | `http://127.0.0.1:54321` |
| `SUPABASE_ANON_KEY` | Supabase anonymous key | From `supabase status` |
| `SUPABASE_SERVICE_KEY` | Supabase service role key | From `supabase status` |
| `RETELL_API_KEY` | Retell AI API key | From [Retell Dashboard](https://dashboard.retellai.com) |
| `WEBHOOK_BASE_URL` | Webhook URL for Retell | Use ngrok URL for local dev |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

### 5. Run Database Migrations

```bash
# Apply all pending migrations
uv run alembic upgrade head

# Verify migration status
uv run alembic current
```

### 6. Run Development Server

```bash
# Using fastapi CLI (recommended)
uv run fastapi dev app/main.py
```

For webhook testing, expose your local server with ngrok:

```bash
ngrok http 8000
# Update WEBHOOK_BASE_URL in .env with the ngrok URL
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

### Supabase (PostgreSQL)

The application uses Supabase (PostgreSQL) for the database. For local development, use the Supabase CLI which runs PostgreSQL in Docker.

#### Managing Supabase

```bash
# Start Supabase services
supabase start

# Stop Supabase services
supabase stop

# View status and credentials
supabase status

# Reset database (clears all data)
supabase db reset
```

#### Database Migrations with Alembic

Migrations are managed with Alembic. Migration files are stored in `migrations/versions/`.

```bash
# Apply all pending migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# Rollback to specific revision
uv run alembic downgrade <revision_id>

# Show current migration status
uv run alembic current

# Show migration history
uv run alembic history

# Generate new migration from model changes
uv run alembic revision --autogenerate -m "description_of_changes"
```

#### View Database (Optional)

Access the database via Supabase Studio at http://127.0.0.1:54323 or use psql:

```bash
# Connect with psql
psql postgresql://postgres:postgres@127.0.0.1:54322/postgres

# View tables
\dt

# View schema
\d calls

# Query data
SELECT * FROM calls;

# Exit
\q
```

#### Reset Database

```bash
# Option 1: Reset via Supabase (recommended)
supabase db reset

# Option 2: Rollback all migrations and re-apply
uv run alembic downgrade base
uv run alembic upgrade head
```

### Using Cloud Supabase

For production or if you prefer not to run Supabase locally:

1. Create a project at [supabase.com](https://supabase.com)
2. Get your credentials from Settings > API
3. Update `.env`:

```bash
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
SUPABASE_URL=https://[project-ref].supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
```

4. Run migrations against the cloud database:

```bash
uv run alembic upgrade head
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

### Database connection errors

**Error**: `connection refused` or `could not connect to server`

**Solution**: Ensure Supabase is running:
```bash
# Check if Supabase is running
supabase status

# Start Supabase if not running
supabase start
```

### Missing tables

**Error**: `relation "calls" does not exist`

**Solution**: Run database migrations:
```bash
uv run alembic upgrade head
```

### Migration errors

**Error**: `Target database is not up to date`

**Solution**: Check and apply pending migrations:
```bash
# Check current status
uv run alembic current

# Apply all pending migrations
uv run alembic upgrade head
```

### Supabase won't start

**Error**: `Cannot connect to the Docker daemon`

**Solution**: Ensure Docker is running:
```bash
# Start Docker Desktop (macOS/Windows)
# Or start Docker daemon (Linux)
sudo systemctl start docker

# Then retry
supabase start
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
| `DATABASE_URL` | Yes | - | PostgreSQL connection string (from Supabase) |
| `SUPABASE_URL` | Yes | - | Supabase API URL |
| `SUPABASE_ANON_KEY` | Yes | - | Supabase anonymous key (for client auth) |
| `SUPABASE_SERVICE_KEY` | Yes | - | Supabase service role key (for admin ops) |
| `RETELL_API_KEY` | Yes | - | Retell AI API key |
| `WEBHOOK_BASE_URL` | Yes | `http://localhost:8000` | Base URL for Retell webhooks |
| `DISPATCH_PHONE_NUMBER` | No | `+1234567890` | Phone for emergency transfers |
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
