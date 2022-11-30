#!/bin/sh
# Initialise the database
python app/init_db_pre.py
# Run Alembic Migrations
alembic upgrade head
# Seed the database
python app/init_db_seed.py