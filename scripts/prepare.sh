#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python app/db_setup.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python app/db_seed.py
