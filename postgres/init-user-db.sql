CREATE USER minatovar WITH PASSWORD 'minatovarshop';
CREATE DATABASE min_db OWNER minatovar;

\connect min_db

ALTER SCHEMA public OWNER TO minatovar;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO minatovar;