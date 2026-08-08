import React, { useEffect, useState } from 'react';
import { settings } from '../api/endpoints';

const TOOL_GROUPS = [
  {
    name: 'Information & Web',
    tools: [
      {
        key: 'web_search',
        name: 'Web Search',
        description: 'Allow PhantomAI to search the web.',
      },
      {
        key: 'weather',
        name: 'Weather',
        description: 'Allow PhantomAI to retrieve weather information.',
      },
      {
        key: 'system_info',
        name: 'System Information',
        description: 'Allow PhantomAI to inspect system information.',
      },
    ],
  },

  {
    name: 'Files & Documents',
    tools: [
      {
        key: 'file_reading',
        name: 'File Reading',
        description: 'Allow PhantomAI to read files.',
      },
      {
        key: 'file_management',
        name: 'File Management',
        description: 'Allow PhantomAI to create, modify, move or delete files.',
      },
      {
        key: 'ocr',
        name: 'OCR',
        description: 'Allow PhantomAI to extract text from images.',
      },
      {
        key: 'pdf',
        name: 'PDF',
        description: 'Allow PhantomAI to work with PDF documents.',
      },
    ],
  },

  {
    name: 'Communication',
    tools: [
      {
        key: 'email_reading',
        name: 'Read Email',
        description: 'Allow PhantomAI to read email messages.',
      },
      {
        key: 'email_sending',
        name: 'Send Email',
        description: 'Allow PhantomAI to send email messages.',
      },
      {
        key: 'notifications',
        name: 'Notifications',
        description: 'Allow PhantomAI to send notifications.',
      },
    ],
  },

  {
    name: 'Productivity',
    tools: [
      {
        key: 'calendar',
        name: 'Calendar',
        description: 'Allow PhantomAI to manage calendar events.',
      },
      {
        key: 'tasks',
        name: 'Tasks',
        description: 'Allow PhantomAI to manage tasks.',
      },
      {
        key: 'reminders',
        name: 'Reminders',
        description: 'Allow PhantomAI to manage reminders.',
      },
      {
        key: 'notes',
        name: 'Notes',
        description: 'Allow PhantomAI to manage notes.',
      },
      {
        key: 'memory',
        name: 'Memory',
        description: 'Allow PhantomAI to access stored memories.',
      },
    ],
  },

  {
    name: 'Development',
    tools: [
      {
        key: 'git',
        name: 'Git',
        description: 'Allow PhantomAI to inspect and work with Git repositories.',
      },
      {
        key: 'code_analysis',
        name: 'Code Analysis',
        description: 'Allow PhantomAI to analyze code.',
      },
      {
        key: 'database',
        name: 'Database',
        description: 'Allow PhantomAI to access database operations.',
      },
    ],
  },

  {
    name: 'Computer Control',
    tools: [
      {
        key: 'application_launcher',
        name: 'Application Launcher',
        description: 'Allow PhantomAI to launch applications.',
      },
      {
        key: 'terminal',
        name: 'Terminal',
        description: 'Allow PhantomAI to execute terminal commands.',
        dangerous: true,
      },
    ],
  },

  {
    name: 'AI Generation',
    tools: [
      {
        key: 'image_generation',
        name: 'Image Generation',
        description: 'Allow PhantomAI to generate images.',
      },
      {
        key: 'video_generation',
        name: 'Video Generation',
        description: 'Allow PhantomAI to generate videos.',
      },
      {
        key: 'calculator',
        name: 'Calculator',
        description: 'Allow PhantomAI to perform calculations.',
      },
    ],
  },
];

const PERMISSION_OPTIONS = [
  {
    value: 'allowed',
    label: 'Allowed',
    description: 'PhantomAI can use it without asking.',
  },
  {
    value: 'confirmation_required',
    label: 'Ask first',
    description: 'PhantomAI must ask before using it.',
  },
  {
    value: 'disabled',
    label: 'Disabled',
    description: 'PhantomAI cannot use it.',
  },
];

const permissionLabel = (permission) => {
  const option = PERMISSION_OPTIONS.find(
    (item) => item.value === permission
  );

  return option?.label || permission;
};

const permissionColor = (permission) => {
  if (permission === 'allowed') {
    return '#32d583';
  }

  if (permission === 'confirmation_required') {
    return '#fdb022';
  }

  return '#f97066';
};

