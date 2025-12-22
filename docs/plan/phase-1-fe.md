# Phase 1 Frontend Implementation Guide (Days 1-2)

**Version:** 1.0
**Last Updated:** December 21, 2025
**Target:** AI Voice Agent - React Frontend Setup

## Document Overview

This document provides actionable, library-specific guidance for implementing the React frontend for the AI Voice Agent application. All recommendations are based on 2025 best practices and the user-specified tech stack.

---

## 1. Project Setup & Build Tools

### 1.1 Vite 6 (Build Tool)

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
```

**Purpose:** Lightning-fast build tool and dev server for modern web projects
**Justification:** Industry standard for React projects in 2025. Instant HMR, native ESM, optimized builds. Better DX and performance than Create React App or Webpack-based setups.

**Key Features:**
- Sub-second cold starts
- Instant Hot Module Replacement (HMR)
- Optimized production builds with Rollup
- First-class TypeScript support
- Rich plugin ecosystem

**Alternatives:**
- **Next.js** - Overkill for non-SSR projects
- **Create React App** - Deprecated, slower
- **Webpack** - More configuration, slower

### 1.2 TypeScript Configuration

```bash
# Already included in Vite React-TS template
```

**tsconfig.json (Recommended Configuration):**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "useDefineForClassFields": true,
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**Purpose:** Strict TypeScript configuration for maximum type safety
**Justification:** Catches bugs at compile time. Path aliases (`@/*`) improve import readability.

### 1.3 Vite Configuration

```bash
npm install -D @vitejs/plugin-react-swc
```

**vite.config.ts:**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

**Purpose:** Configure Vite with React SWC plugin and path aliases
**Justification:** SWC is 20x faster than Babel for compilation. Proxy prevents CORS issues during development.

### 1.4 Recommended Project Structure

```
frontend/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── ui/              # Shadcn components
│   │   ├── forms/           # Form components
│   │   ├── layout/          # Layout components
│   │   └── features/        # Feature-specific components
│   ├── lib/
│   │   ├── api-client.ts    # API client setup
│   │   ├── query-client.ts  # Tanstack Query config
│   │   └── utils.ts         # Utility functions
│   ├── hooks/               # Custom React hooks
│   ├── routes/              # React Router routes
│   ├── stores/              # Zustand stores
│   ├── types/               # TypeScript types
│   │   └── api.ts           # Generated API types
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── .env.example
├── .eslintrc.cjs
├── .prettierrc
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.ts
```

---

## 2. Core React Setup

### 2.1 React 19

```bash
npm install react@^19.0.0 react-dom@^19.0.0
npm install -D @types/react @types/react-dom
```

**Purpose:** Latest React with new features (use, transitions, actions)
**Justification:** React 19 introduces async transitions and built-in form actions. Better performance and DX.

**Key React 19 Features:**
- `use()` hook for async data
- Actions for form submissions
- Optimistic UI updates
- Automatic batching improvements

### 2.2 React Router 7 (Framework Mode, No SSR)

```bash
npm install react-router@^7.0.0
```

**Purpose:** Modern routing with data loading patterns
**Justification:** React Router 7 brings framework-style features (loaders, actions) without requiring SSR. Better than traditional SPA routing, simpler than Next.js.

**Route Structure:**
```typescript
// src/routes/index.tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { RootLayout } from './layout'
import { Dashboard } from '@/pages/dashboard'
import { AgentConfig } from '@/pages/agent-config'
import { TriggerCall } from '@/pages/trigger-call'
import { CallResults } from '@/pages/call-results'

const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: 'config',
        element: <AgentConfig />,
      },
      {
        path: 'calls/trigger',
        element: <TriggerCall />,
      },
      {
        path: 'calls/:id',
        element: <CallResults />,
        loader: async ({ params }) => {
          // Data loading happens here
          const response = await fetch(`/api/call/${params.id}/results`)
          return response.json()
        },
      },
    ],
  },
])

export function Router() {
  return <RouterProvider router={router} />
}
```

**Key Features:**
- Loader functions for data fetching
- Action functions for mutations
- Error boundaries
- Type-safe route params

**Alternatives:**
- **TanStack Router** - More type-safe, but newer and less mature
- **Wouter** - Minimal, but lacks data loading features

---

## 3. Styling - Tailwind CSS 4

### 3.1 Tailwind CSS 4 Installation

```bash
npm install tailwindcss@next @tailwindcss/vite@next
```

**Purpose:** Utility-first CSS framework with new CSS-first configuration
**Justification:** Tailwind 4 introduces a new engine with better performance, CSS-first config, and native CSS features. Perfect integration with Shadcn.

**vite.config.ts (Updated):**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

### 3.2 Tailwind Configuration

**src/index.css:**
```css
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.6 0.2 250);
  --color-secondary: oklch(0.8 0.1 200);

  /* Shadcn color variables */
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --card: 0 0% 100%;
  --card-foreground: 222.2 84% 4.9%;
  --popover: 0 0% 100%;
  --popover-foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
  --secondary: 210 40% 96.1%;
  --secondary-foreground: 222.2 47.4% 11.2%;
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  --accent: 210 40% 96.1%;
  --accent-foreground: 222.2 47.4% 11.2%;
  --destructive: 0 84.2% 60.2%;
  --destructive-foreground: 210 40% 98%;
  --border: 214.3 31.8% 91.4%;
  --input: 214.3 31.8% 91.4%;
  --ring: 222.2 84% 4.9%;
  --radius: 0.5rem;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  /* ... dark mode colors */
}
```

**Purpose:** CSS-first configuration with CSS variables for theming
**Justification:** Tailwind 4's new `@theme` directive allows defining design tokens in CSS. Better performance and easier theme management.

### 3.3 Utility Libraries for Tailwind

```bash
npm install clsx tailwind-merge
```

**Purpose:** Utility for conditionally joining classNames
**Justification:** `clsx` handles conditional classes, `tailwind-merge` prevents conflicts.

**lib/utils.ts:**
```typescript
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

