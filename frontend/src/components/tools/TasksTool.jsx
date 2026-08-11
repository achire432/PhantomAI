import React, {
  useEffect,
  useState,
} from 'react';

import { tools } from '../../api/endpoints';

const TasksTool = () => {
  // ==========================================================
  // STATE
  // ==========================================================

  const [tasks, setTasks] = useState([]);

  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState('');

  const [editingId, setEditingId] =
    useState(null);

  const [statusFilter, setStatusFilter] =
    useState('');

  const [form, setForm] = useState({
    title: '',
    description: '',
    priority: 'medium',
    due_date: '',
  });

  // ==========================================================
  // LOAD TASKS
  // ==========================================================

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError('');

      const response =
        await tools.tasks.getAll();

      setTasks(response.data || []);
    } catch (err) {
      console.error(
        'Failed to load tasks:',
        err
      );

      setError(
        err?.response?.data?.detail ||
          'Unable to load tasks.'
      );
    } finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // INITIAL LOAD
  // ==========================================================

  useEffect(() => {
    loadTasks();
  }, []);

  // ==========================================================
  // FORM CHANGE
  // ==========================================================

  const handleChange = (event) => {
    const {
      name,
      value,
    } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  // ==========================================================
  // RESET FORM
  // ==========================================================

  const resetForm = () => {
    setEditingId(null);

    setForm({
      title: '',
      description: '',
      priority: 'medium',
      due_date: '',
    });

    setError('');
  };

  // ==========================================================
  // EDIT TASK
  // ==========================================================

  const handleEdit = (task) => {
    setError('');

    setEditingId(task.id);

    setForm({
      title: task.title || '',
      description:
        task.description || '',
      priority:
        task.priority || 'medium',
      due_date: task.due_date
        ? toDateTimeLocal(
            task.due_date
          )
        : '',
    });

    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };

  // ==========================================================
  // CREATE / UPDATE TASK
  // ==========================================================

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError('');

    if (!form.title.trim()) {
      setError(
        'Please enter a task title.'
      );
      return;
    }

    try {
      setSaving(true);

      const payload = {
        title: form.title.trim(),
        description:
          form.description.trim(),
        priority: form.priority,
        due_date:
          form.due_date || null,
      };

      // ------------------------------------------------------
      // UPDATE
      // ------------------------------------------------------

      if (editingId) {
        await tools.tasks.update(
          editingId,
          payload
        );
      }

      // ------------------------------------------------------
      // CREATE
      // ------------------------------------------------------

      else {
        await tools.tasks.create(
          payload
        );
      }

      resetForm();

      await loadTasks();
    } catch (err) {
      console.error(
        'Failed to save task:',
        err
      );

      setError(
        err?.response?.data?.detail ||
          'Failed to save task.'
      );
    } finally {
      setSaving(false);
    }
  };

  // ==========================================================
  // DELETE TASK
  // ==========================================================

  const handleDelete = async (id) => {
    const task = tasks.find(
      (item) => item.id === id
    );

    const confirmed =
      window.confirm(
        `Delete "${task?.title || 'this task'}"? This cannot be undone.`
      );

    if (!confirmed) {
      return;
    }

    try {
      setError('');

      await tools.tasks.delete(id);

      if (editingId === id) {
        resetForm();
      }

      await loadTasks();
    } catch (err) {
      console.error(
        'Failed to delete task:',
        err
      );

      setError(
        err?.response?.data?.detail ||
          'Failed to delete task.'
      );
    }
  };

  // ==========================================================
  // CHANGE TASK STATUS
  // ==========================================================

  const handleStatusChange = async (
    task,
    newStatus
  ) => {
    try {
      setError('');

      await tools.tasks.update(
        task.id,
        {
          status: newStatus,
        }
      );

      await loadTasks();
    } catch (err) {
      console.error(
        'Failed to update task status:',
        err
      );

      setError(
        err?.response?.data?.detail ||
          'Failed to update task status.'
      );
    }
  };

  // ==========================================================
  // CHECKBOX
  // ==========================================================

  const handleCheckboxChange = async (
    task
  ) => {
    const newStatus =
      task.status === 'completed'
        ? 'pending'
        : 'completed';

    await handleStatusChange(
      task,
      newStatus
    );
  };

  // ==========================================================
  // STATUS LABEL
  // ==========================================================

  const statusLabel = (status) => {
    if (status === 'completed') {
      return 'Completed';
    }

    if (status === 'in_progress') {
      return 'In Progress';
    }

    return 'Pending';
  };

  // ==========================================================
  // PRIORITY LABEL
  // ==========================================================

  const priorityLabel = (priority) => {
    if (priority === 'high') {
      return 'High';
    }

    if (priority === 'low') {
      return 'Low';
    }

    return 'Medium';
  };

  // ==========================================================
  // DATE HELPERS
  // ==========================================================

  const formatDate = (date) => {
    if (!date) {
      return 'Not set';
    }

    const parsedDate =
      new Date(date);

    if (
      Number.isNaN(
        parsedDate.getTime()
      )
    ) {
      return 'Invalid date';
    }

    return parsedDate.toLocaleString();
  };

  const formatDateOnly = (date) => {
    if (!date) {
      return 'Not set';
    }

    const parsedDate =
      new Date(date);

    if (
      Number.isNaN(
        parsedDate.getTime()
      )
    ) {
      return 'Invalid date';
    }

    return parsedDate.toLocaleDateString();
  };

  const isOverdue = (task) => {
    if (
      !task.due_date ||
      task.status === 'completed'
    ) {
      return false;
    }

    const dueDate =
      new Date(task.due_date);

    if (
      Number.isNaN(
        dueDate.getTime()
      )
    ) {
      return false;
    }

    return dueDate < new Date();
  };

  const isDueToday = (task) => {
    if (!task.due_date) {
      return false;
    }

    const dueDate =
      new Date(task.due_date);

    if (
      Number.isNaN(
        dueDate.getTime()
      )
    ) {
      return false;
    }

    const today = new Date();

    return (
      dueDate.getFullYear() ===
        today.getFullYear() &&
      dueDate.getMonth() ===
        today.getMonth() &&
      dueDate.getDate() ===
        today.getDate()
    );
  };

  // ==========================================================
  // FILTER TASKS
  // ==========================================================

  const filteredTasks =
    statusFilter
      ? tasks.filter(
          (task) =>
            task.status ===
            statusFilter
        )
      : tasks;

  // ==========================================================
  // RENDER
  // ==========================================================

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '900px',
        margin: '0 auto',
        boxSizing: 'border-box',
      }}
    >
      {/* ====================================================
          CREATE / EDIT TASK
      ==================================================== */}

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
            justifyContent:
              'space-between',
            alignItems: 'center',
            marginBottom: '20px',
            gap: '12px',
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
                ? 'Edit Task'
                : 'Create Task'}
            </h3>

            <p
              style={{
                margin:
                  '6px 0 0',
                color: '#77778a',
                fontSize: '13px',
              }}
            >
              Organize what you need
              to get done.
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
                padding:
                  '8px 12px',
                borderRadius: '8px',
                cursor: 'pointer',
              }}
            >
              Cancel
            </button>
          )}
        </div>

        <form
          onSubmit={handleSubmit}
        >
          <input
            name="title"
            value={form.title}
            onChange={handleChange}
            placeholder="Task title"
            style={inputStyle}
          />

          <textarea
            name="description"
            value={
              form.description
            }
            onChange={handleChange}
            placeholder="Description"
            rows={4}
            style={{
              ...inputStyle,
              resize: 'vertical',
            }}
          />

          <div
            style={{
              display: 'grid',
              gridTemplateColumns:
                '1fr 1fr',
              gap: '12px',
            }}
          >
            <select
              name="priority"
              value={
                form.priority
              }
              onChange={handleChange}
              style={inputStyle}
            >
              <option value="low">
                Low priority
              </option>

              <option value="medium">
                Medium priority
              </option>

              <option value="high">
                High priority
              </option>
            </select>

            <input
              type="datetime-local"
              name="due_date"
              value={
                form.due_date
              }
              onChange={handleChange}
              style={inputStyle}
            />
          </div>

          <div
            style={{
              color: '#666679',
              fontSize: '12px',
              marginBottom:
                '10px',
            }}
          >
            The creation date is
            automatically recorded
            when you create the task.
          </div>

          <button
            type="submit"
            disabled={saving}
            style={{
              marginTop: '4px',
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
              opacity: saving
                ? 0.7
                : 1,
            }}
          >
            {saving
              ? 'Saving...'
              : editingId
                ? 'Update Task'
                : 'Create Task'}
          </button>
        </form>
      </div>

      {/* ====================================================
          ERROR
      ==================================================== */}

      {error && (
        <div
          style={{
            marginBottom:
              '18px',
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

      {/* ====================================================
          STATUS FILTER
      ==================================================== */}

      <div
        style={{
          display: 'flex',
          gap: '8px',
          marginBottom:
            '18px',
          flexWrap: 'wrap',
        }}
      >
        {[
          ['', 'All'],
          ['pending', 'Pending'],
          [
            'in_progress',
            'In Progress',
          ],
          [
            'completed',
            'Completed',
          ],
        ].map(
          ([value, label]) => (
            <button
              key={value}
              type="button"
              onClick={() =>
                setStatusFilter(
                  value
                )
              }
              style={{
                border:
                  statusFilter ===
                  value
                    ? '1px solid rgba(0,212,255,0.5)'
                    : '1px solid rgba(255,255,255,0.08)',

                background:
                  statusFilter ===
                  value
                    ? 'rgba(0,212,255,0.1)'
                    : 'rgba(255,255,255,0.04)',

                color:
                  statusFilter ===
                  value
                    ? '#00d4ff'
                    : '#aaa',

                borderRadius:
                  '8px',

                padding:
                  '8px 12px',

                cursor:
                  'pointer',
              }}
            >
              {label}
            </button>
          )
        )}
      </div>

      {/* ====================================================
          TASK LIST
      ==================================================== */}

      {loading ? (
        <div
          style={emptyStyle}
        >
          Loading tasks...
        </div>
      ) : filteredTasks.length ===
        0 ? (
        <div
          style={emptyStyle}
        >
          <div
            style={{
              fontSize: '38px',
              marginBottom:
                '10px',
            }}
          >
            ✓
          </div>

          <div
            style={{
              color: '#fff',
              fontWeight:
                '600',
            }}
          >
            No tasks found
          </div>

          <div
            style={{
              marginTop: '5px',
              color: '#666679',
              fontSize: '13px',
            }}
          >
            {statusFilter
              ? `No ${statusLabel(
                  statusFilter
                ).toLowerCase()} tasks found.`
              : 'Create your first task above.'}
          </div>
        </div>
      ) : (
        <div
          style={{
            display: 'grid',
            gap: '12px',
          }}
        >
          {filteredTasks.map(
            (task) => {
              const completed =
                task.status ===
                'completed';

              const overdue =
                isOverdue(task);

              const dueToday =
                isDueToday(task);

              return (
                <div
                  key={task.id}
                  style={{
                    background:
                      completed
                        ? 'rgba(0,255,150,0.025)'
                        : '#12121a',

                    border:
                      overdue
                        ? '1px solid rgba(255,70,70,0.35)'
                        : completed
                          ? '1px solid rgba(0,255,150,0.15)'
                          : '1px solid rgba(255,255,255,0.07)',

                    borderRadius:
                      '14px',

                    padding:
                      '18px',

                    opacity:
                      completed
                        ? 0.8
                        : 1,
                  }}
                >
                  <div
                    style={{
                      display:
                        'flex',
                      gap: '14px',
                      alignItems:
                        'flex-start',
                    }}
                  >
                    {/* ========================================
                        CHECKBOX
                    ======================================== */}

                    <button
                      type="button"
                      onClick={() =>
                        handleCheckboxChange(
                          task
                        )
                      }
                      title={
                        completed
                          ? 'Mark as pending'
                          : 'Mark as completed'
                      }
                      aria-label={
                        completed
                          ? 'Mark task as pending'
                          : 'Mark task as completed'
                      }
                      style={{
                        flexShrink: 0,
                        width: '28px',
                        height: '28px',
                        borderRadius:
                          '7px',

                        border:
                          completed
                            ? '1px solid #00e69a'
                            : '1px solid rgba(255,255,255,0.25)',

                        background:
                          completed
                            ? 'rgba(0,230,154,0.15)'
                            : 'rgba(255,255,255,0.03)',

                        color:
                          '#00e69a',

                        cursor:
                          'pointer',

                        fontSize:
                          '17px',

                        fontWeight:
                          '700',

                        display:
                          'flex',

                        alignItems:
                          'center',

                        justifyContent:
                          'center',

                        padding: 0,
                      }}
                    >
                      {completed
                        ? '✓'
                        : ''}
                    </button>

                    {/* ========================================
                        MAIN CONTENT
                    ======================================== */}

                    <div
                      style={{
                        minWidth: 0,
                        flex: 1,
                      }}
                    >
                      <div
                        style={{
                          display:
                            'flex',
                          justifyContent:
                            'space-between',
                          gap: '15px',
                          alignItems:
                            'flex-start',
                        }}
                      >
                        <div
                          style={{
                            minWidth: 0,
                            flex: 1,
                          }}
                        >
                          <h4
                            style={{
                              margin: 0,
                              color:
                                completed
                                  ? '#777'
                                  : '#fff',

                              fontSize:
                                '16px',

                              lineHeight:
                                '1.4',

                              textDecoration:
                                completed
                                  ? 'line-through'
                                  : 'none',

                              wordBreak:
                                'break-word',
                            }}
                          >
                            {task.title}
                          </h4>

                          {task.description && (
                            <p
                              style={{
                                color:
                                  completed
                                    ? '#666'
                                    : '#858598',

                                fontSize:
                                  '13px',

                                lineHeight:
                                  '1.5',

                                margin:
                                  '8px 0',

                                textDecoration:
                                  completed
                                    ? 'line-through'
                                    : 'none',
                              }}
                            >
                              {
                                task.description
                              }
                            </p>
                          )}
                        </div>

                        {/* ====================================
                            ACTIONS
                        ==================================== */}

                        <div
                          style={{
                            display:
                              'flex',
                            gap: '6px',
                            flexWrap:
                              'wrap',
                            alignItems:
                              'flex-start',
                            justifyContent:
                              'flex-end',
                          }}
                        >
                          <button
                            type="button"
                            onClick={() =>
                              handleEdit(
                                task
                              )
                            }
                            style={
                              actionButtonStyle
                            }
                          >
                            Edit
                          </button>

                          <button
                            type="button"
                            onClick={() =>
                              handleDelete(
                                task.id
                              )
                            }
                            style={{
                              ...actionButtonStyle,
                              color:
                                '#ff7777',
                            }}
                          >
                            Delete
                          </button>
                        </div>
                      </div>

                      {/* ====================================
                          TASK INFORMATION
                      ==================================== */}

                      <div
                        style={{
                          display:
                            'grid',
                          gridTemplateColumns:
                            'repeat(auto-fit, minmax(180px,1fr))',
                          gap: '8px',
                          marginTop:
                            '14px',
                        }}
                      >
                        {/* STATUS */}

                        <div
                          style={{
                            ...infoBoxStyle,
                            borderColor:
                              completed
                                ? 'rgba(0,230,154,0.15)'
                                : 'rgba(255,255,255,0.06)',
                          }}
                        >
                          <span
                            style={
                              infoLabelStyle
                            }
                          >
                            Status
                          </span>

                          <span
                            style={{
                              color:
                                completed
                                  ? '#00e69a'
                                  : task.status ===
                                      'in_progress'
                                    ? '#00d4ff'
                                    : '#ffc857',

                              fontSize:
                                '12px',

                              fontWeight:
                                '600',
                            }}
                          >
                            {completed
                              ? '✓ Completed'
                              : task.status ===
                                  'in_progress'
                                ? '🔄 In Progress'
                                : '☐ Pending'}
                          </span>
                        </div>

                        {/* PRIORITY */}

                        <div
                          style={
                            infoBoxStyle
                          }
                        >
                          <span
                            style={
                              infoLabelStyle
                            }
                          >
                            Priority
                          </span>

                          <span
                            style={{
                              color:
                                task.priority ===
                                'high'
                                  ? '#ff7777'
                                  : task.priority ===
                                      'low'
                                    ? '#00d4ff'
                                    : '#ffc857',

                              fontSize:
                                '12px',

                              fontWeight:
                                '600',
                            }}
                          >
                            {priorityLabel(
                              task.priority
                            )}
                          </span>
                        </div>

                        {/* CREATED */}

                        <div
                          style={
                            infoBoxStyle
                          }
                        >
                          <span
                            style={
                              infoLabelStyle
                            }
                          >
                            Created
                          </span>

                          <span
                            style={{
                              color:
                                '#bbb',
                              fontSize:
                                '12px',
                            }}
                          >
                            {formatDateOnly(
                              task.created_at
                            )}
                          </span>
                        </div>

                        {/* DUE DATE */}

                        <div
                          style={{
                            ...infoBoxStyle,
                            borderColor:
                              overdue
                                ? 'rgba(255,70,70,0.25)'
                                : dueToday
                                  ? 'rgba(255,200,87,0.25)'
                                  : 'rgba(255,255,255,0.06)',
                          }}
                        >
                          <span
                            style={
                              infoLabelStyle
                            }
                          >
                            Due date
                          </span>

                          {!task.due_date ? (
                            <span
                              style={{
                                color:
                                  '#666679',
                                fontSize:
                                  '12px',
                              }}
                            >
                              No due date
                            </span>
                          ) : (
                            <span
                              style={{
                                color:
                                  overdue
                                    ? '#ff7777'
                                    : dueToday
                                      ? '#ffc857'
                                      : '#bbb',

                                fontSize:
                                  '12px',

                                fontWeight:
                                  overdue ||
                                  dueToday
                                    ? '600'
                                    : '400',
                              }}
                            >
                              {overdue
                                ? '⚠️ Overdue — '
                                : dueToday
                                  ? '⏰ Today — '
                                  : ''}

                              {formatDate(
                                task.due_date
                              )}
                            </span>
                          )}
                        </div>
                      </div>

                      {/* ====================================
                          QUICK STATUS CONTROLS
                      ==================================== */}

                      {!completed && (
                        <div
                          style={{
                            display:
                              'flex',
                            gap: '7px',
                            marginTop:
                              '13px',
                            flexWrap:
                              'wrap',
                          }}
                        >
                          <button
                            type="button"
                            onClick={() =>
                              handleStatusChange(
                                task,
                                'in_progress'
                              )
                            }
                            disabled={
                              task.status ===
                              'in_progress'
                            }
                            style={{
                              ...smallStatusButtonStyle,

                              color:
                                task.status ===
                                'in_progress'
                                  ? '#00d4ff'
                                  : '#aaa',

                              borderColor:
                                task.status ===
                                'in_progress'
                                  ? 'rgba(0,212,255,0.35)'
                                  : 'rgba(255,255,255,0.08)',

                              cursor:
                                task.status ===
                                'in_progress'
                                  ? 'not-allowed'
                                  : 'pointer',

                              opacity:
                                task.status ===
                                'in_progress'
                                  ? 0.7
                                  : 1,
                            }}
                          >
                            🔄 In Progress
                          </button>

                          <button
                            type="button"
                            onClick={() =>
                              handleStatusChange(
                                task,
                                'completed'
                              )
                            }
                            style={{
                              ...smallStatusButtonStyle,
                              color:
                                '#00e69a',
                              borderColor:
                                'rgba(0,230,154,0.2)',
                            }}
                          >
                            ✓ Mark Completed
                          </button>
                        </div>
                      )}

                      {completed && (
                        <button
                          type="button"
                          onClick={() =>
                            handleStatusChange(
                              task,
                              'pending'
                            )
                          }
                          style={{
                            ...smallStatusButtonStyle,
                            marginTop:
                              '13px',
                            color:
                              '#ffc857',
                            borderColor:
                              'rgba(255,200,87,0.2)',
                          }}
                        >
                          ↩ Mark as Pending
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              );
            }
          )}
        </div>
      )}
    </div>
  );
};

// ============================================================
// HELPER: DATETIME-LOCAL VALUE
// ============================================================

const toDateTimeLocal = (
  date
) => {
  const parsedDate =
    new Date(date);

  if (
    Number.isNaN(
      parsedDate.getTime()
    )
  ) {
    return '';
  }

  const offset =
    parsedDate.getTimezoneOffset();

  const localDate =
    new Date(
      parsedDate.getTime() -
        offset * 60 * 1000
    );

  return localDate
    .toISOString()
    .slice(0, 16);
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

const infoBoxStyle = {
  display: 'flex',
  flexDirection: 'column',
  gap: '5px',
  padding: '9px 10px',
  borderRadius: '8px',
  background:
    'rgba(255,255,255,0.025)',
  border:
    '1px solid rgba(255,255,255,0.06)',
};

const infoLabelStyle = {
  color: '#666679',
  fontSize: '10px',
  textTransform: 'uppercase',
  letterSpacing: '0.5px',
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

const smallStatusButtonStyle = {
  border:
    '1px solid rgba(255,255,255,0.08)',
  background:
    'rgba(255,255,255,0.03)',
  padding: '7px 10px',
  borderRadius: '7px',
  cursor: 'pointer',
  fontSize: '11px',
};

export default TasksTool;