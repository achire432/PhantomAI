
import React, { useEffect, useState } from 'react';
import { tools } from '../../api/endpoints';

const FilesTool = () => {
  const [currentPath, setCurrentPath] = useState('');
  const [contents, setContents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searching, setSearching] = useState(false);

  const [selectedFile, setSelectedFile] = useState(null);
  const [folderSize, setFolderSize] = useState(null);
  const [loadingSize, setLoadingSize] = useState(false);

  const [fileText, setFileText] = useState('');
  const [reading, setReading] = useState(false);

  const [question, setQuestion] = useState('');
  const [asking, setAsking] = useState(false);
  const [answer, setAnswer] = useState('');

  const [summary, setSummary] = useState('');
  const [summarizing, setSummarizing] = useState(false);

  const [exporting, setExporting] = useState(false);

  const loadDirectory = async (path = '') => {
    setLoading(true);
    setError('');
    setSelectedFile(null);
    setFolderSize(null);
    setFileText('');
    setAnswer('');
    setSummary('');

    try {
      const response = await tools.files.list(path);

      setContents(response.data.contents || []);
      setCurrentPath(response.data.path || path);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Unable to load this directory.'
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDirectory('');
  }, []);

  const openItem = async (item) => {
    if (item.type === 'directory') {
      const nextPath = `${currentPath}/${item.name}`;
      await loadDirectory(nextPath);
      return;
    }

    setError('');
    setFileText('');
    setAnswer('');
    setSummary('');

    try {
      const response = await tools.files.info(
        `${currentPath}/${item.name}`
      );

      setSelectedFile(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Unable to get file information.'
      );
    }
  };

  const selectFileFromDropdown = async (event) => {
    const path = event.target.value;

    if (!path) {
      setSelectedFile(null);
      setFileText('');
      setAnswer('');
      setSummary('');
      return;
    }

    setError('');
    setFileText('');
    setAnswer('');
    setSummary('');

    try {
      const response = await tools.files.info(path);
      setSelectedFile(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Unable to get file information.'
      );
    }
  };

  const goUp = async () => {
    if (!currentPath) return;

    const parentPath = currentPath.substring(
      0,
      currentPath.lastIndexOf('/')
    );

    await loadDirectory(parentPath || '/');
  };

  const searchFiles = async () => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }

    setSearching(true);
    setError('');

    try {
      const response = await tools.files.search(
        searchQuery,
        currentPath
      );

      setSearchResults(response.data.results || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Unable to search files.'
      );
    } finally {
      setSearching(false);
    }
  };

  const showFolderSize = async () => {
    setLoadingSize(true);
    setError('');

    try {
      const response = await tools.files.size(currentPath);
      setFolderSize(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Unable to calculate folder size.'
      );
    } finally {
      setLoadingSize(false);
    }
  };

  const readSelectedFile = async () => {
    if (!selectedFile?.path) return;

    setReading(true);
    setError('');
    setFileText('');
    setAnswer('');
    setSummary('');

    try {
      const response = await tools.files.read(
        selectedFile.path
      );

      setFileText(response.data.text || '');
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Unable to read this file.'
      );
    } finally {
      setReading(false);
    }
  };

  const askPhantom = async () => {
    if (!selectedFile?.path) return;

    if (!question.trim()) {
      setError('Please enter a question first.');
      return;
    }

    setAsking(true);
    setError('');
    setAnswer('');

    try {
      const response = await tools.files.ask(
        selectedFile.path,
        question
      );

      setAnswer(response.data.answer || '');
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Unable to ask PhantomAI about this file.'
      );
    } finally {
      setAsking(false);
    }
  };

  const summarizeSelectedFile = async () => {
    if (!selectedFile?.path) return;

    setSummarizing(true);
    setError('');
    setSummary('');

    try {
      const response = await tools.files.summarize(
        selectedFile.path
      );

      setSummary(response.data.summary || '');
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Unable to summarize this file.'
      );
    } finally {
      setSummarizing(false);
    }
  };

  const exportSelectedFile = async () => {
    if (!selectedFile?.path) return;

    setExporting(true);
    setError('');

    try {
      const response = await tools.files.exportPdf(
        selectedFile.path
      );

      const blob = new Blob(
        [response.data],
        { type: 'application/pdf' }
      );

      const url = window.URL.createObjectURL(blob);

      const link = document.createElement('a');
      link.href = url;
      link.download = `${selectedFile.name || 'file'}.pdf`;

      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Unable to export this file as PDF.'
      );
    } finally {
      setExporting(false);
    }
  };

  const formatSize = (bytes) => {
    if (bytes === null || bytes === undefined) {
      return '—';
    }

    if (bytes < 1024) {
      return `${bytes} B`;
    }

    if (bytes < 1024 * 1024) {
      return `${(bytes / 1024).toFixed(1)} KB`;
    }

    if (bytes < 1024 * 1024 * 1024) {
      return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    }

    return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`;
  };

  const fileItems = contents.filter(
    (item) => item.type === 'file'
  );

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '900px',
        margin: '0 auto',
        padding: '30px',
        borderRadius: '16px',
        border: '1px solid rgba(255,255,255,0.06)',
        background: 'rgba(18,18,26,0.65)',
        boxSizing: 'border-box',
      }}
    >
      {/* HEADER */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          gap: '15px',
          marginBottom: '20px',
        }}
      >
        <div>
          <div
            style={{
              fontSize: '42px',
              marginBottom: '8px',
            }}
          >
            📁
          </div>

          <h2
            style={{
              margin: 0,
              color: '#ffffff',
              fontSize: '22px',
            }}
          >
            Files
          </h2>

          <p
            style={{
              margin: '6px 0 0',
              color: '#77778a',
              fontSize: '13px',
            }}
          >
            Browse, read and work with your files.
          </p>
        </div>

        <button
          type="button"
          onClick={() => loadDirectory(currentPath)}
          disabled={loading}
          style={{
            padding: '10px 14px',
            borderRadius: '9px',
            border: '1px solid rgba(255,255,255,0.08)',
            background: 'rgba(255,255,255,0.05)',
            color: '#ffffff',
            cursor: loading
              ? 'not-allowed'
              : 'pointer',
          }}
        >
          🔄 Refresh
        </button>
      </div>

      {/* SELECTED FILE DROPDOWN */}
      <div
        style={{
          marginBottom: '15px',
        }}
      >
        <label
          style={{
            display: 'block',
            color: '#aaaabb',
            fontSize: '12px',
            marginBottom: '7px',
          }}
        >
          Selected file
        </label>

        <select
          value={selectedFile?.path || ''}
          onChange={selectFileFromDropdown}
          style={{
            width: '100%',
            padding: '12px',
            borderRadius: '9px',
            border: '1px solid rgba(255,255,255,0.08)',
            background: '#0c0c12',
            color: '#ffffff',
            outline: 'none',
            boxSizing: 'border-box',
          }}
        >
          <option value="">
            Select a file...
          </option>

          {fileItems.map((item) => {
            const itemPath = `${currentPath}/${item.name}`;

            return (
              <option
                key={itemPath}
                value={itemPath}
              >
                📄 {item.name}
              </option>
            );
          })}
        </select>
      </div>

      {/* SELECTED FILE ACTION PANEL */}
      {selectedFile && (
        <div
          style={{
            position: 'sticky',
            top: '12px',
            zIndex: 10,
            marginBottom: '20px',
            padding: '18px',
            borderRadius: '12px',
            border:
              '1px solid rgba(0,212,255,0.20)',
            background:
              'rgba(10,14,24,0.96)',
            boxShadow:
              '0 10px 30px rgba(0,0,0,0.25)',
            backdropFilter: 'blur(12px)',
          }}
        >
          {/* FILE HEADER */}
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'flex-start',
              gap: '15px',
              marginBottom: '15px',
            }}
          >
            <div
              style={{
                minWidth: 0,
              }}
            >
              <div
                style={{
                  color: '#ffffff',
                  fontSize: '17px',
                  fontWeight: '600',
                  wordBreak: 'break-word',
                }}
              >
                📄 {selectedFile.name}
              </div>

              <div
                style={{
                  marginTop: '5px',
                  color: '#77778a',
                  fontSize: '12px',
                  wordBreak: 'break-all',
                }}
              >
                {selectedFile.extension || 'File'} ·{' '}
                {formatSize(selectedFile.size)}
              </div>
            </div>

            <button
              type="button"
              onClick={() => {
                setSelectedFile(null);
                setFileText('');
                setAnswer('');
                setSummary('');
              }}
              style={{
                border: 'none',
                background: 'rgba(255,255,255,0.06)',
                color: '#aaaabb',
                borderRadius: '8px',
                padding: '7px 10px',
                cursor: 'pointer',
              }}
            >
              ✕
            </button>
          </div>

          {/* ACTION BUTTONS */}
          <div
            style={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: '8px',
            }}
          >
            <button
              type="button"
              onClick={readSelectedFile}
              disabled={reading}
              style={{
                padding: '10px 13px',
                borderRadius: '8px',
                border: '1px solid rgba(255,255,255,0.08)',
                background: 'rgba(255,255,255,0.05)',
                color: '#ffffff',
                cursor: reading
                  ? 'not-allowed'
                  : 'pointer',
              }}
            >
              {reading ? 'Reading...' : '📖 Read'}
            </button>

            <button
              type="button"
              onClick={summarizeSelectedFile}
              disabled={summarizing}
              style={{
                padding: '10px 13px',
                borderRadius: '8px',
                border: 'none',
                background: 'rgba(0,212,255,0.9)',
                color: '#ffffff',
                cursor: summarizing
                  ? 'not-allowed'
                  : 'pointer',
              }}
            >
              {summarizing
                ? 'Summarizing...'
                : '📝 Summarize'}
            </button>

            <button
              type="button"
              onClick={exportSelectedFile}
              disabled={exporting}
              style={{
                padding: '10px 13px',
                borderRadius: '8px',
                border: '1px solid rgba(255,255,255,0.08)',
                background: 'rgba(255,255,255,0.05)',
                color: '#ffffff',
                cursor: exporting
                  ? 'not-allowed'
                  : 'pointer',
              }}
            >
              {exporting
                ? 'Exporting...'
                : '📄 Export PDF'}
            </button>
          </div>

          {/* ASK PHANTOM */}
          <div
            style={{
              marginTop: '15px',
              paddingTop: '15px',
              borderTop:
                '1px solid rgba(255,255,255,0.06)',
            }}
          >
            <div
              style={{
                color: '#aaaabb',
                fontSize: '12px',
                marginBottom: '7px',
              }}
            >
              Ask PhantomAI about this file
            </div>

            <div
              style={{
                display: 'flex',
                gap: '8px',
              }}
            >
              <input
                value={question}
                onChange={(e) =>
                  setQuestion(e.target.value)
                }
                onKeyDown={(e) => {
                  if (
                    e.key === 'Enter' &&
                    !asking
                  ) {
                    askPhantom();
                  }
                }}
                placeholder="Ask something about this file..."
                style={{
                  flex: 1,
                  minWidth: 0,
                  padding: '11px 12px',
                  borderRadius: '8px',
                  border:
                    '1px solid rgba(255,255,255,0.08)',
                  background: '#0c0c12',
                  color: '#ffffff',
                  outline: 'none',
                }}
              />

              <button
                type="button"
                onClick={askPhantom}
                disabled={asking}
                style={{
                  padding: '11px 15px',
                  borderRadius: '8px',
                  border: 'none',
                  background:
                    'rgba(0,212,255,0.9)',
                  color: '#ffffff',
                  fontWeight: '600',
                  cursor: asking
                    ? 'not-allowed'
                    : 'pointer',
                }}
              >
                {asking
                  ? 'Thinking...'
                  : '🤖 Ask'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* FILE CONTENT / AI OUTPUT */}
      {selectedFile && (
        <div
          style={{
            marginBottom: '20px',
          }}
        >
          {fileText && (
            <div
              style={{
                marginBottom: '15px',
                padding: '18px',
                borderRadius: '10px',
                background: 'rgba(255,255,255,0.03)',
                border:
                  '1px solid rgba(255,255,255,0.06)',
              }}
            >
              <div
                style={{
                  color: '#ffffff',
                  fontSize: '14px',
                  fontWeight: '600',
                  marginBottom: '10px',
                }}
              >
                📖 File Content
              </div>

              <pre
                style={{
                  margin: 0,
                  color: '#c7c7d4',
                  fontSize: '13px',
                  lineHeight: 1.6,
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word',
                  maxHeight: '450px',
                  overflowY: 'auto',
                }}
              >
                {fileText}
              </pre>
            </div>
          )}

          {summary && (
            <div
              style={{
                marginBottom: '15px',
                padding: '18px',
                borderRadius: '10px',
                background:
                  'rgba(0,212,255,0.05)',
                border:
                  '1px solid rgba(0,212,255,0.12)',
              }}
            >
              <div
                style={{
                  color: '#ffffff',
                  fontSize: '14px',
                  fontWeight: '600',
                  marginBottom: '10px',
                }}
              >
                📝 Summary
              </div>

              <div
                style={{
                  color: '#c7c7d4',
                  fontSize: '13px',
                  lineHeight: 1.6,
                  whiteSpace: 'pre-wrap',
                }}
              >
                {summary}
              </div>
            </div>
          )}

          {answer && (
            <div
              style={{
                marginBottom: '15px',
                padding: '18px',
                borderRadius: '10px',
                background:
                  'rgba(120,80,255,0.06)',
                border:
                  '1px solid rgba(120,80,255,0.14)',
              }}
            >
              <div
                style={{
                  color: '#ffffff',
                  fontSize: '14px',
                  fontWeight: '600',
                  marginBottom: '10px',
                }}
              >
                🤖 PhantomAI
              </div>

              <div
                style={{
                  color: '#c7c7d4',
                  fontSize: '13px',
                  lineHeight: 1.6,
                  whiteSpace: 'pre-wrap',
                }}
              >
                {answer}
              </div>
            </div>
          )}
        </div>
      )}

      {/* PATH BAR */}
      <div
        style={{
          display: 'flex',
          gap: '8px',
          marginBottom: '20px',
        }}
      >
        <button
          type="button"
          onClick={goUp}
          disabled={!currentPath || loading}
          style={{
            padding: '11px 14px',
            borderRadius: '9px',
            border:
              '1px solid rgba(255,255,255,0.08)',
            background:
              'rgba(255,255,255,0.05)',
            color: '#ffffff',
            cursor:
              !currentPath || loading
                ? 'not-allowed'
                : 'pointer',
          }}
        >
          ⬆️
        </button>

        <input
          value={currentPath}
          readOnly
          style={{
            flex: 1,
            minWidth: 0,
            padding: '11px 13px',
            borderRadius: '9px',
            border:
              '1px solid rgba(255,255,255,0.08)',
            background: '#0c0c12',
            color: '#aaaabb',
            outline: 'none',
          }}
        />

        <button
          type="button"
          onClick={showFolderSize}
          disabled={loadingSize || loading}
          style={{
            padding: '11px 14px',
            borderRadius: '9px',
            border:
              '1px solid rgba(255,255,255,0.08)',
            background:
              'rgba(0,212,255,0.08)',
            color: '#ffffff',
            cursor:
              loadingSize || loading
                ? 'not-allowed'
                : 'pointer',
          }}
        >
          {loadingSize
            ? 'Calculating...'
            : '📦 Size'}
        </button>
      </div>

      {/* FOLDER SIZE */}
      {folderSize && (
        <div
          style={{
            marginBottom: '18px',
            padding: '13px',
            borderRadius: '9px',
            background:
              'rgba(0,212,255,0.06)',
            border:
              '1px solid rgba(0,212,255,0.12)',
            color: '#ffffff',
            fontSize: '13px',
          }}
        >
          Folder size:{' '}
          <strong>
            {folderSize.size_readable}
          </strong>
        </div>
      )}

      {/* SEARCH */}
      <div
        style={{
          display: 'flex',
          gap: '8px',
          marginBottom: '20px',
        }}
      >
        <input
          value={searchQuery}
          onChange={(e) =>
            setSearchQuery(e.target.value)
          }
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              searchFiles();
            }
          }}
          placeholder="Search files by name..."
          style={{
            flex: 1,
            padding: '12px 13px',
            borderRadius: '9px',
            border:
              '1px solid rgba(255,255,255,0.08)',
            background: '#0c0c12',
            color: '#ffffff',
            outline: 'none',
            boxSizing: 'border-box',
          }}
        />

        <button
          type="button"
          onClick={searchFiles}
          disabled={searching}
          style={{
            padding: '12px 18px',
            borderRadius: '9px',
            border: 'none',
            background:
              'rgba(0,212,255,0.9)',
            color: '#ffffff',
            fontWeight: '600',
            cursor: searching
              ? 'not-allowed'
              : 'pointer',
          }}
        >
          {searching
            ? 'Searching...'
            : '🔍 Search'}
        </button>
      </div>

      {/* ERROR */}
      {error && (
        <div
          style={{
            marginBottom: '18px',
            padding: '13px',
            borderRadius: '9px',
            background:
              'rgba(255,70,70,0.08)',
            border:
              '1px solid rgba(255,70,70,0.2)',
            color: '#ff8b8b',
            fontSize: '13px',
          }}
        >
          {error}
        </div>
      )}

      {/* SEARCH RESULTS */}
      {searchResults.length > 0 && (
        <div
          style={{
            marginBottom: '20px',
          }}
        >
          <div
            style={{
              color: '#aaaabb',
              fontSize: '12px',
              marginBottom: '8px',
            }}
          >
            Search results
          </div>

          {searchResults.map((item) => (
            <button
              key={item.path}
              type="button"
              onClick={() =>
                selectFileFromDropdown({
                  target: {
                    value: item.path,
                  },
                })
              }
              style={{
                display: 'block',
                width: '100%',
                textAlign: 'left',
                padding: '11px',
                marginBottom: '6px',
                borderRadius: '8px',
                border:
                  '1px solid rgba(255,255,255,0.06)',
                background:
                  'rgba(255,255,255,0.03)',
                color: '#ffffff',
                cursor: 'pointer',
              }}
            >
              📄 {item.name}
            </button>
          ))}
        </div>
      )}

      {/* CURRENT DIRECTORY */}
      <div
        style={{
          color: '#aaaabb',
          fontSize: '12px',
          marginBottom: '8px',
        }}
      >
        Current folder
      </div>

      <div
        style={{
          border:
            '1px solid rgba(255,255,255,0.06)',
          borderRadius: '10px',
          overflow: 'hidden',
        }}
      >
        {loading ? (
          <div
            style={{
              padding: '30px',
              textAlign: 'center',
              color: '#77778a',
            }}
          >
            Loading files...
          </div>
        ) : contents.length === 0 ? (
          <div
            style={{
              padding: '30px',
              textAlign: 'center',
              color: '#77778a',
            }}
          >
            This folder is empty.
          </div>
        ) : (
          contents.map((item) => (
            <button
              key={`${item.type}-${item.name}`}
              type="button"
              onClick={() => openItem(item)}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                width: '100%',
                padding: '13px 15px',
                border: 'none',
                borderBottom:
                  '1px solid rgba(255,255,255,0.04)',
                background:
                  selectedFile?.path ===
                  `${currentPath}/${item.name}`
                    ? 'rgba(0,212,255,0.08)'
                    : 'transparent',
                color: '#ffffff',
                textAlign: 'left',
                cursor: 'pointer',
              }}
            >
              <span
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  minWidth: 0,
                }}
              >
                <span>
                  {item.type === 'directory'
                    ? '📁'
                    : '📄'}
                </span>

                <span
                  style={{
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                  }}
                >
                  {item.name}
                </span>
              </span>

              <span
                style={{
                  marginLeft: '10px',
                  color: '#666677',
                  fontSize: '11px',
                  flexShrink: 0,
                }}
              >
                {item.type === 'directory'
                  ? 'Folder'
                  : formatSize(item.size)}
              </span>
            </button>
          ))
        )}
      </div>
    </div>
  );
};

export default FilesTool;