---

## 4. UI Component Library - Shadcn

### 4.1 Shadcn Setup

```bash
npx shadcn@latest init
```

**Purpose:** Copy-paste component library built on Radix UI and Tailwind
**Justification:** Not a dependency, components are copied to your project. Full control, customizable, accessible, TypeScript-first.

**Configuration (components.json):**
```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "src/index.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

### 4.2 Essential Components for This Project

```bash
# Form components
npx shadcn@latest add form input label textarea select checkbox radio-group switch

# Data display
npx shadcn@latest add table card badge separator

# Feedback
npx shadcn@latest add alert dialog toast sonner

# Navigation
npx shadcn@latest add tabs breadcrumb

# Layout
npx shadcn@latest add button dropdown-menu
```

**Components Breakdown:**

| Component | Use Case |
|-----------|----------|
| Form, Input, Label, Textarea, Select | Agent configuration, call trigger form |
| Table | Call history, structured data display |
| Card | Dashboard widgets, result sections |
| Badge | Call status indicators |
| Alert | Error messages, warnings |
| Dialog | Confirmation modals |
| Sonner (Toast) | Success/error notifications |
| Tabs | Navigation between scenarios |
| Button | Primary actions |

### 4.3 Customization Approach

**Purpose:** Shadcn components use CSS variables for theming
**Justification:** Change colors globally via `index.css` without modifying component code.

**Example - Custom Button Variant:**
```typescript
// components/ui/button.tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground",
        // Add custom variant for call actions
        call: "bg-green-600 text-white hover:bg-green-700",
      },
    },
  }
)
```

---

## 5. Data Fetching - Tanstack Query v5

### 5.1 Installation

```bash
npm install @tanstack/react-query
npm install -D @tanstack/react-query-devtools
```

**Purpose:** Powerful async state management for data fetching
**Justification:** Handles caching, background updates, optimistic updates, and error states automatically. Industry standard for server state in React.

**Key Features:**
- Automatic caching and cache invalidation
- Background refetching
- Optimistic updates
- Request deduplication
- Pagination and infinite scroll support
- DevTools for debugging

### 5.2 Query Client Setup

**lib/query-client.ts:**
```typescript
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      gcTime: 5 * 60 * 1000, // 5 minutes (formerly cacheTime)
      retry: 1,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 0,
    },
  },
})
```

**main.tsx:**
```typescript
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { queryClient } from './lib/query-client'
import { Router } from './routes'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <Router />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </StrictMode>
)
```

### 5.3 Query Patterns

**hooks/use-call-results.ts:**
```typescript
import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/lib/api-client'
import type { CallResult } from '@/types/api'

export function useCallResults(callId: string) {
  return useQuery({
    queryKey: ['call-results', callId],
    queryFn: async () => {
      const response = await apiClient.get<CallResult>(`/api/call/${callId}/results`)
      return response.data
    },
    enabled: !!callId,
  })
}
```

**Usage in Component:**
```typescript
function CallResultsPage({ callId }: { callId: string }) {
  const { data, isLoading, error } = useCallResults(callId)

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div>
      <h1>Call Results</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}
```

### 5.4 Mutation Patterns

**hooks/use-trigger-call.ts:**
```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/lib/api-client'
import type { TriggerCallRequest, CallResponse } from '@/types/api'

