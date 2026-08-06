import api from './client';

export const auth = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (full_name, email, password) => api.post('/auth/register', { full_name, email, password }),
};

export const chat = {
  conversations: () => api.get('/conversations/'),
  createConversation: (title) => api.post('/conversations/', { title }),
  getConversation: (id) => api.get(`/conversations/${id}`),
  sendMessage: (id, message) => api.post(`/chat/${id}/send`, { role: 'user', content: message }),
};
