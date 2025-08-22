# ---- Base Image ----
FROM python:3.11-slim

# ---- Set working directory ----
WORKDIR /app

# ---- Copy and install Python dependencies ----
# Copies requirements.txt from the repo root
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy all project files from the 'app' directory ----
# Copies your Python code into the container
COPY ./app .

# ---- Expose Port ----
ENV PORT=8080
ENV HOST=0.0.0.0

# ---- Run app ----
CMD ["adk", "run", "--host", "0.0.0.0", "--port", "8080"]