export function useTriggerCall() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: TriggerCallRequest) => {
      const response = await apiClient.post<CallResponse>('/api/call/trigger', data)
      return response.data
    },
    onSuccess: (data) => {
      // Invalidate and refetch call list
      queryClient.invalidateQueries({ queryKey: ['calls'] })

      // Navigate to results page
      // or show success toast
    },
  })
}
```

**Usage in Component:**
```typescript
function TriggerCallForm() {
  const triggerCall = useTriggerCall()

  const handleSubmit = (data: TriggerCallRequest) => {
    triggerCall.mutate(data)
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <Button type="submit" disabled={triggerCall.isPending}>
        {triggerCall.isPending ? 'Calling...' : 'Start Test Call'}
      </Button>
    </form>
  )
}
```

### 5.5 Optimistic Updates

```typescript
export function useUpdateAgentConfig() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (config: AgentConfig) => {
      const response = await apiClient.put('/api/agent-config', config)
      return response.data
    },
    onMutate: async (newConfig) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['agent-config'] })

      // Snapshot previous value
      const previousConfig = queryClient.getQueryData(['agent-config'])

      // Optimistically update
      queryClient.setQueryData(['agent-config'], newConfig)

      return { previousConfig }
    },
    onError: (err, newConfig, context) => {
      // Rollback on error
      queryClient.setQueryData(['agent-config'], context?.previousConfig)
    },
    onSettled: () => {
      // Refetch after error or success
      queryClient.invalidateQueries({ queryKey: ['agent-config'] })
    },
  })
}
```

---

## 6. Form Handling - Tanstack Form

### 6.1 Installation

```bash
npm install @tanstack/react-form
npm install zod
npm install @tanstack/zod-form-adapter
```

**Purpose:** Type-safe form library with first-class Zod support
**Justification:** Better TypeScript support than React Hook Form. Integrates seamlessly with Tanstack Query. Zod provides runtime validation.

**Alternatives:**
- **React Hook Form** - More mature, larger ecosystem, but less type-safe
- **Formik** - Legacy, not recommended for new projects

### 6.2 Zod Schema Definition

**schemas/call-trigger.ts:**
```typescript
import { z } from 'zod'

export const callTriggerSchema = z.object({
  driver_name: z.string().min(1, 'Driver name is required'),
  phone_number: z
    .string()
    .regex(/^\+?[1-9]\d{1,14}$/, 'Invalid phone number format'),
  load_number: z.string().min(1, 'Load number is required'),
  agent_config_id: z.string().uuid('Invalid agent configuration'),
})

export type CallTriggerFormData = z.infer<typeof callTriggerSchema>
```

### 6.3 Form with Tanstack Form + Zod

**components/forms/trigger-call-form.tsx:**
```typescript
import { useForm } from '@tanstack/react-form'
import { zodValidator } from '@tanstack/zod-form-adapter'
import { callTriggerSchema, type CallTriggerFormData } from '@/schemas/call-trigger'
import { useTriggerCall } from '@/hooks/use-trigger-call'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export function TriggerCallForm() {
  const triggerCall = useTriggerCall()

  const form = useForm({
    defaultValues: {
      driver_name: '',
      phone_number: '',
      load_number: '',
      agent_config_id: '',
    },
    validatorAdapter: zodValidator(),
    validators: {
      onChange: callTriggerSchema,
    },
    onSubmit: async ({ value }) => {
      await triggerCall.mutateAsync(value)
    },
  })

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
        e.stopPropagation()
        form.handleSubmit()
      }}
    >
      <form.Field name="driver_name">
        {(field) => (
          <div className="space-y-2">
            <Label htmlFor={field.name}>Driver Name</Label>
            <Input
              id={field.name}
              value={field.state.value}
              onBlur={field.handleBlur}
              onChange={(e) => field.handleChange(e.target.value)}
            />
            {field.state.meta.errors && (
              <p className="text-sm text-destructive">
                {field.state.meta.errors.join(', ')}
              </p>
            )}
          </div>
        )}
      </form.Field>

      {/* Repeat for other fields */}

      <Button type="submit" disabled={triggerCall.isPending}>
        {triggerCall.isPending ? 'Starting Call...' : 'Start Test Call'}
      </Button>
    </form>
  )
}
```

### 6.4 Integration with Shadcn Form Component

Shadcn's Form component is built for React Hook Form, but you can use Tanstack Form directly with Shadcn's input components as shown above. Alternatively, create a wrapper:

**components/ui/tanstack-form-field.tsx:**
```typescript
import { FieldApi } from '@tanstack/react-form'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'

interface FormFieldProps {
  field: FieldApi<any, any, any, any>
  label: string
  type?: string
}

