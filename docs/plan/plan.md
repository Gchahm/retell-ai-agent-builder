# AI Voice Agent - High-Level Implementation Plan

## Project Overview
Build a web application for configuring, testing, and reviewing AI voice agent calls for logistics driver check-ins using React, TypeScript, FastAPI, Supabase, and Retell AI.

The system uses a single **"dispatch"** agent that conducts routine status check calls with truck drivers. The agent dynamically branches its conversation based on the driver's status (in-transit vs arrived) and can detect emergencies to transfer to a human dispatcher.

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
- **agent_configurations**: Store prompts, system instructions, Retell settings for the dispatch agent
  - id, name, system_prompt, retell_settings (JSON)
  - Advanced settings: backchanneling, filler words, interruption sensitivity

- **test_calls**: Store call metadata and trigger info
  - id, agent_config_id, driver_name, phone_number, load_number, origin, destination, status, created_at

- **call_results**: Store structured outputs and transcripts
  - id, call_id, transcript, structured_data (JSON), created_at
  - Structured data varies by conversation branch (in-transit vs arrived)

## Phase 3: Backend Development (FastAPI)

### 3.1 Core API Endpoints
- `POST /api/agent-config` - Create/update agent configurations
- `GET /api/agent-config` - List all configurations
- `POST /api/call/trigger` - Initiate test call via Retell API
- `POST /api/webhook/retell` - Receive Retell AI webhooks
- `GET /api/call/{id}/results` - Retrieve structured call results

### 3.2 Retell AI Integration
- Implement webhook handler for real-time conversation guidance
- Dynamic conversation flow based on:
  - Driver status (in-transit vs arrived at destination)
  - Driver responses (determines which conversation branch to follow)
  - Emergency detection (trigger phrase recognition for transfer to human)

### 3.3 Post-Processing Pipeline
- Extract structured data from raw transcripts using LLM (GPT-4/Claude)
- Parse key-value pairs based on scenario requirements
- Store both structured data and full transcript

### 3.4 Dispatch Agent Conversation Logic

The dispatch agent conducts routine status check calls with one of two conversation branches:

- **Branch A: Driver In-Transit or Delayed**
  - Ask open-ended status question to determine driver is on the road
  - Collect current location (highway, mile marker, city)
  - Get ETA to destination
  - Ask about any delays and reasons
  - Remind about POD (Proof of Delivery)
  - Extract: call_outcome, driver_status, current_location, eta, delay_reason, pod_reminder_acknowledged

- **Branch B: Driver Arrived at Destination**
  - Ask open-ended status question to determine driver has arrived
  - Confirm arrival at destination
  - Get unloading status (waiting, assigned to door, in progress)
  - Remind about POD if not yet unloaded
  - Extract: call_outcome, driver_status, current_location, unloading_status, pod_reminder_acknowledged

- **Emergency Detection & Transfer**
  - Continuously monitor for emergency trigger phrases ("blowout", "accident", "breakdown", "medical issue")
  - Immediately call `transfer_call` function to connect to human dispatcher
  - Do not continue with normal conversation flow
  - Priority: safety and immediate escalation

- **Special Cases**
  - Follow-up questions for unclear or vague responses
  - Graceful call termination if wrong person answers or driver unavailable
  - Handle driver questions (next load, detention pay, etc.)

## Phase 4: Frontend Development (React)

### 4.1 Core Pages/Components
- **Dashboard/Home**: Overview of recent calls
- **Agent Configuration Page**:
  - Form to edit dispatch agent system prompt
  - Retell AI settings (backchanneling, filler words, interruption sensitivity, voice selection)
  - Save/update agent configurations

- **Call Trigger Interface**:
  - Input fields: driver name, phone number, load number, origin, destination
  - Agent configuration selector
  - "Start Test Call" button
  - Real-time call status indicator

- **Results Viewer**:
  - Structured data display (clean key-value pairs)
  - Shows which conversation branch was followed (Branch A or B)
  - Full transcript view (collapsible)
  - Call metadata (duration, timestamp)
  - Emergency indicator if call was transferred

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
- System prompt for dispatch agent with clear objectives and branching logic
- Instructions for determining driver status and following appropriate branch
- Emergency trigger phrase list for immediate transfer detection
- Clear data collection requirements for both branches
- Guidelines for handling edge cases and unclear responses

## Phase 6: Testing & Quality Assurance

### 6.1 Agent Testing
- Test Branch A (in-transit) with multiple driver response patterns
  - On-time drivers
  - Delayed drivers with various reasons
  - Vague/unclear responses requiring follow-up
- Test Branch B (arrived) flow
  - Drivers waiting to unload
  - Drivers currently unloading
- Test emergency detection and transfer
  - Various emergency keywords (blowout, accident, breakdown)
  - Verify immediate transfer to human
- Test edge cases
  - Wrong person answers
  - Driver can't talk
  - Driver has questions

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
- Single dispatch agent with modular conversation branches

### Scalability Considerations
- JSON storage for flexible structured data (varies by conversation branch)
- Webhook-based architecture for real-time updates
- Database indexes on frequently queried fields
- Single agent design allows for easy configuration updates without code changes

### User Experience
- Simple, intuitive UI for non-technical users
- Clear visual feedback during call processing
- Structured data presented as clean key-value pairs
- Full transcript available but not overwhelming

## Technical Challenges & Solutions

1. **Dynamic Conversation Branching**: Agent must determine driver status from open-ended responses and follow appropriate branch (A or B)
2. **Emergency Detection & Transfer**: Implement real-time keyword monitoring to immediately call `transfer_call` function when emergency detected
3. **Handling Vague Responses**: Agent must ask follow-up questions when drivers give unclear or incomplete information
4. **Structured Data Extraction**: Use LLM post-processing to extract branch-specific data fields from transcripts
5. **Call Status Updates**: Implement webhook listeners for real-time status changes from Retell AI

## Timeline (4 Days)

- **Day 1**: Setup, database design, basic FastAPI endpoints
- **Day 2**: Retell integration, webhook handler, dispatch agent conversation logic with branching
- **Day 3**: Frontend UI, call triggering, results display with branch indicators
- **Day 4**: Testing all branches and edge cases, refinement, documentation, demo video

## Bonus Features (If Time Permits)

- Call history search/filtering by driver, status, or branch
- Export results to CSV/PDF
- Multiple dispatch agent configurations for A/B testing
- Real-time call monitoring dashboard
- Audio playback of calls
- Analytics dashboard (branch distribution, success rates, emergency detection rates, common delay reasons)
