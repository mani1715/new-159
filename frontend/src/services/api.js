import axios from 'axios';

// Ensure the backend URL always uses relative paths to avoid mixed content issues
const getApiBaseUrl = () => {
  const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
  
  console.log('[API Config v2.0] REACT_APP_BACKEND_URL:', backendUrl);
  console.log('[API Config v2.0] Current protocol:', window.location.protocol);
  console.log('[API Config v2.0] Current host:', window.location.host);
  
  // If backendUrl is a relative path (starts with /), just return it
  if (backendUrl && backendUrl.startsWith('/')) {
    console.log('[API Config v2.0] ✅ Using relative URL:', backendUrl);
    return backendUrl;
  }
  
  // If backendUrl is empty, construct relative URL
  if (!backendUrl || backendUrl.trim() === '') {
    console.log('[API Config v2.0] ✅ Using default relative URL: /api');
    return '/api';
  }
  
  // If backendUrl is provided and absolute, ensure it uses HTTPS in production
  let finalUrl = backendUrl;
  
  // Force HTTPS if we're on an HTTPS page
  if (window.location.protocol === 'https:' && finalUrl.startsWith('http://')) {
    finalUrl = finalUrl.replace('http://', 'https://');
    console.log('[API Config v2.0] ⚠️ Forced HTTPS upgrade:', finalUrl);
  }
  
  // Ensure /api suffix
  if (!finalUrl.endsWith('/api')) {
    finalUrl = `${finalUrl}/api`;
  }
  
  console.log('[API Config v2.0] ✅ Final API Base URL:', finalUrl);
  return finalUrl;
};

const API_BASE_URL = getApiBaseUrl();

// Create axios instance with optimized settings
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000, // 15 second default timeout
});

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin_token') || localStorage.getItem('adminToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle response errors with improved logic
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Handle 401 Unauthorized
    if (error.response?.status === 401 && !originalRequest._retry) {
      const currentPath = window.location.pathname;
      
      // If already on login page, don't redirect
      if (currentPath.includes('/admin/login')) {
        return Promise.reject(error);
      }

      // Check if we have a token
      const token = localStorage.getItem('admin_token') || localStorage.getItem('adminToken');
      
      if (!token) {
        // No token, redirect to login
        window.location.href = '/admin/login';
        return Promise.reject(error);
      }

      // If already refreshing, queue the request
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(() => {
          return api(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      // Clear tokens and redirect
      localStorage.removeItem('admin_token');
      localStorage.removeItem('admin_user');
      localStorage.removeItem('adminToken');
      localStorage.removeItem('adminUser');
      
      processQueue(error, null);
      isRefreshing = false;
      
      // Small delay to prevent multiple redirects
      setTimeout(() => {
        window.location.href = '/admin/login';
      }, 100);
      
      return Promise.reject(error);
    }

    // Handle network errors
    if (!error.response) {
      console.error('Network error:', error.message);
      error.message = 'Network error. Please check your connection.';
    }

    return Promise.reject(error);
  }
);

export default api;
