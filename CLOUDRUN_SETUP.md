# CloudRun Backend Setup - Summary

## What Was Done

Your ADK frontend project has been configured to connect to your CloudRun backend deployment. Here are the changes made:

### 1. Environment Configuration Files Created

- **`nextjs/.env.local`** - Local environment configuration (you need to set your CloudRun URL here)
- **`nextjs/.env.example`** - Template showing all configuration options
- **`BACKEND_CONFIGURATION.md`** - Detailed documentation for all deployment types

### 2. Configuration System Enhanced

- **Enhanced detection** - Added `CLOUD_RUN_SERVICE_URL` to deployment type detection in `nextjs/src/lib/config.ts`
- **Automatic routing** - Frontend automatically detects CloudRun deployment and routes requests accordingly

### 3. Setup Tools Added

- **`setup-cloudrun.js`** - Interactive setup script to configure CloudRun URL
- **`test-config.js`** - Configuration testing script to verify backend connectivity
- **Helper scripts** - Added to root `package.json` for easier management

## Quick Start

### Option 1: Interactive Setup (Recommended)

```bash
# Run the interactive setup script
npm run setup-cloudrun

# Start the frontend
npm run dev
```

### Option 2: Manual Setup

1. **Get your CloudRun URL** from Google Cloud Console
2. **Create environment file**:
   ```bash
   cp nextjs/.env.example nextjs/.env.local
   ```
3. **Edit `nextjs/.env.local`** and replace `YOUR_CLOUDRUN_URL` with your actual CloudRun service URL:
   ```bash
   CLOUD_RUN_SERVICE_URL=https://your-service-name-abc123-uc.a.run.app
   ```
4. **Test the configuration**:
   ```bash
   npm run test-config
   ```
5. **Start the frontend**:
   ```bash
   npm run dev
   ```

## Available Scripts

From the root directory:

```bash
npm run setup-cloudrun    # Interactive CloudRun setup
npm run test-config       # Test backend configuration
npm run dev              # Start development server
npm run build            # Build for production
npm run start            # Start production server
npm run install-deps     # Install frontend dependencies
```

## How It Works

1. **Environment Detection**: The frontend detects CloudRun deployment when `CLOUD_RUN_SERVICE_URL` is set
2. **Automatic Routing**: All API requests are automatically routed to your CloudRun backend
3. **Health Checks**: Built-in health monitoring ensures backend connectivity
4. **Error Handling**: Comprehensive error handling for network issues

## Configuration Verification

After setup, you should see this in your browser console:

```
🔧 Endpoint Configuration: {
  environment: "local",
  deploymentType: "cloud_run", 
  backendUrl: "https://your-service-url.run.app",
  agentEngineUrl: undefined
}
```

## Troubleshooting

### Backend Not Responding
- Verify your CloudRun URL is correct
- Check that your CloudRun service is running
- Test the backend directly: `https://your-service-url.run.app/health`

### CORS Errors
- Ensure your CloudRun backend allows requests from your frontend domain
- Check network tab in browser dev tools for detailed errors

### Configuration Issues
- Run `npm run test-config` to verify your setup
- Check browser console for configuration logs
- Refer to `BACKEND_CONFIGURATION.md` for detailed troubleshooting

## Production Deployment

Once your local testing is complete, you can deploy the frontend to Cloud Run using GitHub Actions:

### Option 1: GitHub Actions (Recommended)

1. **Set up GitHub Secrets** (see `GITHUB_SECRETS_SETUP.md`):
   - `CLOUD_RUN_BACKEND_URL`: Your backend URL
   - `ADK_APP_NAME`: `upskilling_agent`
   - `GOOGLE_APPLICATION_CREDENTIALS`: Service account JSON
   - `GOOGLE_CLOUD_PROJECT`: Your GCP project ID

2. **Push to main branch**:
   ```bash
   git add .
   git commit -m "Deploy frontend with CloudRun backend integration"
   git push origin main
   ```

3. **Monitor deployment** in GitHub Actions tab

### Option 2: Manual CLI Deployment

```bash
gcloud run deploy adk-frontend \
  --source ./nextjs \
  --region us-central1 \
  --set-env-vars "CLOUD_RUN_SERVICE_URL=your-backend-url,ADK_APP_NAME=upskilling_agent"
```

## Security Notes

- **Never commit `.env.local`** files to version control (already in .gitignore)
- **Use GitHub Secrets** for production environment variables
- **Store sensitive URLs** in secrets, not in YAML files
- Use the `.env.example` template to share configuration structure with team members
- For production deployments, use proper secret management instead of environment files

## Need Help?

1. Check `BACKEND_CONFIGURATION.md` for detailed configuration documentation
2. Check `GITHUB_SECRETS_SETUP.md` for deployment secrets setup
3. Run `npm run test-config` to diagnose local issues
4. Check browser console and network tab for error details
5. Monitor GitHub Actions logs for deployment issues
