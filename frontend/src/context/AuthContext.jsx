import React, {
  createContext,
  useState,
  useContext,
} from 'react';

import { auth } from '../api/endpoints';

const AuthContext = createContext(null);

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {

  /*
  |--------------------------------------------------------------------------
  | TOKEN
  |--------------------------------------------------------------------------
  |
  | Read the existing token from localStorage when the application starts.
  | This means refreshing the browser doesn't immediately make the user
  | appear logged out.
  |
  */

  const [token, setToken] = useState(
    () => localStorage.getItem('token')
  );

  const [user, setUser] = useState(null);

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
        full_name,
        user_id,
      } = response.data;


      // Save token permanently in browser storage
      localStorage.setItem('token', access_token);

      // Update React state
      setToken(access_token);

      setUser({
        id: user_id,
        full_name,
      });

      return {
        success: true,
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

    setToken(null);

    setUser(null);
  };


  /*
  |--------------------------------------------------------------------------
  | AUTHENTICATION STATUS
  |--------------------------------------------------------------------------
  */

  const isAuthenticated = !!token;


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