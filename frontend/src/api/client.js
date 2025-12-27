import axios from 'axios';

// Base URL for your Django backend
// DEV: Uses Vite proxy (/api -> http://localhost:8000)
// PROD: Uses full URL from .env.production
const BASE_URL = import.meta.env.VITE_API_URL || (
  import.meta.env.DEV 
    ? '/api'  // Development: Vite proxy
    : 'https://skriptomat-bacend-base.onrender.com/api'  // Production: Render backend
);

console.log(`🔧 Environment: ${import.meta.env.MODE}`);
console.log(`🌐 API Base URL: ${BASE_URL}`);

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for CORS with credentials
  timeout: 10000, // 10 second timeout
});

// Add request/response logging in development
if (import.meta.env.DEV) {
  apiClient.interceptors.request.use((config) => {
    console.log('🚀 API Request:', config.method?.toUpperCase(), config.baseURL + config.url);
    return config;
  });
  
  apiClient.interceptors.response.use(
    (response) => {
      console.log('✅ API Response:', response.config.url, response.status);
      return response;
    },
    (error) => {
      console.error('❌ API Error:', error.config?.url, error.message);
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
      }
      return Promise.reject(error);
    }
  );
}

// Request interceptor - adds auth token to every request
apiClient.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = localStorage.getItem('access_token');
    
    // If token exists, add it to Authorization header
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handles token refresh on 401
apiClient.interceptors.response.use(
  (response) => {
    // If response is successful, just return it
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // If error is 401 (unauthorized) and we haven't tried to refresh yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Get refresh token
        const refreshToken = localStorage.getItem('refresh_token');
        
        if (!refreshToken) {
          // No refresh token, redirect to login
          localStorage.clear();
          window.location.href = '/login';
          return Promise.reject(error);
        }
        
        // Try to refresh the access token
        const response = await axios.post('/api/users/token/refresh/', {
          refresh_token: refreshToken,
        }, {
          withCredentials: true
        });
        
        // Save new tokens
        const { access_token, refresh_token } = response.data;
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        
        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return apiClient(originalRequest);
        
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;