# Next Steps After Database Migration

You've successfully run the SQL migration script in Supabase! Here's what to do next:

## Step 1: Create Your Environment Files

### Backend Environment File

1. Copy the example file:
   ```bash
   cd backend
   copy .env.example .env
   ```

2. Open `backend/.env` and add your Supabase credentials:
   ```env
   SUPABASE_URL=https://your-project-ref.supabase.co
   SUPABASE_SERVICE_KEY=eyJhb... (your service_role key)
   SUPABASE_ANON_KEY=eyJhb... (your anon public key)
   ```

3. Get these values from Supabase:
   - Go to your Supabase project dashboard
   - Click **Settings** → **API**
   - Copy the **Project URL**
   - Copy the **anon public** key
   - Copy the **service_role** key (keep this secret!)

### Frontend Environment File

1. Copy the example file:
   ```bash
   cd frontend
   copy .env.example .env
   ```

2. Open `frontend/.env` and add:
   ```env
   VITE_SUPABASE_URL=https://your-project-ref.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhb... (your anon public key)
   VITE_API_URL=http://127.0.0.1:8000
   ```

## Step 2: Test the Connection

Run the test script to verify everything is set up correctly:

```bash
cd backend
python test_supabase_connection.py
```

You should see:
```
✓ Supabase client imported successfully
✓ Supabase admin client created
✓ Successfully connected to Supabase!
  Events table query successful
  Found 0 events

✓ Testing all tables:
  ✓ matchers              - accessible (count: 0)
  ✓ events                - accessible (count: 0)
  ✓ event_matchers        - accessible (count: 0)
  ✓ form_questions        - accessible (count: 0)
  ✓ participants          - accessible (count: 0)
  ✓ exclusions            - accessible (count: 0)
  ✓ venues                - accessible (count: 0)
  ✓ matches               - accessible (count: 0)
  ✓ matching_weights      - accessible (count: 0)

🎉 All tests passed! Supabase is ready to use.
```

## Step 3: Choose Your Migration Path

You have two options:

### Option A: Gradual Migration (Recommended)

Keep your existing FastAPI backend but use Supabase as the database:
- ✅ Less risky
- ✅ Can test incrementally
- ✅ Keep all existing code working
- ✅ Easier rollback if needed

**Next:** Create CRUD operations that use Supabase (see `MIGRATION_GUIDE.md` Phase 1)

### Option B: Full Migration

Replace both database AND authentication with Supabase:
- ⚠️ More changes required
- ⚠️ Need to migrate existing users
- ✅ Get all Supabase features (auth, real-time, etc.)
- ✅ Less backend code to maintain

**Next:** Follow full migration guide (see `MIGRATION_GUIDE.md` Phase 1-4)

## Step 4: Start with One Module (Recommended)

Let's migrate one feature at a time. I suggest starting with **Venues** because:
- ✅ Simple CRUD operations
- ✅ No complex relationships
- ✅ Easy to test
- ✅ Already has a working UI

### Quick Win: Migrate Venues to Supabase

I can help you:

1. Create `crud_supabase.py` with venue operations
2. Update the venues router to use Supabase
3. Test that the venues page works with Supabase
4. Keep all other features using SQLite for now

This lets you verify Supabase works before migrating everything!

## What's Already Done ✓

- [x] SQL migration script created
- [x] Database schema created in Supabase
- [x] Supabase Python client installed
- [x] Supabase JavaScript client installed
- [x] Environment file templates created
- [x] Backend Supabase client configured
- [x] Frontend Supabase client configured
- [x] Connection test script created

## What's Next

1. **Add your Supabase credentials** to `.env` files (both backend and frontend)
2. **Run the test script** to verify connection
3. **Choose migration approach** (gradual vs full)
4. **Start with one module** (I recommend Venues)

## Need Help?

Ask me to:
- "Migrate venues to Supabase" - I'll update just the venues feature
- "Create CRUD operations for Supabase" - I'll create the full CRUD module
- "Update the auth system to use Supabase" - I'll migrate authentication
- "Show me how to use real-time updates" - I'll add live data features

## Helpful Commands

**Test backend connection:**
```bash
cd backend
python test_supabase_connection.py
```

**View Supabase logs:**
- Go to Supabase Dashboard → Logs → API

**Query database directly:**
- Go to Supabase Dashboard → SQL Editor

**View table data:**
- Go to Supabase Dashboard → Table Editor

## Troubleshooting

**"Missing Supabase configuration" error:**
- Make sure you created the `.env` file
- Check that SUPABASE_URL and SUPABASE_SERVICE_KEY are set

**"Connection error" when testing:**
- Verify your credentials are correct
- Check internet connection
- Make sure the migration script ran successfully

**"Table not found" error:**
- Go back to Supabase Dashboard → SQL Editor
- Re-run the `supabase_migration.sql` script

---

**Ready to continue?** Let me know which approach you'd like to take, and I'll help you implement it!
