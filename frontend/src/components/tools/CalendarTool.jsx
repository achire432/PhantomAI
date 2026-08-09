import React, { useEffect, useState } from 'react';
import { tools } from '../../api/endpoints';

const CalendarTool = () => {
  const [events, setEvents] = useState([]);

  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const [editingId, setEditingId] = useState(null);

  const [form, setForm] = useState({
    title: '',
    description: '',
    location: '',
    start_time: '',
    end_time: '',
    all_day: false,
  });

  // ============================================================
  // LOAD EVENTS
  // ============================================================

  const loadEvents = async () => {
    try {
      setLoading(true);
      setError('');

      const response = await tools.calendar.getAll();

      setEvents(response.data || []);
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          'Failed to load calendar events.'
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, []);

  // ============================================================
  // FORM CHANGE
  // ============================================================

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  // ============================================================
  // RESET FORM
  // ============================================================

  const resetForm = () => {
    setForm({
      title: '',
      description: '',
      location: '',
      start_time: '',
      end_time: '',
      all_day: false,
    });

    setEditingId(null);
  };

  // ============================================================
  // SUBMIT
  // ============================================================

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError('');

    if (!form.title.trim()) {
      setError('Event title is required.');
      return;
    }

    if (!form.start_time) {
      setError('Start date and time are required.');
      return;
    }

    if (!form.end_time) {
      setError('End date and time are required.');
      return;
    }

    const startDate = new Date(form.start_time);
    const endDate = new Date(form.end_time);

    if (Number.isNaN(startDate.getTime())) {
      setError('Invalid start date and time.');
      return;
    }

    if (Number.isNaN(endDate.getTime())) {
      setError('Invalid end date and time.');
      return;
    }

    if (endDate <= startDate) {
      setError('End time must be after start time.');
      return;
    }

    try {
      setSaving(true);

      const payload = {
        title: form.title.trim(),

        description:
          form.description.trim() || null,

        location:
          form.location.trim() || null,

        start_time: startDate.toISOString(),

        end_time: endDate.toISOString(),

        all_day: form.all_day,
      };

      if (editingId) {
        await tools.calendar.update(
          editingId,
          payload
        );
      } else {
        await tools.calendar.create(payload);
      }

      resetForm();

      await loadEvents();
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          'Failed to save calendar event.'
      );
    } finally {
      setSaving(false);
    }
  };

  // ============================================================
  // EDIT
  // ============================================================

  const handleEdit = (event) => {
    setEditingId(event.id);

    setForm({
      title: event.title || '',

      description:
        event.description || '',

      location:
        event.location || '',

      start_time: event.start_time
        ? new Date(event.start_time)
            .toISOString()
            .slice(0, 16)
        : '',

      end_time: event.end_time
        ? new Date(event.end_time)
            .toISOString()
            .slice(0, 16)
        : '',

      all_day: Boolean(event.all_day),
    });

    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };

  // ============================================================
  // DELETE
  // ============================================================

  const handleDelete = async (id) => {
    const confirmed = window.confirm(
      'Delete this calendar event?'
    );

    if (!confirmed) {
      return;
    }

    try {
      setError('');

      await tools.calendar.delete(id);

      await loadEvents();
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          'Failed to delete calendar event.'
      );
    }
  };

  // ============================================================
  // FORMAT DATE
  // ============================================================

  const formatDate = (value) => {
    if (!value) {
      return '';
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
      return 'Invalid date';
    }

    return date.toLocaleString();
  };

  // ============================================================
  // EVENT STATUS
  // ============================================================

  const getEventStatus = (event) => {
    const now = new Date();

    const start = new Date(event.start_time);
    const end = new Date(event.end_time);

    if (now < start) {
      return 'Upcoming';
    }

    if (now >= start && now <= end) {
      return 'In Progress';
    }

    return 'Ended';
  };

  // ============================================================
  // SORT EVENTS
  // ============================================================

  const sortedEvents = [...events].sort(
    (a, b) =>
      new Date(a.start_time) -
      new Date(b.start_time)
  );

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '900px',
        margin: '0 auto',
      }}
    >
      {/* ======================================================
          CREATE / EDIT EVENT
      ====================================================== */}

      <div
        style={{
          background: '#12121a',
          border:
            '1px solid rgba(255,255,255,0.07)',
          borderRadius: '16px',
          padding: '24px',
          marginBottom: '24px',
        }}
      >
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '20px',
          }}
        >
          <div>
            <h3
              style={{
                margin: 0,
                color: '#fff',
              }}
            >
              {editingId
                ? 'Edit Event'
                : 'Create Event'}
            </h3>

            <p
              style={{
                margin: '6px 0 0',
                color: '#77778a',
                fontSize: '13px',
              }}
            >
              Schedule and organize your events.
            </p>
          </div>

          {editingId && (
            <button
              type="button"
              onClick={resetForm}
              style={{
                border: 'none',
                background:
                  'rgba(255,255,255,0.06)',
                color: '#aaa',
                padding: '8px 12px',
                borderRadius: '8px',
                cursor: 'pointer',
              }}
            >
              Cancel
            </button>
          )}
        </div>

        <form onSubmit={handleSubmit}>
          {/* TITLE */}

          <input
            name="title"
            value={form.title}
            onChange={handleChange}
            placeholder="Event title"
            style={inputStyle}
          />

          {/* DESCRIPTION */}

          <textarea
            name="description"
            value={form.description}
            onChange={handleChange}
            placeholder="Description"
            rows={4}
            style={{
              ...inputStyle,
              resize: 'vertical',
            }}
          />

          {/* LOCATION */}

          <input
            name="location"
            value={form.location}
            onChange={handleChange}
            placeholder="Location"
            style={inputStyle}
          />

          {/* ALL DAY */}

          <label
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '9px',
              color: '#bbb',
              fontSize: '13px',
              marginBottom: '14px',
              cursor: 'pointer',
            }}
          >
            <input
              type="checkbox"
              name="all_day"
              checked={form.all_day}
              onChange={handleChange}
            />

            All-day event
          </label>

          {/* START / END */}

          <div
            style={{
              display: 'grid',
              gridTemplateColumns:
                '1fr 1fr',
              gap: '12px',
            }}
          >
            <div>
              <label
                style={labelStyle}
              >
                Start
              </label>

              <input
                type="datetime-local"
                name="start_time"
                value={form.start_time}
                onChange={handleChange}
                style={inputStyle}
              />
            </div>

            <div>
              <label
                style={labelStyle}
              >
                End
              </label>

              <input
                type="datetime-local"
                name="end_time"
                value={form.end_time}
                onChange={handleChange}
                style={inputStyle}
              />
            </div>
          </div>

          {/* SUBMIT */}

          <button
            type="submit"
            disabled={saving}
            style={{
              marginTop: '14px',
              width: '100%',
              border: 'none',
              borderRadius: '10px',
              padding: '12px',
              background: '#00d4ff',
              color: '#050509',
              fontWeight: '700',
              cursor: saving
                ? 'not-allowed'
                : 'pointer',
            }}
          >
            {saving
              ? 'Saving...'
              : editingId
                ? 'Update Event'
                : 'Create Event'}
          </button>
        </form>
      </div>

      {/* ======================================================
          ERROR
      ====================================================== */}

      {error && (
        <div
          style={{
            marginBottom: '18px',
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

      {/* ======================================================
          EVENTS HEADER
      ====================================================== */}

      <div
        style={{
          display: 'flex',
          justifyContent:
            'space-between',
          alignItems: 'center',
          marginBottom: '14px',
        }}
      >
        <div>
          <h3
            style={{
              margin: 0,
              color: '#fff',
            }}
          >
            Calendar Events
          </h3>

          <p
            style={{
              margin: '5px 0 0',
              color: '#666679',
              fontSize: '13px',
            }}
          >
            {events.length}{' '}
            {events.length === 1
              ? 'event'
              : 'events'}
          </p>
        </div>

        <button
          type="button"
          onClick={loadEvents}
          disabled={loading}
          style={{
            border:
              '1px solid rgba(255,255,255,0.08)',
            background:
              'rgba(255,255,255,0.04)',
            color: '#bbb',
            padding: '8px 12px',
            borderRadius: '8px',
            cursor: 'pointer',
          }}
        >
          Refresh
        </button>
      </div>

      {/* ======================================================
          EVENT LIST
      ====================================================== */}

      {loading ? (
        <div style={emptyStyle}>
          Loading calendar events...
        </div>
      ) : sortedEvents.length === 0 ? (
        <div style={emptyStyle}>
          <div
            style={{
              fontSize: '38px',
              marginBottom: '10px',
            }}
          >
            📅
          </div>

          <div
            style={{
              color: '#fff',
              fontWeight: '600',
            }}
          >
            No calendar events
          </div>

          <div
            style={{
              marginTop: '5px',
              color: '#666679',
              fontSize: '13px',
            }}
          >
            Create your first event above.
          </div>
        </div>
      ) : (
        <div
          style={{
            display: 'grid',
            gap: '12px',
          }}
        >
          {sortedEvents.map((event) => {
            const status =
              getEventStatus(event);

            return (
              <div
                key={event.id}
                style={{
                  background: '#12121a',
                  border:
                    '1px solid rgba(255,255,255,0.07)',
                  borderRadius: '14px',
                  padding: '18px',
                }}
              >
                <div
                  style={{
                    display: 'flex',
                    justifyContent:
                      'space-between',
                    gap: '15px',
                  }}
                >
                  {/* EVENT INFO */}

                  <div
                    style={{
                      minWidth: 0,
                      flex: 1,
                    }}
                  >
                    <h4
                      style={{
                        margin: 0,
                        color: '#fff',
                        fontSize: '16px',
                      }}
                    >
                      {event.title}
                    </h4>

                    {event.description && (
                      <p
                        style={{
                          color: '#858598',
                          fontSize: '13px',
                          lineHeight: '1.5',
                          margin:
                            '8px 0',
                        }}
                      >
                        {event.description}
                      </p>
                    )}

                    <div
                      style={{
                        display: 'flex',
                        gap: '8px',
                        flexWrap: 'wrap',
                        marginTop: '10px',
                      }}
                    >
                      {/* STATUS */}

                      <span
                        style={{
                          ...badgeStyle,
                          color:
                            status ===
                            'Upcoming'
                              ? '#00d4ff'
                              : status ===
                                'In Progress'
                                ? '#ffd166'
                                : '#77778a',
                        }}
                      >
                        {status}
                      </span>

                      {/* ALL DAY */}

                      {event.all_day && (
                        <span
                          style={badgeStyle}
                        >
                          All day
                        </span>
                      )}

                      {/* LOCATION */}

                      {event.location && (
                        <span
                          style={badgeStyle}
                        >
                          📍{' '}
                          {event.location}
                        </span>
                      )}
                    </div>

                    {/* DATE / TIME */}

                    <div
                      style={{
                        marginTop: '12px',
                        padding: '10px',
                        borderRadius: '9px',
                        background:
                          'rgba(255,255,255,0.03)',
                        color: '#aaa',
                        fontSize: '12px',
                      }}
                    >
                      <div>
                        <strong
                          style={{
                            color: '#ddd',
                          }}
                        >
                          Starts:
                        </strong>{' '}
                        {formatDate(
                          event.start_time
                        )}
                      </div>

                      <div
                        style={{
                          marginTop: '5px',
                        }}
                      >
                        <strong
                          style={{
                            color: '#ddd',
                          }}
                        >
                          Ends:
                        </strong>{' '}
                        {formatDate(
                          event.end_time
                        )}
                      </div>
                    </div>

                    {/* CREATED */}

                    <div
                      style={{
                        marginTop: '8px',
                        color: '#555566',
                        fontSize: '11px',
                      }}
                    >
                      Created:{' '}
                      {formatDate(
                        event.created_at
                      )}
                    </div>
                  </div>

                  {/* ACTIONS */}

                  <div
                    style={{
                      display: 'flex',
                      gap: '6px',
                      flexWrap: 'wrap',
                      alignItems:
                        'flex-start',
                      justifyContent:
                        'flex-end',
                    }}
                  >
                    <button
                      type="button"
                      onClick={() =>
                        handleEdit(event)
                      }
                      style={actionButtonStyle}
                    >
                      Edit
                    </button>

                    <button
                      type="button"
                      onClick={() =>
                        handleDelete(event.id)
                      }
                      style={{
                        ...actionButtonStyle,
                        color: '#ff7777',
                      }}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
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

const labelStyle = {
  display: 'block',
  color: '#77778a',
  fontSize: '12px',
  marginBottom: '6px',
};

const emptyStyle = {
  padding: '45px 20px',
  textAlign: 'center',
  background: '#12121a',
  border:
    '1px solid rgba(255,255,255,0.07)',
  borderRadius: '14px',
};

const badgeStyle = {
  display: 'inline-block',
  padding: '5px 8px',
  borderRadius: '6px',
  background:
    'rgba(255,255,255,0.05)',
  color: '#9999aa',
  fontSize: '11px',
};

const actionButtonStyle = {
  border:
    '1px solid rgba(255,255,255,0.08)',
  background:
    'rgba(255,255,255,0.04)',
  color: '#bbb',
  padding: '7px 9px',
  borderRadius: '7px',
  cursor: 'pointer',
  fontSize: '11px',
};

export default CalendarTool;