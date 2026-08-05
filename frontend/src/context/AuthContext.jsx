/**
 * PHANTOMAI AUTH CONTEXT
 * ======================
 * This provides a global "User" state to the entire application.
 * Any page can check `if (user)` to know if someone is logged in.
 * This is the foundation for Protected Routes.
 */

import React, { createContext, useState, useContext, useEffect } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // On app start, check if user has a token stored in browser
  useEffect(() => {
    if (authService.isAuthenticated()) {
      // In a real scenario, you would call a '/auth/me' endpoint here 
      // to fetch the actual user's name/email from the token.
      // For now, we just set a placeholder user to indicate they are logged in.
      setUser({ isLoggedIn: true });
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const data = await authService.login(email, password);
    // Here you would update the user state with the info returned from backend
    setUser({ isLoggedIn: true, email });
    return data;
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  const value = { user, login, logout, loading };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};