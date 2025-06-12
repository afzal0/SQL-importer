-- SQL Script to Enable PostGIS Extension
-- Run this script as a PostgreSQL superuser or database administrator

-- Enable PostGIS extension for the current database
CREATE EXTENSION IF NOT EXISTS postgis;

-- Verify PostGIS is installed
SELECT PostGIS_Version();

-- Grant usage on spatial_ref_sys to public (optional)
GRANT SELECT ON spatial_ref_sys TO PUBLIC;

-- Create a test to confirm PostGIS is working
SELECT ST_AsText(ST_Point(1, 1));

-- List all available spatial functions (optional)
-- SELECT proname FROM pg_proc WHERE proname LIKE 'st_%' LIMIT 10;

-- Success message
SELECT 'PostGIS extension enabled successfully!' AS status;