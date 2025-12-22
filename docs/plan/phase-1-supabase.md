# Phase 1 Supabase Implementation Guide (Day 1)

**Version:** 1.0
**Last Updated:** December 22, 2025
**Target:** AI Voice Agent - Supabase Database Setup

## Document Overview

This document provides actionable, step-by-step guidance for setting up Supabase as the PostgreSQL database backend for the AI Voice Agent application. All recommendations follow 2025 best practices and production-ready configurations.

---

## 1. Supabase Project Setup

### 1.1 Create Supabase Project

#### Option 1: Supabase Cloud (Recommended for Development)

1. **Sign up at [supabase.com](https://supabase.com)**
   - Free tier includes: 500MB database, 1GB file storage, 2GB bandwidth
   - No credit card required for development

2. **Create New Project**
   ```
   Organization: Your organization name
   Project Name: ai-voice-agent
   Database Password: [Generate strong password - save this!]
   Region: Choose closest to your users (e.g., us-west-1, eu-central-1)
   ```

3. **Wait for Provisioning** (~2 minutes)
   - PostgreSQL 15.x instance
   - Automatic daily backups
   - Point-in-time recovery (paid plans)

#### Option 2: Self-Hosted Supabase (Production/Advanced)

```bash
# Clone Supabase
git clone --depth 1 https://github.com/supabase/supabase
cd supabase/docker

# Copy environment file
cp .env.example .env

# Edit .env with your secrets
# POSTGRES_PASSWORD, JWT_SECRET, ANON_KEY, SERVICE_ROLE_KEY

# Start Supabase
docker compose up -d

# Access:
# Studio: http://localhost:3000
# API: http://localhost:8000
# PostgreSQL: localhost:5432
```

**Recommendation:** Use Supabase Cloud for Days 1-4, migrate to self-hosted only if needed for production requirements.

### 1.2 Retrieve Connection Details

Navigate to **Project Settings → Database** to find:

#### Connection Strings

**1. Transaction Mode (Recommended for Serverless/Short Connections)**
```
postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres
```
- **Port:** 6543
- **Use Case:** Serverless functions, edge functions, connection pooling
- **Max Connections:** ~100 (shared pool)
- **Best for:** FastAPI with NullPool

**2. Session Mode (Recommended for Long-Running Applications)**
```
postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-us-west-1.pooler.supabase.com:5432/postgres
```
- **Port:** 5432
- **Use Case:** Traditional servers, long-lived connections
- **Max Connections:** ~80 (direct connections)
- **Best for:** FastAPI with SQLAlchemy connection pool

**3. Direct Connection (Not Recommended - No Pooling)**
```
postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
```
- **Port:** 5432
- **Use Case:** Migrations, one-off scripts
- **Max Connections:** Limited (reserved for pooler)

#### API Keys

**Anon (Public) Key:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
- For client-side applications
- Respects Row Level Security (RLS)
- Safe to expose in frontend

**Service Role Key:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
- **NEVER expose in frontend**
- Bypasses RLS
- Full admin access
- Use only in backend

#### Project API URL
```
https://[PROJECT_REF].supabase.co
```

### 1.3 Environment Configuration

Create **backend/.env** file:

```bash
# Supabase Connection (Transaction Mode - Recommended)
DATABASE_URL=postgresql+asyncpg://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres

# Supabase API (Optional - for Auth/Storage features)
SUPABASE_URL=https://[PROJECT_REF].supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Application Secrets
SECRET_KEY=your-secret-key-for-jwt-signing-min-32-chars
RETELL_API_KEY=your-retell-api-key
OPENAI_API_KEY=your-openai-api-key
```

**Security Notes:**
- Add `.env` to `.gitignore`
- Use `postgresql+asyncpg://` for SQLAlchemy async engine
- Transaction mode (6543) with NullPool prevents connection exhaustion

---

## 2. Database Schema Design

### 2.1 Core Tables

Navigate to **SQL Editor** in Supabase Studio and run the following migrations:

#### Table 1: agent_configurations

```sql
-- Agent Configuration Table
CREATE TABLE agent_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    system_prompt TEXT NOT NULL,
    scenario_type VARCHAR(50) NOT NULL CHECK (scenario_type IN ('check-in', 'emergency')),

    -- Retell AI Settings (JSONB for flexibility)
    retell_settings JSONB DEFAULT '{
        "voice_id": "default",
        "backchannel_enabled": true,
        "filler_words_enabled": true,
        "interruption_sensitivity": "high",
        "response_latency_ms": 200
    }'::jsonb,

    -- Conversation Configuration
    conversation_config JSONB DEFAULT '{
        "max_retries": 3,
        "timeout_seconds": 300,
        "emergency_keywords": ["accident", "blowout", "breakdown", "injured"]
    }'::jsonb,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT true
);

-- Indexes
CREATE INDEX idx_agent_config_scenario ON agent_configurations(scenario_type);
CREATE INDEX idx_agent_config_active ON agent_configurations(is_active);
CREATE INDEX idx_agent_config_created ON agent_configurations(created_at DESC);

-- Updated timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_agent_config_updated_at
    BEFORE UPDATE ON agent_configurations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments
COMMENT ON TABLE agent_configurations IS 'AI agent configurations with prompts and Retell settings';
COMMENT ON COLUMN agent_configurations.retell_settings IS 'Retell AI voice settings (backchanneling, filler words, etc.)';
COMMENT ON COLUMN agent_configurations.conversation_config IS 'Conversation flow settings (retries, timeouts, keywords)';
```

#### Table 2: test_calls

```sql
-- Test Calls Table
CREATE TABLE test_calls (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Foreign Keys
    agent_config_id UUID NOT NULL REFERENCES agent_configurations(id) ON DELETE CASCADE,

    -- Driver Information
    driver_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    load_number VARCHAR(100) NOT NULL,

    -- Retell Call Details
    retell_call_id VARCHAR(255) UNIQUE,
    retell_agent_id VARCHAR(255),

    -- Call Status
    status VARCHAR(50) NOT NULL DEFAULT 'initiated'
        CHECK (status IN ('initiated', 'ringing', 'in_progress', 'completed', 'failed', 'no_answer', 'busy')),

    -- Call Metadata
    duration_seconds INTEGER,
    started_at TIMESTAMPTZ,
    ended_at TIMESTAMPTZ,

    -- Error Handling
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_test_calls_agent_config ON test_calls(agent_config_id);
CREATE INDEX idx_test_calls_status ON test_calls(status);
CREATE INDEX idx_test_calls_retell_id ON test_calls(retell_call_id);
CREATE INDEX idx_test_calls_created ON test_calls(created_at DESC);
CREATE INDEX idx_test_calls_phone ON test_calls(phone_number);

-- Updated timestamp trigger
CREATE TRIGGER update_test_calls_updated_at
    BEFORE UPDATE ON test_calls
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments
COMMENT ON TABLE test_calls IS 'Test call records with driver info and Retell call IDs';
COMMENT ON COLUMN test_calls.retell_call_id IS 'Unique call ID from Retell AI API';
COMMENT ON COLUMN test_calls.status IS 'Current call status (initiated, in_progress, completed, failed)';
```

#### Table 3: call_results

```sql
-- Call Results Table
CREATE TABLE call_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Foreign Key
    call_id UUID NOT NULL REFERENCES test_calls(id) ON DELETE CASCADE,

    -- Transcript Data
    transcript TEXT NOT NULL,
    transcript_object JSONB, -- Full Retell transcript with timestamps

    -- Structured Data (Varies by Scenario)
    structured_data JSONB NOT NULL,

    -- Extraction Metadata
    extraction_model VARCHAR(100), -- e.g., "gpt-4o", "claude-3-5-sonnet"
    extraction_confidence DECIMAL(3, 2), -- 0.00 to 1.00
    extraction_timestamp TIMESTAMPTZ DEFAULT NOW(),

    -- Call Analytics
    sentiment_score DECIMAL(3, 2), -- -1.00 (negative) to 1.00 (positive)
    call_quality_score DECIMAL(3, 2), -- 0.00 to 1.00

    -- Audio Recording
    recording_url TEXT,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_call_results_call_id ON call_results(call_id);
CREATE INDEX idx_call_results_created ON call_results(created_at DESC);
CREATE INDEX idx_call_results_structured_data ON call_results USING GIN(structured_data);

-- Comments
COMMENT ON TABLE call_results IS 'Call transcripts and extracted structured data';
COMMENT ON COLUMN call_results.structured_data IS 'Extracted key-value pairs (varies by scenario: check-in vs emergency)';
COMMENT ON COLUMN call_results.transcript_object IS 'Full Retell transcript with timestamps and speaker labels';
```

#### Example Structured Data Schemas

**Check-in Scenario:**
```json
{
  "call_outcome": "successful",
  "driver_status": "In-Transit",
  "current_location": "Interstate 95, near Baltimore",
  "eta": "2025-12-23T14:30:00Z",
  "delays": "Heavy traffic, approximately 30 minutes delay",
  "pod_acknowledged": true,
  "gps_discrepancy": false,
  "additional_notes": "Driver mentioned road construction"
}
```

**Emergency Scenario:**
```json
{
  "call_outcome": "emergency_detected",
  "emergency_type": "vehicle_breakdown",
  "emergency_keywords_detected": ["blowout", "tire"],
  "safety_status": "safe",
  "injury_status": "no_injuries",
  "current_location": "Mile marker 127, I-95 South, pulled over on shoulder",
  "assistance_requested": "tow_truck",
  "escalation_status": "dispatched_to_human",
  "escalation_timestamp": "2025-12-22T10:15:32Z"
}
```

### 2.2 Create Tables via SQL Editor

1. **Navigate to SQL Editor** in Supabase Studio
2. **Create a new query**
3. **Paste and execute** each table creation script sequentially
4. **Verify tables** in Table Editor

### 2.3 Alternative: Alembic Migrations (Recommended for Production)

If using Alembic for version control:

**backend/alembic/versions/001_initial_schema.py**
```python
"""Initial schema

Revision ID: 001
Create Date: 2025-12-22
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMPTZ

def upgrade():
    # Create agent_configurations
    op.create_table(
        'agent_configurations',
        sa.Column('id', UUID, primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('system_prompt', sa.Text, nullable=False),
        sa.Column('scenario_type', sa.String(50), nullable=False),
        sa.Column('retell_settings', JSONB, server_default=sa.text("'{}'::jsonb")),
        sa.Column('conversation_config', JSONB, server_default=sa.text("'{}'::jsonb")),
        sa.Column('created_at', TIMESTAMPTZ, server_default=sa.text('NOW()')),
        sa.Column('updated_at', TIMESTAMPTZ, server_default=sa.text('NOW()')),
        sa.Column('created_by', UUID, nullable=True),
        sa.Column('is_active', sa.Boolean, server_default=sa.text('true')),
    )
    # Add indexes...
    # (See full implementation in SQL above)

def downgrade():
    op.drop_table('call_results')
    op.drop_table('test_calls')
    op.drop_table('agent_configurations')
```

---

## 3. Connection Configuration with FastAPI

### 3.1 SQLAlchemy Engine Setup

**backend/app/core/database.py**

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel
from app.config import get_settings

settings = get_settings()

# Engine Configuration for Supabase Transaction Mode
engine = create_async_engine(
    settings.database_url,

    # Use NullPool for Supabase Transaction Mode (port 6543)
    poolclass=NullPool,

    # Echo SQL queries in development (disable in production)
    echo=settings.environment == "development",

    # Connection arguments for PostgreSQL
    connect_args={
        "server_settings": {
            "application_name": "ai-voice-agent",
            "jit": "off",  # Disable JIT for faster query planning
        },
        "command_timeout": 60,  # Timeout for long queries
        "timeout": 10,  # Connection timeout
    },
)

# Session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncSession:
    """Dependency for getting async database session."""
    async with async_session_maker() as session:
        yield session

async def init_db():
    """Create all tables (development only - use Alembic in production)."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

### 3.2 Alternative: Session Mode with Connection Pool

If using Session Mode (port 5432) for traditional server deployment:

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import QueuePool

engine = create_async_engine(
    settings.database_url,  # Port 5432

    # Connection pooling configuration
    poolclass=QueuePool,
    pool_size=20,  # Permanent connections
    max_overflow=10,  # Additional temporary connections
    pool_pre_ping=True,  # Verify connection health before use
    pool_recycle=3600,  # Recycle connections after 1 hour

    # Same connect_args as above
    connect_args={...},
)
```

**Supabase Connection Limits:**
- Free Tier: 60 connections
- Pro Tier: 200 connections
- If using both Supabase client and direct SQL: limit to 40% of available connections
- If using only direct SQL: can use up to 80% of connections

### 3.3 FastAPI Integration

**backend/app/main.py**

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import init_db, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for FastAPI."""
    # Startup
    await init_db()  # Only in development - use Alembic in production
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(
    title="AI Voice Agent API",
    version="1.0.0",
    lifespan=lifespan,
)
```

---

## 4. Row Level Security (RLS) Policies

### 4.1 Enable RLS on Tables

```sql
-- Enable RLS
ALTER TABLE agent_configurations ENABLE ROW LEVEL SECURITY;
ALTER TABLE test_calls ENABLE ROW LEVEL SECURITY;
ALTER TABLE call_results ENABLE ROW LEVEL SECURITY;
```

### 4.2 Create Policies

#### Policy 1: Service Role Full Access (Backend API)

```sql
-- Service role (backend) has full access
CREATE POLICY "Service role full access" ON agent_configurations
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Service role full access" ON test_calls
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Service role full access" ON call_results
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);
```

#### Policy 2: Authenticated Users (Optional - If Using Supabase Auth)

```sql
-- Authenticated users can read their own data
CREATE POLICY "Users can view own configs" ON agent_configurations
    FOR SELECT
    TO authenticated
    USING (created_by = auth.uid());

