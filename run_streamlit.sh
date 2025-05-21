#!/bin/bash

# Activate virtual environment
source .venv/bin/activate 2>/dev/null || . .venv/bin/activate || .venv\Scripts\activate

# Start Streamlit app
cd frontend
streamlit run app.py --server.port 3000
