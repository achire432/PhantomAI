/**
 * PHANTOMAI CHAT INTERFACE
 * ========================
 * 
 * ARCHITECTURAL IMPORTANCE:
 * This is the core engine room of PhantomAI.
 * Users interact with the AI model (Qwen3-4B) through this interface.
 * It sends requests to your FastAPI backend and renders responses.
 * 
 * SCALABILITY NOTES:
 * 1. This component is designed to scale from a single chat to conversation threads.
 * 2. It uses state management for messages, loading indicators, and errors.
 * 3. It currently uses mock data until we connect to the real API.
 * 4. The input is "controlled" (React state handles the value), which is best practice.
 */

import React, { useState, useRef, useEffect } from 'react';
// We will use this later to talk to the backend
// import api from '../services/api'; 

const Chat = () => {
  // --- STATE MANAGEMENT ---
  // `messages`: An array storing all messages in the current chat
  const [messages, setMessages] = useState([
    // Initial greeting message from the AI
    {
      id: 1,
      role: 'assistant', 
      content: "Hello, I am PhantomAI. I'm powered by Qwen3-4B. How can I assist you today?"
    }
  ]);
  
  // `input`: Stores whatever the user is currently typing
  const [input, setInput] = useState('');
  
  // `isLoading`: Shows a "thinking" indicator while waiting for the AI
  const [isLoading, setIsLoading] = useState(false);
  
  // `error`: Stores an error message if the API fails
  const [error, setError] = useState(null);

  // --- REFS ---
  // `messagesEndRef`: A hook to automatically scroll to the bottom when a new message arrives
  const messagesEndRef = useRef(null);

  /**
   * AUTO-SCROLL EFFECT
   * ------------------
   * Every time `messages` changes, this hook fires.
   * It scrolls the chat window down to the very bottom, ensuring
   * the user always sees the latest message.
   */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  /**
   * handleSendMessage
   * -----------------
   * This is the main brain of the chat.
   * 
   * 1. Validates that the user typed something.
   * 2. Adds the user's message to the `messages` array.
   * 3. Clears the input bar.
   * 4. Simulates a delay (like the AI is thinking).
   * 5. Adds the AI's response to the `messages` array.
   */
  const handleSendMessage = async (e) => {
    e.preventDefault(); // Prevents page refresh
    
    if (!input.trim()) return; // Ignore empty messages

    // 1. Create the user's message object
    const userMessage = {
      id: Date.now(), // Unique ID
      role: 'user',
      content: input
    };

    // 2. Update state: Add user message, clear input, show loading
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      /**
       * FUTURE BACKEND CONNECTION:
       * Instead of the setTimeout below, you will replace this block with:
       * 
       * const response = await api.post('/chat/completions', { 
       *     message: input 
       * });
       * 
       * const aiReply = response.data.content;
       */

      // --- MOCK AI RESPONSE (Temporary until backend connects) ---
      await new Promise((resolve) => setTimeout(resolve, 1500)); // Simulate AI thinking

      // Generate a mock reply
      const aiReply = `I received your message: "${input}". This is a simulated response for Phase 4! Once we connect your FastAPI backend, I will generate real AI replies using Qwen3-4B.`;

      // 3. Add the AI's response to the messages array
      setMessages((prev) => [
        ...prev, 
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: aiReply
        }
      ]);

    } catch (err) {
      // If there's an error, show it to the user
      setError('Failed to get a response from the AI. Please try again.');
      console.error("Chat Error:", err);
    } finally {
      // Turn off the loading indicator
      setIsLoading(false);
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: 'calc(100vh - 70px)', // Account for Navbar height
      maxWidth: '900px',
      margin: '0 auto',
      padding: '20px',
    }}>
      
      {/* --- CHAT HEADER --- */}
      <div style={{
        padding: '16px 0',
        borderBottom: '1px solid rgba(255,255,255,0.05)',
        marginBottom: '20px'
      }}>
        <h2 style={{ color: '#fff', fontSize: '20px', margin: 0 }}>
          💬 PhantomAI Chat
        </h2>
        <p style={{ color: '#a0a0b0', fontSize: '12px', margin: '4px 0 0 0' }}>
          Connected to Qwen3-4B
        </p>
      </div>

      {/* --- MESSAGES DISPLAY AREA --- */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
        paddingRight: '10px',
        marginBottom: '20px'
      }}>
        {messages.map((msg) => (
          <div 
            key={msg.id}
            style={{
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              maxWidth: '75%',
              background: msg.role === 'user' 
                ? 'rgba(0, 212, 255, 0.15)' // Cyan tint for user
                : 'rgba(255, 255, 255, 0.05)', // Dark glass for AI
              padding: '12px 16px',
              borderRadius: '16px',
              border: '1px solid rgba(255,255,255,0.05)',
              color: '#e0e0e0',
              fontSize: '15px',
              lineHeight: '1.5'
            }}
          >
            {msg.content}
          </div>
        ))}

        {/* LOADING INDICATOR (Thinking...) */}
        {isLoading && (
          <div style={{
            alignSelf: 'flex-start',
            maxWidth: '75%',
            background: 'rgba(255, 255, 255, 0.05)',
            padding: '12px 16px',
            borderRadius: '16px',
            color: '#a0a0b0',
            fontSize: '14px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <span>Thinking</span>
            <span style={{ display: 'inline-block', animation: 'dotPulse 1.5s infinite' }}>...</span>
            {/* Simple CSS for dot animation */}
            <style>{`
              @keyframes dotPulse {
                0% { opacity: 0.2; }
                50% { opacity: 1; }
                100% { opacity: 0.2; }
              }
            `}</style>
          </div>
        )}

        {/* Invisible div to auto-scroll to */}
        <div ref={messagesEndRef} />
      </div>

      {/* --- ERROR DISPLAY --- */}
      {error && (
        <div style={{
          background: 'rgba(255, 0, 0, 0.1)',
          border: '1px solid rgba(255, 0, 0, 0.2)',
          color: '#ff6b6b',
          padding: '12px',
          borderRadius: '8px',
          marginBottom: '16px',
          textAlign: 'center',
          fontSize: '14px',
        }}>
          {error}
        </div>
      )}

      {/* --- INPUT AREA --- */}
      <form 
        onSubmit={handleSendMessage}
        style={{
          display: 'flex',
          gap: '12px',
          background: 'rgba(255,255,255,0.05)',
          padding: '12px',
          borderRadius: '12px',
          border: '1px solid rgba(255,255,255,0.1)',
          backdropFilter: 'blur(10px)'
        }}
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask PhantomAI anything..."
          disabled={isLoading}
          style={{
            flex: 1,
            background: 'transparent',
            border: 'none',
            color: '#ffffff',
            fontSize: '16px',
            outline: 'none',
            padding: '8px'
          }}
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          style={{
            padding: '10px 24px',
            background: isLoading ? 'rgba(0, 212, 255, 0.3)' : '#00d4ff',
            color: '#12121a',
            border: 'none',
            borderRadius: '8px',
            fontSize: '14px',
            fontWeight: '600',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            transition: 'all 0.2s'
          }}
        >
          {isLoading ? '...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default Chat;