export function FormField({ field, label, type = 'text' }: FormFieldProps) {
  return (
    <div className="space-y-2">
      <Label htmlFor={field.name}>{label}</Label>
      <Input
        id={field.name}
        type={type}
        value={field.state.value}
        onBlur={field.handleBlur}
        onChange={(e) => field.handleChange(e.target.value)}
      />
      {field.state.meta.errors && (
        <p className="text-sm text-destructive">
          {field.state.meta.errors.join(', ')}
        </p>
      )}
    </div>
  )
}
```

---

## 7. State Management

### 7.1 Zustand for Client State

```bash
npm install zustand
```

**Purpose:** Minimal state management for global client state
**Justification:** Simpler than Redux, better DX than Context for complex state. Perfect TypeScript support. Only 1kb gzipped.

**stores/ui-store.ts:**
```typescript
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface UIState {
  theme: 'light' | 'dark'
  sidebarOpen: boolean
  toggleTheme: () => void
  toggleSidebar: () => void
}

export const useUIStore = create<UIState>()(
  devtools(
    persist(
      (set) => ({
        theme: 'light',
        sidebarOpen: true,
        toggleTheme: () =>
          set((state) => ({
            theme: state.theme === 'light' ? 'dark' : 'light',
          })),
        toggleSidebar: () =>
          set((state) => ({
            sidebarOpen: !state.sidebarOpen,
          })),
      }),
      {
        name: 'ui-storage',
      }
    )
  )
)
```

**Usage:**
```typescript
function Header() {
  const { theme, toggleTheme } = useUIStore()

  return (
    <header>
      <Button onClick={toggleTheme}>
        {theme === 'light' ? 'Dark' : 'Light'} Mode
      </Button>
    </header>
  )
}
```

### 7.2 State Management Strategy

**Server State:** Use Tanstack Query
- API data
- Call results
- Agent configurations
- Call history

**Client State:** Use Zustand
- UI state (theme, sidebar)
- User preferences
- Transient UI state

**Auth State:** Use Context or Zustand with persistence
- User session
- JWT tokens
- Permissions

**Form State:** Use Tanstack Form
- Form values
- Validation errors
- Submission state

---

## 8. Routing - React Router 7

### 8.1 Route Structure

**routes/index.tsx:**
```typescript
import { createBrowserRouter } from 'react-router-dom'
import { RootLayout } from './layout'
import { ErrorBoundary } from '@/components/error-boundary'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <ErrorBoundary />,
    children: [
      {
        index: true,
        lazy: () => import('@/pages/dashboard'),
      },
      {
        path: 'config',
        lazy: () => import('@/pages/agent-config'),
      },
      {
        path: 'calls',
        children: [
          {
            path: 'trigger',
            lazy: () => import('@/pages/trigger-call'),
          },
          {
            path: ':id',
            lazy: () => import('@/pages/call-results'),
          },
        ],
      },
    ],
  },
])
```

### 8.2 Root Layout

**routes/layout.tsx:**
```typescript
import { Outlet, Link } from 'react-router-dom'
import { Toaster } from '@/components/ui/sonner'

export function RootLayout() {
  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center gap-6">
            <Link to="/" className="text-xl font-bold">
              AI Voice Agent
            </Link>
            <Link to="/config" className="text-sm">
              Configuration
            </Link>
            <Link to="/calls/trigger" className="text-sm">
              Trigger Call
            </Link>
          </div>
        </div>
      </nav>

      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>

      <Toaster />
    </div>
  )
}
```

### 8.3 Loader Pattern for Data Fetching

**pages/call-results.tsx:**
```typescript
import { useLoaderData } from 'react-router-dom'
import { queryClient } from '@/lib/query-client'
import { apiClient } from '@/lib/api-client'
import type { CallResult } from '@/types/api'

// Loader function
export async function loader({ params }: { params: { id: string } }) {
  const callId = params.id

  // Use Tanstack Query in loader
  const data = await queryClient.fetchQuery({
    queryKey: ['call-results', callId],
    queryFn: async () => {
      const response = await apiClient.get<CallResult>(`/api/call/${callId}/results`)
      return response.data
    },
  })

  return data
}

// Component
export function Component() {
  const data = useLoaderData() as CallResult

  return (
    <div>
      <h1>Call Results: {data.call_id}</h1>
      {/* Render call results */}
    </div>
  )
}
```

---

## 9. Type Safety

### 9.1 Strict TypeScript Configuration

See section 1.2 for tsconfig.json

### 9.2 API Type Generation

```bash
npm install -D openapi-typescript
```

**Purpose:** Generate TypeScript types from FastAPI's OpenAPI schema
**Justification:** Ensures frontend types match backend API. Automatic type safety across the stack.

**package.json scripts:**
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "generate:api-types": "openapi-typescript http://localhost:8000/openapi.json -o src/types/api.ts"
  }
}
```

**Usage:**
```bash
# Start backend first, then:
npm run generate:api-types
```

**types/api.ts (Generated):**
```typescript
// Auto-generated, do not edit
export interface paths {
  '/api/call/trigger': {
    post: {
      requestBody: {
        content: {
          'application/json': components['schemas']['TriggerCallRequest']
        }
      }
      responses: {
        200: {
          content: {
            'application/json': components['schemas']['CallResponse']
          }
        }
      }
    }
  }
  // ... all API endpoints
}

export interface components {
  schemas: {
    TriggerCallRequest: {
      driver_name: string
      phone_number: string
      load_number: string
      agent_config_id: string
    }
    // ... all schemas
  }
}
```

