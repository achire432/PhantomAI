import React from 'react';

// Path to your new saved logo image
const LOGO_IMAGE = '/assets/phantom-logo.png';

const PhantomLogo = ({ variant = 'full', size = 'medium', animated = false }) => {
  // Determine size in pixels
  let sizePx = 64; // default medium
  if (size === 'small') sizePx = 32;
  if (size === 'large') sizePx = 128;

  return (
    <div style={{ textAlign: 'center', display: 'inline-block' }}>
      <img
        src={LOGO_IMAGE}
        alt="PhantomAI Logo"
        width={sizePx}
        height={sizePx}
        style={{
          borderRadius: '8px',
          animation: animated ? 'spin 4s linear infinite' : 'none',
        }}
      />
      
      {/* Add a simple spin animation if animated is true */}
      {animated && (
        <style>{`
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
        `}</style>
      )}
    </div>
  );
};

export default PhantomLogo;