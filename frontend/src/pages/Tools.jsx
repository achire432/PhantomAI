import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { tools } from '../api/endpoints';

const Tools = () => {
  const { token } = useAuth();
  const [notes, setNotes] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [weather, setWeather] = useState('');
  const [city, setCity] = useState('Kampala');
  const [loading, setLoading] = useState({ notes: true, tasks: true });
  const [activeTool, setActiveTool] = useState('notes');

  useEffect(() => {
    if (!token) return;
    fetchNotes();
    fetchTasks();
  }, [token]);

  const fetchNotes = async () => {
    try {
      const response = await tools.notes.getAll();
      setNotes(response.data);
      setLoading((prev) => ({ ...prev, notes: false }));
    } catch (err) {
      console.error('Failed to fetch notes:', err);
      setLoading((prev) => ({ ...prev, notes: false }));
    }
  };

  const fetchTasks = async () => {
    try {
      const response = await tools.tasks.getAll();
      setTasks(response.data);
      setLoading((prev) => ({ ...prev, tasks: false }));
    } catch (err) {
      console.error('Failed to fetch tasks:', err);
      setLoading((prev) => ({ ...prev, tasks: false }));
    }
  };

  const getWeather = async () => {
    try {
      const response = await tools.weather(city);
      setWeather(response.data);
    } catch (err) {
      console.error('Failed to get weather:', err);
      setWeather({ error: 'Failed to get weather' });
    }
  };

  const toolsList = [
    { id: 'notes', name: '📝 Notes', description: 'Save and retrieve notes' },
    { id: 'tasks', name: '✅ Tasks', description: 'Manage your tasks' },
    { id: 'weather', name: '🌤️ Weather', description: 'Check weather anywhere' },
    { id: 'calculator', name: '🧮 Calculator', description: 'Math operations' },
    { id: 'calendar', name: '📅 Calendar', description: 'Manage events' },
    { id: 'reminders', name: '⏰ Reminders', description: 'Set reminders' },
    { id: 'git', name: '📂 Git', description: 'Git status and logs' },
    { id: 'system', name: '💻 System Info', description: 'CPU, RAM, Disk' },
  ];

  return (
    <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ color: '#fff', marginBottom: '8px' }}>🛠 Tools</h1>
      <p style={{ color: '#606080', marginBottom: '24px' }}>All PhantomAI tools in one place.</p>

      {/* Tools Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px', marginBottom: '32px' }}>
        {toolsList.map((tool) => (
          <button
            key={tool.id}
            onClick={() => setActiveTool(tool.id)}
            style={{
              padding: '16px',
              background: activeTool === tool.id ? 'rgba(0,212,255,0.15)' : 'rgba(18,18,26,0.6)',
              border: activeTool === tool.id ? '1px solid rgba(0,212,255,0.3)' : '1px solid rgba(26,26,46,0.3)',
              borderRadius: '10px',
              color: activeTool === tool.id ? '#00d4ff' : '#a0a0b0',
              cursor: 'pointer',
              textAlign: 'left',
              transition: 'all 0.2s',
            }}
          >
            <div style={{ fontSize: '20px' }}>{tool.name}</div>
            <div style={{ fontSize: '12px', color: '#606080', marginTop: '4px' }}>{tool.description}</div>
          </button>
        ))}
      </div>

      {/* Tool Content */}
      <div style={{ padding: '20px', background: 'rgba(18,18,26,0.4)', borderRadius: '12px', border: '1px solid rgba(26,26,46,0.3)' }}>
        {activeTool === 'notes' && (
          <div>
            <h3 style={{ color: '#fff', marginBottom: '12px' }}>📝 Notes</h3>
            {loading.notes ? (
              <p style={{ color: '#606080' }}>Loading notes...</p>
            ) : notes.length === 0 ? (
              <p style={{ color: '#606080' }}>No notes yet.</p>
            ) : (
              notes.map((note) => (
                <div key={note.id} style={{ padding: '12px', background: 'rgba(10,10,15,0.4)', borderRadius: '6px', marginBottom: '8px' }}>
                  <div style={{ color: '#fff', fontWeight: '600' }}>{note.title}</div>
                  <div style={{ color: '#a0a0b0', fontSize: '13px' }}>{note.content}</div>
                </div>
              ))
            )}
          </div>
        )}

        {activeTool === 'tasks' && (
          <div>
            <h3 style={{ color: '#fff', marginBottom: '12px' }}>✅ Tasks</h3>
            {loading.tasks ? (
              <p style={{ color: '#606080' }}>Loading tasks...</p>
            ) : tasks.length === 0 ? (
              <p style={{ color: '#606080' }}>No tasks yet.</p>
            ) : (
              tasks.map((task) => (
                <div key={task.id} style={{ padding: '12px', background: 'rgba(10,10,15,0.4)', borderRadius: '6px', marginBottom: '8px' }}>
                  <div style={{ color: '#fff', fontWeight: '600' }}>{task.title}</div>
                  <div style={{ color: '#a0a0b0', fontSize: '13px' }}>
                    Priority: {task.priority} | Status: {task.status}
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {activeTool === 'weather' && (
          <div>
            <h3 style={{ color: '#fff', marginBottom: '12px' }}>🌤️ Weather</h3>
            <div style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
              <input
                type="text"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                placeholder="Enter city..."
                style={{
                  flex: 1,
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
                onClick={getWeather}
                style={{
                  padding: '10px 24px',
                  background: '#00d4ff',
                  color: '#0a0a0f',
                  border: 'none',
                  borderRadius: '8px',
                  fontWeight: '600',
                  cursor: 'pointer',
                }}
              >
                Get Weather
              </button>
            </div>
            {weather && weather.city && (
              <div>
                <div style={{ color: '#fff', fontSize: '24px' }}>{weather.city}, {weather.country}</div>
                <div style={{ color: '#00d4ff', fontSize: '32px' }}>{weather.temperature}°C</div>
                <div style={{ color: '#a0a0b0' }}>{weather.condition}</div>
                <div style={{ color: '#606080', fontSize: '13px' }}>Humidity: {weather.humidity}% | Wind: {weather.wind_speed} m/s</div>
              </div>
            )}
          </div>
        )}

        {activeTool !== 'notes' && activeTool !== 'tasks' && activeTool !== 'weather' && (
          <div style={{ textAlign: 'center', color: '#606080', padding: '40px 0' }}>
            <p>Tool coming soon</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Tools;
