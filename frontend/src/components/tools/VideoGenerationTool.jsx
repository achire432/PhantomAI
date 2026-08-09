import React, { useState } from 'react';
import { video } from '../../api/endpoints';

const VideoGenerationTool = () => {
  const [prompt, setPrompt] = useState('');

  const [duration, setDuration] = useState(8);

  const [aspectRatio, setAspectRatio] =
    useState('16:9');

  const [resolution, setResolution] =
    useState('720p');

  const [videoUrl, setVideoUrl] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState('');

  const generateVideo = async () => {
    if (!prompt.trim()) {
      setError(
        'Please describe the video you want to generate.'
      );
      return;
    }

    try {
      setLoading(true);
      setError('');

      if (videoUrl) {
        URL.revokeObjectURL(videoUrl);
        setVideoUrl(null);
      }

      const response =
        await video.text(
          prompt.trim(),
          duration,
          aspectRatio,
          resolution
        );

      const blob = response.data;

      if (!blob || blob.size === 0) {
        throw new Error(
          'The server returned an empty video.'
        );
      }

      const url =
        URL.createObjectURL(blob);

      setVideoUrl(url);

    } catch (err) {
      console.error(
        'Video generation error:',
        err
      );

      let message =
        'Failed to generate video.';

      if (
        err.response?.data
      ) {
        try {
          const text =
            await err.response.data.text();

          const parsed =
            JSON.parse(text);

          message =
            parsed.detail ||
            message;
        } catch {
          // Keep default error.
        }
      }

      if (
        err.message &&
        message ===
          'Failed to generate video.'
      ) {
        message =
          err.message;
      }

      setError(message);

    } finally {
      setLoading(false);
    }
  };

  const clearWorkspace = () => {
    if (videoUrl) {
      URL.revokeObjectURL(videoUrl);
    }

    setPrompt('');
    setVideoUrl(null);
    setError('');
  };

  const downloadVideo = () => {
    if (!videoUrl) return;

    const link =
      document.createElement('a');

    link.href = videoUrl;

    link.download =
      'phantom_ai_veo_video.mp4';

    document.body.appendChild(link);

    link.click();

    link.remove();
  };

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '900px',
        margin: '0 auto',
      }}
    >

      {/* ================================================= */}
      {/* HEADER */}
      {/* ================================================= */}

      <div
        style={{
          marginBottom: '24px',
        }}
      >
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
              background:
                'rgba(255,90,90,0.12)',
              border:
                '1px solid rgba(255,90,90,0.25)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '24px',
            }}
          >
            🎬
          </div>

          <div>
            <h2
              style={{
                margin: 0,
                color: '#ffffff',
                fontSize: '24px',
              }}
            >
              AI Video Generator
            </h2>

            <p
              style={{
                margin:
                  '4px 0 0',
                color: '#77778a',
                fontSize: '13px',
              }}
            >
              Create realistic videos
              with Google Veo 3.1.
            </p>
          </div>

        </div>
      </div>

      {/* ================================================= */}
      {/* PROMPT CARD */}
      {/* ================================================= */}

      <div
        style={{
          background:
            'rgba(18,18,26,0.7)',
          border:
            '1px solid rgba(255,255,255,0.07)',
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
          Describe your video
        </label>

        <textarea
          value={prompt}
          onChange={(event) =>
            setPrompt(
              event.target.value
            )
          }
          placeholder="Example: A realistic cinematic shot of a young child walking through a rainy Kampala street at sunset, natural movement, realistic lighting, documentary camera..."
          rows={8}
          disabled={loading}
          style={{
            width: '100%',
            boxSizing: 'border-box',
            resize: 'vertical',
            padding: '14px',
            borderRadius: '10px',
            border:
              '1px solid rgba(255,255,255,0.08)',
            background: '#0b0b11',
            color: '#ffffff',
            outline: 'none',
            fontSize: '14px',
            lineHeight: '1.5',
          }}
        />

        {/* ================================================= */}
        {/* CONTROLS */}
        {/* ================================================= */}

        <div
          style={{
            display: 'grid',
            gridTemplateColumns:
              '1fr 1fr 1fr',
            gap: '12px',
            marginTop: '14px',
          }}
        >

          {/* Duration */}

          <div>
            <label
              style={{
                display: 'block',
                color: '#8d8da0',
                fontSize: '12px',
                marginBottom: '6px',
              }}
            >
              Duration
            </label>

            <select
              value={duration}
              onChange={(event) =>
                setDuration(
                  Number(
                    event.target.value
                  )
                )
              }
              disabled={loading}
              style={{
                width: '100%',
                padding: '11px 12px',
                borderRadius: '9px',
                border:
                  '1px solid rgba(255,255,255,0.08)',
                background: '#0b0b11',
                color: '#ffffff',
              }}
            >
              <option value={4}>
                4 seconds
              </option>

              <option value={6}>
                6 seconds
              </option>

              <option value={8}>
                8 seconds
              </option>
            </select>
          </div>

          {/* Aspect Ratio */}

          <div>
            <label
              style={{
                display: 'block',
                color: '#8d8da0',
                fontSize: '12px',
                marginBottom: '6px',
              }}
            >
              Aspect Ratio
            </label>

            <select
              value={aspectRatio}
              onChange={(event) =>
                setAspectRatio(
                  event.target.value
                )
              }
              disabled={loading}
              style={{
                width: '100%',
                padding: '11px 12px',
                borderRadius: '9px',
                border:
                  '1px solid rgba(255,255,255,0.08)',
                background: '#0b0b11',
                color: '#ffffff',
              }}
            >
              <option value="16:9">
                16:9 Landscape
              </option>

              <option value="9:16">
                9:16 Portrait
              </option>
            </select>
          </div>

          {/* Resolution */}

          <div>
            <label
              style={{
                display: 'block',
                color: '#8d8da0',
                fontSize: '12px',
                marginBottom: '6px',
              }}
            >
              Resolution
            </label>

            <select
              value={resolution}
              onChange={(event) =>
                setResolution(
                  event.target.value
                )
              }
              disabled={loading}
              style={{
                width: '100%',
                padding: '11px 12px',
                borderRadius: '9px',
                border:
                  '1px solid rgba(255,255,255,0.08)',
                background: '#0b0b11',
                color: '#ffffff',
              }}
            >
              <option value="720p">
                720p
              </option>

              <option
                value="1080p"
              >
                1080p
              </option>
            </select>
          </div>

        </div>

        {/* ================================================= */}
        {/* GENERATE BUTTON */}
        {/* ================================================= */}

        <button
          onClick={generateVideo}
          disabled={
            loading ||
            !prompt.trim()
          }
          style={{
            width: '100%',
            marginTop: '16px',
            padding: '13px 18px',
            border: 'none',
            borderRadius: '9px',
            background:
              loading ||
              !prompt.trim()
                ? '#30303a'
                : '#ff5a5a',
            color:
              loading ||
              !prompt.trim()
                ? '#77778a'
                : '#ffffff',
            fontWeight: '700',
            cursor:
              loading ||
              !prompt.trim()
                ? 'not-allowed'
                : 'pointer',
          }}
        >
          {loading
            ? '🎬 Generating real AI video...'
            : '🎬 Generate AI Video'}
        </button>

        {loading && (
          <p
            style={{
              margin:
                '12px 0 0',
              textAlign: 'center',
              color: '#77778a',
              fontSize: '12px',
            }}
          >
            Veo generation can take
            a few minutes. Keep this
            page open.
          </p>
        )}

      </div>

      {/* ================================================= */}
      {/* ERROR */}
      {/* ================================================= */}

      {error && (
        <div
          style={{
            padding: '14px',
            borderRadius: '10px',
            marginBottom: '20px',
            background:
              'rgba(249,112,102,0.08)',
            border:
              '1px solid rgba(249,112,102,0.25)',
            color: '#ffaaa3',
            fontSize: '14px',
            lineHeight: '1.5',
          }}
        >
          {error}
        </div>
      )}

      {/* ================================================= */}
      {/* VIDEO RESULT */}
      {/* ================================================= */}

      {videoUrl && (
        <div
          style={{
            background:
              'rgba(18,18,26,0.7)',
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
              justifyContent:
                'space-between',
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
              Generated Video
            </h3>

            <div
              style={{
                display: 'flex',
                gap: '8px',
              }}
            >

              <button
                onClick={
                  downloadVideo
                }
                style={{
                  padding:
                    '7px 12px',
                  borderRadius: '7px',
                  border: 'none',
                  background:
                    '#00d4ff',
                  color: '#050509',
                  fontWeight: '700',
                  cursor:
                    'pointer',
                }}
              >
                ⬇ Download
              </button>

              <button
                onClick={
                  clearWorkspace
                }
                style={{
                  padding:
                    '7px 12px',
                  borderRadius: '7px',
                  border:
                    '1px solid rgba(255,255,255,0.08)',
                  background:
                    'transparent',
                  color: '#9999aa',
                  cursor:
                    'pointer',
                }}
              >
                Clear
              </button>

            </div>
          </div>

          <video
            src={videoUrl}
            controls
            playsInline
            style={{
              display: 'block',
              width: '100%',
              maxHeight: '650px',
              borderRadius: '10px',
              background:
                '#050509',
            }}
          />

          <div
            style={{
              marginTop: '14px',
              padding: '12px',
              borderRadius: '8px',
              background:
                'rgba(0,0,0,0.25)',
              color: '#858598',
              fontSize: '12px',
              lineHeight: '1.5',
            }}
          >
            <strong
              style={{
                color: '#b0b0c0',
              }}
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

export default VideoGenerationTool;
