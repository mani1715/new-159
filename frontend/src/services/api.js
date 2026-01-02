import axios from 'axios';

/**
 * API SERVICE – RENDER + VERCEL SAFE (FIXED)
 */

// ⚠️ IMPORTANT: MUST include /api
// Force the correct backend URL with /api prefix
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL 
  ? (process.env.REACT_APP_BACKEND_URL.endsWith('/api') 
      ? process.env.REACT_APP_BACKEND_URL 
      : `${process.env.REACT_APP_BACKEND_URL}/api`)
  : 'https://mspn-dev.onrender.com/api';

if (!BACKEND_URL) {
  console.error('❌ Backend URL not defined');
}

console.log('🔗 API Base URL:', BACKEND_URL);

const api = axios.create({
  baseURL: BACKEND_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
  withCredentials: true,
});

// Attach token automatically
api.interceptors.request.use(
  (config) => {
    const token =
      localStorage.getItem('admin_token') ||
      localStorage.getItem('client_token');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    console.log(
      '[API Request]',
      config.method?.toUpperCase(),
      `${config.baseURL}${config.url}`
    );

    return config;
  },
  (error) => Promise.reject(error)
);

// Global error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error?.response?.data || error.message);

    if (error.response?.status === 401) {
      localStorage.clear();
      window.location.href = '/admin/login';
    }

    return Promise.reject(error);
  }
);

export default api;
