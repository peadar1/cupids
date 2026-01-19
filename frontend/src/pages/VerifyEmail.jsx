import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Heart, CheckCircle, XCircle, Loader } from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

export default function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');

  const [status, setStatus] = useState('verifying'); // verifying, success, error
  const [message, setMessage] = useState('');
  const [participantName, setParticipantName] = useState('');
  const [eventId, setEventId] = useState(null);

  useEffect(() => {
    if (!token) {
      setStatus('error');
      setMessage('Invalid verification link');
      return;
    }

    verifyEmail();
  }, [token]);

  const verifyEmail = async () => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/events/participants/verify/${token}`
      );

      setStatus('success');
      setMessage(response.data.message);
      setParticipantName(response.data.participant_name);
      setEventId(response.data.event_id);
    } catch (err) {
      setStatus('error');
      setMessage(
        err.response?.data?.detail ||
        'Failed to verify email. The link may be invalid or expired.'
      );
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-red-50 to-orange-50 flex items-center justify-center p-4">
      {/* Floating hearts background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {[...Array(15)].map((_, i) => (
          <Heart
            key={i}
            className="absolute text-pink-200 animate-float"
            size={Math.random() * 30 + 20}
            fill="currentColor"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              animationDuration: `${Math.random() * 10 + 10}s`,
            }}
          />
        ))}
      </div>

      <div className="relative bg-white rounded-3xl shadow-2xl p-8 md:p-12 max-w-md w-full border-2 border-pink-100 animate-slideUp">
        <div className="text-center">
          {/* Logo */}
          <div className="flex items-center justify-center gap-3 mb-8">
            <Heart className="text-pink-500" size={40} fill="currentColor" />
            <h1 className="text-3xl font-bold bg-gradient-to-r from-pink-600 to-red-500 bg-clip-text text-transparent">
              Cupid's Matcher
            </h1>
          </div>

          {/* Status Icon */}
          <div className="mb-6">
            {status === 'verifying' && (
              <div className="bg-blue-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto">
                <Loader className="text-blue-600 animate-spin" size={40} />
              </div>
            )}

            {status === 'success' && (
              <div className="bg-green-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto animate-bounce">
                <CheckCircle className="text-green-600" size={40} />
              </div>
            )}

            {status === 'error' && (
              <div className="bg-red-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto animate-shake">
                <XCircle className="text-red-600" size={40} />
              </div>
            )}
          </div>

          {/* Message */}
          <div className="mb-8">
            {status === 'verifying' && (
              <>
                <h2 className="text-2xl font-bold text-gray-800 mb-2">
                  Verifying Email...
                </h2>
                <p className="text-gray-600">
                  Please wait while we verify your email address.
                </p>
              </>
            )}

            {status === 'success' && (
              <>
                <h2 className="text-2xl font-bold text-green-600 mb-2">
                  Email Verified! 🎉
                </h2>
                <p className="text-gray-700 mb-4">
                  {participantName && `Welcome, ${participantName}! `}
                  Your email has been successfully verified.
                </p>
                <div className="bg-green-50 border-2 border-green-200 rounded-xl p-4">
                  <p className="text-sm text-green-800">
                    ✓ You're all set! We'll send you updates about the event.
                  </p>
                </div>
              </>
            )}

            {status === 'error' && (
              <>
                <h2 className="text-2xl font-bold text-red-600 mb-2">
                  Verification Failed
                </h2>
                <p className="text-gray-700 mb-4">{message}</p>
                <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4">
                  <p className="text-sm text-red-800">
                    The verification link may have expired or is invalid.
                  </p>
                </div>
              </>
            )}
          </div>

          {/* Action Buttons */}
          {status === 'success' && eventId && (
            <button
              onClick={() => navigate(`/events/${eventId}/register`)}
              className="w-full bg-gradient-to-r from-pink-500 to-red-500 hover:from-pink-600 hover:to-red-600 text-white font-bold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all"
            >
              View Event Details
            </button>
          )}

          {status === 'error' && (
            <button
              onClick={() => navigate('/')}
              className="w-full bg-gradient-to-r from-pink-500 to-red-500 hover:from-pink-600 hover:to-red-600 text-white font-bold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all"
            >
              Go to Homepage
            </button>
          )}
        </div>
      </div>

      <style>{`
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-10px); }
          75% { transform: translateX(10px); }
        }

        @keyframes float {
          0%, 100% {
            transform: translateY(0) rotate(0deg);
            opacity: 0.3;
          }
          50% {
            transform: translateY(-100px) rotate(180deg);
            opacity: 0.6;
          }
        }

        .animate-slideUp {
          animation: slideUp 0.6s ease-out;
        }

        .animate-shake {
          animation: shake 0.5s ease-in-out;
        }

        .animate-float {
          animation: float linear infinite;
        }
      `}</style>
    </div>
  );
}
