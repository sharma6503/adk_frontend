# GitHub Secrets Setup Guide

To deploy your ADK Frontend using GitHub Actions, you need to configure the following secrets in your GitHub repository.

## How to Add GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Add each secret below

## Required Secrets

### Google Cloud Authentication
| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Service account JSON key (base64 encoded or full JSON) | `{"type": "service_account", ...}` |
| `GOOGLE_CLOUD_PROJECT` | Your Google Cloud project ID | `agents-466910` |

### Backend Configuration (SECURE)
| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `CLOUD_RUN_BACKEND_URL` | Your CloudRun backend service URL | `https://adk-backend-aug23-310799546989.us-central1.run.app` |
| `ADK_APP_NAME` | The app name in your backend | `upskilling_agent` |

### Optional Legacy Secrets (if still needed)
| Secret Name | Description |
|-------------|-------------|
| `GOOGLE_CLOUD_LOCATION` | GCP region (if needed by other services) |
| `GOOGLE_CLOUD_STAGING_BUCKET` | Storage bucket (if needed) |
| `GOOGLE_GENAI_USE_VERTEXAI` | Vertex AI flag (if needed) |

## Security Best Practices

✅ **DO:**
- Store all sensitive URLs and configuration in GitHub Secrets
- Use descriptive secret names
- Regularly rotate service account keys
- Use least-privilege IAM roles

❌ **DON'T:**
- Hardcode URLs or credentials in YAML files
- Commit secrets to the repository
- Share service account keys outside of secure channels

## Current Setup

Your workflow now uses these secrets:
```yaml
--set-env-vars "CLOUD_RUN_SERVICE_URL=${{ secrets.CLOUD_RUN_BACKEND_URL }},ADK_APP_NAME=${{ secrets.ADK_APP_NAME }},NODE_ENV=production"
```

## Values to Set

Based on your current configuration, set these values:

### CLOUD_RUN_BACKEND_URL
```
https://adk-backend-aug23-310799546989.us-central1.run.app
```

### ADK_APP_NAME
```
upskilling_agent
```

## Deployment Trigger

The workflow triggers on pushes to the `main` branch:
- Push your changes to `main` branch
- GitHub Actions will automatically build and deploy
- Check the **Actions** tab for deployment status

## Troubleshooting

1. **Authentication Issues**: Verify `GOOGLE_APPLICATION_CREDENTIALS` and `GOOGLE_CLOUD_PROJECT`
2. **Build Failures**: Check the Actions logs for specific error messages  
3. **Runtime Issues**: Verify `CLOUD_RUN_BACKEND_URL` and `ADK_APP_NAME` are correct
