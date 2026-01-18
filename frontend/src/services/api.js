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
  getAll: () => api.get('/api/events'),
  getById: (id) => api.get(`/api/events/${id}`),
  create: (data) => api.post('/api/events', data),
  update: (id, data) => api.put(`/api/events/${id}`, data),
  delete: (id) => api.delete(`/api/events/${id}`),
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