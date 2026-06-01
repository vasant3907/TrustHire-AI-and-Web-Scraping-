import React, { useEffect, useMemo, useState } from 'react';
import { Navbar } from '../components/Navbar';
import apiService from '../services/apiService';

const parseJson = (value, fallback) => {
  try {
    return value ? JSON.parse(value) : fallback;
  } catch {
    return fallback;
  }
};

export const Dashboard = () => {
  const [reports, setReports] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const [reportsResult, alertsResult] = await Promise.allSettled([
          apiService.getMyReports(),
          apiService.getMyAlerts(),
        ]);

        const loadedReports = reportsResult.status === 'fulfilled' ? reportsResult.value.data : [];
        setReports(loadedReports);

        if (alertsResult.status === 'fulfilled') {
          setAlerts(alertsResult.value.data);
        } else {
          setAlerts(
            loadedReports
              .filter((report) => ['high', 'critical'].includes(report.risk_level))
              .map((report) => ({
                id: `report-${report.id}`,
                report_id: report.id,
                message: `${report.risk_level?.toUpperCase()} risk report created with ${Math.round(report.scam_probability || 0)}% scam probability.`,
                admin_handled: false,
              }))
          );
        }
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, []);

  const metrics = useMemo(() => {
    const total = reports.length;
    const highRisk = reports.filter((report) => ['high', 'critical'].includes(report.risk_level)).length;
    const avgTrust = total ? Math.round(reports.reduce((sum, report) => sum + report.trust_score, 0) / total) : 0;
    const avgScam = total ? Math.round(reports.reduce((sum, report) => sum + (report.scam_probability || 0), 0) / total) : 0;
    return { total, highRisk, avgTrust, avgScam };
  }, [reports]);

  return (
    <div>
      <Navbar />
      <main className="min-h-screen bg-slate-50">
        <div className="container mx-auto px-6 py-8">
          <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-wide text-blue-700">TrustHire Intelligence</p>
              <h2 className="text-3xl font-bold text-slate-950">Dashboard</h2>
              <p className="mt-2 text-slate-600">AI scam detection, public review intelligence, and company verification signals.</p>
            </div>
            <a href="/analyze" className="rounded-md bg-blue-700 px-5 py-3 text-sm font-semibold text-white hover:bg-blue-800">
              New Analysis
            </a>
          </div>

          <section className="grid gap-4 md:grid-cols-4">
            <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Total Analyses</p>
              <p className="mt-2 text-3xl font-bold text-slate-950">{metrics.total}</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Average Trust</p>
              <p className="mt-2 text-3xl font-bold text-blue-700">{metrics.avgTrust}%</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Average Scam Probability</p>
              <p className="mt-2 text-3xl font-bold text-red-700">{metrics.avgScam}%</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">High/Critical</p>
              <p className="mt-2 text-3xl font-bold text-orange-700">{metrics.highRisk}</p>
            </div>
          </section>

          <section className="mt-8 rounded-lg border border-amber-200 bg-amber-50 p-6 shadow-sm">
            <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
              <div>
                <h3 className="text-xl font-semibold text-amber-950">Critical alerts from your reports</h3>
                <p className="mt-1 text-sm text-amber-800">High and critical risk analyses appear here. Admin review status updates automatically after moderation.</p>
              </div>
              <span className="rounded-full bg-white px-3 py-1 text-sm font-semibold text-amber-800">
                {alerts.filter((alert) => !alert.admin_handled).length} pending review
              </span>
            </div>

            <div className="mt-4 space-y-3">
              {alerts.slice(0, 4).map((alert) => (
                <div key={alert.id} className="rounded-md border border-amber-200 bg-white p-4 text-sm">
                  <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                    <p className="font-semibold text-slate-950">Report #{alert.report_id}</p>
                    <span className={alert.admin_handled ? 'font-semibold text-emerald-700' : 'font-semibold text-amber-700'}>
                      {alert.admin_handled ? 'Admin reviewed' : 'Admin review pending'}
                    </span>
                  </div>
                  <p className="mt-2 text-slate-700">{alert.message}</p>
                  <a href={`/analysis/${alert.report_id}`} className="mt-3 inline-flex text-sm font-semibold text-blue-700 hover:underline">
                    Open flagged report -&gt;
                  </a>
                </div>
              ))}
              {!alerts.length && <p className="text-sm text-amber-800">No critical alerts yet.</p>}
            </div>
          </section>

          <section className="mt-8">
            <div className="mb-4 flex items-center justify-between">
              <h3 className="text-xl font-semibold text-slate-950">Recent intelligence reports</h3>
              <a href="/reports" className="text-sm font-semibold text-blue-700 hover:underline">View all</a>
            </div>

            {loading ? (
              <p>Loading...</p>
            ) : reports.length === 0 ? (
              <div className="rounded-lg border border-blue-200 bg-blue-50 p-8 text-center">
                <p className="text-slate-700">No jobs analyzed yet.</p>
                <a href="/analyze" className="mt-4 inline-flex rounded-md bg-blue-700 px-4 py-2 text-white">
                  Analyze Your First Job
                </a>
              </div>
            ) : (
              <div className="grid gap-5 lg:grid-cols-2">
                {reports.slice(0, 6).map((report) => {
                  const intelligence = parseJson(report.company_intelligence, {});
                  return (
                    <div key={report.id} className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <p className="text-sm text-slate-500">Report #{report.id}</p>
                          <h4 className="text-lg font-semibold capitalize text-slate-950">{report.risk_level} risk opportunity</h4>
                        </div>
                        <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-semibold text-slate-700">
                          {Math.round(report.trust_score)}% trust
                        </span>
                      </div>
                      <p className="mt-3 line-clamp-2 text-sm text-slate-600">{report.ai_summary}</p>
                      <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
                        <div className="rounded-md bg-slate-50 p-3">
                          <p className="text-slate-500">Scam Probability</p>
                          <p className="font-semibold text-red-700">{Math.round(report.scam_probability || 0)}%</p>
                        </div>
                        <div className="rounded-md bg-slate-50 p-3">
                          <p className="text-slate-500">Public Reviews</p>
                          <p className="font-semibold text-slate-900">{(intelligence.reviews || []).length} links</p>
                        </div>
                        <div className="rounded-md bg-slate-50 p-3">
                          <p className="text-slate-500">Company Site</p>
                          <p className="truncate font-semibold text-slate-900">{intelligence.website ? 'Found' : 'Not found'}</p>
                        </div>
                        <div className="rounded-md bg-slate-50 p-3">
                          <p className="text-slate-500">LinkedIn/Naukri</p>
                          <p className="font-semibold text-slate-900">{intelligence.linkedin_url || intelligence.naukri_url ? 'Signals found' : 'No signal'}</p>
                        </div>
                      </div>
                      <a href={`/analysis/${report.id}`} className="mt-4 inline-flex text-sm font-semibold text-blue-700 hover:underline">
                        Open analysis -&gt;
                      </a>
                    </div>
                  );
                })}
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
