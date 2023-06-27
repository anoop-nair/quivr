# Wrapper for the supabase client.
# Path: backend/datastores/supabase.py

import os

from logger import get_logger
from supabase import Client, create_client

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")

class SupabaseDatastore:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.supabase_client: Client = create_client(supabase_url, supabase_key)

    def get_client(self):
        return self.supabase_client
