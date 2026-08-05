/**
 * PHANTOMAI APPLICATION ROUTING SYSTEM
 * ====================================
 * 
 * ARCHITECTURAL IMPORTANCE:
 * This file is the "Traffic Controller" for PhantomAI.
 * 
 * It determines exactly what the user sees on their screen based on the URL 
 * they type into the browser (e.g., /login, /chat, /settings).
 * 
 * It works hand-in-hand with the AuthContext to provide strict security.
 * 
 * SCALABILITY & SECURITY NOTES FOR YOUR AI PLATFORM:
 * 
 * 1. PUBLIC ROUTES:
 *    - Routes like "/login" and "/register" are "Public".
 *    - ANYONE can access these pages, even if they aren't logged in.
 *    - This is necessary so new users can create accounts.
 * 
 * 2. PROTECTED ROUTES (The Guardian System):
 *    - Routes like "/chat", "/dashboard", and "/settings" are "Protected".
 *    - To access these, the user MUST be logged in.
 *    - We achieve this using a wrapper component called `<ProtectedRoute />`.
 * 
 * 3. HOW THE PROTECTED ROUTE WORKS:
 *    - The `<ProtectedRoute>` component checks the global `useAuth()` state.
 *    - `if (user)` is true: The user is logged in. We render the requested page (Children).
 *    - `if (!user)` is false: The user is NOT logged in. We FORCE them to `/login`.
 *    - This prevents unauthorized users from seeing the AI Chat or Dashboard.
 * 
 * 4. FALLBACK ROUTES (The Safety Net):
 *    - If a user types a random URL that doesn't exist (like /about), 
 *      the "*" (wildcard) route catches them and redirects them to "/dashboard".
 *    - If a user just goes to the root "/" of the website, we also redirect 
 *      them to "/dashboard" (assuming they are logged in, otherwise they 
 *      will be bounced back to the Login page by the `ProtectedRoute`).
 * 
 * 5. FUTURE EXPANSION:
 *    - As PhantomAI grows, you will add more routes here:
 *        - `/conversations` (To view chat history)
 *        - `/memory` (To manage AI long-term memory)
 *        - `/tools` (To configure web search / file uploads)
 *    - You simply add a new `<Route>` block under the Protected Routes section.
 */

import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// --- IMPORT YOUR REAL PAGES ---
// These are the actual screens the user will see.
import Login from '../pages/Login';
import Chat from '../pages/Chat';
import Settings from '../pages/Settings';
import Register from '../pages/Register';
 // <--- IMPORTED HERE

/**
 * PLACEHOLDER PAGES (Temporary)
 * -----------------------------
 * These are just temporary "Coming Soon" pages so your app doesn't crash.
 * 
 * SCALABILITY ACTION:
 * As soon as you create the real files, replace these imports.
 */
const Dashboard = () => <div style={{ color: 'white', paddingTop: '100px', textAlign: 'center' }}>Dashboard Page Coming Soon</div>;
// NOTE: The "Settings" placeholder was REMOVED here because we imported it above.

/**
 * PROTECTED ROUTE WRAPPER
 * =======================
 * This is a "Guardian" component. It wraps around any page that requires 
 * a user to be logged in.
 * 
 * HOW IT WORKS:
 * 1. We use `useAuth()` to get the current `user` state from the global context.
 * 2. We check if the `user` exists (is logged in).
 * 3. If YES: We return the `{children}` (which is the page they asked for, 
 *    like Dashboard, Chat, or Settings).
 * 4. If NO: We return `<Navigate to="/login" replace />`. 
 *    This instantly redirects them to the Login page. The `replace` attribute 
 *    prevents them from using the "Back" button to go back to the private page.
 */
const ProtectedRoute = ({ children }) => {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" replace />;
};

const AppRoutes = () => {
  return (
    <Routes>
      {/* --- PUBLIC ROUTES (Anyone can see these) --- */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* 
        --- PROTECTED ROUTES (Require Login) --- 
        NOTE: For any route inside this block, we wrap the `<Page />` inside
        the `<ProtectedRoute>` component. This acts as a security gate.
      */}
      <Route 
        path="/dashboard" 
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/chat" 
        element={
          <ProtectedRoute>
            <Chat />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/settings" 
        element={
          <ProtectedRoute>
            <Settings /> {/* Uses the imported Settings component */}
          </ProtectedRoute>
        } 
      />

      <Route path="/register" element={<Register />} />

      {/* 
        --- FALLBACK / REDIRECTS --- 
        If the user goes to an unknown URL, or the root "/", we send them to 
        the Dashboard. (If they aren't logged in, the Dashboard's ProtectedRoute 
        will automatically bounce them back to Login).
      */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
};

export default AppRoutes;