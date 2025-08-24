# Backend Configuration Guide

This document explains how to configure the ADK Frontend to connect to different backend deployment types.

## Overview

The ADK Frontend automatically detects the deployment type based on environment variables and routes requests accordingly. Three deployment types are supported:

1. **Local Development Backend** - Backend running locally (default)
2. **Google Cloud Run Backend** - Backend deployed to Cloud Run
3. **Agent Engine Direct** - Direct access to Google Cloud Agent Engine API

## Configuration Options

### 1. Local Development Backend (Default)

For local development with a backend running on your machine:

```bash
# .env.local
BACKEND_URL=http://127.0.0.1:8000
NODE_ENV=development
```

If no environment variables are set, the frontend defaults to `http://127.0.0.1:8000`.

### 2. Google Cloud Run Backend

For connecting to a backend deployed on Google Cloud Run:

```bash
# .env.local
CLOUD_RUN_SERVICE_URL=https://your-service-name-abc123-uc.a.run.app
NODE_ENV=development
```

**To get your Cloud Run URL:**
1. Go to Google Cloud Console
2. Navigate to Cloud Run
3. Find your deployed service
4. Copy the service URL (e.g., `https://your-service-name-abc123-uc.a.run.app`)

### 3. Agent Engine Direct Access

For direct access to Google Cloud Agent Engine API (requires authentication):

```bash
# .env.local
AGENT_ENGINE_ENDPOINT=https://us-central1-aiplatform.googleapis.com/v1/projects/YOUR_PROJECT/locations/us-central1/reasoningEngines/YOUR_ENGINE_ID
GOOGLE_SERVICE_ACCOUNT_KEY_BASE64=your_base64_encoded_service_account_key
NODE_ENV=development
```

## Setup Instructions

### For Cloud Run Backend (Most Common)

1. **Get your Cloud Run service URL** from Google Cloud Console
2. **Create the environment file**:
   ```bash
   cp .env.example .env.local
   ```
3. **Edit `.env.local`** and set your Cloud Run URL:
   ```bash
   CLOUD_RUN_SERVICE_URL=https://your-actual-service-url.run.app
   ```
4. **Start the frontend**:
   ```bash
   npm run dev
   ```

### Verification

1. **Check the configuration logs** in your browser console. You should see:
   ```
   🔧 Endpoint Configuration: {
     environment: "local",
     deploymentType: "cloud_run",
     backendUrl: "https://your-service-url.run.app",
     agentEngineUrl: undefined
   }
   ```

2. **Test the health check** by visiting `/api/health` in your browser or checking the backend health indicator in the UI.

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `BACKEND_URL` | Generic backend URL (local dev) | `http://127.0.0.1:8000` |
| `CLOUD_RUN_SERVICE_URL` | Google Cloud Run service URL | `https://service-abc123-uc.a.run.app` |
| `AGENT_ENGINE_ENDPOINT` | Direct Agent Engine API endpoint | `https://us-central1-aiplatform.googleapis.com/v1/projects/...` |
| `GOOGLE_SERVICE_ACCOUNT_KEY_BASE64` | Base64-encoded service account key | `ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsLi4uCn0K` |
| `NODE_ENV` | Environment mode | `development` or `production` |

## Deployment Detection Logic

The frontend automatically detects deployment type using this priority:

1. **Agent Engine**: If `AGENT_ENGINE_ENDPOINT` is set
2. **Cloud Run**: If `K_SERVICE` or `CLOUD_RUN_SERVICE_URL` is set
3. **Local**: Default fallback

## Troubleshooting

### Common Issues

1. **Backend not responding**: Check that your Cloud Run service URL is correct and the service is running
2. **CORS errors**: Ensure your backend is configured to allow requests from your frontend domain
3. **Authentication errors**: For Agent Engine, verify your service account key is properly base64-encoded

### Debug Steps

1. **Check environment variables** in browser console logs
2. **Test backend directly** by visiting your Cloud Run URL + `/health`
3. **Check network tab** in browser dev tools for failed requests
4. **Verify CORS headers** in the network response

## Security Notes

- Never commit `.env.local` files to version control
- Use `.env.example` as a template for other developers
- For production deployments, use proper secret management instead of environment files
