# Supabase Quick Start Guide

Quick reference for getting your Supabase credentials and testing the setup.

## Getting Your Supabase Credentials

### 1. Find Your Project Settings
1. Go to [https://supabase.com/dashboard](https://supabase.com/dashboard)
2. Click on your project
3. Click the **Settings** icon (⚙️) in the left sidebar
4. Click **API**

### 2. Copy These Values

| What You Need | Where to Find It | Goes In |
|---------------|------------------|---------|
| **Project URL** | `URL` field (e.g., `https://xxxxx.supabase.co`) | `SUPABASE_URL` in `.env` |
| **Anon Key** | `Project API keys` → `anon` `public` | `SUPABASE_ANON_KEY` in `.env` |
| **Service Role Key** | `Project API keys` → `service_role` (click to reveal) | `SUPABASE_SERVICE_KEY` in `.env` |

⚠️ **Important:** The `service_role` key is secret - never commit it to git or share it publicly!

### 3. Example .env File

Your `backend/.env` should look like this:

```env
# Supabase Configuration
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjk...
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTY5...

# Legacy Database (keep for now)
DATABASE_URL=sqlite:///./cupids.db

# JWT Secret (keep for now)
SECRET_KEY=your-secret-key-change-this-in-production

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@cupidsmatcher.com
```

Your `frontend/.env` should look like this:

```env
# Supabase Configuration
VITE_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTY5...

# API Configuration
VITE_API_URL=http://127.0.0.1:8000
```

## Testing Your Setup

### Step 1: Create .env Files

```bash
# Backend
cd backend
copy .env.example .env
# Edit .env and add your credentials

# Frontend
cd ../frontend
copy .env.example .env
# Edit .env and add your credentials
```

### Step 2: Run the Test Script

```bash
cd backend
python test_supabase_connection.py
```

### Expected Output

✅ **Success looks like this:**
```
✓ Supabase client imported successfully
✓ Supabase admin client created
✓ Successfully connected to Supabase!
  Events table query successful
  Found 0 events

✓ Testing all tables:
  ✓ matchers              - accessible (count: 0)
  ✓ events                - accessible (count: 0)
  ...

🎉 All tests passed! Supabase is ready to use.
```

❌ **Common Errors:**

**"Missing Supabase configuration"**
- You didn't create the `.env` file
- Fix: Copy `.env.example` to `.env` and add your credentials

**"Connection error"**
- Wrong credentials
- Fix: Double-check you copied the right keys from Supabase dashboard

**"Table not found"**
- Migration script didn't run
- Fix: Go to Supabase Dashboard → SQL Editor → paste and run `supabase_migration.sql`

## Verifying Your Database

### Check Tables Were Created

1. Go to Supabase Dashboard
2. Click **Table Editor** in the left sidebar
3. You should see 9 tables:
   - matchers
   - events
   - event_matchers
   - form_questions
   - participants
   - exclusions
   - venues
   - matches
   - matching_weights

### Run a Test Query

1. Go to **SQL Editor**
2. Run this query:
   ```sql
   SELECT table_name
   FROM information_schema.tables
   WHERE table_schema = 'public'
   ORDER BY table_name;
   ```
3. You should see all 9 tables listed

### Check RLS Policies

1. Go to **Authentication** → **Policies**
2. You should see policies for each table

## What's Next?

Once the test passes, you're ready to:

1. **Start using Supabase** - Begin migrating features one at a time
2. **Test with real data** - Create a test event through the UI
3. **Add real-time features** - Get live updates when data changes

See [NEXT_STEPS.md](NEXT_STEPS.md) for detailed migration instructions.

## Quick Commands

| Action | Command |
|--------|---------|
| Test connection | `cd backend && python test_supabase_connection.py` |
| Start backend | `cd backend && uvicorn app.main:app --reload` |
| Start frontend | `cd frontend && npm run dev` |
| View Supabase logs | Dashboard → Logs → API |
| Query database | Dashboard → SQL Editor |
| View data | Dashboard → Table Editor |

## Security Checklist

- [ ] Created `.env` files in both backend and frontend
- [ ] Added `.env` to `.gitignore` (should already be there)
- [ ] Never committed service_role key to git
- [ ] Using anon key (public) in frontend
- [ ] Using service_role key (secret) only in backend

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Python Client Docs](https://supabase.com/docs/reference/python)
- [JavaScript Client Docs](https://supabase.com/docs/reference/javascript)
- Your migration guide: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)

---

Need help? Just ask! I can:
- Help troubleshoot connection issues
- Migrate specific features to Supabase
- Add real-time updates to your app
- Set up Supabase Auth
