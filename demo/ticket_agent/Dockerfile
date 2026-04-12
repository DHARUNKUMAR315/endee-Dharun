FROM python:3.10

WORKDIR /app

# Upgrade pip to ensure it downloads pre-compiled wheels for heavy ML libraries
RUN pip install --no-cache-dir --upgrade pip

# Copy and install dependencies first
COPY requirements.txt .
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Command to run
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
