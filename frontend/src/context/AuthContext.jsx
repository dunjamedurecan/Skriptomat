import React, { createContext, useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// Create the context
const AuthContext = createContext(null);

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Initialize - check if user is already logged in
  useEffect(() => {
    const initAuth = () => {
      const token = localStorage.getItem('access_token');
      const userData = localStorage.getItem('user');

      if (token && userData) {
        try {
          setUser(JSON.parse(userData));
        } catch (err) {
          console.error('Failed to parse user data:', err);
          logout();
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  // Login function
  const login = (tokens, userData) => {
    // Store tokens
    localStorage.setItem('access_token', tokens.access_token);
    localStorage.setItem('refresh_token', tokens.refresh_token);
    
    // Store user data
    localStorage.setItem('user', JSON.stringify(userData));
    
    // Update state
    setUser(userData);
  };

  // Logout function
  const logout = () => {
    // Clear localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    
    // Clear state
    setUser(null);
    
    // Redirect to login
    navigate('/login');
  };

  // Check if user is authenticated
  const isAuthenticated = () => {
    return !!user && !!localStorage.getItem('access_token');
  };

  // Context value
  const value = {
    user,
    login,
    logout,
    isAuthenticated: isAuthenticated(),
    loading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};