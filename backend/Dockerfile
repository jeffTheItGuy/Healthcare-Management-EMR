FROM python:3.12-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Pre-create HuggingFace cache directory
RUN mkdir -p /root/.cache/huggingface

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

ENV PYTHONPATH=/app
ENV HF_HOME=/root/.cache/huggingface

EXPOSE 8000

# Production default (docker-compose.prod.yml overrides with --workers)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]