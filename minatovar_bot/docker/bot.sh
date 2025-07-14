#!/bin/bash

# Wait for PostgreSQL to be ready
python src/wait_postgres.py

# Run database migrations
alembic upgrade head

# Start the bot
PYTHONPATH=/app
python src/main.py