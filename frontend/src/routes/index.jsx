import { createBrowserRouter } from 'react-router-dom';
import App from '../App';
import Login from '../pages/Login';
import Register from '../pages/Register';
import Chat from '../pages/Chat';
import Conversations from '../pages/Conversations';
import Memory from '../pages/Memory';
import Tools from '../pages/Tools';
import Voice from '../pages/Voice';
import Settings from '../pages/Settings';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Conversations /> },
      { path: 'conversations', element: <Conversations /> },
      { path: 'chat', element: <Chat /> },
      { path: 'chat/:id', element: <Chat /> },
      { path: 'memory', element: <Memory /> },
      { path: 'tools', element: <Tools /> },
      { path: 'voice', element: <Voice /> },
      { path: 'settings', element: <Settings /> },
    ],
  },
  { path: '/login', element: <Login /> },
  { path: '/register', element: <Register /> },
]);

export default router;
