"""" This module is responsible for creating the datastore client and vectorstore client."""
import os

from langchain.vectorstores.pgvector import PGVector
from langchain.vectorstores import SupabaseVectorStore

from datastores.supabase import SupabaseDatastore
from datastores.postgres import PostgresDatastore
from utils.common import CommonsDep

from logger import get_logger


logger = get_logger(__name__)

datastore_type = os.environ.get("DATASTORE_TYPE")

datastore = None
documents_vectorstore = None
summaries_vectorstore = None


def get_datastore_client():
    """Returns the datastore client."""
    global datastore
    if datastore is None:
        if datastore_type == "supabase":
            logger.info("Using Supabase datastore")
            datastore = SupabaseDatastore()
        elif datastore_type == "postgres":
            logger.info("Using Postgres datastore")
            datastore = PostgresDatastore()
        else:
            raise Exception(f"Unknown datastore type: {datastore_type}")

    return datastore.get_client()


def get_documents_vectorstore():
    """Returns the documents vectorstore client."""
    global documents_vectorstore
    if documents_vectorstore is None:
        if datastore_type == "supabase":
            logger.info("Using Supabase docs vectorstore")
            documents_vectorstore = SupabaseVectorStore(get_datastore_client(), CommonsDep['embeddings'], table_name="vectors")
        elif datastore_type == "postgres":
            logger.info("Using Postgres docs vectorstore")
            documents_vectorstore = PGVector(CommonsDep['postgres_connection_string'], CommonsDep['embeddings'])
        else:
            raise Exception(f"Unknown datastore type: {datastore_type}")

    return documents_vectorstore


def get_summaries_vectorstore():
    """Returns the summaries vectorstore client."""
    global summaries_vectorstore
    if summaries_vectorstore is None:
        if datastore_type == "supabase":
            logger.info("Using Supabase summaries vectorstore")
            summaries_vectorstore = SupabaseVectorStore(get_datastore_client(), CommonsDep['embeddings'], table_name="summaries")
        elif datastore_type == "postgres":
            logger.info("Using Postgres summaries vectorstore")
            summaries_vectorstore = PGVector(CommonsDep['postgres_connection_string'], CommonsDep['embeddings'])
        else:
            raise Exception(f"Unknown datastore type: {datastore_type}")

    return summaries_vectorstore
