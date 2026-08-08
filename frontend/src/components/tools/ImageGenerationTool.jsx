import React, { useState } from 'react';
import { images } from '../../api/endpoints';

const ImageGenerationTool = () => {
  const [prompt, setPrompt] = useState('');
  const [provider, setProvider] = useState('stability');

  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const generateImage = async () => {
    if (!prompt.trim()) {
      setError('Please describe the image you want to generate.');
      return;
    }

    try {
      setLoading(true);
      setError('');
      setImage(null);

      const response = await images.generate(
        prompt.trim(),
        provider
      );

      const result = response.data;

      if (!result.success) {
        throw new Error(
          result.error || 'Image generation failed.'
        );
      }

      setImage(result.image);

    } catch (err) {
      console.error('Image generation error:', err);

      setError(
        err.response?.data?.detail ||
        err.message ||
        'Failed to generate image.'
      );
    } finally {
      setLoading(false);
    }
  };

  const clearWorkspace = () => {
    setPrompt('');
    setImage(null);
    setError('');
  };

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '900px',
        margin: '0 auto',
      }}
    >
      {/* Header */}

      <div style={{ marginBottom: '24px' }}>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            marginBottom: '8px',
          }}
        >
          <div
            style={{
              width: '46px',
              height: '46px',
              borderRadius: '12px',
              background: 'rgba(0, 212, 255, 0.12)',
              border: '1px solid rgba(0, 212, 255, 0.25)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '24px',
            }}
          >
            🎨
          </div>

          <div>
            <h2
              style={{
                margin: 0,
                color: '#ffffff',
                fontSize: '24px',
              }}
            >
              Image Generator
            </h2>

            <p
              style={{
                margin: '4px 0 0',
                color: '#77778a',
                fontSize: '13px',
              }}
            >
              Turn your imagination into an image.
            </p>
          </div>
        </div>
      </div>

      {/* Prompt */}

      <div
        style={{
          background: 'rgba(18, 18, 26, 0.7)',
          border: '1px solid rgba(255,255,255,0.07)',
          borderRadius: '14px',
          padding: '20px',
          marginBottom: '20px',
        }}
      >
        <label
          style={{
            display: 'block',
            color: '#ffffff',
            fontSize: '14px',
            fontWeight: '600',
            marginBottom: '8px',
          }}
        >
          Describe your image
        </label>

        <textarea
          value={prompt}
          onChange={(event) =>
            setPrompt(event.target.value)
          }
          placeholder="Example: A futuristic Kampala city at night, with neon lights, rain, cinematic atmosphere..."
          rows={6}
          disabled={loading}
          style={{
            width: '100%',
            boxSizing: 'border-box',
            resize: 'vertical',
            padding: '14px',
            borderRadius: '10px',
            border: '1px solid rgba(255,255,255,0.08)',
            background: '#0b0b11',
            color: '#ffffff',
            outline: 'none',
            fontSize: '14px',
            lineHeight: '1.5',
          }}
        />

        {/* Controls */}

        <div
          style={{
            display: 'flex',
            gap: '12px',
            alignItems: 'end',
            marginTop: '14px',
          }}
        >
          <div style={{ flex: 1 }}>
            <label
              style={{
                display: 'block',
                color: '#8d8da0',
                fontSize: '12px',
                marginBottom: '6px',
              }}
            >
              Provider
            </label>

            <select
              value={provider}
              onChange={(event) =>
                setProvider(event.target.value)
              }
              disabled={loading}
              style={{
                width: '100%',
                padding: '11px 12px',
                borderRadius: '9px',
                border: '1px solid rgba(255,255,255,0.08)',
                background: '#0b0b11',
                color: '#ffffff',
                outline: 'none',
              }}
            >
              <option value="stability">
                Stability AI
              </option>

              <option value="openai">
                OpenAI
              </option>
            </select>
          </div>

          <button
            onClick={generateImage}
            disabled={loading || !prompt.trim()}
            style={{
              minWidth: '180px',
              padding: '12px 18px',
              border: 'none',
              borderRadius: '9px',
              background:
                loading || !prompt.trim()
                  ? '#30303a'
                  : '#00d4ff',
              color:
                loading || !prompt.trim()
                  ? '#77778a'
                  : '#050509',
              fontWeight: '700',
              cursor:
                loading || !prompt.trim()
                  ? 'not-allowed'
                  : 'pointer',
            }}
          >
            {loading
              ? 'Generating...'
              : '✨ Generate Image'}
          </button>
        </div>
      </div>

      {/* Error */}

      {error && (
        <div
          style={{
            padding: '14px',
            borderRadius: '10px',
            marginBottom: '20px',
            background: 'rgba(249, 112, 102, 0.08)',
            border:
              '1px solid rgba(249, 112, 102, 0.25)',
            color: '#ffaaa3',
            fontSize: '14px',
          }}
        >
          {error}
        </div>
      )}

      {/* Result */}

      {image && (
        <div
          style={{
            background: 'rgba(18, 18, 26, 0.7)',
            border:
              '1px solid rgba(255,255,255,0.07)',
            borderRadius: '14px',
            padding: '20px',
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginBottom: '14px',
            }}
          >
            <h3
              style={{
                margin: 0,
                color: '#ffffff',
                fontSize: '16px',
              }}
            >
              Generated Image
            </h3>

            <button
              onClick={clearWorkspace}
              style={{
                padding: '7px 12px',
                borderRadius: '7px',
                border:
                  '1px solid rgba(255,255,255,0.08)',
                background: 'transparent',
                color: '#9999aa',
                cursor: 'pointer',
              }}
            >
              Clear
            </button>
          </div>

          <img
            src={
              image.startsWith('data:')
                ? image
                : `data:image/png;base64,${image}`
            }
            alt={prompt}
            style={{
              display: 'block',
              width: '100%',
              maxHeight: '650px',
              objectFit: 'contain',
              borderRadius: '10px',
              background: '#050509',
            }}
          />

          <div
            style={{
              marginTop: '14px',
              padding: '12px',
              borderRadius: '8px',
              background: 'rgba(0,0,0,0.25)',
              color: '#858598',
              fontSize: '12px',
              lineHeight: '1.5',
            }}
          >
            <strong
              style={{ color: '#b0b0c0' }}
            >
              Prompt:
            </strong>{' '}
            {prompt}
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageGenerationTool;