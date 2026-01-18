import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { venueAPI, eventAPI } from "../services/api";
import {
  Heart,
  LogOut,
  ArrowLeft,
  Plus,
  MapPin,
  Users,
  Edit2,
  Trash2,
  Save,
  X,
  AlertCircle,
} from "lucide-react";

export default function Venues() {
  const { eventId } = useParams();
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [event, setEvent] = useState(null);
  const [venues, setVenues] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingId, setEditingId] = useState(null);

  const [formData, setFormData] = useState({
    name: "",
    address: "",
    total_capacity: "",
    min_age: "18",
  });

  useEffect(() => {
    fetchEventAndVenues();
  }, [eventId]);

  const fetchEventAndVenues = async () => {
    try {
      const [eventRes, venuesRes] = await Promise.all([
        eventAPI.getById(eventId),
        venueAPI.getAll(eventId),
      ]);
      setEvent(eventRes.data);
      setVenues(venuesRes.data);
      setLoading(false);
    } catch (err) {
      setError("Failed to load venues");
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      name: "",
      address: "",
      total_capacity: "",
      min_age: "18",
    });
    setShowAddForm(false);
    setEditingId(null);
    setError("");
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleAdd = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await venueAPI.create(eventId, {
        ...formData,
        total_capacity: parseInt(formData.total_capacity),
        min_age: parseInt(formData.min_age),
      });
      fetchEventAndVenues();
      resetForm();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create venue");
    }
  };

  const handleEdit = (venue) => {
    setEditingId(venue.id);
    setFormData({
      name: venue.name,
      address: venue.address || "",
      total_capacity: venue.total_capacity.toString(),
      min_age: venue.min_age.toString(),
    });
    setShowAddForm(false);
  };

  const handleUpdate = async (venueId) => {
    setError("");

    try {
      await venueAPI.update(eventId, venueId, {
        ...formData,
        total_capacity: parseInt(formData.total_capacity),
        min_age: parseInt(formData.min_age),
      });
      fetchEventAndVenues();
      resetForm();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to update venue");
    }
  };

  const handleDelete = async (venueId) => {
    if (window.confirm("Are you sure you want to delete this venue?")) {
      try {
        await venueAPI.delete(eventId, venueId);
        fetchEventAndVenues();
      } catch (err) {
        setError("Failed to delete venue");
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-50 via-red-50 to-orange-50">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-pink-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Loading venues...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-red-50 to-orange-50">
      {/* Header */}
      <header className="bg-white border-b-2 border-pink-100 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6">
              <div
                className="flex items-center gap-3 cursor-pointer"
                onClick={() => navigate("/dashboard")}
              >
                <Heart
                  className="text-pink-500"
                  size={32}
                  fill="currentColor"
                />
                <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-600 to-red-500 bg-clip-text text-transparent">
                  Cupid's Matcher
                </h1>
              </div>

              <nav className="flex gap-4">
                <button
                  onClick={() => navigate("/dashboard")}
                  className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
                >
                  Dashboard
                </button>
                <button
                  onClick={() => navigate("/events")}
                  className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
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
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Back Button & Header */}
        <button
          onClick={() => navigate(`/events/${eventId}`)}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6 font-medium transition-colors"
        >
          <ArrowLeft size={20} />
          Back to Event
        </button>

        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-4xl font-bold text-gray-800 mb-2">Venues</h2>
            <p className="text-gray-600">{event?.name}</p>
          </div>

          <button
            onClick={() => {
              setEditingId(null);
              setFormData({
                name: "",
                address: "",
                total_capacity: "",
                min_age: "18",
              });
              setError("");
              setShowAddForm(true);
            }}
            className="cursor-pointer flex items-center gap-2 bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white font-bold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all"
          >
            <Plus size={20} />
            Add Venue
          </button>
        </div>

        {error && (
          <div className="bg-red-50 border-2 border-red-200 text-red-700 px-6 py-4 rounded-xl mb-6 flex items-center gap-3">
            <AlertCircle size={20} />
            {error}
          </div>
        )}

        {/* Add/Edit Form */}
        {(showAddForm || editingId) && (
          <div className="bg-white rounded-3xl shadow-xl p-8 mb-8 border-2 border-purple-100">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">
              {editingId ? "Edit Venue" : "Add New Venue"}
            </h3>

            <form
              onSubmit={
                editingId
                  ? (e) => {
                      e.preventDefault();
                      handleUpdate(editingId);
                    }
                  : handleAdd
              }
              className="space-y-5"
            >
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                {/* Venue Name */}
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Venue Name *
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:ring-4 focus:ring-purple-100 outline-none transition-all"
                    placeholder="The Library Bar"
                    required
                  />
                </div>

                {/* Address */}
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Address
                  </label>
                  <input
                    type="text"
                    name="address"
                    value={formData.address}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:ring-4 focus:ring-purple-100 outline-none transition-all"
                    placeholder="123 Main St, Dublin"
                  />
                </div>

                {/* Capacity */}
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Total Capacity *
                  </label>
                  <input
                    type="number"
                    name="total_capacity"
                    value={formData.total_capacity}
                    onChange={handleChange}
                    min="1"
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:ring-4 focus:ring-purple-100 outline-none transition-all"
                    placeholder="50"
                    required
                  />
                </div>

                {/* Minimum Age */}
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Minimum Age *
                  </label>
                  <select
                    name="min_age"
                    value={formData.min_age}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:ring-4 focus:ring-purple-100 outline-none transition-all"
                    required
                  >
                    <option value="18">18+</option>
                    <option value="21">21+</option>
                  </select>
                </div>
              </div>

              {/* Info Box */}
              <div className="bg-purple-50 border-2 border-purple-200 rounded-xl p-4">
                <p className="text-sm text-purple-800">
                  💡 <strong>Tip:</strong> Available slots will automatically be
                  set to match total capacity. You can adjust this later as
                  matches are assigned.
                </p>
              </div>

              {/* Buttons */}
              <div className="flex gap-3">
                <button
                  type="submit"
                  className="flex items-center gap-2 bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white font-bold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all"
                >
                  <Save size={20} />
                  {editingId ? "Update Venue" : "Add Venue"}
                </button>

                <button
                  type="button"
                  onClick={resetForm}
                  className="flex items-center gap-2 bg-gray-500 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all"
                >
                  <X size={20} />
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Venues List */}
        {venues.length === 0 ? (
          <div className="bg-white rounded-3xl shadow-xl p-12 text-center border-2 border-purple-100">
            <div className="bg-gradient-to-br from-purple-100 to-indigo-100 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6">
              <MapPin className="text-purple-600" size={48} />
            </div>
            <h3 className="text-2xl font-bold text-gray-800 mb-3">
              No venues yet
            </h3>
            <p className="text-gray-600 mb-6 max-w-md mx-auto">
              Add pubs and locations where participants can meet for their dates
            </p>
            <button
              onClick={() => {
                setShowAddForm(true);
                resetForm();
              }}
              className="inline-flex items-center gap-2 bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white font-bold py-3 px-8 rounded-xl shadow-lg hover:shadow-xl transition-all"
            >
              <Plus size={20} />
              Add Your First Venue
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {venues.map((venue) => (
              <div
                key={venue.id}
                className="bg-white rounded-2xl shadow-lg p-6 border-2 border-purple-100 hover:shadow-xl transition-shadow"
              >
                {editingId === venue.id ? (
                  // Editing mode - show inline
                  <div className="text-sm text-gray-500">Editing above...</div>
                ) : (
                  <>
                    {/* Venue Header */}
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-gray-800 mb-2">
                          {venue.name}
                        </h3>
                        {venue.address && (
                          <div className="flex items-start gap-2 text-gray-600 text-sm mb-3">
                            <MapPin
                              size={16}
                              className="text-purple-500 mt-0.5 flex-shrink-0"
                            />
                            <span>{venue.address}</span>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Stats */}
                    <div className="space-y-2 mb-4">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-600 flex items-center gap-2">
                          <Users size={16} className="text-purple-500" />
                          Capacity
                        </span>
                        <span className="font-semibold text-gray-800">
                          {venue.available_slots} / {venue.total_capacity}
                        </span>
                      </div>

                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-600">Min Age</span>
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            venue.min_age === 21
                              ? "bg-orange-100 text-orange-700"
                              : "bg-green-100 text-green-700"
                          }`}
                        >
                          {venue.min_age}+
                        </span>
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2 pt-4 border-t-2 border-gray-100">
                      <button
                        onClick={() => handleEdit(venue)}
                        className="flex-1 flex items-center justify-center gap-2 bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg transition-colors text-sm font-semibold"
                      >
                        <Edit2 size={16} />
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(venue.id)}
                        className="flex-1 flex items-center justify-center gap-2 bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-lg transition-colors text-sm font-semibold"
                      >
                        <Trash2 size={16} />
                        Delete
                      </button>
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
