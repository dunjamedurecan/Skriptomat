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

  googleRegister: async ({id_token})=>{
    const response=await apiClient.post('/users/googleregister/',{id_token});
    return response.data;
  },

  googleRegisterComplete: async (userData) => {
    const response = await apiClient.post('/users/googleregister/complete/', userData);
    return response.data;
  }
};

// User Profile API functions (for Buy Me a Coffee feature)
export const userAPI = {
  // Get current user's profile
  getMe: async () => {
    const response = await apiClient.get('/users/me/');
    return response.data;
  },
  
  // Update current user's profile (including PayPal email)
  updateMe: async (data) => {
    const response = await apiClient.patch('/users/me/', data);
    return response.data;
  },
  
  // Get public profile of any user (to check if they accept donations)
  getPublicProfile: async (userId) => {
    const response = await apiClient.get(`/users/profile/${userId}/`);
    return response.data;
  },

  // Get all courses
  getCourses: async () => {
    const response = await apiClient.get('/users/courses/');
    return response.data;
  },

  // Get all faculties
  getFaculties: async () => {
    const response = await apiClient.get('/users/faculties/');
    return response.data;
  },

  // Subscribe to a course
  subscribeCourse: async (courseId) => {
    const response = await apiClient.post(`/users/courses/${courseId}/subscribe/`);
    return response.data;
  },

  // Unsubscribe from a course
  unsubscribeCourse: async (courseId) => {
    const response = await apiClient.post(`/users/courses/${courseId}/unsubscribe/`);
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

  like: async(id)=>{
    const response=await apiClient.post(`/posts/documents/${id}/like/`);
    return response.data;
  },

  
};

export const documentFeedAPI={
  getAll: async () => {
    const response = await apiClient.get('/posts/documents-feed/');
    return response.data;
  },
  approve: async(id)=>{
    const response=await apiClient.post(`/posts/documents-feed/${id}/approve/`);
    return response.data;
  },
  decline: async(id)=>{
    // backend action is named `reject`, not `decline` — use that path
    const response=await apiClient.post(`/posts/documents-feed/${id}/reject/`);
    return response.data;
  }
}
export default authAPI;