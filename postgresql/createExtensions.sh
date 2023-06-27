#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname="$POSTGRES_DB"<<-EOSQL
   DROP SCHEMA IF EXISTS public;
    CREATE SCHEMA IF NOT EXISTS quivr;
   ALTER DATABASE quivr SET search_path TO quivr;
   CREATE EXTENSION IF NOT EXISTS pgcrypto;
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
   CREATE EXTENSION IF NOT EXISTS vector;
EOSQL