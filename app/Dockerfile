# Use a lightweight Python image
FROM python:3.11-slim

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements.txt from repo root
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the repo
COPY . .

# Cloud Run requires PORT=8080
ENV PORT=8080

# Run ADK app
CMD ["adk", "run", "--host", "0.0.0.0", "--port", "8080"]