-- Authenticated users can create configs
CREATE POLICY "Users can create configs" ON agent_configurations
    FOR INSERT
    TO authenticated
    WITH CHECK (created_by = auth.uid());
```

#### Policy 3: Anonymous Access (Optional - Public Dashboard)

```sql
-- Public read-only access to call results (if building public dashboard)
CREATE POLICY "Public read access" ON call_results
    FOR SELECT
    TO anon
    USING (true);
```

### 4.3 Best Practices

**For This Project (Backend-Only API):**
- Use **Service Role Key** in backend only
- All database operations bypass RLS
- No need for complex RLS policies

**For Future Frontend Integration:**
- Enable Supabase Auth
- Use RLS policies to restrict access per user
- Frontend uses **Anon Key** with RLS enforcement

---

## 5. Database Optimization

### 5.1 Indexes (Already Created Above)

Verify indexes exist:

```sql
-- Check indexes
SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
```

### 5.2 JSONB Indexing for Fast Queries

```sql
-- GIN index for structured_data queries
CREATE INDEX idx_call_results_structured_data_gin
    ON call_results USING GIN(structured_data);

-- Example queries that benefit:
SELECT * FROM call_results
WHERE structured_data @> '{"call_outcome": "successful"}';

SELECT * FROM call_results
WHERE structured_data ? 'emergency_type';
```

### 5.3 Partitioning (Optional - For High Volume)

If expecting millions of call records:

```sql
-- Partition by created_at month
CREATE TABLE call_results_2025_12 PARTITION OF call_results
    FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');

