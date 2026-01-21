"""Supabase client configuration for backend"""
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Validate configuration
if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise ValueError(
        "Missing Supabase configuration. Please set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env file"
    )

# Service client for admin operations (full access, bypasses RLS)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Anon client for public operations (respects RLS policies)
supabase_anon: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def get_supabase_admin() -> Client:
    """Get Supabase admin client (service role)

    Use this for:
    - Backend API operations
    - Admin tasks
    - Operations that need to bypass RLS
    """
    return supabase_admin


def get_supabase_anon() -> Client:
    """Get Supabase anon client (public role)

    Use this for:
    - Public operations
    - Client-side operations
    - Operations that should respect RLS
    """
    return supabase_anon
