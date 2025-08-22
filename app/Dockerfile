# ---- Base Image ----
FROM python:3.11-slim

# ---- Install system dependencies ----
RUN apt-get update && apt-get install -y \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Set working directory ----
WORKDIR /app

# ---- Copy and install Python dependencies ----
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy all project files ----
COPY . .

# ---- Cloud Run requires PORT=8080 ----
ENV PORT=8080
ENV HOST=0.0.0.0

# ---- Run Google ADK app ----
CMD ["adk", "run", "--host", "0.0.0.0", "--port", "8080"]