CREATE TABLE call_results_2026_01 PARTITION OF call_results
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```

### 5.4 Query Performance Monitoring

Enable **pg_stat_statements** extension:

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- View slowest queries
SELECT
    mean_exec_time,
    calls,
    query
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

---

## 6. Backup and Recovery

### 6.1 Automatic Backups (Supabase Cloud)

**Free Tier:**
- Daily backups retained for 7 days
- Point-in-time recovery: Not available

**Pro Tier:**
- Daily backups retained for 30 days
- Point-in-time recovery: 7 days

**Configuration:** Project Settings → Database → Backups

### 6.2 Manual Backups

```bash
# Using pg_dump
pg_dump -h db.[PROJECT_REF].supabase.co \
        -U postgres \
        -d postgres \
        -F c \
        -f backup_$(date +%Y%m%d).dump

# Restore
pg_restore -h db.[PROJECT_REF].supabase.co \
           -U postgres \
           -d postgres \
           -c \
           backup_20251222.dump
```

### 6.3 Export to CSV (Supabase Studio)

1. Navigate to **Table Editor**
2. Select table
3. Click **Export** → CSV/Excel

---

## 7. Monitoring and Observability

### 7.1 Database Dashboard

Navigate to **Database → Monitoring** to view:
- Connection count
- Query performance
- Table sizes
- Cache hit ratio

### 7.2 Slow Query Logging

```sql
-- Enable slow query logging (queries > 1 second)
ALTER DATABASE postgres SET log_min_duration_statement = 1000;

