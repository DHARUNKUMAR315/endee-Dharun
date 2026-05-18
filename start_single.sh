#!/bin/bash
set -e

echo "Starting Endee Database Server..."
cd /app
./run.sh &

# Wait for the database to be fully up
sleep 10

echo "Populating Endee database with initial data..."
cd /app/demo/ticket_agent
export ENDEE_HOST=http://localhost:8080
python data_pipeline.py

echo "Starting Streamlit App..."
# Use the PORT environment variable provided by Render, default to 8501
PORT="${PORT:-8501}"
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
