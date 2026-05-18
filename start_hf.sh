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

echo "Starting Streamlit App on port 7860..."
streamlit run app.py --server.port=7860 --server.address=0.0.0.0
