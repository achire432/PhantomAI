import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ProductivityTools from '../components/tools/ProductivityTools';

import ImageGenerationTool from '../components/tools/ImageGenerationTool';
import VideoGenerationTool from '../components/tools/VideoGenerationTool';
import PDFTools from '../components/tools/PDFTools';
import NotesTool from '../components/tools/NotesTool';
import RemindersTool from '../components/tools/RemindersTool';
import TasksTool from '../components/tools/TasksTool';
import CalendarTool from '../components/tools/CalendarTool';
import EmailTool from '../components/tools/EmailTool';

// ============================================================
// TOOL LIST
// ============================================================

const TOOL_LIST = [
  {
    id: 'image',
    name: 'Image Generation',
    icon: '🎨',
    description: 'Create images from text prompts.',
    category: 'AI Generation',
  },

  {
    id: 'video',
    name: 'Video Generation',
    icon: '🎬',
    description: 'Create real AI-generated videos.',
    category: 'AI Generation',
  },

  {
    id: 'pdf',
    name: 'PDF Tools',
    icon: '📄',
    description: 'Upload, analyze and export PDF documents.',
    category: 'Documents',
  },

  {
    id: 'voice',
    name: 'Voice',
    icon: '🎤',
    description: 'Talk with PhantomAI using your voice.',
    category: 'AI',
  },

  {
    id: 'database',
    name: 'Database',
    icon: '🗄️',
    description: 'Inspect and work with databases.',
    category: 'Development',
  },

  {
    id: 'code',
    name: 'Code Analysis',
    icon: '💻',
    description: 'Analyze, explain and inspect code.',
    category: 'Development',
  },

  {
    id: 'calculator',
    name: 'Calculator',
    icon: '🧮',
    description: 'Perform calculations.',
    category: 'Utilities',
  },

  {
    id: 'weather',
    name: 'Weather',
    icon: '🌤️',
    description: 'Check weather information.',
    category: 'Utilities',
  },

  {
    id: 'files',
    name: 'Files',
    icon: '📁',
    description: 'Read and manage files.',
    category: 'Documents',
  },

  {
    id: 'web',
    name: 'Web Search',
    icon: '🌐',
    description: 'Search the web for information.',
    category: 'Research',
  },

  {
  id: 'notes',
  name: 'Notes',
  icon: '📝',
  description: 'Create, search, edit and manage your notes.',
  category: 'Productivity',
},

{
  id: 'tasks',
  name: 'Tasks',
  icon: '✅',
  description: 'Create, organize and track your tasks.',
  category: 'Productivity',
},

{
  id: 'reminders',
  name: 'Reminders',
  icon: '⏰',
  description: 'Set and manage reminders for important events.',
  category: 'Productivity',
},

{
  id: 'calendar',
  name: 'Calendar',
  icon: '📅',
  description: 'Create and manage your events and schedule.',
  category: 'Productivity',
},

{
  id: 'email',
  name: 'Email',
  icon: '✉️',
  description: 'Read, summarize, draft and send emails.',
  category: 'Productivity',
},

];

// ============================================================
// COMING SOON COMPONENT
// ============================================================

const ComingSoon = ({ icon, name }) => {
  return (
    <div
      style={{
        width: '100%',
        maxWidth: '760px',
        margin: '0 auto',
        padding: '50px 30px',
        borderRadius: '16px',
        border: '1px solid rgba(255,255,255,0.06)',
        background: 'rgba(18,18,26,0.65)',
        textAlign: 'center',
        boxSizing: 'border-box',
      }}
    >
      <div
        style={{
          fontSize: '48px',
          marginBottom: '15px',
        }}
      >
        {icon}
      </div>

      <h2
        style={{
          margin: '0 0 10px',
          color: '#ffffff',
          fontSize: '22px',
        }}
      >
        {name}
      </h2>

      <p
        style={{
          margin: 0,
          color: '#666679',
          fontSize: '13px',
        }}
      >
        This PhantomAI tool is coming soon.
      </p>
    </div>
  );
};

// ============================================================
// TOOLS PAGE
// ============================================================

