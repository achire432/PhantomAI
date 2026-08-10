import React, { useState } from 'react';
import { tools } from '../../api/endpoints';

const WeatherTool = () => {
  const [city, setCity] = useState('');
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const getWeather = async () => {
    if (!city.trim()) {
      setError('Enter a city first.');
      setWeather(null);
      return;
    }

    setLoading(true);
    setError('');
    setWeather(null);

    try {
      const response = await tools.weather(city.trim());
      setWeather(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Unable to get weather information.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      getWeather();
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
        🌤️
      </div>

      <h2
        style={{
          margin: '0 0 8px',
          color: '#ffffff',
          fontSize: '22px',
        }}
      >
        Weather
      </h2>

      <p
        style={{
          margin: '0 0 25px',
          color: '#77778a',
          fontSize: '13px',
        }}
      >
        Check current weather conditions for any city.
      </p>

      <input
        type="text"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="e.g. Kampala"
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
        onClick={getWeather}
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
        {loading ? 'Checking weather...' : 'Get Weather'}
      </button>

      {weather && (
        <div
          style={{
            marginTop: '20px',
            padding: '20px',
            borderRadius: '12px',
            background: 'rgba(0,212,255,0.06)',
            border: '1px solid rgba(0,212,255,0.15)',
          }}
        >
          <div
            style={{
              color: '#ffffff',
              fontSize: '20px',
              fontWeight: '700',
              marginBottom: '6px',
            }}
          >
            {weather.city}, {weather.country}
          </div>

          <div
            style={{
              color: '#ffffff',
              fontSize: '38px',
              fontWeight: '700',
              margin: '12px 0',
            }}
          >
            {Math.round(weather.temperature)}°C
          </div>

          <div
            style={{
              color: '#aaaabb',
              fontSize: '14px',
              textTransform: 'capitalize',
              marginBottom: '18px',
            }}
          >
            {weather.condition}
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns:
                'repeat(auto-fit, minmax(150px, 1fr))',
              gap: '10px',
            }}
          >
            <div
              style={{
                padding: '12px',
                borderRadius: '9px',
                background: 'rgba(255,255,255,0.03)',
              }}
            >
              <div style={{ color: '#666679', fontSize: '11px' }}>
                Feels Like
              </div>

              <div
                style={{
                  color: '#ffffff',
                  marginTop: '4px',
                  fontSize: '15px',
                  fontWeight: '600',
                }}
              >
                {Math.round(weather.feels_like)}°C
              </div>
            </div>

            <div
              style={{
                padding: '12px',
                borderRadius: '9px',
                background: 'rgba(255,255,255,0.03)',
              }}
            >
              <div style={{ color: '#666679', fontSize: '11px' }}>
                Humidity
              </div>

              <div
                style={{
                  color: '#ffffff',
                  marginTop: '4px',
                  fontSize: '15px',
                  fontWeight: '600',
                }}
              >
                {weather.humidity}%
              </div>
            </div>

            <div
              style={{
                padding: '12px',
                borderRadius: '9px',
                background: 'rgba(255,255,255,0.03)',
              }}
            >
              <div style={{ color: '#666679', fontSize: '11px' }}>
                Wind
              </div>

              <div
                style={{
                  color: '#ffffff',
                  marginTop: '4px',
                  fontSize: '15px',
                  fontWeight: '600',
                }}
              >
                {weather.wind_speed} m/s
              </div>
            </div>
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
        Examples: Kampala · Nairobi · London · New York
      </div>
    </div>
  );
};

export default WeatherTool;