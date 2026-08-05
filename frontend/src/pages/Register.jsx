/**
 * PHANTOMAI REGISTER PAGE (UNIVERSAL FIELD FIX)
 * =============================================
 * 
 * CRITICAL BUG FIX:
 * Your backend's Pydantic schema expects 'full_name', NOT 'username'.
 * This file now sends 'full_name' so the backend accepts the data.
 */

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';
import PhantomLogo from '../components/branding/PhantomLogo.jsx';

const Register = () => {
  const navigate = useNavigate();

  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);

    try {
      // SENDING 'full_name' TO MATCH YOUR BACKEND SCHEMA
      await api.post('/auth/register', {
        full_name: fullName,  // <--- CHANGED FROM 'username' TO 'full_name'
        email: email,
        password: password
      });
      
      setTimeout(() => {
        navigate('/login');
      }, 100);
      
    } catch (err) {
      console.error("Registration Error:", err.response?.data);
      setError(err.response?.data?.detail || 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: 'calc(100vh - 70px)',
      padding: '20px',
    }}>
      <div style={{
        background: 'rgba(18, 18, 26, 0.85)',
        borderRadius: '16px',
        border: '1px solid rgba(26, 26, 46, 0.5)',
        backdropFilter: 'blur(20px)',
        padding: '48px',
        maxWidth: '450px',
        width: '100%',
        textAlign: 'center',
      }}>
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '24px' }}>
          <PhantomLogo variant="full" size="medium" />
        </div>
        <h1 style={{ color: '#ffffff', fontSize: '28px', marginBottom: '8px', fontWeight: '600' }}>
          Create Account
        </h1>
        <p style={{ color: '#a0a0b0', fontSize: '14px', marginBottom: '32px' }}>
          Join PhantomAI and unlock the power of Qwen3-4B.
        </p>

        {error && (
          <div style={{
            background: 'rgba(255, 0, 0, 0.1)',
            border: '1px solid rgba(255, 0, 0, 0.2)',
            color: '#ff6b6b',
            padding: '10px',
            borderRadius: '8px',
            marginBottom: '20px',
            fontSize: '14px',
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '16px', textAlign: 'left' }}>
            <label style={{ color: '#a0a0b0', fontSize: '13px', display: 'block', marginBottom: '6px' }}>
              Full Name
            </label>
            <input
              type="text"
              required
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              style={{
                width: '100%',
                padding: '12px',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
                color: '#ffffff',
                fontSize: '16px',
                outline: 'none',
              }}
              placeholder="Enter your full name"
            />
          </div>

          <div style={{ marginBottom: '16px', textAlign: 'left' }}>
            <label style={{ color: '#a0a0b0', fontSize: '13px', display: 'block', marginBottom: '6px' }}>
              Email Address
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{
                width: '100%',
                padding: '12px',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
                color: '#ffffff',
                fontSize: '16px',
                outline: 'none',
              }}
              placeholder="you@example.com"
            />
          </div>

          <div style={{ marginBottom: '16px', textAlign: 'left' }}>
            <label style={{ color: '#a0a0b0', fontSize: '13px', display: 'block', marginBottom: '6px' }}>
              Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{
                width: '100%',
                padding: '12px',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
                color: '#ffffff',
                fontSize: '16px',
                outline: 'none',
              }}
              placeholder="••••••••"
            />
          </div>

          <div style={{ marginBottom: '24px', textAlign: 'left' }}>
            <label style={{ color: '#a0a0b0', fontSize: '13px', display: 'block', marginBottom: '6px' }}>
              Confirm Password
            </label>
            <input
              type="password"
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              style={{
                width: '100%',
                padding: '12px',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
                color: '#ffffff',
                fontSize: '16px',
                outline: 'none',
              }}
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '14px',
              background: loading ? 'rgba(0, 212, 255, 0.3)' : '#00d4ff',
              color: '#12121a',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'background 0.2s',
            }}
          >
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <div style={{ marginTop: '24px', fontSize: '14px', color: '#606080' }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: '#00d4ff', textDecoration: 'none' }}>
            Sign in
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Register;