FROM python:3.10

USER root

# Install system dependencies including sudo since install.sh expects it
RUN apt-get update && apt-get install -y sudo cmake clang build-essential libssl-dev libcurl4-openssl-dev unzip curl git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app/

# Install Endee Database
RUN chmod +x install.sh && ./install.sh --release

# Setup Streamlit App
WORKDIR /app/demo/ticket_agent
RUN pip install --no-cache-dir -r requirements.txt

# Ensure start script is executable
RUN chmod +x /app/start_single.sh

# Expose port (7860 for Hugging Face)
EXPOSE 7860

CMD ["/app/start_single.sh"]
