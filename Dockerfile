FROM endeeio/endee-server:latest

USER root

# Disable prompts during apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Try apt-get (Debian/Ubuntu) or apk (Alpine)
RUN if command -v apt-get >/dev/null; then \
        apt-get update && apt-get install -y python3 python3-pip curl git && rm -rf /var/lib/apt/lists/*; \
    elif command -v apk >/dev/null; then \
        apk add --no-cache python3 py3-pip curl git; \
    else \
        echo "Unsupported package manager" && exit 1; \
    fi

# Clear any existing entrypoint from the base image so our CMD runs
ENTRYPOINT []

WORKDIR /app
COPY . /app/

WORKDIR /app/demo/ticket_agent

# Install Python requirements. Try with --break-system-packages for Debian 12+, fallback to normal
RUN pip3 install --no-cache-dir -r requirements.txt || pip3 install --break-system-packages --no-cache-dir -r requirements.txt

RUN chmod +x /app/start_single.sh

EXPOSE 7860

CMD ["/app/start_single.sh"]
