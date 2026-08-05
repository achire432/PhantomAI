/**
 * PHANTOMAI LOGIN PAGE
 * ====================
 * 
 * ARCHITECTURAL IMPORTANCE:
 * This is the secure entry point to the PhantomAI platform.
 * It connects directly to your existing FastAPI backend's `/auth/login` endpoint.
 * 
 * HOW IT WORKS:
 * 1. User enters email and password.
 * 2. On submit, the form sends a POST request to `http://localhost:8000/auth/login`.
 * 3. If successful, the backend returns a JWT access_token.
 * 4. The token is saved to the browser's LocalStorage via our `authService`.
 * 5. The user is automatically redirected to the Protected `/dashboard` route.
 * 
 * SCALABILITY NOTE:
 * This component utilizes the `AuthContext` we built in Phase 2.
 * It does NOT handle raw state management; it delegates that to the global Context.
 */

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import PhantomLogo from '../components/branding/PhantomLogo.jsx';

const Login = () => {
  // React Hook to programmatically navigate the user after login
  const navigate = useNavigate();
  
  // Access the global `login` function from our AuthContext
  const { login } = useAuth();

  // Local state to capture user input
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  /**
   * handleSubmit
   * ------------
   * This function is triggered when the user clicks "Sign In".
   * It safely handles the API call and error states.
   */
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevents the browser from refreshing the page
    setError('');
    setLoading(true);

    try {
      // Call the backend via our global authService
      await login(email, password);
      
      // If successful, navigate to the Dashboard
      navigate('/dashboard');
    } catch (err) {
      // Catch the error and display it to the user
      setError(err.response?.data?.detail || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: 'calc(100vh - 70px)', // Account for fixed Navbar
      padding: '20px',
    }}>
      
      {/* THE GLASS LOGIN CARD */}
      <div style={{
        background: 'rgba(18, 18, 26, 0.85)', // Dark translucent background
        borderRadius: '16px', // Rounded corners for modern UI
        border: '1px solid rgba(26, 26, 46, 0.5)', // Subtle glass border
        backdropFilter: 'blur(20px)', // The "frosted glass" effect
        padding: '48px', // Internal spacing
        maxWidth: '450px', // Prevents card from getting too wide on big screens
        width: '100%', // Ensures it takes up available space on mobile
        textAlign: 'center',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.5)', // Dark shadow for depth
      }}>
        
        {/* BRANDING (Logo, Title, Subtitle) */}
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '24px' }}>
          <PhantomLogo variant="full" size="medium" />
        </div>
        <h1 style={{ color: '#ffffff', fontSize: '28px', marginBottom: '8px', fontWeight: '600' }}>
          Welcome Back
        </h1>
        <p style={{ color: '#a0a0b0', fontSize: '14px', marginBottom: '32px' }}>
          Enter your credentials to access your PhantomAI workspace.
        </p>

        {/* ERROR DISPLAY - Shows if user enters wrong password */}
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

        {/* LOGIN FORM */}
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '20px', textAlign: 'left' }}>
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
                transition: 'border-color 0.2s',
              }}
              placeholder="you@example.com"
            />
          </div>

          <div style={{ marginBottom: '24px', textAlign: 'left' }}>
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
                transition: 'border-color 0.2s',
              }}
              placeholder="••••••••"
            />
          </div>

          {/* SIGN IN BUTTON */}
          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '14px',
              background: loading ? 'rgba(0, 212, 255, 0.3)' : '#00d4ff', // Cyan color matching your logo
              color: '#12121a',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'background 0.2s, transform 0.1s',
            }}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        {/* FOOTER LINK */}
        <div style={{ marginTop: '24px', fontSize: '14px', color: '#606080' }}>
          Don't have an account?{' '}
          <Link to="/register" style={{ color: '#00d4ff', textDecoration: 'none' }}>
            Sign up
          </Link>
        </div>

      </div>
    </div>
  );
};

export default Login;