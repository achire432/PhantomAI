import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { memory } from '../api/endpoints';

const Memory = () => {
  const { token } = useAuth();
  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newKey, setNewKey] = useState('');
  const [newValue, setNewValue] = useState('');

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }
    fetchMemories();
  }, [token]);

  const fetchMemories = async () => {
    try {
      const response = await memory.getAll();
      setMemories(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Failed to fetch memories:', err);
      setError('Failed to load memories');
      setLoading(false);
    }
  };

  const addMemory = async (e) => {
    e.preventDefault();
    if (!newKey.trim() || !newValue.trim()) return;

    try {
      await memory.create({ key: newKey, value: newValue });
      setNewKey('');
      setNewValue('');
      fetchMemories();
    } catch (err) {
      console.error('Failed to add memory:', err);
      setError('Failed to add memory');
    }
  };

  const deleteMemory = async (key) => {
    try {
      await memory.delete(key);
      fetchMemories();
    } catch (err) {
      console.error('Failed to delete memory:', err);
      setError('Failed to delete memory');
    }
  };

  if (loading) {
    return <div style={{ padding: '40px', color: '#00d4ff' }}>Loading memories...</div>;
  }

  return (
    <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ color: '#fff', marginBottom: '8px' }}>🧠 Memory</h1>
      <p style={{ color: '#606080', marginBottom: '24px' }}>
        PhantomAI remembers important facts you tell it.
      </p>

      {error && (
        <div style={{ padding: '12px', background: 'rgba(208,96,96,0.1)', border: '1px solid #d06060', borderRadius: '8px', color: '#d06060', marginBottom: '16px' }}>
          {error}
        </div>
      )}

      {/* Add Memory */}
      <form onSubmit={addMemory} style={{ display: 'flex', gap: '12px', marginBottom: '24px' }}>
        <input
          type="text"
          value={newKey}
          onChange={(e) => setNewKey(e.target.value)}
          placeholder="Key (e.g., project_name)"
          style={{
            flex: 1,
            padding: '10px 14px',
            background: 'rgba(18,18,26,0.6)',
            border: '1px solid rgba(26,26,46,0.5)',
            borderRadius: '8px',
            color: '#e0e0e0',
            fontSize: '14px',
            outline: 'none',
          }}
        />
        <input
          type="text"
          value={newValue}
          onChange={(e) => setNewValue(e.target.value)}
          placeholder="Value (e.g., PhantomAI)"
          style={{
            flex: 2,
            padding: '10px 14px',
            background: 'rgba(18,18,26,0.6)',
            border: '1px solid rgba(26,26,46,0.5)',
            borderRadius: '8px',
            color: '#e0e0e0',
            fontSize: '14px',
            outline: 'none',
          }}
        />
        <button
          type="submit"
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
          Save
        </button>
      </form>

      {/* Memory List */}
      {memories.length === 0 ? (
        <p style={{ color: '#606080' }}>No memories stored yet.</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {memories.map((mem) => (
            <div
              key={mem.id}
              style={{
                padding: '16px',
                background: 'rgba(18,18,26,0.6)',
                border: '1px solid rgba(26,26,46,0.3)',
                borderRadius: '8px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}
            >
              <div>
                <div style={{ color: '#00d4ff', fontWeight: '600' }}>{mem.key}</div>
                <div style={{ color: '#a0a0b0', fontSize: '14px' }}>{mem.value}</div>
                <div style={{ color: '#606080', fontSize: '11px' }}>
                  {new Date(mem.created_at).toLocaleDateString()}
                </div>
              </div>
              <button
                onClick={() => deleteMemory(mem.key)}
                style={{
                  padding: '6px 14px',
                  background: 'rgba(208,96,96,0.15)',
                  border: '1px solid rgba(208,96,96,0.3)',
                  borderRadius: '6px',
                  color: '#d06060',
                  cursor: 'pointer',
                  fontSize: '12px',
                }}
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Memory;
