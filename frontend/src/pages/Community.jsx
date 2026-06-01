import React, { useEffect, useState } from 'react';
import { Navbar } from '../components/Navbar';
import apiService from '../services/apiService';

export const Community = () => {
  const [reports, setReports] = useState([]);
  const [watchlist, setWatchlist] = useState([]);
  const [message, setMessage] = useState('');
  const [form, setForm] = useState({ company_name: '', recruiter_email: '', platform: '', description: '', evidence_url: '' });
  const [verification, setVerification] = useState(null);

  const load = async () => {
    const [reportsRes, watchlistRes] = await Promise.all([apiService.getCommunityReports(), apiService.getWatchlist()]);
    setReports(reportsRes.data);
    setWatchlist(watchlistRes.data);
  };

  useEffect(() => {
    Promise.resolve().then(load);
  }, []);

  const submitReport = async (event) => {
    event.preventDefault();
    await apiService.createCommunityReport(form);
    await apiService.addWatchlistEntry({
      company_name: form.company_name,
      recruiter_email: form.recruiter_email,
      reason: form.description,
      severity: 'high',
    });
    setMessage('Community scam report submitted and added to watchlist.');
    setForm({ company_name: '', recruiter_email: '', platform: '', description: '', evidence_url: '' });
    load();
  };

  const verifyEmail = async () => {
    const response = await apiService.verifyEmail({ email: form.recruiter_email, company_name: form.company_name });
    setVerification(response.data);
  };

  return (
    <div>
      <Navbar />
      <main className="min-h-screen bg-slate-50">
        <div className="container mx-auto px-6 py-8">
          <h2 className="text-3xl font-bold text-slate-950">Community Scam Reporting</h2>
          <p className="mt-2 text-slate-600">Report fake recruiters, verify email domains, and build a shared watchlist.</p>

          <form onSubmit={submitReport} className="mt-6 grid gap-4 rounded-lg border border-slate-200 bg-white p-6 shadow-sm lg:grid-cols-2">
            <input className="rounded-md border border-slate-300 px-4 py-2" placeholder="Company name" value={form.company_name} onChange={(e) => setForm({ ...form, company_name: e.target.value })} required />
            <div className="flex gap-2">
              <input className="w-full rounded-md border border-slate-300 px-4 py-2" placeholder="Recruiter email" value={form.recruiter_email} onChange={(e) => setForm({ ...form, recruiter_email: e.target.value })} />
              <button type="button" onClick={verifyEmail} className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white">Verify</button>
            </div>
            <input className="rounded-md border border-slate-300 px-4 py-2" placeholder="Platform: LinkedIn, Naukri, WhatsApp..." value={form.platform} onChange={(e) => setForm({ ...form, platform: e.target.value })} />
            <input className="rounded-md border border-slate-300 px-4 py-2" placeholder="Evidence URL" value={form.evidence_url} onChange={(e) => setForm({ ...form, evidence_url: e.target.value })} />
            <textarea className="rounded-md border border-slate-300 px-4 py-2 lg:col-span-2" placeholder="Describe the scam signals" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} required />
            <button className="rounded-md bg-blue-700 px-4 py-2 font-semibold text-white">Submit Report</button>
          </form>

          {verification && <div className="mt-4 rounded-md bg-blue-50 p-4 text-blue-900">Email check: {verification.status} - {verification.reason}</div>}
          {message && <div className="mt-4 rounded-md bg-emerald-100 p-4 text-emerald-800">{message}</div>}

          <section className="mt-8 grid gap-6 lg:grid-cols-2">
            <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="font-semibold text-slate-950">Recent Community Reports</h3>
              <div className="mt-4 space-y-3">
                {reports.map((report) => (
                  <div key={report.id} className="rounded-md bg-slate-50 p-3 text-sm">
                    <div className="flex items-center justify-between gap-3">
                      <p className="font-medium">{report.company_name}</p>
                      <span className="rounded-full bg-blue-50 px-2.5 py-1 text-xs font-semibold capitalize text-blue-700">
                        {report.status}
                      </span>
                    </div>
                    <p className="text-slate-600">{report.platform || 'Unknown platform'} | {report.recruiter_email || 'No email'}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="font-semibold text-slate-950">Company Watchlist</h3>
              <div className="mt-4 space-y-3">
                {watchlist.map((entry) => (
                  <div key={entry.id} className="rounded-md bg-red-50 p-3 text-sm">
                    <p className="font-medium text-red-900">{entry.company_name} ({entry.severity})</p>
                    <p className="text-red-700">{entry.reason}</p>
                  </div>
                ))}
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
};

export default Community;
