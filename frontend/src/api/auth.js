import apiClient from './client';

// Authentication API functions
export const authAPI = {
  // Register new user
  register: async (userData) => {
    const response = await apiClient.post('/users/register/', userData);
    return response.data;
  },
  
  // Login user
  login: async (credentials) => {
    const response = await apiClient.post('/users/login/', credentials);
    return response.data;
  },
  
  // Refresh token
  refreshToken: async (refreshToken) => {
    const response = await apiClient.post('/users/token/refresh/', {
      refresh_token: refreshToken,
    });
    return response.data;
  },
  google: async ({ id_token }) => {
    const response = await apiClient.post('/users/google/', { id_token });
    return response.data;
  },
};

// Document API functions
export const documentsAPI = {
  // Get all documents
  getAll: async () => {
    const response = await apiClient.get('/posts/documents/');
    return response.data;
  },
  
  // Upload document
  upload: async (formData) => {
    const response = await apiClient.post('/posts/documents/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export default authAPI;