import React from 'react';

const LOGO_SVG = '/assets/phantom-logo.png';

const PhantomLogo = ({ variant = 'full', size = 'medium', animated = false, className = '' }) => {
  const sizeMap = {
    small: { icon: 36, text: 18 },
    medium: { icon: 48, text: 24 },
    large: { icon: 72, text: 32 },
  };

  const { icon, text } = sizeMap[size] || sizeMap.medium;

  if (variant === 'icon') {
    return (
      <div className={`flex items-center justify-center ${className}`}>
        <img src={LOGO_SVG} alt="PhantomAI" width={icon} height={icon} />
      </div>
    );
  }

  if (variant === 'compact') {
    return (
      <div className={`flex items-center gap-2 ${className}`}>
        <img src={LOGO_SVG} alt="PhantomAI" width={icon * 0.7} height={icon * 0.7} />
        <span style={{ fontSize: text * 0.8, fontWeight: 700, color: '#ffffff', letterSpacing: '2px' }}>
          PHANTOMAI
        </span>
      </div>
    );
  }

  return (
    <div className={`flex flex-col items-center ${className}`}>
      <img src={LOGO_SVG} alt="PhantomAI" width={icon} height={icon} className="mb-2" />
      <span style={{ fontSize: text, fontWeight: 700, color: '#ffffff', letterSpacing: '4px' }}>
        PHANTOMAI
      </span>
      <span style={{ fontSize: text * 0.35, fontWeight: 400, color: '#606080', letterSpacing: '6px', marginTop: '2px' }}>
        YOUR INTELLIGENT ASSISTANT
      </span>
    </div>
  );
};

export default PhantomLogo;
