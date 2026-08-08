import React, { useEffect, useState } from 'react';
import { video } from '../../api/endpoints';

const VideoGenerationTool = () => {
  const [mode, setMode] = useState('text');

  // Text → Video
  const [text, setText] = useState('');
  const [duration, setDuration] = useState(5);

  // Images → Slideshow
  const [images, setImages] = useState([]);
  const [durationPerImage, setDurationPerImage] = useState(3);

  // Result
  const [videoUrl, setVideoUrl] = useState(null);
  const [videoBlob, setVideoBlob] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // ----------------------------------------------------------
  // CLEANUP OBJECT URL
  // ----------------------------------------------------------

  useEffect(() => {
    return () => {
      if (videoUrl) {
        URL.revokeObjectURL(videoUrl);
      }
    };
  }, [videoUrl]);

  // ----------------------------------------------------------
  // CLEAR WORKSPACE
  // ----------------------------------------------------------

  const clearWorkspace = () => {
    if (videoUrl) {
      URL.revokeObjectURL(videoUrl);
    }

    setText('');
    setImages([]);
    setVideoUrl(null);
    setVideoBlob(null);
    setError('');
  };

  // ----------------------------------------------------------
  // TEXT → VIDEO
  // ----------------------------------------------------------

  const generateTextVideo = async () => {
    if (!text.trim()) {
      setError('Please enter some text for the video.');
      return;
    }

    try {
      setLoading(true);
      setError('');

      if (videoUrl) {
        URL.revokeObjectURL(videoUrl);
      }

      setVideoUrl(null);
      setVideoBlob(null);

      const response = await video.text(
        text.trim(),
        Number(duration)
      );

      const blob = response.data;

      if (!(blob instanceof Blob)) {
        throw new Error(
          'The server did not return a valid video file.'
        );
      }

      if (blob.size === 0) {
        throw new Error(
          'The generated video is empty.'
        );
      }

      const url = URL.createObjectURL(blob);

      setVideoBlob(blob);
      setVideoUrl(url);

    } catch (err) {
      console.error(
        'Text video generation error:',
        err
      );

      await handleVideoError(
        err,
        'Failed to generate video.'
      );

    } finally {
      setLoading(false);
    }
  };

  // ----------------------------------------------------------
  // IMAGE FILE → BASE64
  // ----------------------------------------------------------

  const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      reader.onload = () => {
        resolve(reader.result);
      };

      reader.onerror = () => {
        reject(
          new Error(
            `Failed to read ${file.name}.`
          )
        );
      };

      reader.readAsDataURL(file);
    });
  };

  // ----------------------------------------------------------
  // SELECT IMAGES
  // ----------------------------------------------------------

  const handleImageSelection = async (event) => {
    try {
      setError('');

      const selectedFiles = Array.from(
        event.target.files || []
      );

      if (!selectedFiles.length) {
        return;
      }

      const validFiles = selectedFiles.filter(
        (file) =>
          file.type.startsWith('image/')
      );

      if (!validFiles.length) {
        setError(
          'Please select valid image files.'
        );
        return;
      }

      const encodedImages = await Promise.all(
        validFiles.map(fileToBase64)
      );

      setImages((previous) => [
        ...previous,
        ...encodedImages,
      ]);

    } catch (err) {
      console.error(
        'Image selection error:',
        err
      );

      setError(
        err.message ||
        'Failed to load images.'
      );
    }

    event.target.value = '';
  };

  // ----------------------------------------------------------
  // REMOVE IMAGE
  // ----------------------------------------------------------

  const removeImage = (index) => {
    setImages((previous) =>
      previous.filter(
        (_, imageIndex) =>
          imageIndex !== index
      )
    );
  };

  // ----------------------------------------------------------
  // SLIDESHOW → VIDEO
  // ----------------------------------------------------------

  const generateSlideshow = async () => {
    if (!images.length) {
      setError(
        'Please select at least one image.'
      );
      return;
    }

    try {
      setLoading(true);
      setError('');

      if (videoUrl) {
        URL.revokeObjectURL(videoUrl);
      }

      setVideoUrl(null);
      setVideoBlob(null);

      const response = await video.slideshow(
        images,
        Number(durationPerImage)
      );

      const blob = response.data;

      if (!(blob instanceof Blob)) {
        throw new Error(
          'The server did not return a valid video file.'
        );
      }

      if (blob.size === 0) {
        throw new Error(
          'The generated slideshow is empty.'
        );
      }

      const url = URL.createObjectURL(blob);

      setVideoBlob(blob);
      setVideoUrl(url);

    } catch (err) {
      console.error(
        'Slideshow generation error:',
        err
      );

      await handleVideoError(
        err,
        'Failed to generate slideshow.'
      );

    } finally {
      setLoading(false);
    }
  };

  // ----------------------------------------------------------
  // ERROR HANDLER
  // ----------------------------------------------------------

  const handleVideoError = async (
    err,
    fallback
  ) => {
    if (
      err?.response?.data instanceof Blob
    ) {
      try {
        const text = await err.response.data.text();

        try {
          const json = JSON.parse(text);

          setError(
            json.detail ||
            fallback
          );

          return;
        } catch {
          setError(
            text ||
            fallback
          );

          return;
        }
      } catch {
        setError(fallback);
        return;
      }
    }

    setError(
      err?.response?.data?.detail ||
      err?.message ||
      fallback
    );
  };

  // ----------------------------------------------------------
  // DOWNLOAD VIDEO
  // ----------------------------------------------------------

  const downloadVideo = () => {
    if (!videoUrl) {
      return;
    }

    const link = document.createElement('a');

    link.href = videoUrl;

    link.download =
      mode === 'text'
        ? 'phantom_ai_text_video.mp4'
        : 'phantom_ai_slideshow.mp4';

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);
  };

  // ----------------------------------------------------------
  // FORMAT FILE SIZE
  // ----------------------------------------------------------

  const formatFileSize = (bytes) => {
    if (!bytes) {
      return '0 KB';
    }

    const mb = bytes / (1024 * 1024);

    if (mb >= 1) {
      return `${mb.toFixed(2)} MB`;
    }

    return `${(bytes / 1024).toFixed(1)} KB`;
  };

  // ----------------------------------------------------------
  // RENDER
  // ----------------------------------------------------------

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '900px',
        margin: '0 auto',
      }}
    >

      {/* HEADER */}

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
                'rgba(0, 212, 255, 0.12)',
              border:
                '1px solid rgba(0, 212, 255, 0.25)',
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
              Video Generator
            </h2>

            <p
              style={{
                margin: '4px 0 0',
                color: '#77778a',
                fontSize: '13px',
              }}
            >
              Create videos from text or images.
            </p>
          </div>
        </div>
      </div>

      {/* MODE SELECTOR */}

      <div
        style={{
          display: 'flex',
          gap: '8px',
          marginBottom: '20px',
        }}
      >
        <button
          onClick={() => {
            setMode('text');
            setError('');
          }}
          disabled={loading}
          style={{
            flex: 1,
            padding: '12px',
            borderRadius: '9px',
            border:
              mode === 'text'
                ? '1px solid rgba(0,212,255,0.35)'
                : '1px solid rgba(255,255,255,0.08)',
            background:
              mode === 'text'
                ? 'rgba(0,212,255,0.10)'
                : '#0b0b11',
            color:
              mode === 'text'
                ? '#00d4ff'
                : '#9999aa',
            cursor: loading
              ? 'not-allowed'
              : 'pointer',
            fontWeight: '600',
          }}
        >
          📝 Text → Video
        </button>

        <button
          onClick={() => {
            setMode('slideshow');
            setError('');
          }}
          disabled={loading}
          style={{
            flex: 1,
            padding: '12px',
            borderRadius: '9px',
            border:
              mode === 'slideshow'
                ? '1px solid rgba(0,212,255,0.35)'
                : '1px solid rgba(255,255,255,0.08)',
            background:
              mode === 'slideshow'
                ? 'rgba(0,212,255,0.10)'
                : '#0b0b11',
            color:
              mode === 'slideshow'
                ? '#00d4ff'
                : '#9999aa',
            cursor: loading
              ? 'not-allowed'
              : 'pointer',
            fontWeight: '600',
          }}
        >
          🖼️ Images → Slideshow
        </button>
      </div>

      {/* WORKSPACE */}

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

        {/* TEXT MODE */}

        {mode === 'text' && (
          <>
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
              value={text}
              onChange={(event) =>
                setText(event.target.value)
              }
              placeholder="Example: Welcome to PhantomAI. This is a demonstration of text-to-video generation."
              rows={7}
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

            <div
              style={{
                marginTop: '14px',
              }}
            >
              <label
                style={{
                  display: 'block',
                  color: '#8d8da0',
                  fontSize: '12px',
                  marginBottom: '6px',
                }}
              >
                Duration: {duration} seconds
              </label>

              <input
                type="range"
                min="1"
                max="30"
                value={duration}
                onChange={(event) =>
                  setDuration(
                    Number(event.target.value)
                  )
                }
                disabled={loading}
                style={{
                  width: '100%',
                }}
              />
            </div>

            <button
              onClick={generateTextVideo}
              disabled={
                loading ||
                !text.trim()
              }
              style={{
                width: '100%',
                marginTop: '18px',
                padding: '13px',
                border: 'none',
                borderRadius: '9px',
                background:
                  loading || !text.trim()
                    ? '#30303a'
                    : '#00d4ff',
                color:
                  loading || !text.trim()
                    ? '#77778a'
                    : '#050509',
                fontWeight: '700',
                cursor:
                  loading || !text.trim()
                    ? 'not-allowed'
                    : 'pointer',
              }}
            >
              {loading
                ? '🎬 Generating Video...'
                : '✨ Generate Video'}
            </button>
          </>
        )}

        {/* SLIDESHOW MODE */}

        {mode === 'slideshow' && (
          <>
            <label
              style={{
                display: 'block',
                color: '#ffffff',
                fontSize: '14px',
                fontWeight: '600',
                marginBottom: '8px',
              }}
            >
              Select images
            </label>

            <input
              type="file"
              accept="image/*"
              multiple
              onChange={handleImageSelection}
              disabled={loading}
              style={{
                width: '100%',
                padding: '12px',
                borderRadius: '9px',
                border:
                  '1px solid rgba(255,255,255,0.08)',
                background: '#0b0b11',
                color: '#ffffff',
                boxSizing: 'border-box',
              }}
            />

            {images.length > 0 && (
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns:
                    'repeat(auto-fill,minmax(140px,1fr))',
                  gap: '12px',
                  marginTop: '18px',
                }}
              >
                {images.map((image, index) => (
                  <div
                    key={`${index}-${image.slice(-20)}`}
                    style={{
                      position: 'relative',
                      background: '#050509',
                      borderRadius: '9px',
                      overflow: 'hidden',
                      border:
                        '1px solid rgba(255,255,255,0.08)',
                    }}
                  >
                    <img
                      src={image}
                      alt={`Selected ${index + 1}`}
                      style={{
                        width: '100%',
                        height: '120px',
                        objectFit: 'cover',
                        display: 'block',
                      }}
                    />

                    <button
                      onClick={() =>
                        removeImage(index)
                      }
                      disabled={loading}
                      style={{
                        position: 'absolute',
                        top: '6px',
                        right: '6px',
                        width: '28px',
                        height: '28px',
                        borderRadius: '50%',
                        border: 'none',
                        background:
                          'rgba(0,0,0,0.75)',
                        color: '#ffffff',
                        cursor: 'pointer',
                      }}
                    >
                      ×
                    </button>

                    <div
                      style={{
                        padding: '7px',
                        color: '#77778a',
                        fontSize: '11px',
                      }}
                    >
                      Image {index + 1}
                    </div>
                  </div>
                ))}
              </div>
            )}

            <div
              style={{
                marginTop: '18px',
              }}
            >
              <label
                style={{
                  display: 'block',
                  color: '#8d8da0',
                  fontSize: '12px',
                  marginBottom: '6px',
                }}
              >
                Seconds per image:{' '}
                {durationPerImage}
              </label>

              <input
                type="range"
                min="1"
                max="15"
                value={durationPerImage}
                onChange={(event) =>
                  setDurationPerImage(
                    Number(event.target.value)
                  )
                }
                disabled={loading}
                style={{
                  width: '100%',
                }}
              />
            </div>

            <button
              onClick={generateSlideshow}
              disabled={
                loading ||
                images.length === 0
              }
              style={{
                width: '100%',
                marginTop: '18px',
                padding: '13px',
                border: 'none',
                borderRadius: '9px',
                background:
                  loading ||
                  images.length === 0
                    ? '#30303a'
                    : '#00d4ff',
                color:
                  loading ||
                  images.length === 0
                    ? '#77778a'
                    : '#050509',
                fontWeight: '700',
                cursor:
                  loading ||
                  images.length === 0
                    ? 'not-allowed'
                    : 'pointer',
              }}
            >
              {loading
                ? '🎬 Creating Slideshow...'
                : '✨ Create Slideshow'}
            </button>
          </>
        )}
      </div>

      {/* ERROR */}

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
          }}
        >
          {error}
        </div>
      )}

      {/* RESULT */}

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
              justifyContent: 'space-between',
              gap: '12px',
              marginBottom: '14px',
              flexWrap: 'wrap',
            }}
          >
            <div>
              <h3
                style={{
                  margin: 0,
                  color: '#ffffff',
                  fontSize: '16px',
                }}
              >
                🎬 Generated Video
              </h3>

              {videoBlob && (
                <p
                  style={{
                    margin:
                      '5px 0 0',
                    color: '#77778a',
                    fontSize: '12px',
                  }}
                >
                  {formatFileSize(
                    videoBlob.size
                  )}
                </p>
              )}
            </div>

            <div
              style={{
                display: 'flex',
                gap: '8px',
              }}
            >
              <button
                onClick={downloadVideo}
                style={{
                  padding: '8px 13px',
                  borderRadius: '7px',
                  border:
                    '1px solid rgba(0,212,255,0.25)',
                  background:
                    'rgba(0,212,255,0.08)',
                  color: '#00d4ff',
                  cursor: 'pointer',
                  fontWeight: '600',
                }}
              >
                ⬇ Download
              </button>

              <button
                onClick={clearWorkspace}
                style={{
                  padding: '8px 13px',
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
              background: '#000000',
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
              Result:
            </strong>{' '}
            Video generated successfully
            by PhantomAI.
          </div>
        </div>
      )}

    </div>
  );
};

export default VideoGenerationTool;