const Tools = () => {
  const navigate = useNavigate();

  const [activeTool, setActiveTool] = useState('image');

  const activeToolData = TOOL_LIST.find(
    (tool) => tool.id === activeTool
  );

  // ==========================================================
  // TOOL WORKSPACE
  // ==========================================================

  const renderToolWorkspace = () => {
    switch (activeTool) {
      // ------------------------------------------------------
      // IMAGE
      // ------------------------------------------------------

      case 'image':
        return <ImageGenerationTool />;

      // ------------------------------------------------------
      // VIDEO
      // ------------------------------------------------------

      case 'video':
        return <VideoGenerationTool />;

      // ------------------------------------------------------
      // PDF
      // ------------------------------------------------------

      case 'pdf':
        return <PDFTools />;

      case 'notes':
        return <NotesTool />;

      case 'reminders':
        return <RemindersTool />;

      case 'tasks':
        return <TasksTool />;

      case 'calendar':
        return <CalendarTool />;

      case 'email':
        return <EmailTool />;

      // ------------------------------------------------------
      // OTHER TOOLS
      // ------------------------------------------------------

      case 'voice':
        return (
          <ComingSoon
            icon="🎤"
            name="Voice"
          />
        );

      case 'database':
        return (
          <ComingSoon
            icon="🗄️"
            name="Database"
          />
        );

      case 'code':
        return (
          <ComingSoon
            icon="💻"
            name="Code Analysis"
          />
        );

      case 'calculator':
        return (
          <ComingSoon
            icon="🧮"
            name="Calculator"
          />
        );

      case 'weather':
        return (
          <ComingSoon
            icon="🌤️"
            name="Weather"
          />
        );

      case 'files':
        return (
          <ComingSoon
            icon="📁"
            name="Files"
          />
        );

      case 'web':
        return (
          <ComingSoon
            icon="🌐"
            name="Web Search"
          />
        );

      default:
        return null;
    }
  };

  // ==========================================================
  // RENDER
  // ==========================================================

  return (
    <div
      style={{
        minHeight: '100vh',
        padding: '32px',
        background: '#050509',
        color: '#ffffff',
        boxSizing: 'border-box',
      }}
    >
      <div
        style={{
          maxWidth: '1250px',
          margin: '0 auto',
        }}
      >
        {/* ==================================================
            HEADER
        ================================================== */}

        <div
          style={{
            marginBottom: '30px',
          }}
        >
          <h1
            style={{
              margin: 0,
              fontSize: '32px',
              fontWeight: '700',
            }}
          >
            🛠 PhantomAI Tools
          </h1>

          <p
            style={{
              marginTop: '8px',
              marginBottom: 0,
              color: '#77778a',
              fontSize: '14px',
            }}
          >
            Powerful tools built directly into PhantomAI.
          </p>
        </div>

        {/* ==================================================
            TOOL SELECTOR
        ================================================== */}

        <div
          style={{
            display: 'grid',
            gridTemplateColumns:
              'repeat(auto-fit, minmax(190px, 1fr))',
            gap: '12px',
            marginBottom: '35px',
          }}
        >
          {TOOL_LIST.map((tool) => {
            const active = activeTool === tool.id;

            return (
              <button
                key={tool.id}
                type="button"
                onClick={() => setActiveTool(tool.id)}
                style={{
                  textAlign: 'left',
                  padding: '16px',
                  borderRadius: '13px',

                  border: active
                    ? '1px solid rgba(0,212,255,0.45)'
                    : '1px solid rgba(255,255,255,0.06)',

                  background: active
                    ? 'rgba(0,212,255,0.08)'
                    : 'rgba(18,18,26,0.65)',

                  color: '#ffffff',
                  cursor: 'pointer',

                  transition: 'all 0.2s ease',
                }}
              >
                <div
                  style={{
                    fontSize: '25px',
                    marginBottom: '10px',
                  }}
                >
                  {tool.icon}
                </div>

                <div
                  style={{
                    fontSize: '14px',
                    fontWeight: '600',
                    marginBottom: '5px',
                  }}
                >
                  {tool.name}
                </div>

                <div
                  style={{
                    color: '#666679',
                    fontSize: '11px',
                    lineHeight: '1.5',
                  }}
                >
                  {tool.description}
                </div>
              </button>
            );
          })}
        </div>

        {/* ==================================================
            ACTIVE TOOL HEADER
        ================================================== */}

        {activeToolData && (
          <div
            style={{
              marginBottom: '20px',
            }}
          >
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
              }}
            >
              <span
                style={{
                  fontSize: '25px',
                }}
              >
                {activeToolData.icon}
              </span>

              <div>
                <h2
                  style={{
                    margin: 0,
                    fontSize: '20px',
                    color: '#ffffff',
                  }}
                >
                  {activeToolData.name}
                </h2>

                <p
                  style={{
                    margin: '4px 0 0',
                    color: '#666679',
                    fontSize: '12px',
                  }}
                >
                  {activeToolData.description}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* ==================================================
            TOOL WORKSPACE
        ================================================== */}

        <div>
          {renderToolWorkspace()}
        </div>
      </div>
    </div>
  );
};

export default Tools;