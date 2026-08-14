import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { chat } from '../api/endpoints';
import StarfieldBackground from '../components/StarfieldBackground';
import Sidebar from '../components/Sidebar';

const Chat = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { token } = useAuth();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [conversationTitle, setConversationTitle] = useState('New Chat');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (id && token) {
      fetchConversation(id);
    } else if (!id) {
      setMessages([
        {
          role: 'assistant',
          content: "Hello! I'm PhantomAI. How can I assist you today?",
        },
      ]);
      setLoading(false);
    }
  }, [id, token]);

  const fetchConversation = async (conversationId) => {
    setLoading(true);
    try {
      const response = await chat.getConversation(conversationId);
      const conv = response.data;
      setConversationTitle(conv.title || 'Conversation');
      if (conv.messages && conv.messages.length > 0) {
        setMessages(conv.messages);
      } else {
        setMessages([
          {
            role: 'assistant',
            content: "Welcome back! How can I help you?",
          },
        ]);
      }
    } catch (err) {
      console.error('Failed to load conversation:', err);
      setMessages([
        {
          role: 'assistant',
          content: "Sorry, I couldn't load this conversation. Please try again.",
        },
      ]);
    }
    setLoading(false);
  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || sending) return;

    const userMessage = input.trim();
    setInput('');
    setSending(true);

    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);

    try {
      let conversationId = id;

      if (!conversationId) {
        const createResponse = await chat.createConversation(
          userMessage.slice(0, 50) || 'New Chat'
        );
        conversationId = createResponse.data.id;
        navigate(`/chat/${conversationId}`, { replace: true });
      }

      const response = await chat.sendMessage(conversationId, userMessage);
      const aiMessage = response.data;
      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      console.error('Failed to send message:', err);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
        },
      ]);
    }
    setSending(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (loading) {
    return (
      <>
        <StarfieldBackground />
        <div style={{ display: 'flex', position: 'relative', zIndex: 1 }}>
          <Sidebar />
          <div style={{ flex: 1, marginLeft: '260px', padding: '40px', background: 'rgba(10,10,15,0.85)', minHeight: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <p style={{ color: '#00d4ff' }}>Loading conversation...</p>
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
          display: 'flex',
          flexDirection: 'column',
          height: '100vh',
          background: 'rgba(10,10,15,0.85)',
        }}>
          {/* Header */}
          <div style={{
            padding: '16px 24px',
            borderBottom: '1px solid rgba(26, 26, 46, 0.5)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}>
            <div>
              <h2 style={{ color: '#fff', fontSize: '18px', fontWeight: '600' }}>
                💬 {conversationTitle}
              </h2>
              
            </div>
          </div>

          {/* Messages */}
          <div style={{
            flex: 1,
            overflowY: 'auto',
            padding: '24px',
            display: 'flex',
            flexDirection: 'column',
            gap: '12px',
          }}>
            {messages.map((msg, index) => (
              <div
                key={index}
                style={{
                  display: 'flex',
                  justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                }}
              >
                <div style={{
                  maxWidth: '75%',
                  padding: '12px 16px',
                  borderRadius: '12px',
                  background: msg.role === 'user'
                    ? 'rgba(0, 212, 255, 0.15)'
                    : 'rgba(26, 26, 46, 0.6)',
                  border: msg.role === 'user'
                    ? '1px solid rgba(0, 212, 255, 0.2)'
                    : '1px solid rgba(26, 26, 46, 0.3)',
                }}>
                  <div style={{
                    fontSize: '12px',
                    color: msg.role === 'user' ? '#00d4ff' : '#8080a0',
                    marginBottom: '4px',
                    fontWeight: '500',
                  }}>
                    {msg.role === 'user' ? 'You' : 'PhantomAI'}
                  </div>
                  <div style={{
                    color: '#e0e0e0',
                    fontSize: '14px',
                    lineHeight: '1.6',
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                  }}>
                    {msg.content}
                  </div>
                </div>
              </div>
            ))}
            {sending && (
              <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
                <div style={{
                  padding: '12px 16px',
                  borderRadius: '12px',
                  background: 'rgba(26, 26, 46, 0.6)',
                  border: '1px solid rgba(26, 26, 46, 0.3)',
                }}>
                  <div style={{ color: '#8080a0', fontSize: '14px' }}>
                    PhantomAI is thinking...
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div style={{
            padding: '16px 24px',
            borderTop: '1px solid rgba(26, 26, 46, 0.5)',
            display: 'flex',
            gap: '12px',
            background: 'rgba(10, 10, 15, 0.6)',
          }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask PhantomAI anything..."
              disabled={sending}
              style={{
                flex: 1,
                padding: '12px 16px',
                background: 'rgba(18, 18, 26, 0.6)',
                border: '1px solid rgba(26, 26, 46, 0.5)',
                borderRadius: '10px',
                color: '#e0e0e0',
                fontSize: '14px',
                outline: 'none',
                transition: 'border-color 0.2s',
              }}
              onFocus={(e) => e.target.style.borderColor = '#00d4ff'}
              onBlur={(e) => e.target.style.borderColor = 'rgba(26, 26, 46, 0.5)'}
            />
            <button
              onClick={sendMessage}
              disabled={sending || !input.trim()}
              style={{
                padding: '12px 24px',
                background: '#00d4ff',
                color: '#0a0a0f',
                border: 'none',
                borderRadius: '10px',
                fontSize: '14px',
                fontWeight: '600',
                cursor: sending || !input.trim() ? 'not-allowed' : 'pointer',
                opacity: sending || !input.trim() ? 0.5 : 1,
                transition: 'all 0.2s',
              }}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default Chat;
