import React, { createContext, useState, useContext } from 'react';
import { auth } from '../api/endpoints';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const response = await auth.login(email, password);
      const { access_token, full_name, user_id } = response.data;
      localStorage.setItem('token', access_token);
      setUser({ id: user_id, full_name });
      setLoading(false);
      return { success: true };
    } catch (error) {
      setLoading(false);
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  };

  const register = async (full_name, email, password) => {
    setLoading(true);
    try {
      const response = await auth.register(full_name, email, password);
      setLoading(false);
      return { success: true, data: response.data };
    } catch (error) {
      setLoading(false);
      return { success: false, error: error.response?.data?.detail || 'Registration failed' };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const isAuthenticated = !!localStorage.getItem('token');

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};
