/**
 * PHANTOMAI SETTINGS PAGE
 * =======================
 * 
 * ARCHITECTURAL IMPORTANCE:
 * This page acts as the "Control Panel" for the user's PhantomAI experience.
 * It connects to your FastAPI backend's `/settings` router to fetch and update
 * user preferences.
 * 
 * HOW IT WORKS:
 * 1. On load (`useEffect`), it fetches current user settings from the backend.
 * 2. The user can update values in the input fields.
 * 3. On "Save Changes", it sends a PUT/POST request to update the backend database.
 * 
 * SCALABILITY NOTE:
 * This component is structured to be easily expanded. You can add new tabs
 * (e.g., "API Keys", "Notifications", "Billing") by simply duplicating the 
 * section patterns below.
 */

import React, { useState, useEffect } from 'react';
// We will use this to talk to the backend
import api from '../services/api'; 

const Settings = () => {
  // --- STATE MANAGEMENT ---
  // We store the user's settings in an object to keep it clean
  const [settings, setSettings] = useState({
    username: '',
    email: '',
    ai_temperature: 0.7, // Default AI randomness
    ai_max_tokens: 2048,  // Default AI response length
  });

  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  /**
   * FETCH SETTINGS ON LOAD
   * ----------------------
   * When the user navigates to this page, we immediately ask the backend 
   * for their current preferences to fill the form.
   * 
   * BACKEND ENDPOINT: GET /settings
   */
  useEffect(() => {
    const fetchSettings = async () => {
      try {
        setIsLoading(true);
        // Make a GET request to your FastAPI backend
        const response = await api.get('/settings');
        
        // Update our state with the backend data
        // Note: Adjust the keys (username, email) to match exactly what your
        // FastAPI `/settings` endpoint returns.
        setSettings({
          username: response.data.username || '',
          email: response.data.email || '',
          ai_temperature: response.data.ai_temperature || 0.7,
          ai_max_tokens: response.data.ai_max_tokens || 2048,
        });
        setMessage({ type: 'success', text: 'Settings loaded successfully.' });
      } catch (err) {
        console.error("Error fetching settings:", err);
        setMessage({ type: 'error', text: 'Failed to load settings. Please refresh the page.' });
      } finally {
        setIsLoading(false);
      }
    };

    fetchSettings();
  }, []);

  /**
   * HANDLE INPUT CHANGES
   * --------------------
   * This function updates the local state whenever the user types in a field.
   * It uses a generic `name` attribute to figure out which field changed.
   */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setSettings((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  /**
   * HANDLE SAVE
   * -----------
   * When the user clicks "Save Changes", we send the updated data to the backend.
   * 
   * BACKEND ENDPOINT: PUT /settings (or POST /settings/update)
   */
  const handleSave = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    setMessage({ type: '', text: '' });

    try {
      // Send the updated settings to your FastAPI backend
      await api.put('/settings', settings);
      
      setMessage({ type: 'success', text: 'Settings saved successfully!' });
      // Auto-clear the success message after 3 seconds
      setTimeout(() => setMessage({ type: '', text: '' }), 3000);
    } catch (err) {
      console.error("Error saving settings:", err);
      setMessage({ type: 'error', text: 'Failed to save settings. Please try again.' });
    } finally {
      setIsSaving(false);
    }
  };

  /**
   * RENDER THE UI
   * -------------
   * The UI uses the exact same dark-glass aesthetic as your Login and Chat pages.
   * This ensures a cohesive PhantomAI user experience.
   */
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'flex-start',
      minHeight: 'calc(100vh - 70px)',
      padding: '40px 20px',
    }}>
      
      {/* --- SETTINGS GLASS CARD --- */}
      <div style={{
        background: 'rgba(18, 18, 26, 0.85)',
        borderRadius: '16px',
        border: '1px solid rgba(26, 26, 46, 0.5)',
        backdropFilter: 'blur(20px)',
        padding: '48px',
        maxWidth: '700px',
        width: '100%',
      }}>
        
        {/* HEADER */}
        <h2 style={{ color: '#ffffff', fontSize: '28px', marginBottom: '8px', fontWeight: '600' }}>
          ⚙️ Settings
        </h2>
        <p style={{ color: '#a0a0b0', fontSize: '14px', marginBottom: '32px' }}>
          Customize your PhantomAI experience. Changes are saved securely.
        </p>

        {/* --- LOADING STATE --- */}
        {isLoading ? (
          <div style={{ color: '#a0a0b0', textAlign: 'center', padding: '40px' }}>
            Loading your settings...
          </div>
        ) : (
          <form onSubmit={handleSave}>
            
            {/* --- USER PROFILE SECTION --- */}
            <div style={{ marginBottom: '32px', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '24px' }}>
              <h3 style={{ color: '#ffffff', fontSize: '18px', marginBottom: '16px' }}>User Profile</h3>
              
              <div style={{ marginBottom: '16px' }}>
                <label style={{ color: '#a0a0b0', fontSize: '13px', display: 'block', marginBottom: '6px' }}>
                  Username
                </label>
                <input
                  type="text"
                  name="username"
                  value={settings.username}
                  onChange={handleChange}
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
                />
              </div>

              <div style={{ marginBottom: '16px' }}>
                <label style={{ color: '#a0a0b0', fontSize: '13px', display: 'block', marginBottom: '6px' }}>
                  Email Address
                </label>
                <input
                  type="email"
                  name="email"
                  value={settings.email}
                  onChange={handleChange}
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
                />
              </div>
            </div>

            {/* --- AI MODEL SETTINGS SECTION --- */}
            <div style={{ marginBottom: '32px' }}>
              <h3 style={{ color: '#ffffff', fontSize: '18px', marginBottom: '16px' }}>AI Model Parameters</h3>
              <p style={{ color: '#606080', fontSize: '13px', marginBottom: '16px' }}>
                These settings control how Qwen3-4B generates responses.
              </p>

              <div style={{ marginBottom: '16px' }}>
                <label style={{ color: '#a0a0b0', fontSize: '13px', display: 'block', marginBottom: '6px' }}>
                  Temperature (Creativity): {settings.ai_temperature}
                </label>
                <input
                  type="range"
                  name="ai_temperature"
                  min="0"
                  max="2"
                  step="0.01"
                  value={settings.ai_temperature}
                  onChange={handleChange}
                  style={{
                    width: '100%',
                    accentColor: '#00d4ff', // Cyan accent for slider
                  }}
                />
                <div style={{ display: 'flex', justifyContent: 'space-between', color: '#606080', fontSize: '11px' }}>
                  <span>Precise</span>
                  <span>Creative</span>
                </div>
              </div>

              <div style={{ marginBottom: '16px' }}>
                <label style={{ color: '#a0a0b0', fontSize: '13px', display: 'block', marginBottom: '6px' }}>
                  Max Tokens (Response Length): {settings.ai_max_tokens}
                </label>
                <input
                  type="range"
                  name="ai_max_tokens"
                  min="256"
                  max="4096"
                  step="64"
                  value={settings.ai_max_tokens}
                  onChange={handleChange}
                  style={{
                    width: '100%',
                    accentColor: '#00d4ff',
                  }}
                />
                <div style={{ display: 'flex', justifyContent: 'space-between', color: '#606080', fontSize: '11px' }}>
                  <span>Short</span>
                  <span>Long</span>
                </div>
              </div>
            </div>

            {/* --- STATUS MESSAGE DISPLAY --- */}
            {message.text && (
              <div style={{
                padding: '12px',
                borderRadius: '8px',
                marginBottom: '20px',
                textAlign: 'center',
                fontSize: '14px',
                background: message.type === 'success' ? 'rgba(0, 212, 255, 0.1)' : 'rgba(255, 0, 0, 0.1)',
                border: message.type === 'success' ? '1px solid rgba(0, 212, 255, 0.2)' : '1px solid rgba(255, 0, 0, 0.2)',
                color: message.type === 'success' ? '#00d4ff' : '#ff6b6b',
              }}>
                {message.text}
              </div>
            )}

            {/* --- SAVE BUTTON --- */}
            <button
              type="submit"
              disabled={isSaving}
              style={{
                width: '100%',
                padding: '14px',
                background: isSaving ? 'rgba(0, 212, 255, 0.3)' : '#00d4ff',
                color: '#12121a',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: '600',
                cursor: isSaving ? 'not-allowed' : 'pointer',
              }}
            >
              {isSaving ? 'Saving Changes...' : 'Save Changes'}
            </button>

          </form>
        )}
      </div>
    </div>
  );
};

export default Settings;