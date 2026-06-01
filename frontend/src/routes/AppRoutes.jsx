import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from '../context/AuthContext';
import ProtectedRoute from './ProtectedRoute';

// Pages
import Login from '../pages/Login';
import Register from '../pages/Register';
import Dashboard from '../pages/Dashboard';
import AnalyzeJob from '../pages/AnalyzeJob';
import Reports from '../pages/Reports';
import AnalysisResult from '../pages/AnalysisResult';
import AdminDashboard from '../pages/AdminDashboard';
import Community from '../pages/Community';
import Profile from '../pages/Profile';

export const AppRoutes = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute userOnly>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/analyze"
            element={
              <ProtectedRoute userOnly>
                <AnalyzeJob />
              </ProtectedRoute>
            }
          />
          <Route
            path="/reports"
            element={
              <ProtectedRoute userOnly>
                <Reports />
              </ProtectedRoute>
            }
          />
          <Route
            path="/report/:reportId"
            element={
              <ProtectedRoute userOnly>
                <AnalysisResult />
              </ProtectedRoute>
            }
          />
          <Route
            path="/analysis/:reportId"
            element={
              <ProtectedRoute userOnly>
                <AnalysisResult />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />
          <Route
            path="/community"
            element={
              <ProtectedRoute>
                <Community />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin"
            element={
              <ProtectedRoute adminOnly>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default AppRoutes;
