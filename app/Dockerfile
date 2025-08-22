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

# Adjust this command based on your actual application
CMD ["python", "agent_engine_app.py"]