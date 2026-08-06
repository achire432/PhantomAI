/**
 * PHANTOMAI APP
 * =============
 * Purpose: The main application container.
 * 
 * This checks if the user is logged in and shows the right content.
 * If logged in → shows the app with sidebar.
 * If not logged in → shows login/register screen.
 */

import React from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import StarfieldBackground from './components/StarfieldBackground';

function App() {
  const { isAuthenticated } = useAuth();

  // If not authenticated, redirect to login
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // If authenticated, show the app with Starfield background
  return (
    <div style={{ position: 'relative', minHeight: '100vh', display: 'flex' }}>
      <StarfieldBackground />
      <Outlet />
    </div>
  );
}

export default App;
