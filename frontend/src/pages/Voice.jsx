import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { voice } from '../api/endpoints';

const Voice = () => {
  const { token } = useAuth();
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [response, setResponse] = useState('');
  const [wakeWordActive, setWakeWordActive] = useState(false);

  const startListening = async () => {
    setIsListening(true);
    setTranscript('Listening...');
    try {
      const result = await voice.listen();
      if (result.data && result.data.text) {
        setTranscript(`You said: "${result.data.text}"`);
        // Get AI response
        const aiResponse = await voice.chat();
        setResponse(aiResponse.data?.ai_response || 'AI responded');
      }
    } catch (err) {
      console.error('Voice error:', err);
      setTranscript('Error listening. Please try again.');
    }
    setIsListening(false);
  };

  const toggleWakeWord = async () => {
    if (wakeWordActive) {
      await voice.wakeStop();
      setWakeWordActive(false);
    } else {
      await voice.wakeStart();
      setWakeWordActive(true);
    }
  };

  return (
    <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ color: '#fff', marginBottom: '8px' }}>🎙️ Voice Mode</h1>
      <p style={{ color: '#606080', marginBottom: '24px' }}>
        Speak to PhantomAI. Say "Hey Phantom" to activate.
      </p>

      <div style={{ display: 'grid', gap: '20px' }}>
        {/* Mic Button */}
        <div
          style={{
            padding: '40px',
            background: 'rgba(18,18,26,0.6)',
            border: '1px solid rgba(26,26,46,0.3)',
            borderRadius: '16px',
            textAlign: 'center',
          }}
        >
          <button
            onClick={startListening}
            disabled={isListening}
            style={{
              width: '120px',
              height: '120px',
              borderRadius: '50%',
              background: isListening ? 'rgba(208,96,96,0.2)' : 'rgba(0,212,255,0.15)',
              border: isListening ? '3px solid #d06060' : '3px solid rgba(0,212,255,0.3)',
              color: isListening ? '#d06060' : '#00d4ff',
              fontSize: '48px',
              cursor: isListening ? 'not-allowed' : 'pointer',
              transition: 'all 0.3s',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {isListening ? '⏳' : '🎤'}
          </button>
          <p style={{ color: '#a0a0b0', marginTop: '12px' }}>
            {isListening ? 'Listening...' : 'Click to speak'}
          </p>
        </div>

        {/* Transcript */}
        {transcript && (
          <div style={{ padding: '16px', background: 'rgba(18,18,26,0.4)', borderRadius: '8px', border: '1px solid rgba(26,26,46,0.3)' }}>
            <div style={{ color: '#a0a0b0', fontSize: '12px' }}>Transcript</div>
            <div style={{ color: '#fff', fontSize: '16px' }}>{transcript}</div>
          </div>
        )}

        {/* AI Response */}
        {response && (
          <div style={{ padding: '16px', background: 'rgba(0,212,255,0.05)', borderRadius: '8px', border: '1px solid rgba(0,212,255,0.15)' }}>
            <div style={{ color: '#00d4ff', fontSize: '12px' }}>PhantomAI</div>
            <div style={{ color: '#fff', fontSize: '16px' }}>{response}</div>
          </div>
        )}

        {/* Wake Word */}
        <div
          style={{
            padding: '16px',
            background: 'rgba(18,18,26,0.6)',
            border: '1px solid rgba(26,26,46,0.3)',
            borderRadius: '12px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <div>
            <div style={{ color: '#fff', fontWeight: '600' }}>🔊 Wake Word</div>
            <div style={{ color: '#606080', fontSize: '13px' }}>
              Say "Hey Phantom" to activate
            </div>
          </div>
          <button
            onClick={toggleWakeWord}
            style={{
              padding: '8px 20px',
              background: wakeWordActive ? 'rgba(96,208,96,0.2)' : 'rgba(208,96,96,0.15)',
              border: wakeWordActive ? '1px solid #60d060' : '1px solid rgba(208,96,96,0.3)',
              borderRadius: '20px',
              color: wakeWordActive ? '#60d060' : '#d06060',
              cursor: 'pointer',
              fontWeight: '600',
              fontSize: '13px',
            }}
          >
            {wakeWordActive ? 'Active' : 'Inactive'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Voice;
