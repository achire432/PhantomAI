import { createBrowserRouter } from 'react-router-dom';
import App from '../App';
import Login from '../pages/Login';
import Register from '../pages/Register';
import Conversations from '../pages/Conversations';
import Chat from '../pages/Chat';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Conversations /> },
      { path: 'conversations', element: <Conversations /> },
      { path: 'chat', element: <Chat /> },
      { path: 'chat/:id', element: <Chat /> },
    ],
  },
  { path: '/login', element: <Login /> },
  { path: '/register', element: <Register /> },
]);

export default router;
