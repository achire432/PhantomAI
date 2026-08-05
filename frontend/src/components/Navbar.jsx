/**
 * PHANTOMAI NAVBAR COMPONENT
 * ===========================
 * 
 * ARCHITECTURAL ROLE:
 * This is the "Main Dashboard Hub" for the application. 
 * Because we have now established Routing and Authentication, this component 
 * dynamically changes based on whether a user is logged in.
 * 
 * CRITICAL SCALABILITY NOTES FOR YOUR AI:
 * 1. CONDITIONAL RENDERING: 
 *    - If the user is NOT logged in: It shows "Login" and "Register" buttons.
 *    - If the user IS logged in: It replaces those with "Dashboard", "Chat", 
 *      "Settings", and a "Logout" button. 
 * 
 * 2. CONNECTION TO BACKEND:
 *    - The "Logout" button triggers the `logout()` function from AuthContext.
 *    - This function removes the JWT token from the browser's LocalStorage.
 *    - It does NOT call an API endpoint (like /auth/logout) because JWT is 
 *      stateless—deleting the token on the frontend effectively logs the user out.
 * 
 * 3. FUTURE EXPANSION:
 *    - In a full AI platform, you will add more links here, such as:
 *        - "Memory" (To manage the AI's context memory)
 *        - "Tools" (To configure web search, file upload, etc.)
 *        - "Conversations" (To view chat history sidebar)
 *    - As your app grows, this Navbar will eventually be wrapped in a 
 *      persistent <Sidebar /> component to keep navigation accessible.
 */

import React from 'react';
// React Router hooks: 
// - `Link` replaces `<a>` tags. It prevents the page from reloading 
//   and swaps the content seamlessly using client-side routing.
// - `useNavigate` allows us to programmatically send the user to a 
//   different page (e.g., to the Login page after they log out).
import { Link, useNavigate } from 'react-router-dom';

// Import the global Auth Context we created earlier.
// `useAuth()` gives us access to the current `user` object and the `logout` function.
import { useAuth } from '../context/AuthContext';
import PhantomLogo from './branding/PhantomLogo.jsx';

const Navbar = () => {
  // Destructure the user and logout function from our global context.
  // If `user` is truthy (not null), the user is logged in.
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  // --- LOGOUT HANDLER ---
  // This function connects the frontend Logout button to your backend logic.
  // 1. It calls the `logout()` function from AuthContext.
  // 2. AuthContext clears the JWT token from LocalStorage.
  // 3. The user is now effectively logged out of the browser.
  // 4. `navigate('/login')` redirects them to the login screen immediately.
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    /**
     * NAVBAR CONTAINER
     * ----------------
     * - `position: fixed`: Keeps it pinned to the top of the screen.
     * - `backdropFilter: blur()`: Creates the frosted glass effect.
     * - `zIndex: 999`: Ensures it always floats above other content.
     */
    <nav style={{
      position: 'fixed',
      top: 0, left: 0, right: 0,
      height: '70px',
      backgroundColor: 'rgba(18, 18, 26, 0.7)',
      backdropFilter: 'blur(12px)',
      borderBottom: '1px solid rgba(26, 26, 46, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 40px',
      zIndex: 999,
    }}>
      
      {/* --- LEFT: BRANDING (Logo + Name) --- */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        {/**
         * SCALABILITY NOTE:
         * Currently, this uses the 'small' variant of your logo.
         * In the future, if you want this to function as a "Home" button,
         * wrap this entire <div> inside a <Link to="/"> component.
         */}
        <PhantomLogo variant="full" size="small" />
        <span style={{ color: '#ffffff', fontSize: '20px', fontWeight: '600' }}>
          PhantomAI
        </span>
      </div>

      {/* --- RIGHT: NAVIGATION LINKS & AUTH BUTTONS --- */}
      <div style={{ display: 'flex', gap: '30px', alignItems: 'center' }}>
        
        {/**
         * CONDITIONAL RENDERING LOGIC:
         * If `user` exists (they are logged in), show the App links + Logout.
         * If `user` is null (they are guest), show Login + Register.
         * 
         * This is critical for your AI platform to separate public vs private zones.
         */}
        {user ? (
          <>
            {/* Protected Application Links (Only for logged-in users) */}
            <Link to="/dashboard" style={{ color: '#a0a0b0', textDecoration: 'none' }}>Dashboard</Link>
            <Link to="/chat" style={{ color: '#a0a0b0', textDecoration: 'none' }}>Chat</Link>
            <Link to="/settings" style={{ color: '#a0a0b0', textDecoration: 'none' }}>Settings</Link>
            
            {/* LOGOUT BUTTON */}
            {/**
             * FUTURE SCALABILITY:
             * This is currently a simple text button. In future iterations,
             * you will likely replace this with a "Profile Dropdown" menu
             * that shows the user's avatar, email, and separate "Logout" option.
             */}
            <button 
              onClick={handleLogout}
              style={{
                background: 'transparent',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                color: '#a0a0b0',
                padding: '6px 16px',
                borderRadius: '6px',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
              // On hover, the button will glow slightly cyan to match your branding
              onMouseOver={(e) => e.target.style.borderColor = '#00e5ff'}
              onMouseOut={(e) => e.target.style.borderColor = 'rgba(255, 255, 255, 0.2)'}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            {/* Public Authentication Links (For non-logged-in users) */}
            <Link to="/login" style={{ color: '#a0a0b0', textDecoration: 'none' }}>Login</Link>
            <Link to="/register" style={{ color: '#a0a0b0', textDecoration: 'none' }}>Register</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;