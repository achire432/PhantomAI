import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import AppRoutes from './routes/AppRoutes';
import StarfieldBackground from './components/StarfieldBackground';
import Navbar from './components/Navbar';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        
        {/* The Starfield is fixed to 100% screen */}
        <StarfieldBackground />
        
        <Navbar />
        
        {/* 
           Main Content Wrapper.
           We removed 'minHeight: 100vh' to stop it from blocking the stars.
           We added 'width: 100%' to ensure content spans the full screen.
        */}
        <div style={{
          position: 'relative',
          zIndex: 1,
          width: '100%',
          height: '100%',
          paddingTop: '70px',
        }}>
          <AppRoutes />
        </div>

      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;