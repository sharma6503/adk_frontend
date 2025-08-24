#!/usr/bin/env node

/**
 * Configuration Test Script
 * 
 * This script tests the backend configuration without starting the full Next.js app.
 * Run this to verify your environment variables are set correctly.
 */

// Load environment variables from .env.local
require('dotenv').config({ path: './nextjs/.env.local' });

console.log('🔍 ADK Frontend Configuration Test');
console.log('=====================================\n');

// Test environment variable detection
console.log('📋 Environment Variables:');
console.log(`CLOUD_RUN_SERVICE_URL: ${process.env.CLOUD_RUN_SERVICE_URL || 'NOT SET'}`);
console.log(`BACKEND_URL: ${process.env.BACKEND_URL || 'NOT SET'}`);
console.log(`AGENT_ENGINE_ENDPOINT: ${process.env.AGENT_ENGINE_ENDPOINT || 'NOT SET'}`);
console.log(`NODE_ENV: ${process.env.NODE_ENV || 'NOT SET'}\n`);

// Simulate deployment type detection
function detectDeploymentType() {
  if (process.env.AGENT_ENGINE_ENDPOINT) {
    return 'agent_engine';
  }
  
  if (process.env.K_SERVICE || process.env.CLOUD_RUN_SERVICE || process.env.CLOUD_RUN_SERVICE_URL) {
    return 'cloud_run';
  }
  
  return 'local';
}

function getBackendUrl() {
  const deploymentType = detectDeploymentType();
  
  switch (deploymentType) {
    case 'agent_engine':
      if (process.env.AGENT_ENGINE_ENDPOINT) {
        return process.env.AGENT_ENGINE_ENDPOINT;
      }
      throw new Error('AGENT_ENGINE_ENDPOINT environment variable is required for Agent Engine deployment');
    
    case 'cloud_run':
      if (process.env.CLOUD_RUN_SERVICE_URL) {
        return process.env.CLOUD_RUN_SERVICE_URL;
      }
      break;
    
    case 'local':
    default:
      return process.env.BACKEND_URL || 'http://127.0.0.1:8000';
  }
  
  return process.env.BACKEND_URL || 'http://127.0.0.1:8000';
}

const deploymentType = detectDeploymentType();
const backendUrl = getBackendUrl();

console.log('🚀 Detected Configuration:');
console.log(`Deployment Type: ${deploymentType}`);
console.log(`Backend URL: ${backendUrl}\n`);

// Test backend connectivity
async function testBackendConnection() {
  console.log('🔗 Testing Backend Connection...');
  
  try {
    const healthUrl = `${backendUrl}/health`;
    console.log(`Testing: ${healthUrl}`);
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
    
    const response = await fetch(healthUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'ADK-Config-Test'
      },
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    if (response.ok) {
      console.log('✅ Backend connection successful!');
      console.log(`   Status: ${response.status} ${response.statusText}`);
      
      // Try to read the response
      try {
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          const data = await response.json();
          console.log('   Response:', JSON.stringify(data, null, 2));
        } else {
          const text = await response.text();
          console.log('   Response:', text.substring(0, 200));
        }
      } catch (err) {
        console.log('   (Unable to read response body)');
      }
    } else {
      console.log('❌ Backend returned error status:');
      console.log(`   Status: ${response.status} ${response.statusText}`);
      
      try {
        const errorText = await response.text();
        console.log(`   Error: ${errorText.substring(0, 500)}`);
      } catch (err) {
        console.log('   (Unable to read error response)');
      }
    }
  } catch (error) {
    if (error.name === 'AbortError') {
      console.log('❌ Connection timeout (10 seconds)');
      console.log('   Your backend might be slow to respond or not running');
    } else if (error.message.includes('fetch')) {
      console.log('❌ Network error - unable to connect to backend');
      console.log(`   Error: ${error.message}`);
      console.log('   Check that your backend URL is correct and the service is running');
    } else {
      console.log('❌ Unexpected error:');
      console.log(`   Error: ${error.message}`);
    }
  }
}

// Run the test
testBackendConnection().then(() => {
  console.log('\n🏁 Configuration test complete!');
  console.log('\nNext steps:');
  console.log('1. If the connection test passed, run: npm run dev');
  console.log('2. If it failed, check your CLOUD_RUN_SERVICE_URL in .env.local');
  console.log('3. Verify your Cloud Run service is running and accessible');
}).catch(error => {
  console.error('Test failed:', error);
  process.exit(1);
});
