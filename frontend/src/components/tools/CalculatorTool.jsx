import React, { useState } from 'react';
import { tools } from '../../api/endpoints';

const CalculatorTool = () => {
  const [expression, setExpression] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const calculate = async () => {
    if (!expression.trim()) {
      setError('Enter an expression first.');
      setResult(null);
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await tools.calculator(expression);

      setResult(response.data.result);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Unable to calculate expression.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      calculate();
    }
  };

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '760px',
        margin: '0 auto',
        padding: '30px',
        borderRadius: '16px',
        border: '1px solid rgba(255,255,255,0.06)',
        background: 'rgba(18,18,26,0.65)',
        boxSizing: 'border-box',
      }}
    >
      <div
        style={{
          fontSize: '42px',
          marginBottom: '10px',
        }}
      >
        🧮
      </div>

      <h2
        style={{
          margin: '0 0 8px',
          color: '#ffffff',
          fontSize: '22px',
        }}
      >
        Calculator
      </h2>

      <p
        style={{
          margin: '0 0 25px',
          color: '#77778a',
          fontSize: '13px',
        }}
      >
        Perform mathematical calculations with PhantomAI.
      </p>

      <input
        type="text"
        value={expression}
        onChange={(e) => setExpression(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="e.g. 5 + 45678"
        style={{
          width: '100%',
          padding: '15px',
          borderRadius: '10px',
          border: '1px solid rgba(255,255,255,0.08)',
          background: '#0c0c12',
          color: '#ffffff',
          fontSize: '16px',
          outline: 'none',
          boxSizing: 'border-box',
        }}
      />

      <button
        type="button"
        onClick={calculate}
        disabled={loading}
        style={{
          width: '100%',
          marginTop: '14px',
          padding: '14px',
          border: 'none',
          borderRadius: '10px',
          background: loading
            ? 'rgba(0,212,255,0.3)'
            : 'rgba(0,212,255,0.9)',
          color: '#ffffff',
          fontSize: '14px',
          fontWeight: '600',
          cursor: loading ? 'not-allowed' : 'pointer',
        }}
      >
        {loading ? 'Calculating...' : 'Calculate'}
      </button>

      {result !== null && (
        <div
          style={{
            marginTop: '20px',
            padding: '18px',
            borderRadius: '10px',
            background: 'rgba(0,212,255,0.06)',
            border: '1px solid rgba(0,212,255,0.15)',
          }}
        >
          <div
            style={{
              color: '#77778a',
              fontSize: '12px',
              marginBottom: '6px',
            }}
          >
            Result
          </div>

          <div
            style={{
              color: '#ffffff',
              fontSize: '28px',
              fontWeight: '700',
              wordBreak: 'break-word',
            }}
          >
            {String(result)}
          </div>
        </div>
      )}

      {error && (
        <div
          style={{
            marginTop: '20px',
            padding: '14px',
            borderRadius: '10px',
            background: 'rgba(255,70,70,0.08)',
            border: '1px solid rgba(255,70,70,0.2)',
            color: '#ff8b8b',
            fontSize: '13px',
          }}
        >
          {error}
        </div>
      )}

      <div
        style={{
          marginTop: '25px',
          color: '#555566',
          fontSize: '12px',
        }}
      >
        Examples: 5 + 45678 · 100 / 4 · 4 * 5 · sqrt(144) · 2^10
      </div>
    </div>
  );
};

export default CalculatorTool;