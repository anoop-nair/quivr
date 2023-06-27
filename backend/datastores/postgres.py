# Wrapper for the PostgREST client.
# Path: backend/datastores/standalone_postgres.py

import os

from logger import get_logger
from postgrest import SyncPostgrestClient

class PostgresDatastore:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.postgres_client: SyncPostgrestClient = SyncPostgrestClient(base_url="http://dockerhost:4000", schema="quivr")

    def get_client(self):
        return self.postgres_client