### 9.3 Type-safe API Client

**lib/api-client.ts:**
```typescript
import type { paths } from '@/types/api'

type ApiPath = keyof paths
type ApiMethod<Path extends ApiPath> = keyof paths[Path]
type ApiRequest<
  Path extends ApiPath,
  Method extends ApiMethod<Path>
> = paths[Path][Method] extends { requestBody: { content: { 'application/json': infer T } } }
  ? T
  : never

type ApiResponse<
  Path extends ApiPath,
  Method extends ApiMethod<Path>
> = paths[Path][Method] extends { responses: { 200: { content: { 'application/json': infer T } } } }
  ? T
  : never

class APIClient {
  private baseURL: string

  constructor(baseURL: string) {
    this.baseURL = baseURL
  }

  async post<Path extends ApiPath>(
    path: Path,
    data: ApiRequest<Path, 'post'>
  ): Promise<ApiResponse<Path, 'post'>> {
    const response = await fetch(`${this.baseURL}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`)
    }

    return response.json()
  }

  // Similar for get, put, delete...
}

export const apiClient = new APIClient(import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000')
```

**Usage (Fully Type-safe):**
```typescript
// TypeScript knows the exact request/response types
const result = await apiClient.post('/api/call/trigger', {
  driver_name: 'John',
  phone_number: '+1234567890',
  load_number: 'LOAD-123',
  agent_config_id: 'uuid-here',
})
// result is typed as CallResponse
```

### 9.4 Zod for Runtime Validation

```typescript
import { z } from 'zod'

// Define schema
export const callResultSchema = z.object({
  call_id: z.string(),
  transcript: z.string(),
  structured_data: z.object({
    call_outcome: z.string(),
    driver_status: z.string(),
    // ... other fields
  }),
})

// Parse API response
const response = await apiClient.get('/api/call/123/results')
const validated = callResultSchema.parse(response) // Throws if invalid
```

---

## 10. Development Tools

### 10.1 ESLint 9 (Flat Config)

```bash
npm install -D eslint @eslint/js typescript-eslint eslint-plugin-react-hooks eslint-plugin-react-refresh
```

**eslint.config.js:**
```javascript
import js from '@eslint/js'
import tseslint from 'typescript-eslint'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'

export default tseslint.config(
  { ignores: ['dist'] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2022,
      globals: { ...globals.browser },
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],
    },
  }
)
```

### 10.2 Prettier

```bash
npm install -D prettier
```

**.prettierrc:**
```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

```bash
npm install -D prettier-plugin-tailwindcss
```

**Purpose:** Auto-sort Tailwind classes
**Justification:** Consistent class ordering across the codebase.

### 10.3 Biome (Alternative to ESLint + Prettier)

```bash
npm install -D @biomejs/biome
```

**Purpose:** Fast, all-in-one linter and formatter (written in Rust)
**Justification:** 100x faster than ESLint. Single tool for linting and formatting. Growing ecosystem.

**biome.json:**
```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "files": {
    "ignoreUnknown": false,
    "ignore": ["dist", "node_modules"]
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space"
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

**Recommendation:** Use ESLint + Prettier for established projects. Try Biome for new projects (faster, simpler).

### 10.4 VSCode Extensions

**Recommended Extensions:**
- **ESLint** (dbaeumer.vscode-eslint)
- **Prettier** (esbenp.prettier-vscode)
- **Tailwind CSS IntelliSense** (bradlc.vscode-tailwindcss)
- **TypeScript Error Translator** (mattpocock.ts-error-translator)
- **Error Lens** (usernamehw.errorlens)
- **Auto Rename Tag** (formulahendry.auto-rename-tag)

**.vscode/settings.json:**
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"],
    ["cn\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)"]
  ]
}
```

---

## 11. Testing

### 11.1 Vitest

```bash
npm install -D vitest @vitejs/plugin-react jsdom
```

**Purpose:** Vite-native test runner
**Justification:** Same config as Vite, instant test execution, ESM support out of the box.

**vite.config.ts (Updated):**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    css: true,
  },
})
```

**src/test/setup.ts:**
```typescript
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import * as matchers from '@testing-library/jest-dom/matchers'

expect.extend(matchers)

afterEach(() => {
  cleanup()
})
```

### 11.2 React Testing Library

```bash
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

**Purpose:** Test React components from user perspective
**Justification:** Focuses on behavior, not implementation. Encourages accessible components.

**Example Test:**
```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect } from 'vitest'
import { TriggerCallForm } from '@/components/forms/trigger-call-form'

