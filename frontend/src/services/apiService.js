import axiosInstance from '../api/axios';

const apiService = {
  // Auth endpoints
  register: (name, email, password) =>
    axiosInstance.post('/auth/register', { name, email, password }),
  
  login: (email, password) =>
    axiosInstance.post('/auth/login', { email, password }),

  updateProfile: (payload) =>
    axiosInstance.put('/auth/me', payload),

  changePassword: (payload) =>
    axiosInstance.post('/auth/change-password', payload),

  forgotPassword: (payload) =>
    axiosInstance.post('/auth/forgot-password', payload),

  resetPassword: (payload) =>
    axiosInstance.post('/auth/reset-password', payload),

  // Job endpoints
  createJob: (jobData) =>
    axiosInstance.post('/jobs/', jobData),
  
  getJob: (jobId) =>
    axiosInstance.get(`/jobs/${jobId}`),
  
  getMyJobs: () =>
    axiosInstance.get('/jobs/my-jobs'),

  // Company endpoints
  getCompany: (companyId) =>
    axiosInstance.get(`/companies/${companyId}`),
  
  searchCompany: (companyName) =>
    axiosInstance.get(`/companies/search/${companyName}`),

  // Report endpoints
  getReport: (reportId) =>
    axiosInstance.get(`/reports/${reportId}`),

  getMyReports: (riskLevel = '') =>
    axiosInstance.get(`/reports/my-reports${riskLevel ? `?risk_level=${riskLevel}` : ''}`),
  
  analyzeJob: (jobId) =>
    axiosInstance.post(`/reports/analyze/${jobId}`),

  analyzeUpload: (formData) =>
    axiosInstance.post('/reports/analyze-upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),

  downloadReport: (reportId) =>
    axiosInstance.get(`/reports/download/${reportId}`, { responseType: 'blob' }),

  downloadReportPdf: (reportId) =>
    axiosInstance.get(`/reports/pdf/${reportId}`, { responseType: 'blob' }),

  saveReportNote: (reportId, payload) =>
    axiosInstance.post(`/reports/${reportId}/notes`, payload),

  getReportNote: (reportId) =>
    axiosInstance.get(`/reports/${reportId}/notes`),

  getReportTimeline: (reportId) =>
    axiosInstance.get(`/reports/${reportId}/timeline`),

  createCommunityReport: (payload) =>
    axiosInstance.post('/features/community-reports', payload),

  getCommunityReports: () =>
    axiosInstance.get('/features/community-reports'),

  verifyEmail: (payload) =>
    axiosInstance.post('/features/verify-email', payload),

  addWatchlistEntry: (payload) =>
    axiosInstance.post('/features/watchlist', payload),

  getWatchlist: () =>
    axiosInstance.get('/features/watchlist'),

  getMyAlerts: () =>
    axiosInstance.get('/features/alerts'),

  getAdminSummary: () =>
    axiosInstance.get('/admin/summary'),

  getAdminReports: () =>
    axiosInstance.get('/admin/reports'),

  getAdminUsers: () =>
    axiosInstance.get('/admin/users'),

  getAdminCommunityReports: () =>
    axiosInstance.get('/admin/community-reports'),

  getAdminWatchlist: () =>
    axiosInstance.get('/admin/watchlist'),

  getAdminAlerts: () =>
    axiosInstance.get('/admin/alerts'),

  updateCommunityReportStatus: (reportId, payload) =>
    axiosInstance.patch(`/admin/community-reports/${reportId}/status`, payload),

  markAdminAlertHandled: (alertId) =>
    axiosInstance.patch(`/admin/alerts/${alertId}/handled`),
};

export default apiService;
