#!/bin/bash

# Navigate to the backend
cd ~/Desktop/nba_project/nba_backend
nohup uvicorn main:app --reload > /tmp/backend.log 2>&1 &

# Navigate to the frontend
cd ~/Desktop/nba_project/nba_frontend
nohup npm start > /tmp/frontend.log 2>&1 &

# Wait for them to start up
sleep 8

# Open Chrome
open -a "Google Chrome" http://localhost:3000