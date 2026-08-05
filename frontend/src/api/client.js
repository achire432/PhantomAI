
import axios from 'axios';

// Create a connection to the backend
const api = axios.create({
  baseURL: 'http://localhost:8000',  // Your backend URL
  headers: { 'Content-Type': 'application/json' },
});

// Automatically add the JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// If token expires, redirect to login
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
