import axios from 'axios';

// ============================================================
// AXIOS CLIENT
// ============================================================

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    Accept: 'application/json',
  },
});

// ============================================================
// AUTH TOKEN INTERCEPTOR
// ============================================================

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// ============================================================
// AUTHENTICATION
// ============================================================

export const auth = {
  login: (email, password) =>
    api.post(
      '/auth/login',
      new URLSearchParams({
        username: email,
        password,
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    ),

  register: (full_name, email, password) =>
    api.post('/auth/register', {
      full_name,
      email,
      password,
    }),

  me: () =>
    api.get('/auth/me'),
};

// ============================================================
// CHAT / CONVERSATIONS
// ============================================================

export const chat = {
  conversations: () =>
    api.get('/conversations/'),

  createConversation: (title) =>
    api.post('/conversations/', {
      title,
    }),

  getConversation: (id) =>
    api.get(`/conversations/${id}`),

  getMessages: (id) =>
    api.get(`/conversations/${id}/messages`),

  sendMessage: (id, message) =>
    api.post(`/chat/${id}/send`, {
      role: 'user',
      content: message,
    }),
};

// ============================================================
// MEMORY
// ============================================================

export const memory = {
  getAll: () =>
    api.get('/memory/'),

  create: (data) =>
    api.post('/memory/', data),

  delete: (key) =>
    api.delete(`/memory/${encodeURIComponent(key)}`),

  search: (query) =>
    api.get(
      `/memory/search/${encodeURIComponent(query)}`
    ),

  forAI: () =>
    api.get('/memory/for-ai'),
};

// ============================================================
// GENERAL TOOLS
// ============================================================

export const tools = {
  // ----------------------------------------------------------
  // NOTES
  // ----------------------------------------------------------

  notes: {
    getAll: () =>
      api.get('/notes/'),

    get: (id) =>
      api.get(`/notes/${id}`),

    create: (data) =>
      api.post('/notes/', data),

    update: (id, data) =>
      api.put(`/notes/${id}`, data),

    delete: (id) =>
      api.delete(`/notes/${id}`),
  },

  // ----------------------------------------------------------
  // TASKS
  // ----------------------------------------------------------

  tasks: {
    getAll: () =>
      api.get('/tasks/'),

    get: (id) =>
      api.get(`/tasks/${id}`),

    create: (data) =>
      api.post('/tasks/', data),

    update: (id, data) =>
      api.put(`/tasks/${id}`, data),

    delete: (id) =>
      api.delete(`/tasks/${id}`),
  },

  // ----------------------------------------------------------
  // WEATHER
  // ----------------------------------------------------------

  weather: (city) =>
    api.get(
      `/weather/${encodeURIComponent(city)}`
    ),

  // ----------------------------------------------------------
  // CALENDAR
  // ----------------------------------------------------------

  calendar: {
    getAll: () =>
      api.get('/calendar/'),

    get: (id) =>
      api.get(`/calendar/${id}`),

    create: (data) =>
      api.post('/calendar/', data),

    update: (id, data) =>
      api.put(`/calendar/${id}`, data),

    delete: (id) =>
      api.delete(`/calendar/${id}`),
  },

  // ----------------------------------------------------------
  // REMINDERS
  // ----------------------------------------------------------

  reminders: {
    getAll: () =>
      api.get('/reminders/'),

    get: (id) =>
      api.get(`/reminders/${id}`),

    create: (data) =>
      api.post('/reminders/', data),

    update: (id, data) =>
      api.put(`/reminders/${id}`, data),

    delete: (id) =>
      api.delete(`/reminders/${id}`),

    complete: (id) =>
      api.post(`/reminders/${id}/complete`),
  },

  // ----------------------------------------------------------
  // SYSTEM
  // ----------------------------------------------------------

  system: {
    info: () =>
      api.get('/system/info'),
  },

  // ----------------------------------------------------------
  // GIT
  // ----------------------------------------------------------

  git: {
    status: () =>
      api.get('/git/status'),

    log: () =>
      api.get('/git/log'),

    branches: () =>
      api.get('/git/branches'),

    branch: () =>
      api.get('/git/branch'),

    diff: () =>
      api.get('/git/diff'),

    remote: () =>
      api.get('/git/remote'),
  },

  // ----------------------------------------------------------
  // FILES
  // ----------------------------------------------------------

  files: {
    list: () =>
      api.get('/files/list'),

    info: (path) =>
      api.get('/files/info', {
        params: {
          path,
        },
      }),

    search: (query) =>
      api.get('/files/search', {
        params: {
          query,
        },
      }),

    size: (path) =>
      api.get('/files/size', {
        params: {
          path,
        },
      }),
  },

  // ----------------------------------------------------------
  // DATABASE
  // ----------------------------------------------------------

  database: {
    tables: () =>
      api.get('/database/tables'),

    table: (tableName) =>
      api.get(
        `/database/table/${encodeURIComponent(tableName)}`
      ),

    query: (query) =>
      api.post('/database/query', {
        query,
      }),
  },

  // ----------------------------------------------------------
  // NOTIFICATIONS
  // ----------------------------------------------------------

  notifications: {
    getAll: () =>
      api.get('/notifications/'),

    check: () =>
      api.get('/notifications/check'),

    markRead: (id) =>
      api.post(`/notifications/${id}/read`),
  },
};

// ============================================================
// IMAGE GENERATION
// ============================================================

export const images = {
  generate: (
    prompt,
    provider = 'stability',
    aspectRatio = '1:1'
  ) =>
    api.post('/images/generate', {
      prompt,
      provider,
      aspect_ratio: aspectRatio,
    }),

  providers: () =>
    api.get('/images/providers'),
};

// ============================================================
// VIDEO GENERATION
// ============================================================

export const video = {

  // ----------------------------------------------------------
  // TEXT → VIDEO
  // ----------------------------------------------------------

  text: (
    text,
    duration = 5
  ) =>
    api.post(
      '/video/text',
      {
        text,
        duration,
      },
      {
        responseType: 'blob',
      }
    ),

  // ----------------------------------------------------------
  // IMAGES → SLIDESHOW VIDEO
  // ----------------------------------------------------------

  slideshow: (
    images,
    duration_per_image = 3
  ) =>
    api.post(
      '/video/slideshow',
      {
        images,
        duration_per_image,
      },
      {
        responseType: 'blob',
      }
    ),

};

// ============================================================
// VOICE
// ============================================================

export const voice = {
  speak: (text) =>
    api.post(
      '/voice/speak',
      {
        text,
      },
      {
        responseType: 'blob',
      }
    ),

  listen: () =>
    api.post('/voice/listen'),

  chat: (message) =>
    api.post('/voice/chat', {
      message,
    }),

  wakeStart: () =>
    api.get('/voice/wake/start'),

  wakeStop: () =>
    api.get('/voice/wake/stop'),

  wakeStatus: () =>
    api.get('/voice/wake/status'),
};

// ============================================================
// SETTINGS
// ============================================================

export const settings = {
  // ----------------------------------------------------------
  // GENERAL SETTINGS
  // ----------------------------------------------------------

  get: () =>
    api.get('/settings/'),

  update: (data) =>
    api.put('/settings/', data),

  reset: () =>
    api.post('/settings/reset'),

  // ----------------------------------------------------------
  // TOOL PERMISSIONS
  // ----------------------------------------------------------

  tools: {
    // Get all permissions
    getAll: () =>
      api.get('/settings/tools'),

    // Change one tool
    update: (
      toolName,
      permission
    ) =>
      api.put(
        `/settings/tool/${encodeURIComponent(toolName)}`,
        null,
        {
          params: {
            permission,
          },
        }
      ),

    // Change every tool
    updateAll: (
      permission
    ) =>
      api.put(
        '/settings/tools/all',
        null,
        {
          params: {
            permission,
          },
        }
      ),

    // Reset permissions
    reset: () =>
      api.post('/settings/tools/reset'),
  },

  // ----------------------------------------------------------
  // INDIVIDUAL TOOL PERMISSION
  // ----------------------------------------------------------

  getToolPermission: (
    toolName
  ) =>
    api.get(
      `/settings/tool/${encodeURIComponent(toolName)}`
    ),

  setToolPermission: (
    toolName,
    permission
  ) =>
    api.put(
      `/settings/tool/${encodeURIComponent(toolName)}`,
      null,
      {
        params: {
          permission,
        },
      }
    ),

  // ----------------------------------------------------------
  // ACTIVE MODEL
  // ----------------------------------------------------------

  getActiveModel: () =>
    api.get('/settings/active-model'),
};

// ============================================================
// UPLOADS
// ============================================================

export const upload = {
  file: (formData) =>
    api.post(
      '/upload/file',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    ),
};

// ============================================================
// PDF
// ============================================================

export const pdf = {
  conversation: (conversationId) =>
    api.get(
      `/pdf/conversation/${conversationId}`,
      {
        responseType: 'blob',
      }
    ),

  notes: () =>
    api.get('/pdf/notes', {
      responseType: 'blob',
    }),

  tasks: () =>
    api.get('/pdf/tasks', {
      responseType: 'blob',
    }),
};

// ============================================================
// MODELS
// ============================================================

export const models = {
  getAll: () =>
    api.get('/models/'),

  available: () =>
    api.get('/models/available'),

  active: () =>
    api.get('/models/active'),

  activate: (modelName) =>
    api.post(
      `/models/activate/${encodeURIComponent(modelName)}`
    ),

  status: () =>
    api.get('/models/status'),
};

// ============================================================
// APPLICATIONS
// ============================================================

export const apps = {
  list: () =>
    api.get('/apps/list'),

  launch: (appName) =>
    api.post('/apps/launch', {
      app_name: appName,
    }),
};

// ============================================================
// TERMINAL
// ============================================================

export const terminal = {
  commands: () =>
    api.get('/terminal/commands'),

  run: (command) =>
    api.post('/terminal/run', {
      command,
    }),
};

// ============================================================
// CODE
// ============================================================

export const code = {
  analyze: (codeContent) =>
    api.post('/code/analyze', {
      code: codeContent,
    }),

  function: (codeContent) =>
    api.get('/code/function', {
      params: {
        code: codeContent,
      },
    }),
};

// ============================================================
// API KEYS
// ============================================================

export const apiKeys = {
  status: () =>
    api.get('/api-keys/status'),
};

// ============================================================
// DATA
// ============================================================

export const data = {
  export: () =>
    api.get('/data/export'),

  import: (payload) =>
    api.post('/data/import', payload),
};

// ============================================================
// PROACTIVE
// ============================================================

export const proactive = {
  check: () =>
    api.get('/proactive/check'),

  alerts: () =>
    api.get('/proactive/alerts'),

  clear: () =>
    api.post('/proactive/clear'),
};

// ============================================================
// CONTEXT
// ============================================================

export const context = {
  get: () =>
    api.get('/context/'),

  update: (data) =>
    api.put('/context/', data),

  summary: () =>
    api.get('/context/summary'),
};

// ============================================================
// MARKDOWN
// ============================================================

export const markdown = {
  render: (file) =>
    api.post('/markdown/', {
      file,
    }),
};

// ============================================================
// OCR
// ============================================================

export const ocr = {
  process: (file) => {
    const formData = new FormData();

    formData.append('file', file);

    return api.post(
      '/ocr/',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
  },
};

// ============================================================
// EMAIL
// ============================================================

export const email = {
  recent: () =>
    api.get('/email/recent'),

  summarize: (emailId) =>
    api.get(
      `/email/${emailId}/summarize`
    ),

  draft: (data) =>
    api.post('/email/draft', data),

  send: (data) =>
    api.post('/email/send', data),

  drafts: () =>
    api.get('/email/drafts'),
};

// ============================================================
// DEFAULT AXIOS CLIENT
// ============================================================

export default api;