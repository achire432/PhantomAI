
import api from './client';

// Authentication
export const auth = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (full_name, email, password) => api.post('/auth/register', { full_name, email, password }),
};

// Settings
export const settings = {
  get: () => api.get('/settings/'),
  update: (data) => api.put('/settings/', data),
};

// Chat
export const chat = {
  conversations: () => api.get('/conversations/'),
  createConversation: (title) => api.post('/conversations/', { title }),
  sendMessage: (id, message) => api.post(`/chat/${id}/send`, { role: 'user', content: message }),
};

// System
export const system = {
  info: () => api.get('/system/info'),
};

// Tools
export const tools = {
  notes: {
    getAll: () => api.get('/notes/'),
    create: (data) => api.post('/notes/', data),
    delete: (id) => api.delete(`/notes/${id}`),
  },
  tasks: {
    getAll: () => api.get('/tasks/'),
    create: (data) => api.post('/tasks/', data),
    delete: (id) => api.delete(`/tasks/${id}`),
  },
  weather: (city) => api.get(`/weather/${city}`),
};

// Memory
export const memory = {
  getAll: () => api.get('/memory/'),
  create: (data) => api.post('/memory/', data),
};

// Voice
export const voice = {
  speak: (text) => api.post('/voice/speak', { text }),
  listen: () => api.post('/voice/listen'),
  chat: () => api.post('/voice/chat'),
};

// Video
export const video = {
  generate: (data) => api.post('/video/generate', data),
  getStatus: (id) => api.get(`/video/status/${id}`),
  download: (id) => api.get(`/video/download/${id}`, { responseType: 'blob' }),
};