import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { eventAPI } from '../services/api';
import { Heart, LogOut, Calendar, FileText, ArrowLeft, Sparkles } from 'lucide-react';

export default function CreateEvent() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    event_date: '',
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await eventAPI.create(formData);
      navigate(`/events/${response.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create event');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-red-50 to-orange-50">
      {/* Header */}
      <header className="bg-white border-b-2 border-pink-100 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6">
              <div className="flex items-center gap-3 cursor-pointer" onClick={() => navigate('/dashboard')}>
                <Heart className="text-pink-500" size={32} fill="currentColor" />
                <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-600 to-red-500 bg-clip-text text-transparent">
                  Cupid's Matcher
                </h1>
              </div>
              
              <nav className="flex gap-4">
                <button
                  onClick={() => navigate('/dashboard')}
                  className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
                >
                  Dashboard
                </button>
                <button
                  onClick={() => navigate('/events')}
                  className="text-pink-600 font-semibold"
                >
                  Events
                </button>
              </nav>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm text-gray-500">Welcome back,</p>
                <p className="font-semibold text-gray-800">{user?.name}</p>
              </div>
              <button
                onClick={logout}
                className="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
              >
                <LogOut size={18} />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Back Button */}
        <button
          onClick={() => navigate('/events')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6 font-medium transition-colors"
        >
          <ArrowLeft size={20} />
          Back to Events
        </button>

        {/* Page Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-3">
            <div className="bg-gradient-to-br from-pink-400 to-red-400 p-3 rounded-2xl">
              <Sparkles className="text-white" size={28} />
            </div>
            <h2 className="text-4xl font-bold text-gray-800">Create New Event</h2>
          </div>
          <p className="text-gray-600">Set up your cupid matching event in just a few steps</p>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-3xl shadow-xl p-8 border-2 border-pink-100">
          {error && (
            <div className="bg-red-50 border-2 border-red-200 text-red-700 px-4 py-3 rounded-xl mb-6">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Event Name */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">
                Event Name *
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all"
                placeholder="Valentine's Day 2026"
                required
              />
            </div>

            {/* Event Date */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">
                Event Date *
              </label>
              <div className="relative">
                <Calendar className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="date"
                  name="event_date"
                  value={formData.event_date}
                  onChange={handleChange}
                  className="w-full pl-12 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all"
                  required
                />
              </div>
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">
                Description (Optional)
              </label>
              <div className="relative">
                <FileText className="absolute left-4 top-4 text-gray-400" size={20} />
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  rows={4}
                  className="w-full pl-12 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-pink-400 focus:ring-4 focus:ring-pink-100 outline-none transition-all resize-none"
                  placeholder="Tell participants about your event..."
                />
              </div>
            </div>

            {/* Info Box */}
            <div className="bg-pink-50 border-2 border-pink-200 rounded-xl p-4">
              <p className="text-sm text-pink-800">
                💡 <strong>Next steps:</strong> After creating your event, you'll be able to customize the registration form, add venues, and configure matching preferences.
              </p>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-pink-500 to-red-500 hover:from-pink-600 hover:to-red-600 text-white font-bold py-4 px-6 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Creating Event...
                </>
              ) : (
                <>
                  <Sparkles size={20} />
                  Create Event
                </>
              )}
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}