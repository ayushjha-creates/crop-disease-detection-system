#!/bin/bash
# Helper script to run the backend server
cd "$(dirname "$0")/backend"
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

