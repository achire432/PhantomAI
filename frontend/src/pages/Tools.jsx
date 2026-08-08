import React, { useState } from 'react';

import ImageGenerationTool from '../components/tools/ImageGenerationTool';
import VideoGenerationTool from '../components/tools/VideoGenerationTool';


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
    description: 'Create videos from text and images.',
    category: 'AI Generation',
  },

  {
    id: 'pdf',
    name: 'PDF Tools',
    icon: '📄',
    description: 'Read, analyze and work with PDF files.',
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
];


const Tools = () => {

  const [activeTool, setActiveTool] =
    useState('image');


  const activeToolData =
    TOOL_LIST.find(
      (tool) =>
        tool.id === activeTool
    );


  const renderToolWorkspace = () => {

    switch (activeTool) {

      case 'image':
        return (
          <ImageGenerationTool />
        );


      case 'video':
        return (
          <VideoGenerationTool />
        );


      case 'pdf':
        return (
          <ComingSoon
            icon="📄"
            name="PDF Tools"
          />
        );


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

        {/* HEADER */}

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
            Use PhantomAI's capabilities directly.
          </p>

        </div>


        {/* MAIN LAYOUT */}

        <div
          style={{
            display: 'grid',
            gridTemplateColumns:
              '280px minmax(0, 1fr)',
            gap: '20px',
            alignItems: 'start',
          }}
        >

          {/* SIDEBAR */}

          <div
            style={{
              background:
                'rgba(18,18,26,0.65)',
              border:
                '1px solid rgba(255,255,255,0.06)',
              borderRadius: '14px',
              padding: '12px',
            }}
          >

            <div
              style={{
                color: '#666679',
                fontSize: '11px',
                textTransform: 'uppercase',
                letterSpacing: '1px',
                padding: '8px 10px',
                marginBottom: '4px',
              }}
            >
              Tools
            </div>


            {TOOL_LIST.map((tool) => {

              const selected =
                activeTool === tool.id;


              return (
                <button
                  key={tool.id}
                  onClick={() =>
                    setActiveTool(
                      tool.id
                    )
                  }
                  style={{
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '12px',
                    marginBottom: '4px',
                    borderRadius: '9px',
                    border: selected
                      ? '1px solid rgba(0,212,255,0.25)'
                      : '1px solid transparent',
                    background: selected
                      ? 'rgba(0,212,255,0.10)'
                      : 'transparent',
                    color: selected
                      ? '#00d4ff'
                      : '#b0b0c0',
                    cursor: 'pointer',
                    textAlign: 'left',
                  }}
                >

                  <span
                    style={{
                      fontSize: '20px',
                      width: '28px',
                      textAlign: 'center',
                    }}
                  >
                    {tool.icon}
                  </span>


                  <span
                    style={{
                      minWidth: 0,
                    }}
                  >

                    <span
                      style={{
                        display: 'block',
                        fontSize: '13px',
                        fontWeight: '600',
                      }}
                    >
                      {tool.name}
                    </span>


                    <span
                      style={{
                        display: 'block',
                        marginTop: '3px',
                        fontSize: '11px',
                        color: '#626274',
                      }}
                    >
                      {tool.category}
                    </span>

                  </span>

                </button>
              );
            })}

          </div>


          {/* WORKSPACE */}

          <div
            style={{
              minWidth: 0,
              background:
                'rgba(10,10,16,0.45)',
              border:
                '1px solid rgba(255,255,255,0.06)',
              borderRadius: '14px',
              padding: '24px',
              minHeight: '600px',
            }}
          >

            {/* WORKSPACE TITLE */}

            <div
              style={{
                borderBottom:
                  '1px solid rgba(255,255,255,0.06)',
                paddingBottom: '18px',
                marginBottom: '24px',
              }}
            >

              <div
                style={{
                  color: '#555568',
                  fontSize: '11px',
                  textTransform: 'uppercase',
                  letterSpacing: '1px',
                  marginBottom: '6px',
                }}
              >
                {activeToolData?.category}
              </div>


              <h2
                style={{
                  margin: 0,
                  fontSize: '20px',
                  color: '#ffffff',
                }}
              >
                {activeToolData?.icon}{' '}
                {activeToolData?.name}
              </h2>


              <p
                style={{
                  margin:
                    '6px 0 0',
                  color: '#686879',
                  fontSize: '13px',
                }}
              >
                {activeToolData?.description}
              </p>

            </div>


            {renderToolWorkspace()}

          </div>

        </div>

      </div>

    </div>
  );
};


const ComingSoon = ({
  icon,
  name,
}) => {

  return (
    <div
      style={{
        minHeight: '400px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
      }}
    >

      <div
        style={{
          fontSize: '52px',
          marginBottom: '16px',
        }}
      >
        {icon}
      </div>


      <h3
        style={{
          margin: 0,
          color: '#ffffff',
          fontSize: '20px',
        }}
      >
        {name}
      </h3>


      <p
        style={{
          color: '#666679',
          fontSize: '13px',
          marginTop: '8px',
        }}
      >
        This workspace will be connected next.
      </p>

    </div>
  );
};


export default Tools;
