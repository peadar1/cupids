import { useAuth } from '../context/AuthContext';
import { Heart, LogOut, Calendar, Users, Sparkles } from 'lucide-react';

export default function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-red-50 to-orange-50">
      {/* Header */}
      <header className="bg-white border-b-2 border-pink-100 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Heart className="text-pink-500" size={32} fill="currentColor" />
              <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-600 to-red-500 bg-clip-text text-transparent">
                Cupid's Matcher
              </h1>
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
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Welcome Card */}
        <div className="bg-white rounded-3xl shadow-xl p-8 mb-8 border-2 border-pink-100 animate-slideUp">
          <div className="flex items-center gap-4 mb-6">
            <div className="bg-gradient-to-br from-pink-400 to-red-400 p-4 rounded-2xl">
              <Sparkles className="text-white" size={32} />
            </div>
            <div>
              <h2 className="text-3xl font-bold text-gray-800">Welcome, {user?.name}! 👋</h2>
              <p className="text-gray-600 mt-1">Ready to create some magical matches?</p>
            </div>
          </div>
          
          <div className="bg-gradient-to-r from-pink-50 to-red-50 rounded-2xl p-6 border-2 border-pink-200">
            <p className="text-gray-700 text-lg">
              🎉 You're all set! Your matcher account is active and ready to go.
            </p>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-2xl shadow-lg p-6 border-2 border-purple-100 hover:shadow-xl transition-shadow animate-slideUp" style={{animationDelay: '0.1s'}}>
            <div className="flex items-center gap-4">
              <div className="bg-purple-100 p-3 rounded-xl">
                <Calendar className="text-purple-600" size={28} />
              </div>
              <div>
                <p className="text-gray-500 text-sm">Events Created</p>
                <p className="text-3xl font-bold text-gray-800">0</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6 border-2 border-blue-100 hover:shadow-xl transition-shadow animate-slideUp" style={{animationDelay: '0.2s'}}>
            <div className="flex items-center gap-4">
              <div className="bg-blue-100 p-3 rounded-xl">
                <Users className="text-blue-600" size={28} />
              </div>
              <div>
                <p className="text-gray-500 text-sm">Total Participants</p>
                <p className="text-3xl font-bold text-gray-800">0</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6 border-2 border-pink-100 hover:shadow-xl transition-shadow animate-slideUp" style={{animationDelay: '0.3s'}}>
            <div className="flex items-center gap-4">
              <div className="bg-pink-100 p-3 rounded-xl">
                <Heart className="text-pink-600" size={28} fill="currentColor" />
              </div>
              <div>
                <p className="text-gray-500 text-sm">Matches Made</p>
                <p className="text-3xl font-bold text-gray-800">0</p>
              </div>
            </div>
          </div>
        </div>

        {/* Coming Soon Section */}
        <div className="bg-white rounded-3xl shadow-xl p-8 border-2 border-pink-100 animate-slideUp" style={{animationDelay: '0.4s'}}>
          <h3 className="text-2xl font-bold text-gray-800 mb-4">🚀 Coming Soon</h3>
          <div className="space-y-3">
            <div className="flex items-center gap-3 text-gray-700">
              <div className="w-2 h-2 bg-pink-500 rounded-full"></div>
              <span>Create and manage cupid events</span>
            </div>
            <div className="flex items-center gap-3 text-gray-700">
              <div className="w-2 h-2 bg-pink-500 rounded-full"></div>
              <span>Customize registration forms</span>
            </div>
            <div className="flex items-center gap-3 text-gray-700">
              <div className="w-2 h-2 bg-pink-500 rounded-full"></div>
              <span>Smart matching algorithm</span>
            </div>
            <div className="flex items-center gap-3 text-gray-700">
              <div className="w-2 h-2 bg-pink-500 rounded-full"></div>
              <span>Venue management</span>
            </div>
            <div className="flex items-center gap-3 text-gray-700">
              <div className="w-2 h-2 bg-pink-500 rounded-full"></div>
              <span>Participant notifications</span>
            </div>
          </div>
        </div>
      </main>

      <style>{`
        @keyframes slideUp {
          from { opacity: 0; transform: translateY(30px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-slideUp {
          animation: slideUp 0.6s ease-out;
          animation-fill-mode: both;
        }
      `}</style>
    </div>
  );
}