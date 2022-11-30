#!/bin/sh
# This script is run before the database is initialized.
rm -rf *.db.sqlite3
# Initialise the database
python app/init_db_pre.py