-- View logs in Dashboard → Logs
```

### 7.3 Connection Monitoring

```sql
-- Check active connections
SELECT
    datname,
    usename,
    application_name,
    state,
    COUNT(*)
FROM pg_stat_activity
GROUP BY datname, usename, application_name, state;

-- Kill idle connections (if needed)
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
    AND state_change < NOW() - INTERVAL '10 minutes';
```

---

## 8. Security Best Practices

### 8.1 SSL/TLS Enforcement

Supabase enforces SSL by default. Verify in connection strings:
```
postgresql://...?sslmode=require
```

### 8.2 API Key Rotation

**Dashboard:** Project Settings → API → Regenerate Keys

**After rotation:**
1. Update `.env` file
2. Redeploy backend
3. Update frontend (if using Supabase client)

### 8.3 Database Firewall (Optional)

**Pro/Enterprise Only:** Restrict database access by IP whitelist

**Configuration:** Project Settings → Database → Network Restrictions

### 8.4 Secret Management

**Never commit:**
- `.env` files
- `DATABASE_URL` with passwords
- `SUPABASE_SERVICE_ROLE_KEY`

**Production secrets storage:**
- GitHub Secrets (for CI/CD)
- AWS Secrets Manager
- Kubernetes Secrets
- HashiCorp Vault

---

## 9. Testing Database Setup

### 9.1 Connection Test Script

**backend/test_connection.py**

```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def test_connection():
    engine = create_async_engine("postgresql+asyncpg://...")

    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT version()"))
        version = result.scalar()
        print(f"✓ Connected to PostgreSQL: {version}")

        # Test table access
        result = await conn.execute(text("SELECT COUNT(*) FROM agent_configurations"))
        count = result.scalar()
        print(f"✓ Found {count} agent configurations")

    await engine.dispose()
    print("✓ Connection closed successfully")

