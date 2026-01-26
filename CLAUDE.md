# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cupid's Matcher is a full-stack web application for managing college dating events. Event organizers ("matchers") create events, manage participant registrations via customizable forms, and create matches between participants.

## Development Commands

### Backend (FastAPI + Supabase)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload          # Start dev server on http://127.0.0.1:8000

# Run test scripts (manual integration tests)
python test_auth_supabase.py           # Test auth flow
python test_events_supabase.py         # Test event operations
python test_venues_supabase.py         # Test venue operations
python test_connection.py              # Test Supabase connection
```

### Frontend (React 19 + Vite)
```bash
cd frontend
npm install
npm run dev      # Start dev server on http://localhost:5173
npm run build    # Production build
npm run lint     # Run ESLint
npm run preview  # Preview production build
```

## Architecture

### Backend Structure
- `main.py` - FastAPI app with CORS middleware, includes all routers prefixed with `/api/`
- `auth.py` - JWT token creation/validation using python-jose, bcrypt password hashing
- `supabase_client.py` - Supabase admin client (bypasses RLS for server operations)
- `crud_supabase.py` - All database operations organized by entity (Matcher, Event, Participant, Venue, FormQuestion, Match)
- `schemas.py` - Pydantic models with validation (Base/Create/Update/Response pattern per entity)
- `routers/` - API endpoints, each router handles one entity type

### Frontend Structure
- `context/AuthContext.jsx` - Global auth state, JWT stored in localStorage
- `services/api.js` - Axios instance with auth interceptor, exports typed API objects (authAPI, eventAPI, venueAPI, participantAPI, formQuestionAPI, matchAPI)
- `components/ProtectedRoute.jsx` - Auth guard for private routes
- `pages/` - Route components, each tied to a specific feature

### Authentication Flow
1. User signs up/logs in via `/api/auth/signup` or `/api/auth/login`
2. Backend returns JWT token + matcher data
3. Frontend stores token in localStorage, adds to all requests via Axios interceptor
4. Protected routes use `get_current_matcher` dependency to validate token

### Data Model Relationships
- Matcher (organizer) -> creates Events
- Event -> has Participants, FormQuestions, Venues, Matches
- Match links two Participants with a compatibility score and optional Venue

## API Conventions

- All routes prefixed with `/api/`
- Protected routes require `Authorization: Bearer <token>` header
- Public endpoints (no auth):
  - `GET /api/events/{id}/public` - Event info for registration page
  - `POST /api/events/{id}/participants/register` - Participant registration
  - `GET /api/events/{id}/form-questions/public` - Active form questions

## Key Patterns

- Backend uses Supabase admin client to bypass RLS (Row Level Security)
- Form answers stored as JSON in participants.form_answers column
- UUIDs used for all entity IDs (Supabase default)
- Event statuses: setup, registration_open, matching_in_progress, completed, cancelled
- Participant statuses: registered, matched, withdrawn, waitlisted

## Environment Variables

### Backend (.env)
```
SUPABASE_URL=your_project_url
SUPABASE_SERVICE_KEY=your_service_role_key
SUPABASE_ANON_KEY=your_anon_key
JWT_SECRET_KEY=your_jwt_secret  # Generate with: openssl rand -hex 32
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```
