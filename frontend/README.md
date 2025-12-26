# AI Voice Agent Frontend

React frontend for the AI Voice Agent application.

## Prerequisites

- Node.js 18+ (recommended: 20+)
- npm 9+
- Backend API running locally (for API client generation)

## Setup

### 1. Install dependencies

```bash
npm install
```

### 2. Configure environment variables

Copy the example environment file and update with your values:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-publishable-key
VITE_API_URL=http://localhost:8000
```

- `VITE_SUPABASE_URL`: Your Supabase project URL
- `VITE_SUPABASE_ANON_KEY`: Your Supabase anonymous/public key
- `VITE_API_URL`: Backend API URL (default: `http://localhost:8000`)

### 3. Generate API client (optional)

The API client is auto-generated from the backend OpenAPI spec. If you need to regenerate it after backend changes:

```bash
# Ensure backend is running on localhost:8000
npm run generate
```

This uses [Kubb](https://kubb.dev/) to generate TypeScript types, Zod schemas, and React Query hooks from the backend's OpenAPI specification.

## Development

Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173`.

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |
| `npm run generate` | Regenerate API client from OpenAPI spec |

## Tech Stack

- **React 19** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **TailwindCSS 4** - Styling
- **React Router** - Client-side routing
- **React Query** - Server state management
- **React Hook Form** - Form handling
- **Zod** - Schema validation
- **Supabase** - Authentication
- **Radix UI** - Accessible UI primitives
