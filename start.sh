#!/bin/bash

# Production startup script for Render
echo "Starting Shift Management System..."

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations (if needed)
# python -m app.backend.migrations

# Start the application with gunicorn
gunicorn -w 4 -b 0.0.0.0:$PORT app.backend.app:app
