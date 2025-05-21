#!/bin/bash

# Check Python environment
if [ ! -d ".venv" ]; then
    echo "Setting up virtual environment..."
    python -m venv .venv
fi

# Determine OS and activate environment
case "$(uname -s)" in
    Linux*|Darwin*)
        source .venv/bin/activate
        ;;
    MINGW*|CYGWIN*|MSYS*)
        source .venv/Scripts/activate
        ;;
    *)
        .venv\Scripts\activate
        ;;
esac

# Install/update dependencies
pip install -r backend/requirements.txt

# Start FastAPI server with options
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
