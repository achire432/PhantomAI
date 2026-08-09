import React, { useEffect, useState } from 'react';
import { chat, pdf } from '../../api/endpoints';

const PDFTools = () => {
  const [conversations, setConversations] = useState([]);
  const [selectedConversationId, setSelectedConversationId] =
    useState('');

  const [loadingConversations, setLoadingConversations] =
    useState(false);

  const [loading, setLoading] = useState(null);

  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  // ============================================================
  // LOAD CONVERSATIONS
  // ============================================================

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    setLoadingConversations(true);
    setError('');
    setMessage('');

    try {
      const response = await chat.conversations();

      const data = response.data;

      if (Array.isArray(data)) {
        setConversations(data);

        if (data.length > 0) {
          setSelectedConversationId(String(data[0].id));
        }
      } else {
        setConversations([]);
      }
    } catch (err) {
      console.error(
        'Failed to load conversations:',
        err
      );

      setError(
        getErrorMessage(
          err,
          'Failed to load your conversations.'
        )
      );
    } finally {
      setLoadingConversations(false);
    }
  };

  // ============================================================
  // ERROR HANDLER
  // ============================================================

  const getErrorMessage = (err, fallback) => {
    if (err?.response?.data?.detail) {
      return err.response.data.detail;
    }

    if (err?.message) {
      return err.message;
    }

    return fallback;
  };

  // ============================================================
  // DOWNLOAD HELPER
  // ============================================================

  const downloadBlob = (blob, filename) => {
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');

    link.href = url;
    link.download = filename;

    document.body.appendChild(link);

    link.click();

    link.remove();

    URL.revokeObjectURL(url);
  };

  // ============================================================
  // CONVERSATION PDF
  // ============================================================

  const exportConversation = async () => {
    if (!selectedConversationId) {
      setError(
        'Please select a conversation first.'
      );

      setMessage('');

      return;
    }

    setLoading('conversation');
    setMessage('');
    setError('');

    try {
      const response = await pdf.conversation(
        selectedConversationId
      );

      downloadBlob(
        response.data,
        `conversation_${selectedConversationId}.pdf`
      );

      setMessage(
        'Conversation PDF generated successfully.'
      );
    } catch (err) {
      console.error(
        'Conversation PDF export failed:',
        err
      );

      setError(
        getErrorMessage(
          err,
          'Failed to generate conversation PDF.'
        )
      );
    } finally {
      setLoading(null);
    }
  };

  // ============================================================
  // NOTES PDF
  // ============================================================

  const exportNotes = async () => {
    setLoading('notes');
    setMessage('');
    setError('');

    try {
      const response = await pdf.notes();

      downloadBlob(
        response.data,
        'notes.pdf'
      );

      setMessage(
        'Notes PDF generated successfully.'
      );
    } catch (err) {
      console.error(
        'Notes PDF export failed:',
        err
      );

      setError(
        getErrorMessage(
          err,
          'Failed to generate notes PDF.'
        )
      );
    } finally {
      setLoading(null);
    }
  };

  // ============================================================
  // TASKS PDF
  // ============================================================

  const exportTasks = async () => {
    setLoading('tasks');
    setMessage('');
    setError('');

    try {
      const response = await pdf.tasks();

      downloadBlob(
        response.data,
        'tasks.pdf'
      );

      setMessage(
        'Tasks PDF generated successfully.'
      );
    } catch (err) {
      console.error(
        'Tasks PDF export failed:',
        err
      );

      setError(
        getErrorMessage(
          err,
          'Failed to generate tasks PDF.'
        )
      );
    } finally {
      setLoading(null);
    }
  };

  // ============================================================
  // STYLES
  // ============================================================

  const cardStyle = {
    background: 'rgba(18, 18, 26, 0.65)',
    border: '1px solid rgba(255,255,255,0.06)',
    borderRadius: '14px',
    padding: '20px',
    marginBottom: '14px',
  };

  const buttonStyle = (disabled = false) => ({
    width: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',

    padding: '13px 16px',

    borderRadius: '9px',

    border: disabled
      ? '1px solid rgba(255,255,255,0.05)'
      : '1px solid rgba(0,212,255,0.20)',

    background: disabled
      ? 'rgba(255,255,255,0.03)'
      : 'rgba(0,212,255,0.08)',

    color: disabled
      ? '#555568'
      : '#00d4ff',

    cursor: disabled
      ? 'not-allowed'
      : 'pointer',

    fontSize: '13px',

    fontWeight: '600',

    transition: 'all 0.2s ease',
  });

  const selectStyle = {
    width: '100%',

    padding: '13px 14px',

    borderRadius: '9px',

    border:
      '1px solid rgba(255,255,255,0.08)',

    background:
      'rgba(5,5,9,0.9)',

    color: '#ffffff',

    fontSize: '13px',

    outline: 'none',

    boxSizing: 'border-box',

    marginBottom: '12px',

    cursor:
      conversations.length > 0
        ? 'pointer'
        : 'not-allowed',
  };

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '760px',
        margin: '0 auto',
      }}
    >

      {/* ======================================================
          CONVERSATION PDF
      ======================================================= */}

      <div style={cardStyle}>

        <div
          style={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: '14px',
            marginBottom: '16px',
          }}
        >

          <div
            style={{
              width: '44px',
              height: '44px',

              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',

              borderRadius: '10px',

              background:
                'rgba(0,212,255,0.08)',

              border:
                '1px solid rgba(0,212,255,0.12)',

              fontSize: '22px',

              flexShrink: 0,
            }}
          >
            📄
          </div>

          <div>

            <h3
              style={{
                margin: '0 0 5px',

                color: '#ffffff',

                fontSize: '16px',

                fontWeight: '600',
              }}
            >
              Conversation PDF
            </h3>

            <p
              style={{
                margin: 0,

                color: '#666679',

                fontSize: '12px',

                lineHeight: '1.5',
              }}
            >
              Select one of your PhantomAI conversations
              and export the complete conversation as a PDF.
            </p>

          </div>

        </div>

        {/* ==================================================
            CONVERSATION SELECTOR
        ================================================== */}

        <label
          style={{
            display: 'block',

            marginBottom: '7px',

            color: '#aaaabd',

            fontSize: '12px',

            fontWeight: '600',
          }}
        >
          Select conversation
        </label>

        {loadingConversations ? (

          <div
            style={{
              padding: '13px',

              marginBottom: '12px',

              borderRadius: '9px',

              background:
                'rgba(255,255,255,0.025)',

              border:
                '1px solid rgba(255,255,255,0.05)',

              color: '#666679',

              fontSize: '12px',
            }}
          >
            Loading your conversations...
          </div>

        ) : conversations.length === 0 ? (

          <div
            style={{
              padding: '13px',

              marginBottom: '12px',

              borderRadius: '9px',

              background:
                'rgba(255,255,255,0.025)',

              border:
                '1px solid rgba(255,255,255,0.05)',

              color: '#666679',

              fontSize: '12px',

              lineHeight: '1.5',
            }}
          >
            You don't have any conversations yet.
            Start a conversation with PhantomAI first.
          </div>

        ) : (

          <select
            value={selectedConversationId}
            onChange={(e) =>
              setSelectedConversationId(
                e.target.value
              )
            }
            style={selectStyle}
            disabled={loading !== null}
          >

            <option
              value=""
              style={{
                background: '#101018',
              }}
            >
              Select a conversation...
            </option>

            {conversations.map((conversation) => (

              <option
                key={conversation.id}
                value={conversation.id}
                style={{
                  background: '#101018',
                }}
              >
                {conversation.title ||
                  `Conversation #${conversation.id}`}
              </option>

            ))}

          </select>

        )}

        <button
          type="button"
          onClick={exportConversation}
          disabled={
            !selectedConversationId ||
            loading !== null ||
            loadingConversations
          }
          style={buttonStyle(
            !selectedConversationId ||
            loading !== null ||
            loadingConversations
          )}
        >

          {loading === 'conversation' ? (

            <>
              <span>⏳</span>
              <span>
                Generating PDF...
              </span>
            </>

          ) : (

            <>
              <span>⬇</span>
              <span>
                Export Conversation
              </span>
            </>

          )}

        </button>

      </div>

      {/* ======================================================
          NOTES PDF
      ======================================================= */}

      <div style={cardStyle}>

        <div
          style={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: '14px',
            marginBottom: '16px',
          }}
        >

          <div
            style={{
              width: '44px',
              height: '44px',

              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',

              borderRadius: '10px',

              background:
                'rgba(0,212,255,0.08)',

              border:
                '1px solid rgba(0,212,255,0.12)',

              fontSize: '22px',

              flexShrink: 0,
            }}
          >
            📝
          </div>

          <div>

            <h3
              style={{
                margin: '0 0 5px',

                color: '#ffffff',

                fontSize: '16px',

                fontWeight: '600',
              }}
            >
              Notes PDF
            </h3>

            <p
              style={{
                margin: 0,

                color: '#666679',

                fontSize: '12px',

                lineHeight: '1.5',
              }}
            >
              Export your saved PhantomAI notes
              into a PDF document.
            </p>

          </div>

        </div>

        <button
          type="button"
          onClick={exportNotes}
          disabled={loading !== null}
          style={buttonStyle(
            loading !== null
          )}
        >

          {loading === 'notes' ? (

            <>
              <span>⏳</span>
              <span>
                Generating PDF...
              </span>
            </>

          ) : (

            <>
              <span>⬇</span>
              <span>
                Export Notes
              </span>
            </>

          )}

        </button>

      </div>

      {/* ======================================================
          TASKS PDF
      ======================================================= */}

      <div style={cardStyle}>

        <div
          style={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: '14px',
            marginBottom: '16px',
          }}
        >

          <div
            style={{
              width: '44px',
              height: '44px',

              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',

              borderRadius: '10px',

              background:
                'rgba(0,212,255,0.08)',

              border:
                '1px solid rgba(0,212,255,0.12)',

              fontSize: '22px',

              flexShrink: 0,
            }}
          >
            ✅
          </div>

          <div>

            <h3
              style={{
                margin: '0 0 5px',

                color: '#ffffff',

                fontSize: '16px',

                fontWeight: '600',
              }}
            >
              Tasks PDF
            </h3>

            <p
              style={{
                margin: 0,

                color: '#666679',

                fontSize: '12px',

                lineHeight: '1.5',
              }}
            >
              Export your PhantomAI tasks
              with their status, priority,
              and due dates.
            </p>

          </div>

        </div>

        <button
          type="button"
          onClick={exportTasks}
          disabled={loading !== null}
          style={buttonStyle(
            loading !== null
          )}
        >

          {loading === 'tasks' ? (

            <>
              <span>⏳</span>
              <span>
                Generating PDF...
              </span>
            </>

          ) : (

            <>
              <span>⬇</span>
              <span>
                Export Tasks
              </span>
            </>

          )}

        </button>

      </div>

      {/* ======================================================
          SUCCESS
      ======================================================= */}

      {message && (

        <div
          style={{
            marginTop: '16px',

            padding: '12px 14px',

            borderRadius: '9px',

            border:
              '1px solid rgba(0,212,255,0.15)',

            background:
              'rgba(0,212,255,0.06)',

            color: '#00d4ff',

            fontSize: '12px',

            lineHeight: '1.5',
          }}
        >
          ✓ {message}
        </div>

      )}

      {/* ======================================================
          ERROR
      ======================================================= */}

      {error && (

        <div
          style={{
            marginTop: '16px',

            padding: '12px 14px',

            borderRadius: '9px',

            border:
              '1px solid rgba(255,80,80,0.15)',

            background:
              'rgba(255,80,80,0.06)',

            color: '#ff7777',

            fontSize: '12px',

            lineHeight: '1.5',
          }}
        >
          ✕ {error}
        </div>

      )}

    </div>
  );
};

export default PDFTools;