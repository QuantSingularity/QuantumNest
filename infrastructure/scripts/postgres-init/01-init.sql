-- QuantumNest PostgreSQL Initialization Script
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Create application schema
CREATE SCHEMA IF NOT EXISTS quantumnest;

-- Set default search path
ALTER DATABASE quantumnest SET search_path TO quantumnest, public;

-- Create read-only role for reporting
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'quantumnest_readonly') THEN
    CREATE ROLE quantumnest_readonly;
  END IF;
END$$;

GRANT CONNECT ON DATABASE quantumnest TO quantumnest_readonly;
GRANT USAGE ON SCHEMA quantumnest TO quantumnest_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA quantumnest GRANT SELECT ON TABLES TO quantumnest_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA quantumnest GRANT SELECT ON SEQUENCES TO quantumnest_readonly;

-- Enable row-level security for compliance
ALTER DATABASE quantumnest SET row_security = on;
