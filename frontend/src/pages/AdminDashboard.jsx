import React, { useCallback, useEffect, useState } from 'react';
import { Navbar } from '../components/Navbar';
import apiService from '../services/apiService';

export const AdminDashboard = () => {
  const [summary, setSummary] = useState(null);
  const [reports, setReports] = useState([]);
  const [users, setUsers] = useState([]);
  const [communityReports, setCommunityReports] = useState([]);
  const [watchlist, setWatchlist] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [error, setError] = useState('');

  const loadAdminData = useCallback(async () => {
    try {
      const [summaryRes, reportsRes, usersRes, communityRes, watchlistRes, alertsRes] = await Promise.all([
        apiService.getAdminSummary(),
        apiService.getAdminReports(),
        apiService.getAdminUsers(),
        apiService.getAdminCommunityReports(),
        apiService.getAdminWatchlist(),
        apiService.getAdminAlerts(),
      ]);
      setSummary(summaryRes.data);
      setReports(reportsRes.data);
      setUsers(usersRes.data);
      setCommunityReports(communityRes.data);
      setWatchlist(watchlistRes.data);
      setAlerts(alertsRes.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Admin data failed to load. Sign in with an email listed in ADMIN_EMAILS.');
    }
  }, []);

  useEffect(() => {
    Promise.resolve().then(loadAdminData);
  }, [loadAdminData]);

  const updateCommunityStatus = async (reportId, status) => {
    await apiService.updateCommunityReportStatus(reportId, { status });
    await loadAdminData();
  };

  const markAlertHandled = async (alertId) => {
    await apiService.markAdminAlertHandled(alertId);
    await loadAdminData();
  };

  const riskCounts = summary?.risk_counts || {};
  const maxRisk = Math.max(1, ...Object.values(riskCounts));

  return (
    <div>
      <Navbar />
      <main className="min-h-screen bg-slate-50">
        <div className="container mx-auto px-6 py-8">
          <h2 className="text-3xl font-bold text-slate-950">Admin Dashboard</h2>
          <p className="mt-2 text-slate-600">Admin-only monitoring for users, high-risk reports, community evidence, watchlist entries, and alert delivery.</p>

          {error && <div className="mt-6 rounded-md bg-red-100 p-4 text-red-700">{error}</div>}

          {summary && (
            <>
              <section className="mt-6 grid gap-4 md:grid-cols-4">
                {[
                  ['Users', summary.users],
                  ['Reports', summary.reports],
                  ['Community Reports', summary.community_reports],
                  ['Watchlist Entries', summary.watchlist_entries],
                  ['Alerts', summary.alerts],
                ].map(([label, value]) => (
                  <div key={label} className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
                    <p className="text-sm text-slate-500">{label}</p>
                    <p className="mt-2 text-3xl font-bold text-slate-950">{value}</p>
                  </div>
                ))}
              </section>

              <section className="mt-6 grid gap-6 lg:grid-cols-2">
                <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="font-semibold text-slate-950">Risk Distribution</h3>
                  <div className="mt-4 space-y-3">
                    {['low', 'medium', 'high', 'critical'].map((risk) => (
                      <div key={risk}>
                        <div className="flex justify-between text-sm capitalize text-slate-600">
                          <span>{risk}</span><span>{riskCounts[risk] || 0}</span>
                        </div>
                        <div className="mt-1 h-3 rounded-full bg-slate-100">
                          <div className="h-3 rounded-full bg-blue-700" style={{ width: `${((riskCounts[risk] || 0) / maxRisk) * 100}%` }} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="font-semibold text-slate-950">Top Suspicious Keywords</h3>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {(summary.top_keywords || []).map(([keyword, count]) => (
                      <span key={keyword} className="rounded-full bg-red-50 px-3 py-1 text-sm font-medium text-red-700">
                        {keyword} ({count})
                      </span>
                    ))}
                  </div>
                </div>
              </section>

              <section className="mt-6 grid gap-6 lg:grid-cols-2">
                <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-slate-950">Critical Alert Review Queue</h3>
                    <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-700">
                      {alerts.filter((alert) => !alert.sent).length} needs review
                    </span>
                  </div>
                  <div className="mt-4 space-y-3">
                    {alerts.slice(0, 6).map((alert) => (
                      <div key={alert.id} className="rounded-md bg-slate-50 p-3 text-sm">
                        <div className="flex justify-between gap-3">
                          <span className="font-medium text-slate-900">Report #{alert.report_id}</span>
                          <span className={alert.sent ? 'text-emerald-700' : 'text-amber-700'}>
                            {alert.sent ? 'reviewed' : 'pending review'}
                          </span>
                        </div>
                        <p className="mt-1 line-clamp-2 text-slate-600">{alert.message}</p>
                        {!alert.sent && (
                          <button
                            type="button"
                            onClick={() => markAlertHandled(alert.id)}
                            className="mt-3 rounded-md bg-slate-900 px-3 py-1.5 text-xs font-semibold text-white hover:bg-slate-700"
                          >
                            Mark reviewed
                          </button>
                        )}
                      </div>
                    ))}
                    {!alerts.length && <p className="text-sm text-slate-500">No critical alerts yet.</p>}
                  </div>
                </div>

                <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="font-semibold text-slate-950">Recent Reports</h3>
                  <div className="mt-4 space-y-3">
                    {reports.slice(0, 8).map((report) => (
                      <div key={report.id} className="flex justify-between rounded-md bg-slate-50 p-3 text-sm">
                        <span>#{report.id} {report.risk_level}</span>
                        <span>{Math.round(report.scam_probability || 0)}% scam</span>
                      </div>
                    ))}
                    {!reports.length && <p className="text-sm text-slate-500">No job analyses yet.</p>}
                  </div>
                </div>
              </section>

              <section className="mt-6 grid gap-6 lg:grid-cols-2">
                <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="font-semibold text-slate-950">Community Scam Reports</h3>
                  <div className="mt-4 space-y-3">
                    {communityReports.slice(0, 6).map((report) => (
                      <div key={report.id} className="rounded-md bg-slate-50 p-3 text-sm">
                        <div className="flex justify-between gap-3">
                          <span className="font-medium text-slate-900">{report.company_name}</span>
                          <span className="capitalize text-slate-500">{report.status}</span>
                        </div>
                        <p className="text-slate-600">{report.recruiter_email || report.platform || 'Public report'}</p>
                        <p className="mt-1 line-clamp-2 text-slate-500">{report.description}</p>
                        <div className="mt-3 flex flex-wrap gap-2">
                          <button type="button" onClick={() => updateCommunityStatus(report.id, 'reviewing')} className="rounded-md border border-slate-300 px-3 py-1.5 text-xs font-semibold text-slate-700">Reviewing</button>
                          <button type="button" onClick={() => updateCommunityStatus(report.id, 'verified')} className="rounded-md bg-emerald-700 px-3 py-1.5 text-xs font-semibold text-white">Verify</button>
                          <button type="button" onClick={() => updateCommunityStatus(report.id, 'rejected')} className="rounded-md bg-red-700 px-3 py-1.5 text-xs font-semibold text-white">Reject</button>
                        </div>
                      </div>
                    ))}
                    {!communityReports.length && <p className="text-sm text-slate-500">No community reports submitted yet.</p>}
                  </div>
                </div>

                <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                  <h3 className="font-semibold text-slate-950">Company Watchlist</h3>
                  <div className="mt-4 space-y-3">
                    {watchlist.slice(0, 6).map((entry) => (
                      <div key={entry.id} className="rounded-md bg-slate-50 p-3 text-sm">
                        <div className="flex justify-between gap-3">
                          <span className="font-medium text-slate-900">{entry.company_name}</span>
                          <span className="capitalize text-red-700">{entry.severity}</span>
                        </div>
                        <p className="text-slate-600">{entry.recruiter_email || 'Company-level watch'}</p>
                        <p className="mt-1 line-clamp-2 text-slate-500">{entry.reason}</p>
                      </div>
                    ))}
                    {!watchlist.length && <p className="text-sm text-slate-500">No watchlist entries yet.</p>}
                  </div>
                </div>
              </section>

              <section className="mt-6 rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <h3 className="font-semibold text-slate-950">Recent Users</h3>
                <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
                  {users.slice(0, 9).map((user) => (
                    <div key={user.id} className="rounded-md bg-slate-50 p-3 text-sm">
                      <p className="font-medium text-slate-900">{user.name}</p>
                      <p className="text-slate-600">{user.email}</p>
                    </div>
                  ))}
                  {!users.length && <p className="text-sm text-slate-500">No users found.</p>}
                  </div>
              </section>
            </>
          )}
        </div>
      </main>
    </div>
  );
};

export default AdminDashboard;
