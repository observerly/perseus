#!/bin/sh
# Start the Perseus API server
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload --workers 1