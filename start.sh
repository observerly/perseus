#!/bin/sh
# Start the Perseus API server
hypercorn app.main:app --bind '[::]:5000' --reload --workers 1