import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { chat } from '../api/endpoints';
import StarfieldBackground from '../components/StarfieldBackground';
import Sidebar from '../components/Sidebar';

const Conversations = () => {
  const { token } = useAuth();
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const response = await chat.conversations();
        setConversations(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Failed to fetch:', err);
        setLoading(false);
      }
    };

    if (token) {
      fetchConversations();
    }
  }, [token]);

  if (loading) {
    return (
      <>
        <StarfieldBackground />
        <div style={{ display: 'flex', position: 'relative', zIndex: 1 }}>
          <Sidebar />
          <div style={{ flex: 1, marginLeft: '260px', padding: '40px', background: 'rgba(10,10,15,0.85)', minHeight: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <p style={{ color: '#00d4ff' }}>Loading conversations...</p>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <StarfieldBackground />
      <div style={{ display: 'flex', position: 'relative', zIndex: 1 }}>
        <Sidebar />
        <div style={{
          flex: 1,
          marginLeft: '260px',
          padding: '32px',
          background: 'rgba(10, 10, 15, 0.85)',
          minHeight: '100vh',
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '24px',
          }}>
            <h1 style={{ color: '#fff', fontSize: '24px' }}>💬 Conversations</h1>
            <Link to="/chat" style={{
              padding: '10px 24px',
              background: '#00d4ff',
              color: '#0a0a0f',
              borderRadius: '8px',
              textDecoration: 'none',
              fontWeight: '600',
            }}>
              + New Chat
            </Link>
          </div>

          {conversations.length === 0 ? (
            <p style={{ color: '#606080' }}>No conversations yet. Start a new chat!</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {conversations.map((conv) => (
                <Link key={conv.id} to={`/chat/${conv.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                  <div style={{
                    padding: '12px 16px',
                    background: 'rgba(18,18,26,0.6)',
                    border: '1px solid rgba(26,26,46,0.3)',
                    borderRadius: '8px',
                  }}>
                    <div style={{ color: '#fff', fontWeight: '600' }}>{conv.title || `Chat ${conv.id}`}</div>
                    <div style={{ color: '#606080', fontSize: '12px' }}>{new Date(conv.updated_at).toLocaleDateString()}</div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Conversations;
