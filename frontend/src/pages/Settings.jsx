import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { settings } from '../api/endpoints';

const Settings = () => {
  const { token } = useAuth();
  const [userSettings, setUserSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (!token) return;
    fetchSettings();
  }, [token]);

  const fetchSettings = async () => {
    try {
      const response = await settings.get();
      setUserSettings(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Failed to fetch settings:', err);
      setLoading(false);
    }
  };

  const updateSetting = async (key, value) => {
    setSaving(true);
    try {
      await settings.update({ [key]: value });
      setUserSettings((prev) => ({ ...prev, [key]: value }));
      setMessage('Settings updated successfully!');
      setTimeout(() => setMessage(''), 3000);
    } catch (err) {
      console.error('Failed to update settings:', err);
      setMessage('Failed to update settings');
      setTimeout(() => setMessage(''), 3000);
    }
    setSaving(false);
  };

  const resetSettings = async () => {
    if (!confirm('Reset all settings to defaults?')) return;
    try {
      await settings.reset();
      fetchSettings();
      setMessage('Settings reset successfully!');
      setTimeout(() => setMessage(''), 3000);
    } catch (err) {
      console.error('Failed to reset settings:', err);
      setMessage('Failed to reset settings');
      setTimeout(() => setMessage(''), 3000);
    }
  };

  if (loading) {
    return <div style={{ padding: '40px', color: '#00d4ff' }}>Loading settings...</div>;
  }

  if (!userSettings) {
    return <div style={{ padding: '40px', color: '#d06060' }}>Failed to load settings</div>;
  }

  return (
    <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ color: '#fff', marginBottom: '8px' }}>⚙️ Settings</h1>
      <p style={{ color: '#606080', marginBottom: '24px' }}>Customize your PhantomAI experience.</p>

      {message && (
        <div style={{ padding: '12px', background: 'rgba(0,212,255,0.1)', border: '1px solid rgba(0,212,255,0.3)', borderRadius: '8px', color: '#00d4ff', marginBottom: '16px' }}>
          {message}
        </div>
      )}

      <div style={{ display: 'grid', gap: '20px' }}>
        {/* Assistant Name */}
        <div style={{ padding: '16px', background: 'rgba(18,18,26,0.6)', border: '1px solid rgba(26,26,46,0.3)', borderRadius: '12px' }}>
          <label style={{ display: 'block', color: '#a0a0b0', fontSize: '14px', marginBottom: '6px' }}>Assistant Name</label>
          <input
            type="text"
            value={userSettings.assistant_name || 'PhantomAI'}
            onChange={(e) => setUserSettings({ ...userSettings, assistant_name: e.target.value })}
            style={{
              width: '100%',
              padding: '10px 14px',
              background: 'rgba(10,10,15,0.4)',
              border: '1px solid rgba(26,26,46,0.5)',
              borderRadius: '8px',
              color: '#e0e0e0',
              fontSize: '14px',
              outline: 'none',
            }}
          />
          <button
            onClick={() => updateSetting('assistant_name', userSettings.assistant_name)}
            disabled={saving}
            style={{
              marginTop: '8px',
              padding: '8px 20px',
              background: '#00d4ff',
              color: '#0a0a0f',
              border: 'none',
              borderRadius: '8px',
              fontWeight: '600',
              cursor: 'pointer',
              opacity: saving ? 0.6 : 1,
            }}
          >
            Save
          </button>
        </div>

        {/* Response Style */}
        <div style={{ padding: '16px', background: 'rgba(18,18,26,0.6)', border: '1px solid rgba(26,26,46,0.3)', borderRadius: '12px' }}>
          <label style={{ display: 'block', color: '#a0a0b0', fontSize: '14px', marginBottom: '6px' }}>Response Style</label>
          <select
            value={userSettings.response_style || 'balanced'}
            onChange={(e) => setUserSettings({ ...userSettings, response_style: e.target.value })}
            style={{
              width: '100%',
              padding: '10px 14px',
              background: 'rgba(10,10,15,0.4)',
              border: '1px solid rgba(26,26,46,0.5)',
              borderRadius: '8px',
              color: '#e0e0e0',
              fontSize: '14px',
              outline: 'none',
            }}
          >
            <option value="balanced">Balanced</option>
            <option value="concise">Concise</option>
            <option value="detailed">Detailed</option>
          </select>
          <button
            onClick={() => updateSetting('response_style', userSettings.response_style)}
            disabled={saving}
            style={{
              marginTop: '8px',
              padding: '8px 20px',
              background: '#00d4ff',
              color: '#0a0a0f',
              border: 'none',
              borderRadius: '8px',
              fontWeight: '600',
              cursor: 'pointer',
              opacity: saving ? 0.6 : 1,
            }}
          >
            Save
          </button>
        </div>

        {/* Theme */}
        <div style={{ padding: '16px', background: 'rgba(18,18,26,0.6)', border: '1px solid rgba(26,26,46,0.3)', borderRadius: '12px' }}>
          <label style={{ display: 'block', color: '#a0a0b0', fontSize: '14px', marginBottom: '6px' }}>Theme</label>
          <select
            value={userSettings.theme || 'dark'}
            onChange={(e) => setUserSettings({ ...userSettings, theme: e.target.value })}
            style={{
              width: '100%',
              padding: '10px 14px',
              background: 'rgba(10,10,15,0.4)',
              border: '1px solid rgba(26,26,46,0.5)',
              borderRadius: '8px',
              color: '#e0e0e0',
              fontSize: '14px',
              outline: 'none',
            }}
          >
            <option value="dark">Dark</option>
            <option value="light">Light</option>
            <option value="system">System</option>
          </select>
          <button
            onClick={() => updateSetting('theme', userSettings.theme)}
            disabled={saving}
            style={{
              marginTop: '8px',
              padding: '8px 20px',
              background: '#00d4ff',
              color: '#0a0a0f',
              border: 'none',
              borderRadius: '8px',
              fontWeight: '600',
              cursor: 'pointer',
              opacity: saving ? 0.6 : 1,
            }}
          >
            Save
          </button>
        </div>

        {/* Reset */}
        <div style={{ padding: '16px', background: 'rgba(18,18,26,0.6)', border: '1px solid rgba(26,26,46,0.3)', borderRadius: '12px' }}>
          <div style={{ color: '#fff', fontWeight: '600', marginBottom: '4px' }}>Reset Settings</div>
          <div style={{ color: '#606080', fontSize: '13px', marginBottom: '12px' }}>
            Reset all settings to their default values.
          </div>
          <button
            onClick={resetSettings}
            style={{
              padding: '8px 20px',
              background: 'rgba(208,96,96,0.15)',
              border: '1px solid rgba(208,96,96,0.3)',
              borderRadius: '8px',
              color: '#d06060',
              cursor: 'pointer',
              fontWeight: '600',
            }}
          >
            Reset All
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings;
