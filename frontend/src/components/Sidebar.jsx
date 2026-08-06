import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Sidebar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div style={{
      width: '260px',
      height: '100vh',
      background: 'rgba(10, 10, 15, 0.95)',
      borderRight: '1px solid rgba(26, 26, 46, 0.5)',
      display: 'flex',
      flexDirection: 'column',
      position: 'fixed',
      left: 0,
      top: 0,
      zIndex: 10,
      padding: '20px',
    }}>
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ color: '#00d4ff', fontSize: '24px', fontWeight: '700' }}>🧠 PHANTOMAI</h1>
      </div>

      <nav style={{ flex: 1 }}>
        <Link to="/chat" style={{
          display: 'block',
          padding: '12px 16px',
          color: '#a0a0b0',
          textDecoration: 'none',
          borderRadius: '8px',
          marginBottom: '4px',
          fontSize: '14px',
          fontWeight: '500',
          transition: 'all 0.2s',
        }}>
          💬 New Chat
        </Link>
        <Link to="/conversations" style={{
          display: 'block',
          padding: '12px 16px',
          color: '#a0a0b0',
          textDecoration: 'none',
          borderRadius: '8px',
          marginBottom: '4px',
          fontSize: '14px',
          fontWeight: '500',
          transition: 'all 0.2s',
        }}>
          📂 Conversations
        </Link>
        <Link to="/memory" style={{
          display: 'block',
          padding: '12px 16px',
          color: '#a0a0b0',
          textDecoration: 'none',
          borderRadius: '8px',
          marginBottom: '4px',
          fontSize: '14px',
          fontWeight: '500',
          transition: 'all 0.2s',
        }}>
          🧠 Memory
        </Link>
        <Link to="/tools" style={{
          display: 'block',
          padding: '12px 16px',
          color: '#a0a0b0',
          textDecoration: 'none',
          borderRadius: '8px',
          marginBottom: '4px',
          fontSize: '14px',
          fontWeight: '500',
          transition: 'all 0.2s',
        }}>
          🛠 Tools
        </Link>
        <Link to="/voice" style={{
          display: 'block',
          padding: '12px 16px',
          color: '#a0a0b0',
          textDecoration: 'none',
          borderRadius: '8px',
          marginBottom: '4px',
          fontSize: '14px',
          fontWeight: '500',
          transition: 'all 0.2s',
        }}>
          🎙️ Voice
        </Link>
        <Link to="/settings" style={{
          display: 'block',
          padding: '12px 16px',
          color: '#a0a0b0',
          textDecoration: 'none',
          borderRadius: '8px',
          marginBottom: '4px',
          fontSize: '14px',
          fontWeight: '500',
          transition: 'all 0.2s',
        }}>
          ⚙ Settings
        </Link>
      </nav>

      <div style={{
        paddingTop: '16px',
        borderTop: '1px solid rgba(26, 26, 46, 0.3)',
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          marginBottom: '12px',
        }}>
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            background: '#1a3a6e',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '14px',
            fontWeight: '600',
            color: '#00d4ff',
          }}>
            {user?.full_name?.charAt(0) || 'U'}
          </div>
          <div>
            <div style={{ fontSize: '14px', fontWeight: '600', color: '#ffffff' }}>
              {user?.full_name || 'User'}
            </div>
            <div style={{ fontSize: '12px', color: '#60d060' }}>
              ● Online
            </div>
          </div>
        </div>
        <button onClick={handleLogout} style={{
          width: '100%',
          padding: '8px 16px',
          background: 'rgba(208, 96, 96, 0.15)',
          border: '1px solid rgba(208, 96, 96, 0.2)',
          borderRadius: '8px',
          color: '#d06060',
          fontSize: '13px',
          cursor: 'pointer',
          transition: 'all 0.2s',
        }}>
          Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
