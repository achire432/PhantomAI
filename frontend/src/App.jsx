import React from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import StarfieldBackground from './components/StarfieldBackground';
import Sidebar from './components/Sidebar';

function App() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div style={{ position: 'relative', minHeight: '100vh', display: 'flex' }}>
      <StarfieldBackground />
      <Sidebar />
      <div style={{
        flex: 1,
        marginLeft: '260px',
        background: 'rgba(10, 10, 15, 0.85)',
        minHeight: '100vh',
        overflowY: 'auto',
      }}>
        <Outlet />
      </div>
    </div>
  );
}

export default App;