if __name__ == "__main__":
    asyncio.run(test_connection())
```

Run:
```bash
python backend/test_connection.py
```

### 9.2 Seed Data for Testing

```sql
-- Insert test agent configuration
INSERT INTO agent_configurations (name, system_prompt, scenario_type, retell_settings)
VALUES (
    'Test Check-In Agent',
    'You are a friendly logistics coordinator calling to check on driver status...',
    'check-in',
    '{"voice_id": "default", "backchannel_enabled": true, "interruption_sensitivity": "medium"}'::jsonb
);

-- Insert test call
INSERT INTO test_calls (agent_config_id, driver_name, phone_number, load_number, status)
VALUES (
    (SELECT id FROM agent_configurations LIMIT 1),
    'John Smith',
    '+15555551234',
    'LOAD-2025-001',
    'completed'
);
```

---

## 10. Migration from Local PostgreSQL to Supabase

If you started with local PostgreSQL and want to migrate:

### Step 1: Export Schema
```bash
pg_dump -h localhost -U postgres -d ai_voice_agent --schema-only > schema.sql
```

### Step 2: Export Data
```bash
pg_dump -h localhost -U postgres -d ai_voice_agent --data-only > data.sql
```

### Step 3: Import to Supabase
```bash
psql -h db.[PROJECT_REF].supabase.co -U postgres -d postgres -f schema.sql
psql -h db.[PROJECT_REF].supabase.co -U postgres -d postgres -f data.sql
```

---

## 11. Troubleshooting

### Issue 1: Connection Refused

**Error:** `could not connect to server`

**Solutions:**
1. Check DATABASE_URL format: `postgresql+asyncpg://...`
2. Verify port: 6543 (transaction) or 5432 (session)
3. Check IP allowlist (if using network restrictions)
4. Verify project is not paused (Supabase free tier auto-pauses after 7 days inactivity)