describe('TriggerCallForm', () => {
  it('shows validation error for invalid phone number', async () => {
    const user = userEvent.setup()
    render(<TriggerCallForm />)

    const phoneInput = screen.getByLabelText(/phone number/i)
    await user.type(phoneInput, 'invalid')
    await user.tab() // Trigger blur

    expect(await screen.findByText(/invalid phone number/i)).toBeInTheDocument()
  })
})
```

### 11.3 MSW (Mock Service Worker)

```bash
npm install -D msw
```

**Purpose:** Mock API requests at the network level
**Justification:** More realistic than mocking fetch. Works in both tests and browser for development.

**src/mocks/handlers.ts:**
```typescript
import { http, HttpResponse } from 'msw'
import type { CallResult } from '@/types/api'

export const handlers = [
  http.post('/api/call/trigger', async () => {
    return HttpResponse.json({
      call_id: 'test-123',
      status: 'initiated',
    })
  }),

  http.get('/api/call/:id/results', async ({ params }) => {
    const callResult: CallResult = {
      call_id: params.id as string,
      transcript: 'Test transcript',
      structured_data: {
        call_outcome: 'In-Transit Update',
        driver_status: 'Driving',
      },
    }
    return HttpResponse.json(callResult)
  }),
]
```

**src/test/setup.ts (Updated):**
```typescript
import { expect, afterEach, beforeAll, afterAll } from 'vitest'
import { cleanup } from '@testing-library/react'
import { setupServer } from 'msw/node'
import { handlers } from '@/mocks/handlers'

const server = setupServer(...handlers)

beforeAll(() => server.listen())
afterEach(() => {
  cleanup()
  server.resetHandlers()
})
afterAll(() => server.close())
```

### 11.4 Playwright (E2E Testing)

```bash
npm install -D @playwright/test
npx playwright install
```

**Purpose:** End-to-end testing across browsers
**Justification:** More reliable than Cypress, better performance, multi-browser support. Industry standard for E2E in 2025.

**playwright.config.ts:**
```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
})
```

**e2e/trigger-call.spec.ts:**
```typescript
import { test, expect } from '@playwright/test'

test('trigger call flow', async ({ page }) => {
  await page.goto('/')

  await page.click('text=Trigger Call')
  await page.fill('[name="driver_name"]', 'John Doe')
  await page.fill('[name="phone_number"]', '+1234567890')
  await page.fill('[name="load_number"]', 'LOAD-123')

  await page.click('text=Start Test Call')

  await expect(page.locator('text=Call initiated')).toBeVisible()
})
```

---

## 12. Additional Utilities

### 12.1 Date Handling - date-fns

```bash
npm install date-fns
```

**Purpose:** Modern date utility library
**Justification:** Tree-shakeable (only import what you use), functional API, comprehensive.

**Usage:**
```typescript
import { format, formatDistanceToNow } from 'date-fns'

const timestamp = new Date(call.created_at)
const formatted = format(timestamp, 'PPpp') // "Apr 29, 2021, 12:00:00 PM"
const relative = formatDistanceToNow(timestamp, { addSuffix: true }) // "2 hours ago"
```

**Alternatives:**
- **dayjs** - Smaller bundle, but less comprehensive
- **Luxon** - Most powerful, but largest

### 12.2 Icons - lucide-react

```bash
npm install lucide-react
```

**Purpose:** Beautiful, consistent icon set optimized for React
**Justification:** Recommended by Shadcn. Tree-shakeable. Over 1000 icons. TypeScript support.

**Usage:**
```typescript
import { Phone, Calendar, User } from 'lucide-react'

function CallButton() {
  return (
    <Button>
      <Phone className="mr-2 h-4 w-4" />
      Start Call
    </Button>
  )
}
```

**Alternatives:**
- **Heroicons** - Smaller set, but high quality
- **React Icons** - Massive collection, but larger bundle

### 12.3 Notifications - sonner

```bash
npm install sonner
```

**Purpose:** Toast notifications designed for React
**Justification:** Recommended by Shadcn. Beautiful design, excellent DX, accessible.

**Usage:**
```typescript
import { toast } from 'sonner'
import { Toaster } from '@/components/ui/sonner'

// In layout
function Layout() {
  return (
    <>
      {/* Your app */}
      <Toaster />
    </>
  )
}

// Anywhere in app
function TriggerCallButton() {
  const handleClick = () => {
    toast.success('Call initiated successfully!')
    // or
    toast.error('Failed to trigger call')
    // or
    toast.promise(
      triggerCall(),
      {
        loading: 'Starting call...',
        success: 'Call started!',
        error: 'Failed to start call',
      }
    )
  }
}
```

### 12.4 Real-time Updates - SSE

For call status updates from the backend:

```typescript
// hooks/use-call-status.ts
import { useEffect, useState } from 'react'