const Settings = () => {
  const [permissions, setPermissions] = useState({});
  const [loading, setLoading] = useState(true);
  const [savingTool, setSavingTool] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const loadPermissions = async () => {
    try {
      setLoading(true);
      setError('');

      const response = await settings.tools.getAll();

      setPermissions(
        response.data.tool_permissions || {}
      );
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Failed to load tool permissions.'
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPermissions();
  }, []);

  const updatePermission = async (
    toolName,
    permission
  ) => {
    try {
      setSavingTool(toolName);
      setError('');
      setMessage('');

      await settings.tools.update(
        toolName,
        permission
      );

      setPermissions((previous) => ({
        ...previous,
        [toolName]: permission,
      }));

      setMessage(
        `${toolName.replaceAll('_', ' ')} permission updated.`
      );
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        `Failed to update ${toolName}.`
      );
    } finally {
      setSavingTool(null);
    }
  };

  const updateAll = async (permission) => {
    try {
      setSavingTool('__all__');
      setError('');
      setMessage('');

      const response =
        await settings.tools.updateAll(
          permission
        );

      setPermissions(
        response.data.tool_permissions || {}
      );

      setMessage(
        `All tools are now ${permissionLabel(permission).toLowerCase()}.`
      );
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Failed to update all permissions.'
      );
    } finally {
      setSavingTool(null);
    }
  };

  const resetPermissions = async () => {
    try {
      setSavingTool('__reset__');
      setError('');
      setMessage('');

      const response =
        await settings.tools.reset();

      setPermissions(
        response.data.tool_permissions || {}
      );

      setMessage(
        'Tool permissions restored to defaults.'
      );
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Failed to reset permissions.'
      );
    } finally {
      setSavingTool(null);
    }
  };

  const enabledCount = Object.values(
    permissions
  ).filter(
    (value) => value === 'allowed'
  ).length;

  const confirmationCount =
    Object.values(permissions).filter(
      (value) =>
        value === 'confirmation_required'
    ).length;

  const disabledCount =
    Object.values(permissions).filter(
      (value) => value === 'disabled'
    ).length;

  return (
    <div
      style={{
        minHeight: '100vh',
        padding: '40px',
        color: '#ffffff',
        background: '#050509',
      }}
    >
      <div
        style={{
          maxWidth: '1100px',
          margin: '0 auto',
        }}
      >
        <div
          style={{
            marginBottom: '35px',
          }}
        >
          <h1
            style={{
              margin: 0,
              fontSize: '32px',
            }}
          >
            PhantomAI Settings
          </h1>

          <p
            style={{
              marginTop: '10px',
              color: '#9ca3af',
              fontSize: '15px',
            }}
          >
            Control what PhantomAI is allowed to access
            and what it must ask you to do first.
          </p>
        </div>

        {message && (
          <div
            style={{
              marginBottom: '20px',
              padding: '14px 16px',
              borderRadius: '10px',
              background: 'rgba(50, 213, 131, 0.10)',
              border: '1px solid rgba(50, 213, 131, 0.30)',
              color: '#8ff0bb',
            }}
          >
            {message}
          </div>
        )}

        {error && (
          <div
            style={{
              marginBottom: '20px',
              padding: '14px 16px',
              borderRadius: '10px',
              background: 'rgba(249, 112, 102, 0.10)',
              border: '1px solid rgba(249, 112, 102, 0.30)',
              color: '#ffaaa3',
            }}
          >
            {error}
          </div>
        )}

        {/* SUMMARY */}

        <div
          style={{
            display: 'grid',
            gridTemplateColumns:
              'repeat(3, 1fr)',
            gap: '15px',
            marginBottom: '25px',
          }}
        >
          <SummaryCard
            title="Allowed"
            value={enabledCount}
            description="Runs automatically"
            color="#32d583"
          />

          <SummaryCard
            title="Ask First"
            value={confirmationCount}
            description="Requires confirmation"
            color="#fdb022"
          />

          <SummaryCard
            title="Disabled"
            value={disabledCount}
            description="Cannot be used"
            color="#f97066"
          />
        </div>

        {/* GLOBAL CONTROLS */}

        <div
          style={{
            padding: '22px',
            marginBottom: '30px',
            borderRadius: '14px',
            background: '#0b0b12',
            border: '1px solid #20202b',
          }}
        >
          <h2
            style={{
              marginTop: 0,
              fontSize: '18px',
            }}
          >
            Global Tool Permissions
          </h2>

          <p
            style={{
              color: '#8b8d98',
              fontSize: '14px',
              marginBottom: '18px',
            }}
          >
            Change the permission level of every
            PhantomAI tool at once.
          </p>

          <div
            style={{
              display: 'flex',
              gap: '10px',
              flexWrap: 'wrap',
            }}
          >
            <ActionButton
              disabled={savingTool !== null}
              onClick={() =>
                updateAll('allowed')
              }
            >
              Allow All
            </ActionButton>

            <ActionButton
              disabled={savingTool !== null}
              onClick={() =>
                updateAll(
                  'confirmation_required'
                )
              }
            >
              Ask Before Everything
            </ActionButton>

            <ActionButton
              disabled={savingTool !== null}
              onClick={() =>
                updateAll('disabled')
              }
            >
              Disable All
            </ActionButton>

            <ActionButton
              disabled={savingTool !== null}
              onClick={resetPermissions}
            >
              Reset Defaults
            </ActionButton>
          </div>
        </div>

        {/* TOOL GROUPS */}

        {loading ? (
          <div
            style={{
              padding: '50px',
              textAlign: 'center',
              color: '#8b8d98',
            }}
          >
            Loading PhantomAI permissions...
          </div>
        ) : (
          TOOL_GROUPS.map((group) => (
            <div
              key={group.name}
              style={{
                marginBottom: '30px',
              }}
            >
              <h2
                style={{
                  fontSize: '18px',
                  marginBottom: '12px',
                }}
              >
                {group.name}
              </h2>

              <div
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '10px',
                }}
              >
                {group.tools.map((tool) => (
                  <ToolPermissionRow
                    key={tool.key}
                    tool={tool}
                    permission={
                      permissions[tool.key] ||
                      'disabled'
                    }
                    saving={
                      savingTool === tool.key
                    }
                    onChange={
                      updatePermission
                    }
                  />
                ))}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};


// ============================================================
// SUMMARY CARD
// ============================================================

const SummaryCard = ({
  title,
  value,
  description,
  color,
}) => (
  <div
    style={{
      padding: '20px',
      borderRadius: '14px',
      background: '#0b0b12',
      border: '1px solid #20202b',
    }}
  >
    <div
      style={{
        color,
        fontSize: '28px',
        fontWeight: '700',
      }}
    >
      {value}
    </div>

    <div
      style={{
        marginTop: '5px',
        fontWeight: '600',
      }}
    >
      {title}
    </div>

    <div
      style={{
        marginTop: '4px',
        color: '#777b87',
        fontSize: '13px',
      }}
    >
      {description}
    </div>
  </div>
);


// ============================================================
// TOOL ROW
// ============================================================

const ToolPermissionRow = ({
  tool,
  permission,
  saving,
  onChange,
}) => {
  const color =
    permissionColor(permission);

  return (
    <div
      style={{
        padding: '18px 20px',
        borderRadius: '12px',
        background: '#0b0b12',
        border: '1px solid #20202b',
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '20px',
          flexWrap: 'wrap',
        }}
      >
        <div
          style={{
            flex: 1,
            minWidth: '250px',
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
            }}
          >
            <strong>
              {tool.name}
            </strong>

            {tool.dangerous && (
              <span
                style={{
                  fontSize: '11px',
                  padding: '3px 7px',
                  borderRadius: '5px',
                  background:
                    'rgba(249,112,102,0.12)',
                  color: '#f97066',
                }}
              >
                SENSITIVE
              </span>
            )}
          </div>

          <div
            style={{
              marginTop: '6px',
              color: '#777b87',
              fontSize: '13px',
            }}
          >
            {tool.description}
          </div>
        </div>

        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
          }}
        >
          <span
            style={{
              minWidth: '75px',
              textAlign: 'center',
              fontSize: '12px',
              fontWeight: '600',
              color,
            }}
          >
            {saving
              ? 'Saving...'
              : permissionLabel(
                  permission
                )}
          </span>

          <select
            value={permission}
            disabled={saving}
            onChange={(event) =>
              onChange(
                tool.key,
                event.target.value
              )
            }
            style={{
              minWidth: '190px',
              padding: '10px 12px',
              borderRadius: '8px',
              border: '1px solid #30303b',
              background: '#12121a',
              color: '#ffffff',
              outline: 'none',
              cursor: saving
                ? 'wait'
                : 'pointer',
            }}
          >
            {PERMISSION_OPTIONS.map(
              (option) => (
                <option
                  key={option.value}
                  value={option.value}
                >
                  {option.label}
                </option>
              )
            )}
          </select>
        </div>
      </div>
    </div>
  );
};


// ============================================================
// ACTION BUTTON
// ============================================================

const ActionButton = ({
  children,
  onClick,
  disabled,
}) => (
  <button
    type="button"
    disabled={disabled}
    onClick={onClick}
    style={{
      padding: '10px 15px',
      borderRadius: '8px',
      border: '1px solid #30303b',
      background: '#12121a',
      color: '#ffffff',
      cursor: disabled
        ? 'not-allowed'
        : 'pointer',
      opacity: disabled ? 0.5 : 1,
    }}
  >
    {children}
  </button>
);

export default Settings;
