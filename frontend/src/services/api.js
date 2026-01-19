import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API calls
export const authAPI = {
  signup: (data) => api.post('/api/auth/signup', data),
  login: (data) => api.post('/api/auth/login', data),
};

// Event API calls
export const eventAPI = {
  // Protected routes (require auth)
  getAll: () => api.get('/api/events'),
  getById: (id) => api.get(`/api/events/${id}`),
  create: (data) => api.post('/api/events', data),
  update: (id, data) => api.put(`/api/events/${id}`, data),
  delete: (id) => api.delete(`/api/events/${id}`),
  
  // Public route (no auth required) - for participant registration
  getPublic: (id) => api.get(`/api/events/${id}/public`),
};

// Venue API calls
export const venueAPI = {
  getAll: (eventId) => api.get(`/api/events/${eventId}/venues`),
  getById: (eventId, venueId) => api.get(`/api/events/${eventId}/venues/${venueId}`),
  create: (eventId, data) => api.post(`/api/events/${eventId}/venues`, data),
  update: (eventId, venueId, data) => api.put(`/api/events/${eventId}/venues/${venueId}`, data),
  delete: (eventId, venueId) => api.delete(`/api/events/${eventId}/venues/${venueId}`),
};

// Participant API calls
export const participantAPI = {
  // Public registration (no auth required)
  register: (eventId, data) => api.post(`/api/events/${eventId}/participants/register`, data),
  
  // Protected routes (for event organizers)
  getAll: (eventId) => api.get(`/api/events/${eventId}/participants`),
  getById: (eventId, participantId) => api.get(`/api/events/${eventId}/participants/${participantId}`),
  update: (eventId, participantId, data) => api.put(`/api/events/${eventId}/participants/${participantId}`, data),
  delete: (eventId, participantId) => api.delete(`/api/events/${eventId}/participants/${participantId}`),
};

// Form Question API calls
export const formQuestionAPI = {
  getAll: (eventId) => api.get(`/api/events/${eventId}/form-questions`),
  getById: (eventId, questionId) => api.get(`/api/events/${eventId}/form-questions/${questionId}`),
  create: (eventId, data) => api.post(`/api/events/${eventId}/form-questions`, data),
  update: (eventId, questionId, data) => api.put(`/api/events/${eventId}/form-questions/${questionId}`, data),
  delete: (eventId, questionId) => api.delete(`/api/events/${eventId}/form-questions/${questionId}`),
  reorder: (eventId, data) => api.put(`/api/events/${eventId}/form-questions/reorder`, data),
  
  // Public route - get active questions for registration form
  getPublic: (eventId) => api.get(`/api/events/${eventId}/form-questions/public`),
};

// Match API calls (for future use)
export const matchAPI = {
  getAll: (eventId) => api.get(`/api/events/${eventId}/matches`),
  generate: (eventId) => api.post(`/api/events/${eventId}/matches/generate`),
  getById: (eventId, matchId) => api.get(`/api/events/${eventId}/matches/${matchId}`),
  update: (eventId, matchId, data) => api.put(`/api/events/${eventId}/matches/${matchId}`, data),
};

// Venue API calls
export const venueAPI = {
  getAll: (eventId) => api.get(`/api/events/${eventId}/venues`),
  getById: (eventId, venueId) => api.get(`/api/events/${eventId}/venues/${venueId}`),
  create: (eventId, data) => api.post(`/api/events/${eventId}/venues`, data),
  update: (eventId, venueId, data) => api.put(`/api/events/${eventId}/venues/${venueId}`, data),
  delete: (eventId, venueId) => api.delete(`/api/events/${eventId}/venues/${venueId}`),
};

// Export the axios instance for direct use if needed
export default api;
