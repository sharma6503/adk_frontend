# Use a lightweight Python image
FROM python:3.11-slim

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python dependencies directly
RUN pip install --no-cache-dir \
    google-adk \
    ddtrace \
    requests \
    python-dotenv
    # Add other dependencies your project needs

# Copy the rest of the code
COPY . .

# Cloud Run requires PORT=8080
ENV PORT=8080

# Expose the port
EXPOSE 8080


CMD ["adk", "run", "--host", "0.0.0.0", "--port", "8080"]
