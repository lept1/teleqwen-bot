FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install system dependencies (curl is needed to install Ollama)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl ca-certificates git build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama CLI and pull the model used by the project
# Note: the Ollama install script is run non-interactively here.
RUN curl -sSfL https://ollama.com/install.sh | sh

# Download the model referenced in `logic.py` at build time
RUN ollama pull qwen2.5:0.5b

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/requirements.txt
# Ensure aiohttp is available for the health HTTP server
RUN pip install --no-cache-dir -r /app/requirements.txt aiohttp

# Copy application code
COPY . /app

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

CMD ["python", "webhook.py"]
