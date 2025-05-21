#!/bin/bash

# Create and activate virtual environment
uv venv .venv
source .venv/bin/activate  # For Unix/MacOS
# .venv\Scripts\activate  # For Windows

# Install dependencies
uv pip install -r backend/requirements.txt
