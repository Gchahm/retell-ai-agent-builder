# Retell AI Agent Builder

A full-stack web application for creating, managing, and testing AI-powered voice agents for logistics operations. Built to automate driver check-ins, load tracking, and emergency handling through conversational voice calls.

## Demo

[![Watch the demo](https://cdn.loom.com/sessions/thumbnails/83dfed03e6174419b61306d875f0201b-ec7bf6b5a93fb0d9-full-play.gif)](https://www.loom.com/share/83dfed03e6174419b61306d875f0201b)

## Overview

This project demonstrates a production-ready integration with [Retell AI](https://www.retellai.com/) to build conversational voice agents. The platform enables logistics companies to automate routine driver communications while maintaining the ability to handle emergencies and edge cases gracefully.

**Key capabilities:**
- Create and manage multiple voice agents with custom conversation prompts
- Trigger voice calls directly from the browser
- Inject dynamic variables (driver name, load number, etc.) into conversations
- Extract structured data from calls (ETAs, locations, status updates)
- Track call history with full transcripts

## Tech Stack

### Backend
- **FastAPI** - Async Python API framework
- **SQLModel** - ORM combining SQLAlchemy + Pydantic
- **Supabase (PostgreSQL)** - Database and authentication
- **Retell AI SDK** - Voice agent management
- **Alembic** - Database migrations

### Frontend
- **React 19** - UI framework with latest hooks
- **TypeScript** - Type safety throughout
- **Vite** - Build tool and dev server
- **TailwindCSS 4** - Utility-first styling
- **React Query** - Server state management
- **React Hook Form + Zod** - Form handling with validation
- **Radix UI** - Accessible component primitives
- **Kubb** - Auto-generated API client from OpenAPI spec

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  React Frontend │────▶│  FastAPI Backend│────▶│   Retell AI     │
│                 │     │                 │     │                 │
└─────────────────┘     └────────┬────────┘     └────────┬────────┘
                                 │                       │
                                 ▼                       │
                        ┌─────────────────┐              │
                        │                 │              │
                        │    Supabase     │◀─────────────┘
                        │   (PostgreSQL)  │    webhooks
                        │                 │
                        └─────────────────┘
```

**Data flow:**
1. Users create/configure agents through the React dashboard
2. Backend stores configurations and syncs with Retell AI
3. Calls are triggered from the browser using Retell's client SDK
4. Retell AI handles voice synthesis, transcription, and conversation flow
5. Webhooks notify the backend of call events and extracted data
6. Call results are stored in Supabase for history and analysis

## Features

### Agent Management
- Create voice agents with custom prompts tailored to specific use cases
- Update agent configurations with real-time sync to Retell AI
- Sensible defaults optimized for logistics calls (voice, responsiveness, boosted keywords)

### Web Call Interface
- Start voice calls directly from the browser
- Pass dynamic variables that inject into the conversation context
- Real-time call status tracking

### Call History & Analysis
- Browse past calls with pagination
- View full transcripts
- Access structured data extracted from conversations (status, location, ETA, issues)

### Webhook Integration
- Real-time event processing (call started, ended, analyzed)
- Secure webhook signature verification
- Background processing for optimal performance

## Project Structure

```
retell-ai-agent-builder/
├── api/                    # FastAPI backend
│   ├── app/
│   │   ├── models/         # SQLModel database models
│   │   ├── routes/         # API endpoints
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   └── services/       # Business logic & Retell integration
│   └── alembic/            # Database migrations
│
└── frontend/               # React application
    ├── src/
    │   ├── api/            # Auto-generated API client (Kubb)
    │   ├── components/     # Reusable UI components
    │   ├── pages/          # Route components
    │   └── lib/            # Utilities and providers
    └── public/
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Supabase CLI (for local development)
- Retell AI account with API key

### Backend Setup

```bash
cd api
uv sync                          # Install dependencies
supabase start                   # Start local Supabase
cp .env.example .env             # Configure environment
uv run alembic upgrade head      # Run migrations
uv run fastapi dev app/main.py   # Start dev server
```

### Frontend Setup

```bash
cd frontend
npm install                      # Install dependencies
cp .env.example .env             # Configure environment
npm run dev                      # Start dev server
```

See individual READMEs for detailed setup instructions:
- [API Setup](api/README.md)
- [Frontend Setup](frontend/README.md)

## Voice Agent Configuration

Agents are configured with logistics-optimized defaults:
- **Voice**: Professional male voice (11labs-Adrian)
- **Model**: GPT-4o-mini via conversation flow
- **Responsiveness**: 0.8 (fast reactions for natural conversation)
- **Backchannel**: Enabled with 0.5 frequency (active listening cues)
- **STT Mode**: Accurate (handles noisy truck environments)
- **Boosted Keywords**: POD, BOL, lumper, detention, ETA, mile marker, etc.

## License

MIT
