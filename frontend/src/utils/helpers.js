// Shared utility functions for the application

/**
 * Get Tailwind CSS classes for event status badges
 */
export function getEventStatusColor(status) {
  switch (status) {
    case 'setup':
      return 'bg-yellow-100 text-yellow-700 border-yellow-200';
    case 'registration_open':
      return 'bg-green-100 text-green-700 border-green-200';
    case 'matching_in_progress':
      return 'bg-blue-100 text-blue-700 border-blue-200';
    case 'completed':
      return 'bg-gray-100 text-gray-700 border-gray-200';
    case 'cancelled':
      return 'bg-red-100 text-red-700 border-red-200';
    default:
      return 'bg-gray-100 text-gray-700 border-gray-200';
  }
}

/**
 * Get Tailwind CSS classes for participant status badges
 */
export function getParticipantStatusColor(status) {
  switch (status) {
    case 'registered':
      return 'bg-green-100 text-green-700 border-green-200';
    case 'matched':
      return 'bg-blue-100 text-blue-700 border-blue-200';
    case 'withdrawn':
      return 'bg-red-100 text-red-700 border-red-200';
    case 'waitlisted':
      return 'bg-yellow-100 text-yellow-700 border-yellow-200';
    default:
      return 'bg-gray-100 text-gray-700 border-gray-200';
  }
}

/**
 * Get Tailwind CSS classes for match status badges
 */
export function getMatchStatusColor(status) {
  switch (status) {
    case 'pending':
      return 'bg-yellow-100 text-yellow-700 border-yellow-200';
    case 'approved':
      return 'bg-green-100 text-green-700 border-green-200';
    case 'notified':
      return 'bg-blue-100 text-blue-700 border-blue-200';
    case 'confirmed':
      return 'bg-purple-100 text-purple-700 border-purple-200';
    default:
      return 'bg-gray-100 text-gray-700 border-gray-200';
  }
}

/**
 * Format a date string into a readable format
 */
export function formatDate(dateString, options = {}) {
  if (!dateString) return 'N/A';

  const defaultOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    ...options
  };

  return new Date(dateString).toLocaleDateString('en-US', defaultOptions);
}

/**
 * Calculate age from date of birth
 */
export function calculateAge(dateOfBirth) {
  if (!dateOfBirth) return null;
  const today = new Date();
  const birthDate = new Date(dateOfBirth);
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDiff = today.getMonth() - birthDate.getMonth();
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  return age;
}