### Issue 2: Too Many Connections

**Error:** `FATAL: remaining connection slots are reserved`

**Solutions:**
1. Use Transaction Mode (port 6543) with NullPool
2. Reduce pool_size in SQLAlchemy
3. Close idle connections:
```sql
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle';
```

### Issue 3: Slow Queries

**Solutions:**
1. Add indexes to frequently queried columns
2. Use EXPLAIN ANALYZE to diagnose:
```sql
EXPLAIN ANALYZE SELECT * FROM test_calls WHERE phone_number = '+15555551234';
```
3. Check cache hit ratio:
```sql
SELECT
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit) as heap_hit,
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio
FROM pg_statio_user_tables;
```

### Issue 4: Alembic Migration Failures

**Error:** `Target database is not up to date`

**Solutions:**
1. Check current revision:
```bash
alembic current
```
2. Generate migration from models:
```bash
alembic revision --autogenerate -m "Add new column"
```
3. Upgrade to latest:
```bash
alembic upgrade head
```

---

## 12. Day 1 Checklist

- [ ] Create Supabase project on supabase.com
- [ ] Save connection string (Transaction Mode - port 6543)
- [ ] Save API keys (Anon Key, Service Role Key)
- [ ] Create `.env` file with all credentials
- [ ] Add `.env` to `.gitignore`
- [ ] Create `agent_configurations` table with indexes
- [ ] Create `test_calls` table with foreign keys
- [ ] Create `call_results` table with JSONB columns
- [ ] Enable Row Level Security (RLS)
- [ ] Create service role policies
- [ ] Test database connection with `test_connection.py`
- [ ] Insert seed data for testing
- [ ] Configure SQLAlchemy engine in `database.py`
- [ ] Verify tables in Supabase Table Editor

---

## 13. Key Configuration Summary

### Recommended Setup for This Project

| Setting | Value | Reason |
|---------|-------|--------|
| **Connection Mode** | Transaction (port 6543) | Better for serverless/short-lived connections |
| **Pool Class** | NullPool | Prevents connection exhaustion with Supabase pooler |
| **RLS** | Enabled with service role bypass | Security best practice |
| **Indexes** | GIN on JSONB, B-tree on FKs | Fast queries on structured data |
| **Backups** | Automatic daily (Supabase) | Built-in disaster recovery |
| **Migrations** | Alembic (recommended) | Version control for schema changes |

### Connection String Format

```python
# For asyncpg (recommended)
DATABASE_URL = "postgresql+asyncpg://postgres.[REF]:[PASS]@[HOST]:6543/postgres"

# For psycopg3 (alternative)
DATABASE_URL = "postgresql+psycopg://postgres.[REF]:[PASS]@[HOST]:6543/postgres"
```

---

## Conclusion

This guide provides a complete, production-ready Supabase setup for the AI Voice Agent project. Key takeaways:

1. **Use Transaction Mode (6543) with NullPool** for serverless-friendly connections
2. **Enable RLS** but bypass with service role for backend
3. **Use JSONB columns** for flexible structured data storage
4. **Index strategically** (GIN for JSONB, B-tree for foreign keys)
5. **Test connection** before proceeding to backend implementation

Next steps:
1. Complete this Supabase setup (Day 1 morning)
2. Proceed to Phase 1 Backend Implementation Guide
3. Test end-to-end flow by Day 2

**Estimated Time:** 1-2 hours (including table creation and testing)
