import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { chat } from '../api/endpoints';

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
    return <div style={{ color: '#00d4ff', padding: '40px' }}>Loading...</div>;
  }

  return (
    <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ color: '#fff' }}>💬 Conversations</h1>
      {conversations.length === 0 ? (
        <p style={{ color: '#606080' }}>No conversations yet.</p>
      ) : (
        <div>
          {conversations.map((conv) => (
            <Link key={conv.id} to={`/chat/${conv.id}`} style={{ textDecoration: 'none', display: 'block', marginBottom: '10px' }}>
              <div style={{ padding: '16px', background: '#12121a', borderRadius: '8px', border: '1px solid #1a1a2e' }}>
                <div style={{ color: '#fff', fontWeight: '600' }}>{conv.title || `Chat ${conv.id}`}</div>
                <div style={{ color: '#606080', fontSize: '12px' }}>{new Date(conv.updated_at).toLocaleDateString()}</div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default Conversations;
