import React, { useEffect, useMemo, useState } from 'react';
import { tools } from '../../api/endpoints';

const NotesTool = () => {
  const [notes, setNotes] = useState([]);
  const [selectedNote, setSelectedNote] = useState(null);

  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const [search, setSearch] = useState('');

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // ============================================================
  // LOAD NOTES
  // ============================================================

  const loadNotes = async () => {
    try {
      setLoading(true);
      setError('');

      const response = await tools.notes.getAll();

      setNotes(response.data || []);
    } catch (err) {
      console.error('Failed to load notes:', err);

      setError(
        err?.response?.data?.detail ||
          'Unable to load your notes.'
      );
    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // INITIAL LOAD
  // ============================================================

  useEffect(() => {
    loadNotes();
  }, []);

  // ============================================================
  // CLEAR MESSAGES
  // ============================================================

  const clearMessages = () => {
    setError('');
    setSuccess('');
  };

  // ============================================================
  // NEW NOTE
  // ============================================================

  const createNewNote = () => {
    clearMessages();

    setSelectedNote(null);
    setTitle('');
    setContent('');
  };

  // ============================================================
  // SELECT NOTE
  // ============================================================

  const selectNote = (note) => {
    clearMessages();

    setSelectedNote(note);
    setTitle(note.title || '');
    setContent(note.content || '');
  };

  // ============================================================
  // SAVE NOTE
  // ============================================================

  const saveNote = async () => {
    clearMessages();

    if (!title.trim()) {
      setError('Please enter a note title.');
      return;
    }

    if (!content.trim()) {
      setError('Please enter some note content.');
      return;
    }

    try {
      setSaving(true);

      let response;

      // --------------------------------------------------------
      // CREATE
      // --------------------------------------------------------

      if (!selectedNote) {
        response = await tools.notes.create({
          title: title.trim(),
          content: content.trim(),
        });

        const createdNote = response.data;

        setNotes((previous) => [
          createdNote,
          ...previous,
        ]);

        setSelectedNote(createdNote);

        setTitle(createdNote.title || '');
        setContent(createdNote.content || '');

        setSuccess('Note created successfully.');
      }

      // --------------------------------------------------------
      // UPDATE
      // --------------------------------------------------------

      else {
        response = await tools.notes.update(
          selectedNote.id,
          {
            title: title.trim(),
            content: content.trim(),
          }
        );

        const updatedNote = response.data;

        setNotes((previous) =>
          previous.map((note) =>
            note.id === updatedNote.id
              ? updatedNote
              : note
          )
        );

        setSelectedNote(updatedNote);

        setTitle(updatedNote.title || '');
        setContent(updatedNote.content || '');

        setSuccess('Note updated successfully.');
      }
    } catch (err) {
      console.error('Failed to save note:', err);

      setError(
        err?.response?.data?.detail ||
          'Unable to save the note.'
      );
    } finally {
      setSaving(false);
    }
  };

  // ============================================================
  // DELETE NOTE
  // ============================================================

  const deleteNote = async () => {
    if (!selectedNote) {
      return;
    }

    const confirmed = window.confirm(
      `Delete "${selectedNote.title}"? This cannot be undone.`
    );

    if (!confirmed) {
      return;
    }

    try {
      setDeleting(true);
      clearMessages();

      await tools.notes.delete(selectedNote.id);

      setNotes((previous) =>
        previous.filter(
          (note) => note.id !== selectedNote.id
        )
      );

      setSelectedNote(null);
      setTitle('');
      setContent('');

      setSuccess('Note deleted successfully.');
    } catch (err) {
      console.error('Failed to delete note:', err);

      setError(
        err?.response?.data?.detail ||
          'Unable to delete the note.'
      );
    } finally {
      setDeleting(false);
    }
  };

  // ============================================================
  // SEARCH
  // ============================================================

  const filteredNotes = useMemo(() => {
    const query = search.trim().toLowerCase();

    if (!query) {
      return notes;
    }

    return notes.filter((note) => {
      const noteTitle = (
        note.title || ''
      ).toLowerCase();

      const noteContent = (
        note.content || ''
      ).toLowerCase();

      return (
        noteTitle.includes(query) ||
        noteContent.includes(query)
      );
    });
  }, [notes, search]);

  // ============================================================
  // FORMAT DATE
  // ============================================================

  const formatDate = (date) => {
    if (!date) {
      return '';
    }

    try {
      return new Date(date).toLocaleString();
    } catch {
      return '';
    }
  };

  // ============================================================
  // UI
  // ============================================================

  return (
    <div
      style={{
        width: '100%',
        minHeight: '650px',
        display: 'grid',
        gridTemplateColumns: '300px minmax(0, 1fr)',
        borderRadius: '18px',
        overflow: 'hidden',
        border: '1px solid rgba(255,255,255,0.07)',
        background: '#0b0b12',
        boxSizing: 'border-box',
      }}
    >

      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <aside
        style={{
          borderRight:
            '1px solid rgba(255,255,255,0.07)',
          background: '#08080e',
          display: 'flex',
          flexDirection: 'column',
          minWidth: 0,
        }}
      >

        {/* HEADER */}

        <div
          style={{
            padding: '20px',
            borderBottom:
              '1px solid rgba(255,255,255,0.07)',
          }}
        >
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              gap: '10px',
              marginBottom: '15px',
            }}
          >
            <div>
              <div
                style={{
                  color: '#ffffff',
                  fontSize: '17px',
                  fontWeight: '700',
                }}
              >
                📝 Notes
              </div>

              <div
                style={{
                  color: '#68687a',
                  fontSize: '11px',
                  marginTop: '4px',
                }}
              >
                {notes.length} note
                {notes.length === 1 ? '' : 's'}
              </div>
            </div>

            <button
              type="button"
              onClick={createNewNote}
              style={{
                border: 'none',
                borderRadius: '9px',
                padding: '8px 11px',
                background:
                  'rgba(0,212,255,0.12)',
                border:
                  '1px solid rgba(0,212,255,0.25)',
                color: '#00d4ff',
                cursor: 'pointer',
                fontWeight: '700',
                fontSize: '12px',
              }}
            >
              + New
            </button>
          </div>

          {/* SEARCH */}

          <input
            value={search}
            onChange={(event) =>
              setSearch(event.target.value)
            }
            placeholder="Search notes..."
            style={{
              width: '100%',
              boxSizing: 'border-box',
              padding: '10px 12px',
              borderRadius: '9px',
              border:
                '1px solid rgba(255,255,255,0.08)',
              background: '#11111a',
              color: '#ffffff',
              outline: 'none',
              fontSize: '12px',
            }}
          />
        </div>

        {/* NOTE LIST */}

        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: '10px',
          }}
        >
          {loading ? (
            <div
              style={{
                padding: '20px 10px',
                color: '#68687a',
                fontSize: '12px',
                textAlign: 'center',
              }}
            >
              Loading notes...
            </div>
          ) : filteredNotes.length === 0 ? (
            <div
              style={{
                padding: '30px 15px',
                color: '#68687a',
                fontSize: '12px',
                textAlign: 'center',
                lineHeight: '1.6',
              }}
            >
              {search
                ? 'No notes match your search.'
                : 'You have no notes yet.'}
            </div>
          ) : (
            filteredNotes.map((note) => {
              const active =
                selectedNote?.id === note.id;

              return (
                <button
                  key={note.id}
                  type="button"
                  onClick={() => selectNote(note)}
                  style={{
                    width: '100%',
                    textAlign: 'left',
                    borderRadius: '10px',
                    border: active
                      ? '1px solid rgba(0,212,255,0.3)'
                      : '1px solid transparent',
                    background: active
                      ? 'rgba(0,212,255,0.08)'
                      : 'transparent',
                    padding: '12px',
                    marginBottom: '6px',
                    cursor: 'pointer',
                    color: '#ffffff',
                  }}
                >
                  <div
                    style={{
                      fontWeight: '600',
                      fontSize: '13px',
                      marginBottom: '5px',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {note.title}
                  </div>

                  <div
                    style={{
                      color: '#77778a',
                      fontSize: '11px',
                      lineHeight: '1.4',
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden',
                    }}
                  >
                    {note.content}
                  </div>

                  <div
                    style={{
                      color: '#4e4e60',
                      fontSize: '9px',
                      marginTop: '7px',
                    }}
                  >
                    {formatDate(note.updated_at)}
                  </div>
                </button>
              );
            })
          )}
        </div>
      </aside>

      {/* ======================================================
          EDITOR
      ====================================================== */}

      <main
        style={{
          minWidth: 0,
          display: 'flex',
          flexDirection: 'column',
          background: '#0d0d15',
        }}
      >

        {/* EDITOR HEADER */}

        <div
          style={{
            minHeight: '70px',
            padding: '15px 20px',
            boxSizing: 'border-box',
            borderBottom:
              '1px solid rgba(255,255,255,0.07)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '15px',
          }}
        >
          <div>
            <div
              style={{
                color: '#ffffff',
                fontWeight: '700',
                fontSize: '15px',
              }}
            >
              {selectedNote
                ? 'Edit Note'
                : 'New Note'}
            </div>

            <div
              style={{
                color: '#5e5e70',
                fontSize: '10px',
                marginTop: '4px',
              }}
            >
              {selectedNote
                ? `Last updated ${formatDate(
                    selectedNote.updated_at
                  )}`
                : 'Create a new personal note'}
            </div>
          </div>

          <div
            style={{
              display: 'flex',
              gap: '8px',
            }}
          >
            {selectedNote && (
              <button
                type="button"
                onClick={deleteNote}
                disabled={deleting}
                style={{
                  padding: '9px 13px',
                  borderRadius: '8px',
                  border:
                    '1px solid rgba(255,80,80,0.25)',
                  background:
                    'rgba(255,80,80,0.08)',
                  color: '#ff7373',
                  cursor: deleting
                    ? 'not-allowed'
                    : 'pointer',
                  fontSize: '11px',
                  opacity: deleting ? 0.6 : 1,
                }}
              >
                {deleting
                  ? 'Deleting...'
                  : 'Delete'}
              </button>
            )}

            <button
              type="button"
              onClick={saveNote}
              disabled={saving}
              style={{
                padding: '9px 15px',
                borderRadius: '8px',
                border:
                  '1px solid rgba(0,212,255,0.3)',
                background:
                  'rgba(0,212,255,0.12)',
                color: '#00d4ff',
                cursor: saving
                  ? 'not-allowed'
                  : 'pointer',
                fontSize: '11px',
                fontWeight: '700',
                opacity: saving ? 0.6 : 1,
              }}
            >
              {saving
                ? 'Saving...'
                : selectedNote
                  ? 'Save Changes'
                  : 'Save Note'}
            </button>
          </div>
        </div>

        {/* MESSAGES */}

        {(error || success) && (
          <div
            style={{
              padding: '10px 20px',
              borderBottom:
                '1px solid rgba(255,255,255,0.05)',
              background: error
                ? 'rgba(255,70,70,0.05)'
                : 'rgba(0,255,150,0.04)',
              color: error
                ? '#ff7c7c'
                : '#66e0ad',
              fontSize: '11px',
            }}
          >
            {error || success}
          </div>
        )}

        {/* TITLE */}

        <div
          style={{
            padding: '25px 25px 10px',
          }}
        >
          <input
            value={title}
            onChange={(event) =>
              setTitle(event.target.value)
            }
            placeholder="Note title..."
            style={{
              width: '100%',
              boxSizing: 'border-box',
              border: 'none',
              outline: 'none',
              background: 'transparent',
              color: '#ffffff',
              fontSize: '25px',
              fontWeight: '700',
            }}
          />
        </div>

        {/* CONTENT */}

        <div
          style={{
            flex: 1,
            padding: '10px 25px 25px',
            display: 'flex',
          }}
        >
          <textarea
            value={content}
            onChange={(event) =>
              setContent(event.target.value)
            }
            placeholder="Start writing your note..."
            style={{
              width: '100%',
              minHeight: '420px',
              resize: 'vertical',
              boxSizing: 'border-box',
              border: 'none',
              outline: 'none',
              background: 'transparent',
              color: '#d7d7e0',
              fontSize: '14px',
              lineHeight: '1.8',
              fontFamily:
                'inherit',
            }}
          />
        </div>

        {/* FOOTER */}

        <div
          style={{
            padding: '10px 20px',
            borderTop:
              '1px solid rgba(255,255,255,0.05)',
            color: '#505061',
            fontSize: '10px',
            display: 'flex',
            justifyContent: 'space-between',
          }}
        >
          <span>
            {content.length} characters
          </span>

          <span>
            PhantomAI Notes
          </span>
        </div>
      </main>
    </div>
  );
};

export default NotesTool;