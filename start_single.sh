#!/bin/bash
set -e

echo "Finding and starting Endee Database Server..."
cd /app
BINARY_PATH=$(command -v ndd || command -v ndd-avx2 || command -v ndd-avx512 || command -v endee-server || find /usr /opt /app -name "ndd*" -type f -executable 2>/dev/null | head -n 1)
if [ -z "$BINARY_PATH" ]; then
    echo "Could not find Endee binary!"
    # Fallback just in case
    BINARY_PATH="ndd"
fi
echo "Running $BINARY_PATH..."
export NDD_DATA_DIR="./data"
$BINARY_PATH &

# Wait for the database to be fully up
sleep 10

echo "Populating Endee database with initial data..."
cd /app/demo/ticket_agent
export ENDEE_HOST=http://localhost:8080
python3 data_pipeline.py

echo "Starting Streamlit App..."
# Use the PORT environment variable provided by Render, default to 7860 for Hugging Face Spaces
PORT="${PORT:-7860}"
python3 -m streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
