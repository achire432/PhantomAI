import React, { useEffect, useMemo, useState } from 'react';
import { tools } from '../../api/endpoints';

const RemindersTool = () => {
  const [reminders, setReminders] = useState([]);
  const [selectedReminder, setSelectedReminder] = useState(null);

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [remindAt, setRemindAt] = useState('');

  const [showCompleted, setShowCompleted] = useState(false);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [completing, setCompleting] = useState(false);

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // ============================================================
  // LOAD REMINDERS
  // ============================================================

  const loadReminders = async () => {
    try {
      setLoading(true);
      setError('');

      /*
       * We request ALL reminders here.
       *
       * The backend supports:
       *
       * GET /reminders/?upcoming=true
       *
       * and
       *
       * GET /reminders/?upcoming=false
       *
       * Using false allows the frontend to display both
       * upcoming and completed reminders.
       */

      const response = await tools.reminders.getAll({
        upcoming: false,
      });

      setReminders(response.data || []);
    } catch (err) {
      console.error(
        'Failed to load reminders:',
        err
      );

      setError(
        err?.response?.data?.detail ||
          'Unable to load your reminders.'
      );
    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // INITIAL LOAD
  // ============================================================

  useEffect(() => {
    loadReminders();
  }, []);

  // ============================================================
  // CLEAR MESSAGES
  // ============================================================

  const clearMessages = () => {
    setError('');
    setSuccess('');
  };

  // ============================================================
  // NEW REMINDER
  // ============================================================

  const createNewReminder = () => {
    clearMessages();

    setSelectedReminder(null);
    setTitle('');
    setDescription('');
    setRemindAt('');
  };

  // ============================================================
  // SELECT REMINDER
  // ============================================================

  const selectReminder = (reminder) => {
    clearMessages();

    setSelectedReminder(reminder);

    setTitle(reminder.title || '');
    setDescription(reminder.description || '');

    /*
     * HTML datetime-local expects:
     *
     * YYYY-MM-DDTHH:MM
     */

    if (reminder.remind_at) {
      const date = new Date(reminder.remind_at);

      const localDate = new Date(
        date.getTime() -
          date.getTimezoneOffset() * 60000
      );

      setRemindAt(
        localDate.toISOString().slice(0, 16)
      );
    } else {
      setRemindAt('');
    }
  };

  // ============================================================
  // SAVE REMINDER
  // ============================================================

  const saveReminder = async () => {
    clearMessages();

    if (!title.trim()) {
      setError(
        'Please enter a reminder title.'
      );
      return;
    }

    if (!remindAt) {
      setError(
        'Please choose a reminder date and time.'
      );
      return;
    }

    try {
      setSaving(true);

      /*
       * Convert the datetime-local value into an
       * ISO datetime that FastAPI/Pydantic can parse.
       */

      const reminderDate =
        new Date(remindAt);

      if (
        Number.isNaN(
          reminderDate.getTime()
        )
      ) {
        setError(
          'The reminder date and time is invalid.'
        );
        return;
      }

      const payload = {
        title: title.trim(),
        description:
          description.trim() || null,
        remind_at:
          reminderDate.toISOString(),
      };

      let response;

      // ========================================================
      // CREATE
      // ========================================================

      if (!selectedReminder) {
        response =
          await tools.reminders.create(
            payload
          );

        const createdReminder =
          response.data;

        setReminders((previous) => [
          ...previous,
          createdReminder,
        ]);

        setSelectedReminder(
          createdReminder
        );

        setTitle(
          createdReminder.title || ''
        );

        setDescription(
          createdReminder.description || ''
        );

        setRemindAt(
          createdReminder.remind_at
            ? new Date(
                new Date(
                  createdReminder.remind_at
                ).getTime() -
                  new Date(
                    createdReminder.remind_at
                  ).getTimezoneOffset() *
                    60000
              )
                .toISOString()
                .slice(0, 16)
            : ''
        );

        setSuccess(
          'Reminder created successfully.'
        );
      }

      // ========================================================
      // UPDATE
      // ========================================================

      else {
        response =
          await tools.reminders.update(
            selectedReminder.id,
            payload
          );

        const updatedReminder =
          response.data;

        setReminders((previous) =>
          previous.map((reminder) =>
            reminder.id ===
            updatedReminder.id
              ? updatedReminder
              : reminder
          )
        );

        setSelectedReminder(
          updatedReminder
        );

        setSuccess(
          'Reminder updated successfully.'
        );
      }
    } catch (err) {
      console.error(
        'Failed to save reminder:',
        err
      );

      setError(
        err?.response?.data?.detail ||
          'Unable to save the reminder.'
      );
    } finally {
      setSaving(false);
    }
  };

  // ============================================================
  // COMPLETE REMINDER
  // ============================================================

  const completeReminder = async () => {
    if (!selectedReminder) {
      return;
    }

    try {
      setCompleting(true);
      clearMessages();

      await tools.reminders.complete(
        selectedReminder.id
      );

      setReminders((previous) =>
        previous.map((reminder) =>
          reminder.id ===
          selectedReminder.id
            ? {
                ...reminder,
                is_completed: true,
              }
            : reminder
        )
      );

      setSelectedReminder((previous) =>
        previous
          ? {
              ...previous,
              is_completed: true,
            }
          : previous
      );

      setSuccess(
        'Reminder marked as completed.'
      );
    } catch (err) {
      console.error(
        'Failed to complete reminder:',
        err
      );

      setError(
        err?.response?.data?.detail ||
          'Unable to complete the reminder.'
      );
    } finally {
      setCompleting(false);
    }
  };

  // ============================================================
  // DELETE REMINDER
  // ============================================================

  const deleteReminder = async () => {
    if (!selectedReminder) {
      return;
    }

    const confirmed = window.confirm(
      `Delete "${selectedReminder.title}"? This cannot be undone.`
    );

    if (!confirmed) {
      return;
    }

    try {
      setDeleting(true);
      clearMessages();

      await tools.reminders.delete(
        selectedReminder.id
      );

      setReminders((previous) =>
        previous.filter(
          (reminder) =>
            reminder.id !==
            selectedReminder.id
        )
      );

      setSelectedReminder(null);
      setTitle('');
      setDescription('');
      setRemindAt('');

      setSuccess(
        'Reminder deleted successfully.'
      );
    } catch (err) {
      console.error(
        'Failed to delete reminder:',
        err
      );

      setError(
        err?.response?.data?.detail ||
          'Unable to delete the reminder.'
      );
    } finally {
      setDeleting(false);
    }
  };

  // ============================================================
  // FILTER REMINDERS
  // ============================================================

  const filteredReminders = useMemo(() => {
    return reminders
      .filter((reminder) => {
        if (showCompleted) {
          return true;
        }

        return !reminder.is_completed;
      })
      .sort(
        (a, b) =>
          new Date(a.remind_at) -
          new Date(b.remind_at)
      );
  }, [reminders, showCompleted]);

  // ============================================================
  // FORMAT DATE
  // ============================================================

  const formatDate = (date) => {
    if (!date) {
      return '';
    }

    try {
      return new Date(
        date
      ).toLocaleString([], {
        dateStyle: 'medium',
        timeStyle: 'short',
      });
    } catch {
      return '';
    }
  };

  // ============================================================
  // CHECK OVERDUE
  // ============================================================

  const isOverdue = (reminder) => {
    if (
      reminder.is_completed ||
      !reminder.remind_at
    ) {
      return false;
    }

    return (
      new Date(
        reminder.remind_at
      ).getTime() <
      Date.now()
    );
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
        gridTemplateColumns:
          '320px minmax(0, 1fr)',
        borderRadius: '18px',
        overflow: 'hidden',
        border:
          '1px solid rgba(255,255,255,0.07)',
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
              justifyContent:
                'space-between',
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
                ⏰ Reminders
              </div>

              <div
                style={{
                  color: '#68687a',
                  fontSize: '11px',
                  marginTop: '4px',
                }}
              >
                {
                  reminders.filter(
                    (reminder) =>
                      !reminder.is_completed
                  ).length
                }{' '}
                active reminder
                {reminders.filter(
                  (reminder) =>
                    !reminder.is_completed
                ).length === 1
                  ? ''
                  : 's'}
              </div>
            </div>

            <button
              type="button"
              onClick={
                createNewReminder
              }
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

          {/* FILTER */}

          <button
            type="button"
            onClick={() =>
              setShowCompleted(
                (previous) => !previous
              )
            }
            style={{
              width: '100%',
              padding: '9px 10px',
              borderRadius: '8px',
              border:
                '1px solid rgba(255,255,255,0.07)',
              background: showCompleted
                ? 'rgba(0,212,255,0.08)'
                : '#11111a',
              color: showCompleted
                ? '#00d4ff'
                : '#77778a',
              cursor: 'pointer',
              fontSize: '11px',
              textAlign: 'left',
            }}
          >
            {showCompleted
              ? '✓ Showing all reminders'
              : '○ Showing active reminders'}
          </button>
        </div>

        {/* REMINDER LIST */}

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
              Loading reminders...
            </div>
          ) : filteredReminders.length ===
            0 ? (
            <div
              style={{
                padding: '30px 15px',
                color: '#68687a',
                fontSize: '12px',
                textAlign: 'center',
                lineHeight: '1.6',
              }}
            >
              {showCompleted
                ? 'No reminders yet.'
                : 'No active reminders.'}
            </div>
          ) : (
            filteredReminders.map(
              (reminder) => {
                const active =
                  selectedReminder?.id ===
                  reminder.id;

                const overdue =
                  isOverdue(reminder);

                return (
                  <button
                    key={reminder.id}
                    type="button"
                    onClick={() =>
                      selectReminder(
                        reminder
                      )
                    }
                    style={{
                      width: '100%',
                      textAlign: 'left',
                      borderRadius: '10px',
                      border: active
                        ? '1px solid rgba(0,212,255,0.3)'
                        : '1px solid transparent',
                      background:
                        active
                          ? 'rgba(0,212,255,0.08)'
                          : 'transparent',
                      padding: '12px',
                      marginBottom: '6px',
                      cursor: 'pointer',
                      color: '#ffffff',
                      opacity:
                        reminder.is_completed
                          ? 0.55
                          : 1,
                    }}
                  >
                    <div
                      style={{
                        display: 'flex',
                        justifyContent:
                          'space-between',
                        gap: '8px',
                        marginBottom:
                          '5px',
                      }}
                    >
                      <div
                        style={{
                          fontWeight: '600',
                          fontSize: '13px',
                          overflow: 'hidden',
                          textOverflow:
                            'ellipsis',
                          whiteSpace:
                            'nowrap',
                        }}
                      >
                        {reminder.is_completed
                          ? '✓ '
                          : '⏰ '}
                        {reminder.title}
                      </div>
                    </div>

                    <div
                      style={{
                        color:
                          reminder.is_completed
                            ? '#66e0ad'
                            : overdue
                              ? '#ff7474'
                              : '#00d4ff',
                        fontSize: '10px',
                        marginBottom: '6px',
                      }}
                    >
                      {reminder.is_completed
                        ? 'Completed'
                        : overdue
                          ? 'Overdue'
                          : formatDate(
                              reminder.remind_at
                            )}
                    </div>

                    {reminder.description && (
                      <div
                        style={{
                          color: '#77778a',
                          fontSize: '10px',
                          lineHeight:
                            '1.4',
                          display:
                            '-webkit-box',
                          WebkitLineClamp: 2,
                          WebkitBoxOrient:
                            'vertical',
                          overflow: 'hidden',
                        }}
                      >
                        {
                          reminder.description
                        }
                      </div>
                    )}
                  </button>
                );
              }
            )
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

        {/* HEADER */}

        <div
          style={{
            minHeight: '75px',
            padding: '15px 20px',
            boxSizing: 'border-box',
            borderBottom:
              '1px solid rgba(255,255,255,0.07)',
            display: 'flex',
            alignItems: 'center',
            justifyContent:
              'space-between',
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
              {selectedReminder
                ? 'Edit Reminder'
                : 'New Reminder'}
            </div>

            <div
              style={{
                color: '#5e5e70',
                fontSize: '10px',
                marginTop: '4px',
              }}
            >
              {selectedReminder
                ? `Scheduled for ${formatDate(
                    selectedReminder.remind_at
                  )}`
                : 'Tell PhantomAI when you need to be reminded'}
            </div>
          </div>

          <div
            style={{
              display: 'flex',
              gap: '8px',
              flexWrap: 'wrap',
              justifyContent:
                'flex-end',
            }}
          >
            {selectedReminder &&
              !selectedReminder.is_completed && (
                <button
                  type="button"
                  onClick={
                    completeReminder
                  }
                  disabled={completing}
                  style={{
                    padding:
                      '9px 13px',
                    borderRadius: '8px',
                    border:
                      '1px solid rgba(0,255,150,0.25)',
                    background:
                      'rgba(0,255,150,0.07)',
                    color: '#66e0ad',
                    cursor:
                      completing
                        ? 'not-allowed'
                        : 'pointer',
                    fontSize: '11px',
                    opacity:
                      completing
                        ? 0.6
                        : 1,
                  }}
                >
                  {completing
                    ? 'Completing...'
                    : '✓ Complete'}
                </button>
              )}

            {selectedReminder && (
              <button
                type="button"
                onClick={
                  deleteReminder
                }
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
                  opacity: deleting
                    ? 0.6
                    : 1,
                }}
              >
                {deleting
                  ? 'Deleting...'
                  : 'Delete'}
              </button>
            )}

            <button
              type="button"
              onClick={saveReminder}
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
                opacity: saving
                  ? 0.6
                  : 1,
              }}
            >
              {saving
                ? 'Saving...'
                : selectedReminder
                  ? 'Save Changes'
                  : 'Create Reminder'}
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

        {/* FORM */}

        <div
          style={{
            flex: 1,
            padding: '30px',
            overflowY: 'auto',
          }}
        >
          {/* TITLE */}

          <label
            style={{
              display: 'block',
              color: '#858597',
              fontSize: '11px',
              marginBottom: '8px',
            }}
          >
            Reminder title
          </label>

          <input
            value={title}
            onChange={(event) =>
              setTitle(event.target.value)
            }
            placeholder="e.g. Call John about the project"
            style={{
              width: '100%',
              boxSizing: 'border-box',
              padding: '13px 14px',
              borderRadius: '10px',
              border:
                '1px solid rgba(255,255,255,0.08)',
              background: '#11111a',
              color: '#ffffff',
              outline: 'none',
              fontSize: '14px',
              marginBottom: '22px',
            }}
          />

          {/* DATE/TIME */}

          <label
            style={{
              display: 'block',
              color: '#858597',
              fontSize: '11px',
              marginBottom: '8px',
            }}
          >
            Remind me at
          </label>

          <input
            type="datetime-local"
            value={remindAt}
            onChange={(event) =>
              setRemindAt(
                event.target.value
              )
            }
            style={{
              width: '100%',
              boxSizing: 'border-box',
              padding: '13px 14px',
              borderRadius: '10px',
              border:
                '1px solid rgba(255,255,255,0.08)',
              background: '#11111a',
              color: '#ffffff',
              outline: 'none',
              fontSize: '13px',
              marginBottom: '22px',
              colorScheme: 'dark',
            }}
          />

          {/* DESCRIPTION */}

          <label
            style={{
              display: 'block',
              color: '#858597',
              fontSize: '11px',
              marginBottom: '8px',
            }}
          >
            Description
          </label>

          <textarea
            value={description}
            onChange={(event) =>
              setDescription(
                event.target.value
              )
            }
            placeholder="Add more details about this reminder..."
            style={{
              width: '100%',
              minHeight: '180px',
              resize: 'vertical',
              boxSizing: 'border-box',
              padding: '14px',
              borderRadius: '10px',
              border:
                '1px solid rgba(255,255,255,0.08)',
              background: '#11111a',
              color: '#d7d7e0',
              outline: 'none',
              fontSize: '13px',
              lineHeight: '1.6',
              fontFamily: 'inherit',
            }}
          />

          {/* STATUS CARD */}

          {selectedReminder && (
            <div
              style={{
                marginTop: '25px',
                padding: '15px',
                borderRadius: '10px',
                border:
                  '1px solid rgba(255,255,255,0.06)',
                background:
                  'rgba(255,255,255,0.02)',
              }}
            >
              <div
                style={{
                  color: '#77778a',
                  fontSize: '10px',
                  marginBottom: '8px',
                }}
              >
                STATUS
              </div>

              <div
                style={{
                  color:
                    selectedReminder.is_completed
                      ? '#66e0ad'
                      : isOverdue(
                            selectedReminder
                          )
                        ? '#ff7474'
                        : '#00d4ff',
                  fontSize: '12px',
                  fontWeight: '600',
                }}
              >
                {selectedReminder.is_completed
                  ? '✓ Completed'
                  : isOverdue(
                        selectedReminder
                      )
                    ? '⚠ Overdue'
                    : '⏰ Scheduled'}
              </div>

              <div
                style={{
                  color: '#555566',
                  fontSize: '10px',
                  marginTop: '5px',
                }}
              >
                {selectedReminder.is_completed
                  ? 'This reminder has been completed.'
                  : `PhantomAI will use this reminder time: ${formatDate(
                      selectedReminder.remind_at
                    )}`}
              </div>
            </div>
          )}
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
            justifyContent:
              'space-between',
          }}
        >
          <span>
            {selectedReminder
              ? `Reminder #${selectedReminder.id}`
              : 'New reminder'}
          </span>

          <span>
            PhantomAI Reminders
          </span>
        </div>
      </main>
    </div>
  );
};

export default RemindersTool;