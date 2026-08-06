import api from './client';

/*
|--------------------------------------------------------------------------
| AUTHENTICATION
|--------------------------------------------------------------------------
*/

export const auth = {
  login: (email, password) =>
    api.post('/auth/login', {
      email,
      password,
    }),

  register: (full_name, email, password) =>
    api.post('/auth/register', {
      full_name,
      email,
      password,
    }),
};


/*
|--------------------------------------------------------------------------
| CHAT / CONVERSATIONS
|--------------------------------------------------------------------------
*/

export const chat = {
  // Get all conversations belonging to the logged-in user
  conversations: () =>
    api.get('/conversations/'),

  // Create a new conversation
  createConversation: (title) =>
    api.post('/conversations/', {
      title,
    }),

  // Get one conversation
  getConversation: (id) =>
    api.get(`/conversations/${id}`),

  // Get messages belonging to a conversation
  getMessages: (id) =>
    api.get(`/conversations/${id}/messages`),

  // Send a message
  sendMessage: (id, message) =>
    api.post(`/conversations/${id}/messages`, {
      role: 'user',
      content: message,
    }),
};


/*
|--------------------------------------------------------------------------
| MEMORY
|--------------------------------------------------------------------------
|
| IMPORTANT:
| These URLs must match your FastAPI memory router.
| If your backend uses different URLs, we will change them after
| checking the backend router.
|
*/

export const memory = {
  getAll: () =>
    api.get('/memory/'),

  create: (data) =>
    api.post('/memory/', data),

  delete: (key) =>
    api.delete(`/memory/${encodeURIComponent(key)}`),
};


/*
|--------------------------------------------------------------------------
| TOOLS
|--------------------------------------------------------------------------
*/

export const tools = {

  notes: {
    getAll: () =>
      api.get('/tools/notes/'),
  },

  tasks: {
    getAll: () =>
      api.get('/tools/tasks/'),
  },

  weather: (city) =>
    api.get('/tools/weather/', {
      params: {
        city,
      },
    }),
};


/*
|--------------------------------------------------------------------------
| VOICE
|--------------------------------------------------------------------------
*/

export const voice = {

  listen: () =>
    api.post('/voice/listen'),

  chat: () =>
    api.post('/voice/chat'),

  wakeStart: () =>
    api.post('/voice/wake/start'),

  wakeStop: () =>
    api.post('/voice/wake/stop'),
};


/*
|--------------------------------------------------------------------------
| SETTINGS
|--------------------------------------------------------------------------
*/

export const settings = {

  get: () =>
    api.get('/settings/'),

  update: (data) =>
    api.put('/settings/', data),

  reset: () =>
    api.post('/settings/reset'),
};