export function useCallStatus(callId: string) {
  const [status, setStatus] = useState<string>('pending')

  useEffect(() => {
    const eventSource = new EventSource(`/api/call/${callId}/status`)

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setStatus(data.status)
    }

    return () => {
      eventSource.close()
    }
  }, [callId])

  return status
}
```

---

## 13. Complete Dependency List

### 13.1 package.json

```json
{
  "name": "ai-voice-agent-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint .",
    "format": "prettier --write \"src/**/*.{ts,tsx}\"",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:e2e": "playwright test",
    "generate:api-types": "openapi-typescript http://localhost:8000/openapi.json -o src/types/api.ts"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router": "^7.0.0",
    "@tanstack/react-query": "^5.62.0",
    "@tanstack/react-form": "^0.38.0",
    "@tanstack/zod-form-adapter": "^0.38.0",
    "zod": "^3.24.0",
    "date-fns": "^4.1.0",
    "lucide-react": "^0.468.0",
    "sonner": "^1.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.6.0",
    "zustand": "^5.0.2"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react-swc": "^3.7.0",
    "vite": "^6.0.0",
    "typescript": "^5.7.0",
    "tailwindcss": "^4.0.0",
    "@tailwindcss/vite": "^4.0.0",
    "@tanstack/react-query-devtools": "^5.62.0",
    "eslint": "^9.17.0",
    "@eslint/js": "^9.17.0",
    "typescript-eslint": "^8.18.0",
    "eslint-plugin-react-hooks": "^5.0.0",
    "eslint-plugin-react-refresh": "^0.4.16",
    "prettier": "^3.4.0",
    "prettier-plugin-tailwindcss": "^0.6.9",
    "vitest": "^2.1.0",
    "@testing-library/react": "^16.1.0",
    "@testing-library/jest-dom": "^6.6.0",
    "@testing-library/user-event": "^14.5.2",
    "@playwright/test": "^1.49.0",
    "msw": "^2.7.0",
    "openapi-typescript": "^7.4.0",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.48"
  }
}
```

---

## 14. Day 1-2 Implementation Checklist

### Day 1: Foundation
- [ ] Initialize Vite project with React + TypeScript template
- [ ] Install and configure Tailwind CSS 4
- [ ] Set up Shadcn UI and install essential components
- [ ] Configure path aliases in tsconfig.json and vite.config.ts
- [ ] Install React Router 7 and set up basic routes
- [ ] Install Tanstack Query and configure QueryClient
- [ ] Set up ESLint and Prettier
- [ ] Create project structure (components, lib, hooks, routes)
- [ ] Set up environment variables (.env.example)

### Day 2: Core Integration
- [ ] Generate API types from FastAPI OpenAPI schema
- [ ] Create type-safe API client
- [ ] Install and configure Tanstack Form with Zod
- [ ] Install Zustand for client state management
- [ ] Build Dashboard page with call history
- [ ] Build Agent Configuration page with form
- [ ] Build Trigger Call page with validation
- [ ] Build Call Results page with structured data display
- [ ] Set up MSW for API mocking in development
- [ ] Add toast notifications with Sonner
- [ ] Test complete flow: config → trigger → results

---

## 15. Critical Files for Implementation

Based on this implementation plan, here are the most critical frontend files to create:

1. **frontend/vite.config.ts** - Vite configuration with React SWC, Tailwind, path aliases, API proxy
2. **frontend/tsconfig.json** - Strict TypeScript configuration with path mappings
3. **frontend/tailwind.config.ts** - Tailwind CSS 4 configuration (may use CSS-first in index.css)
4. **frontend/src/index.css** - Tailwind imports and CSS variables for Shadcn theming
5. **frontend/src/main.tsx** - App entry point with QueryClientProvider and Router
6. **frontend/src/lib/api-client.ts** - Type-safe API client using generated types
7. **frontend/src/lib/query-client.ts** - Tanstack Query configuration
8. **frontend/src/lib/utils.ts** - cn() utility for Tailwind class merging
9. **frontend/src/routes/index.tsx** - React Router configuration with all routes
10. **frontend/src/routes/layout.tsx** - Root layout with navigation and Toaster
11. **frontend/src/types/api.ts** - Generated TypeScript types from FastAPI OpenAPI
12. **frontend/.env.example** - Environment variables template
13. **frontend/package.json** - Complete dependency list and scripts

---

## 16. Integration with Backend

### 16.1 Environment Variables

**frontend/.env.example:**
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

**frontend/.env:**
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### 16.2 API Client Integration

**lib/api-client.ts:**
```typescript
import type { paths } from '@/types/api'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export class APIError extends Error {
  constructor(
    public status: number,
    public statusText: string,
    message?: string
  ) {
    super(message || statusText)
  }
}

