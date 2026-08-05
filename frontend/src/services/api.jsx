/**
 * PHANTOMAI API CLIENT
 * ====================
 * This is the central hub for all communication with your FastAPI backend.
 * It sets up Axios to handle requests and automatically attaches the JWT token
 * to every request if the user is logged in.
 * 
 * CRITICAL: We do NOT invent endpoints here. We only use the ones that 
 * already exist in your backend.
 */

import axios from 'axios';

// CHANGE THIS to the actual port your FastAPI backend is running on (usually 8000)
const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// REQUEST INTERCEPTOR: Automatically adds the JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('phantomai_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;