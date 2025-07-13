#!/bin/bash

python src/wait_postgres.py

alembic upgrade head

PYTHONPATH=/app

python src/main.py