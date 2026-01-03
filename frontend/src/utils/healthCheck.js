/**
 * Backend Health Check Utility
 * Checks if the backend is available before making API calls
 */

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '/api';

/**
 * Check if backend is responsive
 * @returns {Promise<boolean>} True if backend is healthy
 */
export const checkBackendHealth = async () => {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout for health check

    const response = await fetch(`${BACKEND_URL}/`, {
      method: 'GET',
      signal: controller.signal,
    });

    clearTimeout(timeoutId);
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ Backend is healthy:', data);
      return true;
    }
    
    console.warn('⚠️ Backend responded but not healthy:', response.status);
    return false;
  } catch (error) {
    if (error.name === 'AbortError') {
      console.error('❌ Backend health check timeout - backend might be sleeping');
    } else {
      console.error('❌ Backend health check failed:', error.message);
    }
    return false;
  }
};

/**
 * Wait for backend to become available (useful for cold starts)
 * @param {number} maxAttempts Maximum number of attempts
 * @param {number} delayMs Delay between attempts in milliseconds
 * @returns {Promise<boolean>} True if backend becomes available
 */
export const waitForBackend = async (maxAttempts = 3, delayMs = 3000) => {
  for (let i = 0; i < maxAttempts; i++) {
    console.log(`🔍 Checking backend availability (attempt ${i + 1}/${maxAttempts})...`);
    
    const isHealthy = await checkBackendHealth();
    
    if (isHealthy) {
      return true;
    }
    
    if (i < maxAttempts - 1) {
      console.log(`⏳ Waiting ${delayMs / 1000} seconds before retry...`);
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }
  
  console.error('❌ Backend is not available after', maxAttempts, 'attempts');
  console.log('💡 Possible reasons:');
  console.log('   - Backend is sleeping (Render free tier sleeps after 15 min inactivity)');
  console.log('   - Backend deployment failed');
  console.log('   - Network connectivity issues');
  console.log('   - Environment variables not set correctly');
  
  return false;
};

export default {
  checkBackendHealth,
  waitForBackend,
};
