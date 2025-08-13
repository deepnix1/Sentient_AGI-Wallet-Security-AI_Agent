#!/bin/bash
# Production start script for Sentient Wallet Security AI Agent

# Set environment variables
export FLASK_ENV=production
export FLASK_APP=app.py

# Start the application with Gunicorn
gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app
