import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

import { useAuth } from './context/AuthContext';

import StarfieldBackground from './components/StarfieldBackground';
import Sidebar from './components/Sidebar';

const App = () => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        position: 'relative',
        background: '#050509',
        color: '#ffffff',
      }}
    >
      <StarfieldBackground />

      <div
        style={{
          position: 'relative',
          zIndex: 1,
          minHeight: '100vh',
        }}
      >
        <Sidebar />

        <main
          style={{
            marginLeft: '260px',
            minHeight: '100vh',
            position: 'relative',
          }}
        >
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default App;