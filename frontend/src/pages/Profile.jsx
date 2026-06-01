import React, { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import AuthContext from '../context/AuthContext';
import apiService from '../services/apiService';

export const Profile = () => {
  const { user, updateSession, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [profileForm, setProfileForm] = useState({
    name: user?.name || '',
    email: user?.email || '',
  });
  const [passwordForm, setPasswordForm] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  });
  const [editingProfile, setEditingProfile] = useState(false);
  const [changingPassword, setChangingPassword] = useState(false);
  const [savingProfile, setSavingProfile] = useState(false);
  const [savingPassword, setSavingPassword] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const saveProfile = async (event) => {
    event.preventDefault();
    setSavingProfile(true);
    setMessage('');
    setError('');

    try {
      const response = await apiService.updateProfile(profileForm);
      const { access_token, user_id, name, email, is_admin } = response.data;
      updateSession({ id: user_id, name, email, is_admin }, access_token);
      setEditingProfile(false);
      setMessage('Profile updated successfully.');
    } catch (err) {
      setError(err.response?.data?.detail || 'Profile update failed');
    } finally {
      setSavingProfile(false);
    }
  };

  const savePassword = async (event) => {
    event.preventDefault();
    setSavingPassword(true);
    setMessage('');
    setError('');

    if (passwordForm.new_password !== passwordForm.confirm_password) {
      setError('New password and confirmation do not match.');
      setSavingPassword(false);
      return;
    }

    try {
      await apiService.changePassword({
        current_password: passwordForm.current_password,
        new_password: passwordForm.new_password,
      });
      setPasswordForm({ current_password: '', new_password: '', confirm_password: '' });
      setChangingPassword(false);
      setMessage('Password changed successfully.');
    } catch (err) {
      setError(err.response?.data?.detail || 'Password change failed');
    } finally {
      setSavingPassword(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />

      <main className="container mx-auto px-6 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-slate-950">My Profile</h2>
          <p className="mt-2 text-slate-600">Manage your account information and password.</p>
        </div>

        {message && <div className="mb-6 rounded-md bg-emerald-50 p-4 text-emerald-700">{message}</div>}
        {error && <div className="mb-6 rounded-md bg-red-50 p-4 text-red-700">{error}</div>}

        <section className="mx-auto max-w-5xl overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
          <div className="h-32 bg-gradient-to-r from-blue-700 via-slate-900 to-emerald-700" />

          <div className="px-6 pb-8">
            <div className="-mt-14 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
              <div className="flex items-end gap-4">
                <img
                  src={`https://ui-avatars.com/api/?name=${encodeURIComponent(user?.name || 'User')}&background=ffffff&color=2563eb&size=160`}
                  alt="Profile"
                  className="h-28 w-28 rounded-full border-4 border-white shadow-lg"
                />
                <div className="pb-2">
                  <h3 className="text-2xl font-bold text-slate-950">{user?.name}</h3>
                  <p className="break-all text-slate-600">{user?.email}</p>
                  <span className="mt-2 inline-flex rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
                    {user?.is_admin ? 'Admin account' : 'User account'}
                  </span>
                </div>
              </div>

              <button
                onClick={handleLogout}
                className="rounded-md bg-red-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-red-700"
              >
                Logout
              </button>
            </div>

            <div className="mt-8 grid gap-6 lg:grid-cols-2">
              <form onSubmit={saveProfile} className="rounded-lg border border-slate-200 p-5">
                <div className="flex items-center justify-between">
                  <h4 className="text-lg font-semibold text-slate-950">Profile Details</h4>
                  <button
                    type="button"
                    onClick={() => setEditingProfile((value) => !value)}
                    className="rounded-md border border-slate-300 px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                  >
                    {editingProfile ? 'Cancel' : 'Edit Profile'}
                  </button>
                </div>

                <div className="mt-5 space-y-4">
                  <label className="block">
                    <span className="text-sm font-medium text-slate-600">Full Name</span>
                    <input
                      value={profileForm.name}
                      onChange={(event) => setProfileForm({ ...profileForm, name: event.target.value })}
                      disabled={!editingProfile}
                      className="mt-2 w-full rounded-md border border-slate-300 px-4 py-2 disabled:bg-slate-50"
                      required
                    />
                  </label>

                  <label className="block">
                    <span className="text-sm font-medium text-slate-600">Email Address</span>
                    <input
                      type="email"
                      value={profileForm.email}
                      onChange={(event) => setProfileForm({ ...profileForm, email: event.target.value })}
                      disabled={!editingProfile}
                      className="mt-2 w-full rounded-md border border-slate-300 px-4 py-2 disabled:bg-slate-50"
                      required
                    />
                  </label>
                </div>

                {editingProfile && (
                  <button
                    type="submit"
                    disabled={savingProfile}
                    className="mt-5 rounded-md bg-blue-700 px-5 py-2.5 text-sm font-semibold text-white hover:bg-blue-800 disabled:opacity-60"
                  >
                    {savingProfile ? 'Saving...' : 'Save Profile'}
                  </button>
                )}
              </form>

              <form onSubmit={savePassword} className="rounded-lg border border-slate-200 p-5">
                <div className="flex items-center justify-between">
                  <h4 className="text-lg font-semibold text-slate-950">Password</h4>
                  <button
                    type="button"
                    onClick={() => setChangingPassword((value) => !value)}
                    className="rounded-md border border-slate-300 px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                  >
                    {changingPassword ? 'Cancel' : 'Change Password'}
                  </button>
                </div>

                {changingPassword ? (
                  <div className="mt-5 space-y-4">
                    <input
                      type="password"
                      placeholder="Current password"
                      value={passwordForm.current_password}
                      onChange={(event) => setPasswordForm({ ...passwordForm, current_password: event.target.value })}
                      className="w-full rounded-md border border-slate-300 px-4 py-2"
                      autoComplete="current-password"
                      required
                    />
                    <input
                      type="password"
                      placeholder="New password"
                      value={passwordForm.new_password}
                      onChange={(event) => setPasswordForm({ ...passwordForm, new_password: event.target.value })}
                      className="w-full rounded-md border border-slate-300 px-4 py-2"
                      autoComplete="new-password"
                      minLength={8}
                      required
                    />
                    <input
                      type="password"
                      placeholder="Confirm new password"
                      value={passwordForm.confirm_password}
                      onChange={(event) => setPasswordForm({ ...passwordForm, confirm_password: event.target.value })}
                      className="w-full rounded-md border border-slate-300 px-4 py-2"
                      autoComplete="new-password"
                      minLength={8}
                      required
                    />
                    <button
                      type="submit"
                      disabled={savingPassword}
                      className="rounded-md bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white hover:bg-slate-800 disabled:opacity-60"
                    >
                      {savingPassword ? 'Updating...' : 'Update Password'}
                    </button>
                  </div>
                ) : (
                  <p className="mt-5 rounded-md bg-slate-50 p-4 text-sm text-slate-600">
                    Change your password by entering your current password and a new password of at least 8 characters.
                  </p>
                )}
              </form>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Profile;
