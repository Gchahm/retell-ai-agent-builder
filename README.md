# AI Voice Agent

AI-powered voice agent for logistics call automation using Retell AI.

## Getting Started

Set up the projects in this order:

1. **[API (Backend)](api/README.md)** - Set up the FastAPI backend first
2. **[Frontend](frontend/README.md)** - Then set up the React frontend

## Features

### API

- **Agent Management** - Create, list, update, and retrieve voice agent configurations
- **Web Calls** - Initiate browser-based voice calls with dynamic variables (driver name, load number, etc.)
- **Call History** - List and retrieve call details with transcripts and structured data
- **Webhooks** - Receive real-time call events from Retell AI (started, ended, analyzed)
- **Authentication** - Supabase-based user authentication

### Frontend

- **Agent Dashboard** - View and manage voice agent configurations
- **Agent Editor** - Create and edit agent prompts
- **Web Call Interface** - Start voice calls directly from the browser
- **Call History** - Browse past calls with transcripts and extracted data
- **Authentication** - Login/logout with Supabase Auth
