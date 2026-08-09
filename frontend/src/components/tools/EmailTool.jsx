import React, { useEffect, useState } from 'react';
import { tools } from '../../api/endpoints';

const EmailTool = () => {
  const [emails, setEmails] = useState([]);
  const [drafts, setDrafts] = useState([]);

  const [loading, setLoading] = useState(false);
  const [draftLoading, setDraftLoading] = useState(false);
  const [sending, setSending] = useState(false);

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [activeView, setActiveView] = useState('inbox');

  const [selectedEmail, setSelectedEmail] = useState(null);
  const [summaryLoading, setSummaryLoading] = useState(false);

  const [draftForm, setDraftForm] = useState({
    to: '',
    subject: '',
    body: '',
  });

  // ==========================================================
  // LOAD EMAILS
  // ==========================================================

  const loadEmails = async () => {
    try {
      setLoading(true);
      setError('');

      const response = await tools.email.getRecent(10);

      setEmails(response.data || []);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
        'Failed to load emails.'
      );
    } finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // LOAD DRAFTS
  // ==========================================================

  const loadDrafts = async () => {
    try {
      setDraftLoading(true);
      setError('');

      const response = await tools.email.getDrafts();

      setDrafts(response.data || []);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
        'Failed to load drafts.'
      );
    } finally {
      setDraftLoading(false);
    }
  };

  useEffect(() => {
    loadEmails();
    loadDrafts();
  }, []);

  // ==========================================================
  // SUMMARIZE EMAIL
  // ==========================================================

  const handleSummarize = async (email) => {
    try {
      setSummaryLoading(true);
      setError('');
      setSuccess('');

      const response = await tools.email.summarize(email.id);

      const summary = response.data?.summary || '';

      setEmails((previous) =>
        previous.map((item) =>
          item.id === email.id
            ? {
                ...item,
                summary,
                is_read: true,
              }
            : item
        )
      );

      setSelectedEmail({
        ...email,
        summary,
        is_read: true,
      });

      setSuccess('Email summarized successfully.');
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
        'Failed to summarize email.'
      );
    } finally {
      setSummaryLoading(false);
    }
  };

  // ==========================================================
  // DRAFT FORM
  // ==========================================================

  const handleDraftChange = (event) => {
    const { name, value } = event.target;

    setDraftForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const resetDraftForm = () => {
    setDraftForm({
      to: '',
      subject: '',
      body: '',
    });
  };

  // ==========================================================
  // CREATE AI DRAFT
  // ==========================================================

  const handleCreateDraft = async (event) => {
    event.preventDefault();

    if (!draftForm.to.trim()) {
      setError('Recipient email is required.');
      return;
    }

    if (!draftForm.subject.trim()) {
      setError('Subject is required.');
      return;
    }

    if (!draftForm.body.trim()) {
      setError('Email instructions or content are required.');
      return;
    }

    try {
      setDraftLoading(true);
      setError('');
      setSuccess('');

      const response =
        await tools.email.createDraft({
          to: draftForm.to.trim(),
          subject: draftForm.subject.trim(),
          body: draftForm.body.trim(),
        });

      const newDraft = response.data;

      setDrafts((previous) => [
        newDraft,
        ...previous,
      ]);

      setDraftForm({
        to: newDraft.to || '',
        subject: newDraft.subject || '',
        body: newDraft.body || '',
      });

      setSuccess('AI draft created successfully.');
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
        'Failed to create draft.'
      );
    } finally {
      setDraftLoading(false);
    }
  };

  // ==========================================================
  // SEND EMAIL
  // ==========================================================

  const handleSendEmail = async (event) => {
    event.preventDefault();

    if (!draftForm.to.trim()) {
      setError('Recipient email is required.');
      return;
    }

    if (!draftForm.subject.trim()) {
      setError('Subject is required.');
      return;
    }

    if (!draftForm.body.trim()) {
      setError('Email body is required.');
      return;
    }

    const confirmed = window.confirm(
      `Send this email to ${draftForm.to}?`
    );

    if (!confirmed) {
      return;
    }

    try {
      setSending(true);
      setError('');
      setSuccess('');

      const response =
        await tools.email.send({
          to: draftForm.to.trim(),
          subject: draftForm.subject.trim(),
          body: draftForm.body.trim(),
        });

      setSuccess(
        response.data?.message ||
        'Email sent successfully.'
      );

      resetDraftForm();

      await loadDrafts();
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
        'Failed to send email.'
      );
    } finally {
      setSending(false);
    }
  };

  // ==========================================================
  // OPEN EMAIL
  // ==========================================================

  const handleOpenEmail = (email) => {
    setSelectedEmail(email);
    setError('');
    setSuccess('');
  };

  // ==========================================================
  // FORMAT DATE
  // ==========================================================

  const formatDate = (date) => {
    if (!date) {
      return '';
    }

    try {
      return new Date(date).toLocaleString();
    } catch {
      return date;
    }
  };

  // ==========================================================
  // EMAIL LIST
  // ==========================================================

  const renderInbox = () => {
    if (loading) {
      return (
        <div style={emptyStyle}>
          Loading emails...
        </div>
      );
    }

    if (emails.length === 0) {
      return (
        <div style={emptyStyle}>
          <div
            style={{
              fontSize: '38px',
              marginBottom: '10px',
            }}
          >
            ✉️
          </div>

          <div
            style={{
              color: '#fff',
              fontWeight: '600',
            }}
          >
            No recent emails
          </div>

          <div
            style={{
              marginTop: '6px',
              color: '#666679',
              fontSize: '13px',
            }}
          >
            PhantomAI could not find any recent emails.
          </div>
        </div>
      );
    }

    return (
      <div
        style={{
          display: 'grid',
          gap: '10px',
        }}
      >
        {emails.map((email) => (
          <div
            key={email.id}
            onClick={() => handleOpenEmail(email)}
            style={{
              background: '#12121a',
              border: email.is_read
                ? '1px solid rgba(255,255,255,0.07)'
                : '1px solid rgba(0,212,255,0.25)',
              borderRadius: '12px',
              padding: '15px',
              cursor: 'pointer',
              transition: '0.2s',
            }}
          >
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                gap: '12px',
              }}
            >
              <div
                style={{
                  minWidth: 0,
                  flex: 1,
                }}
              >
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    marginBottom: '5px',
                  }}
                >
                  {!email.is_read && (
                    <span
                      style={{
                        width: '7px',
                        height: '7px',
                        borderRadius: '50%',
                        background: '#00d4ff',
                        display: 'inline-block',
                      }}
                    />
                  )}

                  <strong
                    style={{
                      color: '#fff',
                      fontSize: '14px',
                    }}
                  >
                    {email.sender}
                  </strong>
                </div>

                <div
                  style={{
                    color: '#ddd',
                    fontSize: '14px',
                    fontWeight: '600',
                  }}
                >
                  {email.subject || 'No Subject'}
                </div>

                <div
                  style={{
                    color: '#77778a',
                    fontSize: '12px',
                    marginTop: '6px',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                  }}
                >
                  {email.body}
                </div>
              </div>

              <div
                style={{
                  color: '#666679',
                  fontSize: '11px',
                  whiteSpace: 'nowrap',
                }}
              >
                {formatDate(email.received_at)}
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  };

  // ==========================================================
  // EMAIL DETAIL
  // ==========================================================

  const renderEmailDetail = () => {
    if (!selectedEmail) {
      return (
        <div style={emptyStyle}>
          Select an email to view it.
        </div>
      );
    }

    return (
      <div
        style={{
          background: '#12121a',
          border:
            '1px solid rgba(255,255,255,0.07)',
          borderRadius: '14px',
          padding: '20px',
        }}
      >
        <button
          type="button"
          onClick={() => setSelectedEmail(null)}
          style={{
            ...actionButtonStyle,
            marginBottom: '18px',
          }}
        >
          ← Back
        </button>

        <h3
          style={{
            margin: '0 0 8px',
            color: '#fff',
          }}
        >
          {selectedEmail.subject || 'No Subject'}
        </h3>

        <div
          style={{
            color: '#77778a',
            fontSize: '12px',
            marginBottom: '18px',
          }}
        >
          From: {selectedEmail.sender}
          <br />
          Received: {formatDate(selectedEmail.received_at)}
        </div>

        <div
          style={{
            background: '#08080d',
            borderRadius: '10px',
            padding: '15px',
            color: '#d4d4df',
            fontSize: '13px',
            lineHeight: '1.6',
            whiteSpace: 'pre-wrap',
            maxHeight: '350px',
            overflowY: 'auto',
          }}
        >
          {selectedEmail.body}
        </div>

        <div
          style={{
            marginTop: '16px',
            display: 'flex',
            gap: '8px',
            flexWrap: 'wrap',
          }}
        >
          <button
            type="button"
            onClick={() =>
              handleSummarize(selectedEmail)
            }
            disabled={summaryLoading}
            style={{
              ...primaryButtonStyle,
              opacity: summaryLoading ? 0.6 : 1,
            }}
          >
            {summaryLoading
              ? 'Summarizing...'
              : '✨ Summarize with AI'}
          </button>

          <button
            type="button"
            onClick={() => {
              setDraftForm({
                to: selectedEmail.sender || '',
                subject: `Re: ${selectedEmail.subject || ''}`,
                body: '',
              });

              setActiveView('compose');
              setSelectedEmail(null);
            }}
            style={actionButtonStyle}
          >
            ↩ Reply
          </button>
        </div>

        {selectedEmail.summary && (
          <div
            style={{
              marginTop: '18px',
              padding: '15px',
              borderRadius: '10px',
              background:
                'rgba(0,212,255,0.06)',
              border:
                '1px solid rgba(0,212,255,0.15)',
            }}
          >
            <div
              style={{
                color: '#00d4ff',
                fontSize: '12px',
                fontWeight: '700',
                marginBottom: '7px',
              }}
            >
              AI SUMMARY
            </div>

            <div
              style={{
                color: '#ccc',
                fontSize: '13px',
                lineHeight: '1.5',
              }}
            >
              {selectedEmail.summary}
            </div>
          </div>
        )}
      </div>
    );
  };

  // ==========================================================
  // COMPOSE
  // ==========================================================

  const renderCompose = () => {
    return (
      <div
        style={{
          background: '#12121a',
          border:
            '1px solid rgba(255,255,255,0.07)',
          borderRadius: '14px',
          padding: '20px',
        }}
      >
        <h3
          style={{
            margin: '0 0 6px',
            color: '#fff',
          }}
        >
          Compose Email
        </h3>

        <p
          style={{
            margin: '0 0 18px',
            color: '#77778a',
            fontSize: '12px',
          }}
        >
          Write your instructions and let PhantomAI create the email.
        </p>

        <form onSubmit={handleCreateDraft}>
          <input
            name="to"
            value={draftForm.to}
            onChange={handleDraftChange}
            placeholder="Recipient email"
            type="email"
            style={inputStyle}
          />

          <input
            name="subject"
            value={draftForm.subject}
            onChange={handleDraftChange}
            placeholder="Subject"
            style={inputStyle}
          />

          <textarea
            name="body"
            value={draftForm.body}
            onChange={handleDraftChange}
            placeholder="Tell PhantomAI what you want to say..."
            rows={8}
            style={{
              ...inputStyle,
              resize: 'vertical',
            }}
          />

          <div
            style={{
              display: 'flex',
              gap: '8px',
              flexWrap: 'wrap',
            }}
          >
            <button
              type="submit"
              disabled={draftLoading}
              style={{
                ...primaryButtonStyle,
                opacity: draftLoading ? 0.6 : 1,
              }}
            >
              {draftLoading
                ? 'Creating...'
                : '✨ Create AI Draft'}
            </button>

            <button
              type="button"
              onClick={handleSendEmail}
              disabled={sending}
              style={{
                ...sendButtonStyle,
                opacity: sending ? 0.6 : 1,
              }}
            >
              {sending
                ? 'Sending...'
                : '📤 Send Email'}
            </button>

            <button
              type="button"
              onClick={resetDraftForm}
              style={actionButtonStyle}
            >
              Clear
            </button>
          </div>
        </form>
      </div>
    );
  };

  // ==========================================================
  // DRAFTS
  // ==========================================================

  const renderDrafts = () => {
    if (draftLoading) {
      return (
        <div style={emptyStyle}>
          Loading drafts...
        </div>
      );
    }

    if (drafts.length === 0) {
      return (
        <div style={emptyStyle}>
          <div
            style={{
              fontSize: '38px',
              marginBottom: '10px',
            }}
          >
            📝
          </div>

          <div
            style={{
              color: '#fff',
              fontWeight: '600',
            }}
          >
            No drafts
          </div>

          <div
            style={{
              marginTop: '6px',
              color: '#666679',
              fontSize: '13px',
            }}
          >
            Your saved email drafts will appear here.
          </div>
        </div>
      );
    }

    return (
      <div
        style={{
          display: 'grid',
          gap: '10px',
        }}
      >
        {drafts.map((draft) => (
          <div
            key={draft.id}
            style={{
              background: '#12121a',
              border:
                '1px solid rgba(255,255,255,0.07)',
              borderRadius: '12px',
              padding: '15px',
            }}
          >
            <div
              style={{
                color: '#fff',
                fontWeight: '600',
                fontSize: '14px',
              }}
            >
              {draft.subject}
            </div>

            <div
              style={{
                color: '#77778a',
                fontSize: '12px',
                marginTop: '5px',
              }}
            >
              To: {draft.to}
            </div>

            <div
              style={{
                color: '#9999aa',
                fontSize: '12px',
                marginTop: '10px',
                whiteSpace: 'pre-wrap',
              }}
            >
              {draft.body}
            </div>

            <div
              style={{
                display: 'flex',
                gap: '8px',
                marginTop: '12px',
              }}
            >
              <button
                type="button"
                onClick={() =>
                  setDraftForm({
                    to: draft.to || '',
                    subject: draft.subject || '',
                    body: draft.body || '',
                  })
                }
                style={actionButtonStyle}
              >
                Edit Draft
              </button>
            </div>
          </div>
        ))}
      </div>
    );
  };

  // ==========================================================
  // MAIN
  // ==========================================================

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '900px',
        margin: '0 auto',
      }}
    >
      <div
        style={{
          background: '#12121a',
          border:
            '1px solid rgba(255,255,255,0.07)',
          borderRadius: '16px',
          padding: '20px',
          marginBottom: '18px',
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            marginBottom: '18px',
          }}
        >
          <div
            style={{
              width: '42px',
              height: '42px',
              borderRadius: '11px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              background:
                'rgba(0,212,255,0.1)',
              fontSize: '22px',
            }}
          >
            ✉️
          </div>

          <div>
            <h2
              style={{
                margin: 0,
                color: '#fff',
                fontSize: '20px',
              }}
            >
              Email
            </h2>

            <p
              style={{
                margin: '4px 0 0',
                color: '#77778a',
                fontSize: '12px',
              }}
            >
              Read, summarize, draft and send emails.
            </p>
          </div>
        </div>

        <div
          style={{
            display: 'flex',
            gap: '7px',
            flexWrap: 'wrap',
          }}
        >
          <button
            type="button"
            onClick={() => {
              setActiveView('inbox');
              setSelectedEmail(null);
            }}
            style={
              activeView === 'inbox'
                ? activeTabStyle
                : inactiveTabStyle
            }
          >
            📥 Inbox
          </button>

          <button
            type="button"
            onClick={() => {
              setActiveView('compose');
              setSelectedEmail(null);
            }}
            style={
              activeView === 'compose'
                ? activeTabStyle
                : inactiveTabStyle
            }
          >
            ✍️ Compose
          </button>

          <button
            type="button"
            onClick={() => {
              setActiveView('drafts');
              setSelectedEmail(null);
            }}
            style={
              activeView === 'drafts'
                ? activeTabStyle
                : inactiveTabStyle
            }
          >
            📝 Drafts
          </button>

          <button
            type="button"
            onClick={() => {
              loadEmails();
              loadDrafts();
            }}
            style={inactiveTabStyle}
          >
            ↻ Refresh
          </button>
        </div>
      </div>

      {error && (
        <div
          style={{
            marginBottom: '14px',
            padding: '12px',
            borderRadius: '10px',
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

      {success && (
        <div
          style={{
            marginBottom: '14px',
            padding: '12px',
            borderRadius: '10px',
            background:
              'rgba(0,220,150,0.08)',
            border:
              '1px solid rgba(0,220,150,0.18)',
            color: '#70e0b8',
            fontSize: '13px',
          }}
        >
          {success}
        </div>
      )}

      {activeView === 'inbox' &&
        (selectedEmail
          ? renderEmailDetail()
          : renderInbox())}

      {activeView === 'compose' &&
        renderCompose()}

      {activeView === 'drafts' &&
        renderDrafts()}
    </div>
  );
};

// ============================================================
// STYLES
// ============================================================

const inputStyle = {
  width: '100%',
  boxSizing: 'border-box',
  marginBottom: '12px',
  padding: '12px',
  borderRadius: '9px',
  border:
    '1px solid rgba(255,255,255,0.08)',
  background: '#08080d',
  color: '#fff',
  outline: 'none',
  fontSize: '13px',
};

const emptyStyle = {
  padding: '45px 20px',
  textAlign: 'center',
  background: '#12121a',
  border:
    '1px solid rgba(255,255,255,0.07)',
  borderRadius: '14px',
};

const primaryButtonStyle = {
  border: 'none',
  background: '#00d4ff',
  color: '#050509',
  padding: '9px 13px',
  borderRadius: '8px',
  cursor: 'pointer',
  fontSize: '12px',
  fontWeight: '700',
};

const sendButtonStyle = {
  border: 'none',
  background: '#19c37d',
  color: '#04140d',
  padding: '9px 13px',
  borderRadius: '8px',
  cursor: 'pointer',
  fontSize: '12px',
  fontWeight: '700',
};

const actionButtonStyle = {
  border:
    '1px solid rgba(255,255,255,0.08)',
  background:
    'rgba(255,255,255,0.04)',
  color: '#bbb',
  padding: '8px 11px',
  borderRadius: '7px',
  cursor: 'pointer',
  fontSize: '11px',
};

const activeTabStyle = {
  ...actionButtonStyle,
  border:
    '1px solid rgba(0,212,255,0.4)',
  background:
    'rgba(0,212,255,0.1)',
  color: '#00d4ff',
};

const inactiveTabStyle = {
  ...actionButtonStyle,
};

export default EmailTool;