CREATE USER minatovar WITH PASSWORD 'minatovarshop';
CREATE DATABASE min_db OWNER minatovar;

\connect min_db

ALTER SCHEMA public OWNER TO minatovar;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO minatovar;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO minatovar;