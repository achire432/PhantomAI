import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import StarfieldBackground from '../components/StarfieldBackground';
import PhantomLogo from '../components/branding/PhantomLogo';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(email, password);
    if (result.success) {
      navigate('/');
    } else {
      setError(result.error || 'Login failed');
      setLoading(false);
    }
  };

  return (
    <>
      <StarfieldBackground />
      <div style={{
        position: 'relative',
        zIndex: 1,
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px',
      }}>
        <div style={{
          background: 'rgba(18, 18, 26, 0.85)',
          borderRadius: '16px',
          border: '1px solid rgba(26, 26, 46, 0.5)',
          backdropFilter: 'blur(20px)',
          padding: '40px',
          maxWidth: '400px',
          width: '100%',
        }}>
          <div style={{ textAlign: 'center', marginBottom: '32px' }}>
            <PhantomLogo variant="full" size="medium" />
            <p style={{ color: '#8080a0', fontSize: '14px', marginTop: '8px' }}>
              Welcome Back
            </p>
          </div>

          {error && (
            <div style={{
              padding: '12px',
              background: 'rgba(208, 96, 96, 0.15)',
              border: '1px solid #d06060',
              borderRadius: '8px',
              color: '#d06060',
              fontSize: '14px',
              marginBottom: '16px',
            }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', color: '#a0a0b0', fontSize: '14px', marginBottom: '6px' }}>
                Email Address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                required
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  background: 'rgba(10, 10, 15, 0.6)',
                  border: '1px solid rgba(26, 26, 46, 0.5)',
                  borderRadius: '8px',
                  color: '#e0e0e0',
                  fontSize: '14px',
                  outline: 'none',
                }}
              />
            </div>

            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', color: '#a0a0b0', fontSize: '14px', marginBottom: '6px' }}>
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  background: 'rgba(10, 10, 15, 0.6)',
                  border: '1px solid rgba(26, 26, 46, 0.5)',
                  borderRadius: '8px',
                  color: '#e0e0e0',
                  fontSize: '14px',
                  outline: 'none',
                }}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              style={{
                width: '100%',
                padding: '14px',
                background: '#00d4ff',
                color: '#0a0a0f',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: 'pointer',
                opacity: loading ? 0.7 : 1,
              }}
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <div style={{ textAlign: 'center', marginTop: '16px' }}>
            <Link to="/register" style={{ color: '#00d4ff', textDecoration: 'none', fontSize: '14px' }}>
              Don't have an account? Sign up
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default Login;
