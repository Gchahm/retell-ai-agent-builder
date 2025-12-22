# AI Voice Agent - High-Level Implementation Plan

## Project Overview
Build a web application for configuring, testing, and reviewing AI voice agent calls for logistics scenarios using React, TypeScript, FastAPI, Supabase, and Retell AI.

## Phase 1: Project Setup & Architecture

### 1.1 Repository & Environment Setup
- Initialize monorepo structure with frontend and backend directories
- Set up development environments for React + TypeScript and FastAPI
- Configure environment variables for Retell AI, Supabase
- Create initial commit (START)

### 1.2 Core Technology Stack
- **Frontend**: React + TypeScript + Vite/Next.js
- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **Voice AI**: Retell AI
- **Styling**: Tailwind CSS or Material-UI

## Phase 2: Database Schema Design

### 2.1 Core Tables
- **agent_configurations**: Store prompts, system instructions, Retell settings
  - id, name, system_prompt, scenario_type, retell_settings (JSON)
  - Advanced settings: backchanneling, filler words, interruption sensitivity

- **test_calls**: Store call metadata and trigger info
  - id, agent_config_id, driver_name, phone_number, load_number, status, created_at

- **call_results**: Store structured outputs and transcripts
  - id, call_id, transcript, structured_data (JSON), created_at
  - Structured data varies by scenario (check-in vs emergency)

## Phase 3: Backend Development (FastAPI)

### 3.1 Core API Endpoints
- `POST /api/agent-config` - Create/update agent configurations
- `GET /api/agent-config` - List all configurations
- `POST /api/call/trigger` - Initiate test call via Retell API
- `POST /api/webhook/retell` - Receive Retell AI webhooks
- `GET /api/call/{id}/results` - Retrieve structured call results

### 3.2 Retell AI Integration
- Implement webhook handler for real-time conversation guidance
- Dynamic prompt injection based on:
  - Scenario type (check-in vs emergency)
  - Driver responses (status determination)
  - Emergency detection (trigger phrase recognition)

### 3.3 Post-Processing Pipeline
- Extract structured data from raw transcripts using LLM (GPT-4/Claude)
- Parse key-value pairs based on scenario requirements
- Store both structured data and full transcript

### 3.4 Conversation Logic
- **Scenario 1 (Check-in)**:
  - Open-ended status inquiry
  - Dynamic branching based on "In-Transit" vs "Arrived" responses
  - Extract: call_outcome, driver_status, location, ETA, delays, POD acknowledgment

- **Scenario 2 (Emergency)**:
  - Detect emergency trigger phrases ("blowout", "accident", "breakdown")
  - Immediate context switch
  - Gather safety info, location, escalate to human
  - Extract: emergency_type, safety_status, injury_status, location, escalation_status

- **Special Cases**:
  - Retry logic for unclear responses (max 2-3 attempts)
  - Graceful termination for uncooperative drivers
  - Non-confrontational GPS discrepancy handling

## Phase 4: Frontend Development (React)

### 4.1 Core Pages/Components
- **Dashboard/Home**: Overview of recent calls
- **Agent Configuration Page**:
  - Form to edit system prompts
  - Retell AI settings (backchanneling, filler words, interruption sensitivity)
  - Scenario selection (check-in vs emergency)
  - Save/update configurations

- **Call Trigger Interface**:
  - Input fields: driver name, phone number, load number
  - Agent configuration selector
  - "Start Test Call" button
  - Real-time call status indicator

- **Results Viewer**:
  - Structured data display (clean key-value pairs)
  - Full transcript view (collapsible)
  - Call metadata (duration, timestamp)

### 4.2 State Management
- React Context or Zustand for global state
- Handle call status polling/webhooks (optional: WebSockets)

## Phase 5: Retell AI Advanced Configuration

### 5.1 Voice Optimization Settings
- **Backchanneling**: Enable natural "uh-huh", "I see" responses
- **Filler Words**: Add "um", "let me see" for human-like pauses
- **Interruption Sensitivity**: High sensitivity for emergency scenarios
- **Voice Selection**: Choose appropriate voice profile
- **Response Latency**: Optimize for natural conversation flow

### 5.2 Dynamic Prompt Engineering
- System prompts for each scenario with clear objectives
- Few-shot examples for extraction tasks
- Emergency trigger phrase list
- Escalation protocols

## Phase 6: Testing & Quality Assurance

### 6.1 Scenario Testing
- Test Scenario 1 with multiple driver response patterns
- Test Scenario 2 with various emergency types
- Test special cases (uncooperative, noisy, conflicting)

### 6.2 Edge Cases
- Invalid phone numbers
- Call failures/timeouts
- Partial data extraction
- Database error handling

### 6.3 Code Quality
- Modular component structure
- Consistent naming conventions
- Error handling and logging
- Type safety (TypeScript)

## Phase 7: Documentation & Deployment

### 7.1 README.md
- Setup instructions
- Environment variable configuration
- How to run locally
- Design decisions and architecture notes
- Additional features implemented (bonus)

### 7.2 Commit History
- Clear, atomic commits with descriptive messages
- Identifiable START commit
- Identifiable END commit

### 7.3 Optional: Demo Video
- Configure an agent via UI
- Trigger a test call
- View and explain structured results

## Key Design Decisions

### Modularity
- Separate concerns: UI components, API routes, database models, AI logic
- Reusable components for different scenarios

### Scalability Considerations
- JSON storage for flexible structured data (varies by scenario)
- Webhook-based architecture for real-time updates
- Database indexes on frequently queried fields

### User Experience
- Simple, intuitive UI for non-technical users
- Clear visual feedback during call processing
- Structured data presented as clean key-value pairs
- Full transcript available but not overwhelming

## Technical Challenges & Solutions

1. **Dynamic Conversation Flow**: Use Retell's webhook system to inject context-aware prompts in real-time
2. **Emergency Detection**: Implement keyword/phrase matching with high interruption sensitivity
3. **Structured Data Extraction**: Use LLM post-processing with schema validation
4. **Call Status Updates**: Poll Retell API or implement webhook listeners for status changes

## Timeline (4 Days)

- **Day 1**: Setup, database design, basic FastAPI endpoints
- **Day 2**: Retell integration, webhook handler, conversation logic
- **Day 3**: Frontend UI, call triggering, results display
- **Day 4**: Testing, refinement, documentation, demo video

## Bonus Features (If Time Permits)

- Call history search/filtering
- Export results to CSV/PDF
- Multiple agent configurations with A/B testing
- Real-time call monitoring dashboard
- Audio playback of calls
- Analytics dashboard (success rates, common issues)
