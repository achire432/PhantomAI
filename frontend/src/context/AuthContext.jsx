import React, {
  createContext,
  useState,
  useContext,
  useEffect,
} from 'react';

import { auth } from '../api/endpoints';

const AuthContext = createContext(null);

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(
    () => localStorage.getItem('token')
  );

  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem('user');

    if (!storedUser) {
      return null;
    }

    try {
      return JSON.parse(storedUser);
    } catch {
      localStorage.removeItem('user');
      return null;
    }
  });

  const [loading, setLoading] = useState(false);

  /*
  |--------------------------------------------------------------------------
  | LOGIN
  |--------------------------------------------------------------------------
  */

  const login = async (email, password) => {
    setLoading(true);

    try {
      const response = await auth.login(email, password);

      const {
        access_token,
        user_id,
        full_name,
        email: returnedEmail,
      } = response.data;

      const userData = {
        id: user_id,
        full_name,
        email: returnedEmail || email,
      };

      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(userData));

      setToken(access_token);
      setUser(userData);

      return {
        success: true,
        data: userData,
      };
    } catch (error) {
      return {
        success: false,
        error:
          error.response?.data?.detail ||
          'Login failed',
      };
    } finally {
      setLoading(false);
    }
  };

  /*
  |--------------------------------------------------------------------------
  | REGISTER
  |--------------------------------------------------------------------------
  */

  const register = async (
    full_name,
    email,
    password
  ) => {
    setLoading(true);

    try {
      const response = await auth.register(
        full_name,
        email,
        password
      );

      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error:
          error.response?.data?.detail ||
          'Registration failed',
      };
    } finally {
      setLoading(false);
    }
  };

  /*
  |--------------------------------------------------------------------------
  | LOGOUT
  |--------------------------------------------------------------------------
  */

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');

    setToken(null);
    setUser(null);
  };

  /*
  |--------------------------------------------------------------------------
  | AUTHENTICATION STATUS
  |--------------------------------------------------------------------------
  */

  const isAuthenticated = Boolean(token);

  /*
  |--------------------------------------------------------------------------
  | PROVIDER
  |--------------------------------------------------------------------------
  */

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        login,
        register,
        logout,
        isAuthenticated,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};