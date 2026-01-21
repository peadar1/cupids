# Cupid's Matcher

A college cupids matching event management system built with FastAPI, React, and Supabase.

## Features

- **Authentication**: Secure signup and login for event organizers
- **Event Management**: Create and manage matching events
- **Participant Registration**: Public registration form for participants
- **Custom Form Questions**: Create custom questions for participant registration
- **Venue Management**: Add and manage venues with age restrictions
- **Match Generation**: Create and manage matches between participants

## Tech Stack

**Backend:**
- FastAPI (Python web framework)
- Supabase (PostgreSQL database)
- JWT authentication with bcrypt password hashing

**Frontend:**
- React + Vite
- React Router for navigation
- Axios for API calls
- Tailwind CSS for styling

## Prerequisites

- Python 3.8+
- Node.js 16+
- Supabase account

## Setup Instructions

### 1. Supabase Setup

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to the SQL Editor and run the migration script from `supabase_migration.sql`
3. Get your Supabase credentials from Settings → API:
   - Project URL
   - Service Role Key (for backend)
   - Anon/Public Key (for frontend)

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your Supabase credentials:
# SUPABASE_URL=your_project_url
# SUPABASE_SERVICE_KEY=your_service_role_key
# JWT_SECRET_KEY=your_random_secret_key
# JWT_ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Run the server
uvicorn app.main:app --reload
```

Backend will be available at `http://127.0.0.1:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env and add:
# VITE_API_URL=http://127.0.0.1:8000
# VITE_SUPABASE_URL=your_project_url
# VITE_SUPABASE_ANON_KEY=your_anon_key

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

## API Documentation

Visit `http://127.0.0.1:8000/docs` for interactive API documentation (Swagger UI).

## Database Schema

Main tables (all use UUIDs as primary keys):
- `matchers` - Event organizers (with password hashing)
- `events` - Matching events
- `participants` - Event participants
- `venues` - Match venues with capacity tracking
- `form_questions` - Custom registration questions
- `matches` - Participant matches with compatibility scores

## Security Notes

- Never commit `.env` files
- Keep your Supabase service role key secure (backend only)
- Frontend uses anon key with Row Level Security (RLS)
- JWT tokens expire after 7 days by default

## Development Team

Peadar Walsh

## License

[To be determined]
