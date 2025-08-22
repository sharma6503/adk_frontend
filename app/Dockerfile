# Use a lightweight Python image
FROM python:3.11-slim

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy the entire project first to access requirements.txt
COPY . .

# Then install dependencies (this will still use Docker layer caching effectively)
# Alternatively, if requirements.txt is in a specific subdirectory:
# COPY path/to/requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Cloud Run requires PORT=8080
ENV PORT=8080

# Expose the port
EXPOSE 8080

# If ADK has a runner, use this
# Make sure this command is correct for your application
CMD ["adk", "run", "--host", "0.0.0.0", "--port", "8080"]