import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';

export const ProtectedRoute = ({ children, adminOnly = false, userOnly = false }) => {
  const { user, token, loading } = useContext(AuthContext);

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (adminOnly && !user?.is_admin) {
    return <Navigate to="/dashboard" replace />;
  }

  if (userOnly && user?.is_admin) {
    return <Navigate to="/admin" replace />;
  }

  return children;
};

export default ProtectedRoute;
