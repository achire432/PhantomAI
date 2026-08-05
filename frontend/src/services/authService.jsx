/**
 * PHANTOMAI AUTHENTICATION SERVICE
 * ================================
 * This file interacts directly with your FastAPI backend's auth endpoints.
 * DO NOT change the endpoint strings unless your backend changes.
 */

import api from './api';

export const authService = {
  // POST /auth/login - uses your existing backend
  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    if (response.data.access_token) {
      localStorage.setItem('phantomai_token', response.data.access_token);
    }
    return response.data;
  },

  // POST /auth/register - uses your existing backend
  register: async (email, password, username) => {
    const response = await api.post('/auth/register', { email, password, username });
    return response.data;
  },

  // Logout helper - clears local storage
  logout: () => {
    localStorage.removeItem('phantomai_token');
  },

  // Helper to check if user is currently logged in
  isAuthenticated: () => {
    return !!localStorage.getItem('phantomai_token');
  }
};