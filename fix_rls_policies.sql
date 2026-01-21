-- Fix RLS Policy Infinite Recursion Issue
-- Run this in Supabase SQL Editor

-- Drop problematic policies
DROP POLICY IF EXISTS "Matchers can view their events" ON events;
DROP POLICY IF EXISTS "View event matchers" ON event_matchers;

-- Recreate events policies without recursion
CREATE POLICY "Matchers can view their events" ON events
    FOR SELECT USING (
        creator_id::text = auth.uid()::text
    );

CREATE POLICY "Matchers can create events" ON events
    FOR INSERT WITH CHECK (creator_id::text = auth.uid()::text);

CREATE POLICY "Creators can update their events" ON events
    FOR UPDATE USING (creator_id::text = auth.uid()::text);

CREATE POLICY "Creators can delete their events" ON events
    FOR DELETE USING (creator_id::text = auth.uid()::text);

-- Recreate event_matchers policy without recursion
CREATE POLICY "View event matchers" ON event_matchers
    FOR SELECT USING (
        matcher_id::text = auth.uid()::text
    );

-- For testing with service_role key, you can temporarily disable RLS
-- Uncomment these lines if you want to bypass RLS during development:
-- ALTER TABLE events DISABLE ROW LEVEL SECURITY;
-- ALTER TABLE event_matchers DISABLE ROW LEVEL SECURITY;
-- ALTER TABLE form_questions DISABLE ROW LEVEL SECURITY;
-- ALTER TABLE participants DISABLE ROW LEVEL SECURITY;
-- ALTER TABLE exclusions DISABLE ROW LEVEL SECURITY;
-- ALTER TABLE venues DISABLE ROW LEVEL SECURITY;
-- ALTER TABLE matches DISABLE ROW LEVEL SECURITY;
-- ALTER TABLE matching_weights DISABLE ROW LEVEL SECURITY;
-- ALTER TABLE matchers DISABLE ROW LEVEL SECURITY;

COMMIT;