export const apiClient = {
  async request<T>(path: string, init?: RequestInit): Promise<T> {
    const response = await fetch(`${BASE_URL}${path}`, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        ...init?.headers,
      },
    })

    if (!response.ok) {
      throw new APIError(response.status, response.statusText)
    }

    return response.json()
  },

  get<T>(path: string) {
    return this.request<T>(path)
  },

  post<T>(path: string, data?: unknown) {
    return this.request<T>(path, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },

  put<T>(path: string, data?: unknown) {
    return this.request<T>(path, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  },

  delete<T>(path: string) {
    return this.request<T>(path, {
      method: 'DELETE',
    })
  },
}
```

### 16.3 CORS Configuration

Ensure backend FastAPI has CORS configured to accept requests from frontend:

**Backend (app/main.py):**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 16.4 Type Generation Workflow

```bash
# 1. Start backend
cd backend && uvicorn app.main:app --reload

# 2. In another terminal, generate types
cd frontend && npm run generate:api-types

# 3. Types are now available in src/types/api.ts
```

**Integration in CI/CD:**
- Generate types as part of build process
- Commit generated types to version control OR
- Generate on-demand during development only

---

## 17. Key Design Decisions

### Why React Router 7 Framework Mode over Next.js?
- **No SSR requirement:** Next.js is overkill for client-only apps
- **Modern patterns:** Loaders and actions without SSR complexity
- **Lighter bundle:** No server runtime in production
- **Simpler deployment:** Static files only

### Why Tanstack Form over React Hook Form?
- **Better TypeScript:** First-class type inference
- **Consistency:** Same ecosystem as Tanstack Query
- **Modern API:** Designed for React 19 patterns
- **Zod integration:** Native adapter for Zod validation

### Why Zustand over Redux Toolkit?
- **Minimal boilerplate:** Define state in one place
- **No Context providers:** Direct store access
- **Excellent TypeScript:** No manual type definitions
- **Tiny bundle:** 1kb gzipped vs Redux's 3kb+

### Why Vitest over Jest?
- **Native Vite integration:** Same config, faster
- **ESM support:** No CJS/ESM compatibility issues
- **Faster:** Instant test execution
- **Better DX:** Hot reload for tests

### Why Playwright over Cypress?
- **Better performance:** Faster, more reliable
- **Multi-browser:** Chrome, Firefox, Safari, Edge
- **Better debugging:** Time-travel debugging, trace viewer
- **Industry standard:** Recommended by most orgs in 2025

### Why date-fns over dayjs/Luxon?
- **Tree-shakeable:** Import only what you need
- **Comprehensive:** Covers all use cases
- **Functional:** Pure functions, immutable
- **Active maintenance:** Large community, regular updates

---

## 18. Performance Optimizations

### 18.1 Code Splitting

React Router 7 supports route-based code splitting with `lazy`:

```typescript
{
  path: 'config',
  lazy: () => import('@/pages/agent-config'),
}
```

Each route is a separate chunk, loaded on demand.

### 18.2 Tanstack Query Optimization

```typescript
// Prefetch on hover
const queryClient = useQueryClient()

<Link
  to={`/calls/${id}`}
  onMouseEnter={() => {
    queryClient.prefetchQuery({
      queryKey: ['call-results', id],
      queryFn: () => fetchCallResults(id),
    })
  }}
>
  View Results
</Link>
```

### 18.3 Image Optimization

```bash
npm install -D vite-plugin-image-optimizer
```

**vite.config.ts:**
```typescript
import { ViteImageOptimizer } from 'vite-plugin-image-optimizer'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    ViteImageOptimizer(),
  ],
})
```

### 18.4 Bundle Analysis

```bash
npm install -D rollup-plugin-visualizer
```

**vite.config.ts:**
```typescript
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    visualizer({ open: true }),
  ],
})
```

Run `npm run build` to see bundle composition.

---

## Conclusion

This document provides a complete, production-ready frontend setup for Days 1-2 of the AI Voice Agent project. All library recommendations are based on:

1. **User specifications:** React Router framework mode, Tailwind 4, Tanstack Query/Form, Shadcn
2. **2025 best practices:** Latest stable versions of all tools
3. **Type safety:** End-to-end TypeScript with generated API types
4. **Developer experience:** Fast tooling (Vite, Vitest, Playwright)
5. **Production readiness:** Optimized builds, error handling, testing

Focus on the minimal dependency set for Day 1-2, then expand with optional libraries as needed. Prioritize getting the core flow working:

**Dashboard → Agent Config → Trigger Call → View Results**

The frontend integrates seamlessly with the FastAPI backend documented in phase-1-be.md through:
- Type-safe API client using OpenAPI-generated types
- Tanstack Query for server state management
- Zod schemas for runtime validation matching backend Pydantic models
- Real-time updates via SSE for call status

All tools chosen prioritize developer experience, type safety, and modern React patterns while maintaining simplicity and avoiding over-engineering.
