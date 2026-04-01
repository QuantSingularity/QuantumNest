-- PostgreSQL bootstrap script
-- Runs once when the DB container is first created.

-- Enable useful extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";   -- for fuzzy text search on symbols/names

-- The actual tables are created by SQLAlchemy init_db() / Alembic migrations.
-- This file is intentionally minimal; add seed data here if needed.

-- Example: create a read-only reporting role
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'reporting') THEN
    CREATE ROLE reporting NOLOGIN;
  END IF;
END
$$;
