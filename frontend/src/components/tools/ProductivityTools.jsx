import React, { useEffect, useState } from 'react';
import { tools } from '../../api/endpoints';

// ============================================================
// PRODUCTIVITY TOOLS
// Notes + Tasks + Reminders
// ============================================================

const ProductivityTools = () => {
  const [activeTab, setActiveTab] = useState('notes');

  // ============================================================
  // NOTES
  // ============================================================

  const [notes, setNotes] = useState([]);
  const [noteSearch, setNoteSearch] = useState('');
  const [notesLoading, setNotesLoading] = useState(false);

  const [noteTitle, setNoteTitle] = useState('');
  const [noteContent, setNoteContent] = useState('');
  const [editingNoteId, setEditingNoteId] = useState(null);

  // ============================================================
  // TASKS
  // ============================================================

  const [tasks, setTasks] = useState([]);
  const [taskStatusFilter, setTaskStatusFilter] = useState('');

  const [taskTitle, setTaskTitle] = useState('');
  const [taskDescription, setTaskDescription] = useState('');
  const [taskPriority, setTaskPriority] = useState('medium');
  const [taskDueDate, setTaskDueDate] = useState('');
  const [editingTaskId, setEditingTaskId] = useState(null);

  const [tasksLoading, setTasksLoading] = useState(false);

  // ============================================================
  // REMINDERS
  // ============================================================

  const [reminders, setReminders] = useState([]);
  const [remindersLoading, setRemindersLoading] = useState(false);

  const [reminderTitle, setReminderTitle] = useState('');
  const [reminderDescription, setReminderDescription] = useState('');
  const [reminderDate, setReminderDate] = useState('');
  const [editingReminderId, setEditingReminderId] = useState(null);

  // ============================================================
  // MESSAGE
  // ============================================================

  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('success');

  const showMessage = (text, type = 'success') => {
    setMessage(text);
    setMessageType(type);

    setTimeout(() => {
      setMessage('');
    }, 3500);
  };

  // ============================================================
  // LOAD NOTES
  // ============================================================

  const loadNotes = async () => {
    try {
      setNotesLoading(true);

      const response = await tools.notes.getAll();

      setNotes(response.data || []);
    } catch (error) {
      console.error('Failed to load notes:', error);

      showMessage(
        error.response?.data?.detail ||
          'Failed to load notes.',
        'error'
      );
    } finally {
      setNotesLoading(false);
    }
  };

  // ============================================================
  // LOAD TASKS
  // ============================================================

  const loadTasks = async () => {
    try {
      setTasksLoading(true);

      const response = await tools.tasks.getAll();

      setTasks(response.data || []);
    } catch (error) {
      console.error('Failed to load tasks:', error);

      showMessage(
        error.response?.data?.detail ||
          'Failed to load tasks.',
        'error'
      );
    } finally {
      setTasksLoading(false);
    }
  };

  // ============================================================
  // LOAD REMINDERS
  // ============================================================

  const loadReminders = async () => {
    try {
      setRemindersLoading(true);

      const response = await tools.reminders.getAll();

      setReminders(response.data || []);
    } catch (error) {
      console.error('Failed to load reminders:', error);

      showMessage(
        error.response?.data?.detail ||
          'Failed to load reminders.',
        'error'
      );
    } finally {
      setRemindersLoading(false);
    }
  };

  // ============================================================
  // INITIAL LOAD
  // ============================================================

  useEffect(() => {
    loadNotes();
    loadTasks();
    loadReminders();
  }, []);

  // ============================================================
  // NOTE FORM RESET
  // ============================================================

  const resetNoteForm = () => {
    setNoteTitle('');
    setNoteContent('');
    setEditingNoteId(null);
  };

  // ============================================================
  // CREATE / UPDATE NOTE
  // ============================================================

  const saveNote = async (event) => {
    event.preventDefault();

    if (!noteTitle.trim()) {
      showMessage('Please enter a note title.', 'error');
      return;
    }

    if (!noteContent.trim()) {
      showMessage('Please enter note content.', 'error');
      return;
    }

    try {
      if (editingNoteId) {
        await tools.notes.update(editingNoteId, {
          title: noteTitle,
          content: noteContent,
        });

        showMessage('Note updated successfully.');
      } else {
        await tools.notes.create({
          title: noteTitle,
          content: noteContent,
        });

        showMessage('Note created successfully.');
      }

      resetNoteForm();
      await loadNotes();
    } catch (error) {
      console.error('Failed to save note:', error);

      showMessage(
        error.response?.data?.detail ||
          'Failed to save note.',
        'error'
      );
    }
  };

  // ============================================================
  // EDIT NOTE
  // ============================================================

  const editNote = (note) => {
    setEditingNoteId(note.id);
    setNoteTitle(note.title || '');
    setNoteContent(note.content || '');

    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };

  // ============================================================
  // DELETE NOTE
  // ============================================================

  const deleteNote = async (id) => {
    const confirmed = window.confirm(
      'Delete this note permanently?'
    );

    if (!confirmed) {
      return;
    }

    try {
      await tools.notes.delete(id);

      showMessage('Note deleted successfully.');

      await loadNotes();
    } catch (error) {
      console.error('Failed to delete note:', error);

      showMessage(
        error.response?.data?.detail ||
          'Failed to delete note.',
        'error'
      );
    }
  };

  // ============================================================
  // TASK FORM RESET
  // ============================================================

  const resetTaskForm = () => {
    setTaskTitle('');
    setTaskDescription('');
    setTaskPriority('medium');
    setTaskDueDate('');
    setEditingTaskId(null);
  };

  // ============================================================
  // CREATE / UPDATE TASK
  // ============================================================

  const saveTask = async (event) => {
    event.preventDefault();

    if (!taskTitle.trim()) {
      showMessage('Please enter a task title.', 'error');
      return;
    }

    try {
      const payload = {
        title: taskTitle,
        description: taskDescription,
        priority: taskPriority,
        due_date: taskDueDate
          ? new Date(taskDueDate).toISOString()
          : null,
      };

      if (editingTaskId) {
        await tools.tasks.update(
          editingTaskId,
          payload
        );

        showMessage('Task updated successfully.');
      } else {
        await tools.tasks.create(payload);

        showMessage('Task created successfully.');
      }

      resetTaskForm();
      await loadTasks();
    } catch (error) {
      console.error('Failed to save task:', error);

      showMessage(
        error.response?.data?.detail ||
          'Failed to save task.',
        'error'
      );
    }
  };

  // ============================================================
  // EDIT TASK
  // ============================================================

  const editTask = (task) => {
    setEditingTaskId(task.id);
    setTaskTitle(task.title || '');
    setTaskDescription(task.description || '');
    setTaskPriority(task.priority || 'medium');

    if (task.due_date) {
      const date = new Date(task.due_date);

      const localValue =
        new Date(
          date.getTime() -
            date.getTimezoneOffset() * 60000
        )
          .toISOString()
          .slice(0, 16);

      setTaskDueDate(localValue);
    } else {
      setTaskDueDate('');
    }

    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };

  // ============================================================
  // CHANGE TASK STATUS
  // ============================================================

  const changeTaskStatus = async (task, status) => {
    try {
      await tools.tasks.update(task.id, {
        status,
      });

      showMessage('Task status updated.');

      await loadTasks();
    } catch (error) {
      console.error(
        'Failed to update task status:',
        error
      );

      showMessage(
        error.response?.data?.detail ||
          'Failed to update task.',
        'error'
      );
    }
  };

  // ============================================================
  // DELETE TASK
  // ============================================================

  const deleteTask = async (id) => {
    const confirmed = window.confirm(
      'Delete this task permanently?'
    );

    if (!confirmed) {
      return;
    }

    try {
      await tools.tasks.delete(id);

      showMessage('Task deleted successfully.');

      await loadTasks();
    } catch (error) {
      console.error('Failed to delete task:', error);

      showMessage(
        error.response?.data?.detail ||
          'Failed to delete task.',
        'error'
      );
    }
  };

  // ============================================================
  // REMINDER FORM RESET
  // ============================================================

  const resetReminderForm = () => {
    setReminderTitle('');
    setReminderDescription('');
    setReminderDate('');
    setEditingReminderId(null);
  };

  // ============================================================
  // CREATE / UPDATE REMINDER
  // ============================================================

  const saveReminder = async (event) => {
    event.preventDefault();

    if (!reminderTitle.trim()) {
      showMessage(
        'Please enter a reminder title.',
        'error'
      );
      return;
    }

    if (!reminderDate) {
      showMessage(
        'Please choose a reminder date and time.',
        'error'
      );
      return;
    }

    try {
      const payload = {
        title: reminderTitle,
        description: reminderDescription,
        remind_at: new Date(
          reminderDate
        ).toISOString(),
      };

      if (editingReminderId) {
        await tools.reminders.update(
          editingReminderId,
          payload
        );

        showMessage(
          'Reminder updated successfully.'
        );
      } else {
        await tools.reminders.create(payload);

        showMessage(
          'Reminder created successfully.'
        );
      }

      resetReminderForm();
      await loadReminders();
    } catch (error) {
      console.error(
        'Failed to save reminder:',
        error
      );

      showMessage(
        error.response?.data?.detail ||
          'Failed to save reminder.',
        'error'
      );
    }
  };

  // ============================================================
  // EDIT REMINDER
  // ============================================================

  const editReminder = (reminder) => {
    setEditingReminderId(reminder.id);

    setReminderTitle(
      reminder.title || ''
    );

    setReminderDescription(
      reminder.description || ''
    );

    if (reminder.remind_at) {
      const date = new Date(
        reminder.remind_at
      );

      const localValue =
        new Date(
          date.getTime() -
            date.getTimezoneOffset() * 60000
        )
          .toISOString()
          .slice(0, 16);

      setReminderDate(localValue);
    }

    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };

  // ============================================================
  // COMPLETE REMINDER
  // ============================================================

  const completeReminder = async (id) => {
    try {
      await tools.reminders.complete(id);

      showMessage(
        'Reminder marked as completed.'
      );

      await loadReminders();
    } catch (error) {
      console.error(
        'Failed to complete reminder:',
        error
      );

      showMessage(
        error.response?.data?.detail ||
          'Failed to complete reminder.',
        'error'
      );
    }
  };

  // ============================================================
  // DELETE REMINDER
  // ============================================================

  const deleteReminder = async (id) => {
    const confirmed = window.confirm(
      'Delete this reminder permanently?'
    );

    if (!confirmed) {
      return;
    }

    try {
      await tools.reminders.delete(id);

      showMessage(
        'Reminder deleted successfully.'
      );

      await loadReminders();
    } catch (error) {
      console.error(
        'Failed to delete reminder:',
        error
      );

      showMessage(
        error.response?.data?.detail ||
          'Failed to delete reminder.',
        'error'
      );
    }
  };

  // ============================================================
  // FORMAT DATE
  // ============================================================

  const formatDate = (value) => {
    if (!value) {
      return 'No date';
    }

    return new Date(value).toLocaleString();
  };

  // ============================================================
  // FILTER NOTES
  // ============================================================

  const filteredNotes = notes.filter((note) => {
    const query = noteSearch
      .trim()
      .toLowerCase();

    if (!query) {
      return true;
    }

    return (
      note.title
        ?.toLowerCase()
        .includes(query) ||
      note.content
        ?.toLowerCase()
        .includes(query)
    );
  });

  // ============================================================
  // FILTER TASKS
  // ============================================================

  const filteredTasks = taskStatusFilter
    ? tasks.filter(
        (task) =>
          task.status === taskStatusFilter
      )
    : tasks;

  // ============================================================
  // UI
  // ============================================================

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '1100px',
        margin: '0 auto',
        color: '#ffffff',
      }}
    >
      {/* =====================================================
          MESSAGE
      ===================================================== */}

      {message && (
        <div
          style={{
            marginBottom: '18px',
            padding: '12px 15px',
            borderRadius: '10px',
            background:
              messageType === 'error'
                ? 'rgba(255,70,70,0.10)'
                : 'rgba(0,212,255,0.08)',
            border:
              messageType === 'error'
                ? '1px solid rgba(255,70,70,0.25)'
                : '1px solid rgba(0,212,255,0.20)',
            color:
              messageType === 'error'
                ? '#ff7777'
                : '#72e8ff',
            fontSize: '13px',
          }}
        >
          {message}
        </div>
      )}

      {/* =====================================================
          TABS
      ===================================================== */}

      <div
        style={{
          display: 'flex',
          gap: '8px',
          marginBottom: '24px',
          padding: '6px',
          borderRadius: '13px',
          background: 'rgba(18,18,26,0.75)',
          border:
            '1px solid rgba(255,255,255,0.06)',
        }}
      >
        {[
          ['notes', '📝', 'Notes'],
          ['tasks', '✅', 'Tasks'],
          ['reminders', '⏰', 'Reminders'],
        ].map(([id, icon, label]) => (
          <button
            key={id}
            type="button"
            onClick={() => setActiveTab(id)}
            style={{
              flex: 1,
              border: 'none',
              borderRadius: '9px',
              padding: '11px',
              cursor: 'pointer',
              color:
                activeTab === id
                  ? '#ffffff'
                  : '#77778a',
              background:
                activeTab === id
                  ? 'rgba(0,212,255,0.12)'
                  : 'transparent',
              fontWeight:
                activeTab === id
                  ? '600'
                  : '400',
            }}
          >
            {icon} {label}
          </button>
        ))}
      </div>

      {/* =====================================================
          NOTES
      ===================================================== */}

      {activeTab === 'notes' && (
        <div>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns:
                'minmax(300px, 380px) 1fr',
              gap: '20px',
            }}
          >
            {/* NOTE FORM */}

            <div style={panelStyle}>
              <h3 style={headingStyle}>
                {editingNoteId
                  ? '✏️ Edit Note'
                  : '📝 New Note'}
              </h3>

              <form onSubmit={saveNote}>
                <input
                  value={noteTitle}
                  onChange={(event) =>
                    setNoteTitle(
                      event.target.value
                    )
                  }
                  placeholder="Note title"
                  style={inputStyle}
                />

                <textarea
                  value={noteContent}
                  onChange={(event) =>
                    setNoteContent(
                      event.target.value
                    )
                  }
                  placeholder="Write your note..."
                  rows={9}
                  style={{
                    ...inputStyle,
                    resize: 'vertical',
                  }}
                />

                <button
                  type="submit"
                  style={primaryButton}
                >
                  {editingNoteId
                    ? 'Update Note'
                    : 'Save Note'}
                </button>

                {editingNoteId && (
                  <button
                    type="button"
                    onClick={resetNoteForm}
                    style={secondaryButton}
                  >
                    Cancel
                  </button>
                )}
              </form>
            </div>

            {/* NOTES LIST */}

            <div>
              <input
                value={noteSearch}
                onChange={(event) =>
                  setNoteSearch(
                    event.target.value
                  )
                }
                placeholder="🔎 Search notes..."
                style={{
                  ...inputStyle,
                  marginBottom: '15px',
                }}
              />

              {notesLoading ? (
                <div style={emptyStyle}>
                  Loading notes...
                </div>
              ) : filteredNotes.length === 0 ? (
                <div style={emptyStyle}>
                  <div style={{ fontSize: '35px' }}>
                    📝
                  </div>

                  <div>
                    No notes found.
                  </div>
                </div>
              ) : (
                filteredNotes.map((note) => (
                  <div
                    key={note.id}
                    style={cardStyle}
                  >
                    <div
                      style={{
                        display: 'flex',
                        justifyContent:
                          'space-between',
                        gap: '10px',
                      }}
                    >
                      <h3
                        style={{
                          margin: 0,
                          fontSize: '16px',
                        }}
                      >
                        {note.title}
                      </h3>

                      <div
                        style={{
                          display: 'flex',
                          gap: '6px',
                        }}
                      >
                        <button
                          type="button"
                          onClick={() =>
                            editNote(note)
                          }
                          style={smallButton}
                        >
                          Edit
                        </button>

                        <button
                          type="button"
                          onClick={() =>
                            deleteNote(note.id)
                          }
                          style={{
                            ...smallButton,
                            color: '#ff7777',
                          }}
                        >
                          Delete
                        </button>
                      </div>
                    </div>

                    <p
                      style={{
                        color: '#b0b0bd',
                        whiteSpace: 'pre-wrap',
                        lineHeight: '1.6',
                        fontSize: '13px',
                        marginBottom: '12px',
                      }}
                    >
                      {note.content}
                    </p>

                    <div
                      style={{
                        color: '#666679',
                        fontSize: '11px',
                      }}
                    >
                      Updated:{' '}
                      {formatDate(
                        note.updated_at
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {/* =====================================================
          TASKS
      ===================================================== */}

      {activeTab === 'tasks' && (
        <div>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns:
                'minmax(300px, 380px) 1fr',
              gap: '20px',
            }}
          >
            {/* TASK FORM */}

            <div style={panelStyle}>
              <h3 style={headingStyle}>
                {editingTaskId
                  ? '✏️ Edit Task'
                  : '✅ New Task'}
              </h3>

              <form onSubmit={saveTask}>
                <input
                  value={taskTitle}
                  onChange={(event) =>
                    setTaskTitle(
                      event.target.value
                    )
                  }
                  placeholder="Task title"
                  style={inputStyle}
                />

                <textarea
                  value={taskDescription}
                  onChange={(event) =>
                    setTaskDescription(
                      event.target.value
                    )
                  }
                  placeholder="Description"
                  rows={5}
                  style={{
                    ...inputStyle,
                    resize: 'vertical',
                  }}
                />

                <label style={labelStyle}>
                  Priority
                </label>

                <select
                  value={taskPriority}
                  onChange={(event) =>
                    setTaskPriority(
                      event.target.value
                    )
                  }
                  style={inputStyle}
                >
                  <option value="low">
                    Low
                  </option>

                  <option value="medium">
                    Medium
                  </option>

                  <option value="high">
                    High
                  </option>
                </select>

                <label style={labelStyle}>
                  Due date
                </label>

                <input
                  type="datetime-local"
                  value={taskDueDate}
                  onChange={(event) =>
                    setTaskDueDate(
                      event.target.value
                    )
                  }
                  style={inputStyle}
                />

                <button
                  type="submit"
                  style={primaryButton}
                >
                  {editingTaskId
                    ? 'Update Task'
                    : 'Create Task'}
                </button>

                {editingTaskId && (
                  <button
                    type="button"
                    onClick={resetTaskForm}
                    style={secondaryButton}
                  >
                    Cancel
                  </button>
                )}
              </form>
            </div>

            {/* TASK LIST */}

            <div>
              <select
                value={taskStatusFilter}
                onChange={(event) =>
                  setTaskStatusFilter(
                    event.target.value
                  )
                }
                style={{
                  ...inputStyle,
                  marginBottom: '15px',
                }}
              >
                <option value="">
                  All tasks
                </option>

                <option value="pending">
                  Pending
                </option>

                <option value="in_progress">
                  In Progress
                </option>

                <option value="completed">
                  Completed
                </option>
              </select>

              {tasksLoading ? (
                <div style={emptyStyle}>
                  Loading tasks...
                </div>
              ) : filteredTasks.length === 0 ? (
                <div style={emptyStyle}>
                  <div style={{ fontSize: '35px' }}>
                    ✅
                  </div>

                  <div>
                    No tasks found.
                  </div>
                </div>
              ) : (
                filteredTasks.map((task) => (
                  <div
                    key={task.id}
                    style={cardStyle}
                  >
                    <div
                      style={{
                        display: 'flex',
                        justifyContent:
                          'space-between',
                        gap: '10px',
                      }}
                    >
                      <div>
                        <h3
                          style={{
                            margin: '0 0 6px',
                            fontSize: '16px',
                          }}
                        >
                          {task.title}
                        </h3>

                        <span
                          style={{
                            fontSize: '11px',
                            padding:
                              '3px 7px',
                            borderRadius:
                              '20px',
                            background:
                              'rgba(0,212,255,0.08)',
                            color: '#72e8ff',
                          }}
                        >
                          {task.priority}
                        </span>
                      </div>

                      <div
                        style={{
                          display: 'flex',
                          gap: '6px',
                        }}
                      >
                        <button
                          type="button"
                          onClick={() =>
                            editTask(task)
                          }
                          style={smallButton}
                        >
                          Edit
                        </button>

                        <button
                          type="button"
                          onClick={() =>
                            deleteTask(task.id)
                          }
                          style={{
                            ...smallButton,
                            color: '#ff7777',
                          }}
                        >
                          Delete
                        </button>
                      </div>
                    </div>

                    {task.description && (
                      <p
                        style={{
                          color: '#a7a7b5',
                          fontSize: '13px',
                          lineHeight: '1.5',
                        }}
                      >
                        {task.description}
                      </p>
                    )}

                    <div
                      style={{
                        display: 'flex',
                        gap: '8px',
                        flexWrap: 'wrap',
                        marginTop: '12px',
                      }}
                    >
                      {[
                        [
                          'pending',
                          'Pending',
                        ],
                        [
                          'in_progress',
                          'In Progress',
                        ],
                        [
                          'completed',
                          'Completed',
                        ],
                      ].map(
                        ([status, label]) => (
                          <button
                            key={status}
                            type="button"
                            onClick={() =>
                              changeTaskStatus(
                                task,
                                status
                              )
                            }
                            style={{
                              ...smallButton,
                              background:
                                task.status ===
                                status
                                  ? 'rgba(0,212,255,0.12)'
                                  : 'transparent',
                              color:
                                task.status ===
                                status
                                  ? '#72e8ff'
                                  : '#77778a',
                            }}
                          >
                            {label}
                          </button>
                        )
                      )}
                    </div>

                    <div
                      style={{
                        marginTop: '12px',
                        color: '#666679',
                        fontSize: '11px',
                      }}
                    >
                      Status: {task.status}
                      <br />
                      Due:{' '}
                      {formatDate(
                        task.due_date
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {/* =====================================================
          REMINDERS
      ===================================================== */}

      {activeTab === 'reminders' && (
        <div>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns:
                'minmax(300px, 380px) 1fr',
              gap: '20px',
            }}
          >
            {/* REMINDER FORM */}

            <div style={panelStyle}>
              <h3 style={headingStyle}>
                {editingReminderId
                  ? '✏️ Edit Reminder'
                  : '⏰ New Reminder'}
              </h3>

              <form
                onSubmit={saveReminder}
              >
                <input
                  value={reminderTitle}
                  onChange={(event) =>
                    setReminderTitle(
                      event.target.value
                    )
                  }
                  placeholder="Reminder title"
                  style={inputStyle}
                />

                <textarea
                  value={
                    reminderDescription
                  }
                  onChange={(event) =>
                    setReminderDescription(
                      event.target.value
                    )
                  }
                  placeholder="Description"
                  rows={5}
                  style={{
                    ...inputStyle,
                    resize: 'vertical',
                  }}
                />

                <label style={labelStyle}>
                  Remind me at
                </label>

                <input
                  type="datetime-local"
                  value={reminderDate}
                  onChange={(event) =>
                    setReminderDate(
                      event.target.value
                    )
                  }
                  style={inputStyle}
                />

                <button
                  type="submit"
                  style={primaryButton}
                >
                  {editingReminderId
                    ? 'Update Reminder'
                    : 'Set Reminder'}
                </button>

                {editingReminderId && (
                  <button
                    type="button"
                    onClick={
                      resetReminderForm
                    }
                    style={secondaryButton}
                  >
                    Cancel
                  </button>
                )}
              </form>
            </div>

            {/* REMINDER LIST */}

            <div>
              {remindersLoading ? (
                <div style={emptyStyle}>
                  Loading reminders...
                </div>
              ) : reminders.length === 0 ? (
                <div style={emptyStyle}>
                  <div style={{ fontSize: '35px' }}>
                    ⏰
                  </div>

                  <div>
                    No upcoming reminders.
                  </div>
                </div>
              ) : (
                reminders.map(
                  (reminder) => (
                    <div
                      key={reminder.id}
                      style={cardStyle}
                    >
                      <div
                        style={{
                          display: 'flex',
                          justifyContent:
                            'space-between',
                          gap: '10px',
                        }}
                      >
                        <div>
                          <h3
                            style={{
                              margin:
                                '0 0 6px',
                              fontSize:
                                '16px',
                            }}
                          >
                            {reminder.title}
                          </h3>

                          <div
                            style={{
                              color:
                                '#72e8ff',
                              fontSize:
                                '12px',
                            }}
                          >
                            ⏰{' '}
                            {formatDate(
                              reminder.remind_at
                            )}
                          </div>
                        </div>

                        <div
                          style={{
                            display: 'flex',
                            gap: '6px',
                          }}
                        >
                          <button
                            type="button"
                            onClick={() =>
                              editReminder(
                                reminder
                              )
                            }
                            style={smallButton}
                          >
                            Edit
                          </button>

                          <button
                            type="button"
                            onClick={() =>
                              deleteReminder(
                                reminder.id
                              )
                            }
                            style={{
                              ...smallButton,
                              color:
                                '#ff7777',
                            }}
                          >
                            Delete
                          </button>
                        </div>
                      </div>

                      {reminder.description && (
                        <p
                          style={{
                            color:
                              '#a7a7b5',
                            fontSize:
                              '13px',
                            lineHeight:
                              '1.5',
                          }}
                        >
                          {
                            reminder.description
                          }
                        </p>
                      )}

                      <button
                        type="button"
                        onClick={() =>
                          completeReminder(
                            reminder.id
                          )
                        }
                        style={{
                          ...smallButton,
                          marginTop:
                            '8px',
                          color: '#72e8ff',
                        }}
                      >
                        ✓ Mark Completed
                      </button>
                    </div>
                  )
                )
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// ============================================================
// STYLES
// ============================================================

const panelStyle = {
  padding: '20px',
  borderRadius: '15px',
  border:
    '1px solid rgba(255,255,255,0.06)',
  background: 'rgba(18,18,26,0.65)',
  boxSizing: 'border-box',
};

const cardStyle = {
  padding: '18px',
  marginBottom: '12px',
  borderRadius: '14px',
  border:
    '1px solid rgba(255,255,255,0.06)',
  background: 'rgba(18,18,26,0.65)',
};

const headingStyle = {
  margin: '0 0 16px',
  fontSize: '17px',
  color: '#ffffff',
};

const inputStyle = {
  width: '100%',
  boxSizing: 'border-box',
  padding: '11px 12px',
  marginBottom: '12px',
  borderRadius: '9px',
  border:
    '1px solid rgba(255,255,255,0.08)',
  background: '#0b0b12',
  color: '#ffffff',
  outline: 'none',
  fontSize: '13px',
};

const labelStyle = {
  display: 'block',
  marginBottom: '6px',
  color: '#77778a',
  fontSize: '11px',
};

const primaryButton = {
  width: '100%',
  border: 'none',
  borderRadius: '9px',
  padding: '11px',
  marginBottom: '8px',
  background: 'rgba(0,212,255,0.13)',
  borderColor: 'rgba(0,212,255,0.25)',
  color: '#72e8ff',
  cursor: 'pointer',
  fontWeight: '600',
};

const secondaryButton = {
  width: '100%',
  border:
    '1px solid rgba(255,255,255,0.08)',
  borderRadius: '9px',
  padding: '11px',
  background: 'transparent',
  color: '#9999aa',
  cursor: 'pointer',
};

const smallButton = {
  border:
    '1px solid rgba(255,255,255,0.08)',
  borderRadius: '7px',
  padding: '5px 8px',
  background: 'transparent',
  color: '#9999aa',
  cursor: 'pointer',
  fontSize: '11px',
};

const emptyStyle = {
  padding: '45px 20px',
  textAlign: 'center',
  borderRadius: '14px',
  border:
    '1px solid rgba(255,255,255,0.06)',
  background: 'rgba(18,18,26,0.5)',
  color: '#666679',
  fontSize: '13px',
};

export default ProductivityTools;