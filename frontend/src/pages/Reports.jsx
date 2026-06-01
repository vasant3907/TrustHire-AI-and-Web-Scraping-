import React, { useEffect, useMemo, useState } from 'react';
import { Navbar } from '../components/Navbar';
import apiService from '../services/apiService';

export const Reports = () => {
  const [reports, setReports] = useState([]);
  const [riskFilter, setRiskFilter] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchReports = async () => {
      setLoading(true);
      try {
        const response = await apiService.getMyReports(riskFilter);
        setReports(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load reports');
      } finally {
        setLoading(false);
      }
    };
    fetchReports();
  }, [riskFilter]);

  const averageTrust = useMemo(() => {
    if (!reports.length) return 0;
    return Math.round(reports.reduce((sum, report) => sum + report.trust_score, 0) / reports.length);
  }, [reports]);

  const handlePdfDownload = async (reportId) => {
    const response = await apiService.downloadReportPdf(reportId);
    const url = URL.createObjectURL(response.data);
    const link = document.createElement('a');
    link.href = url;
    link.download = `trusthire-report-${reportId}.pdf`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      <Navbar />
      <main className="min-h-screen bg-slate-50">
        <div className="container mx-auto px-6 py-8">
          <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-wide text-blue-700">Report Management</p>
              <h2 className="text-3xl font-bold text-slate-950">Analysis history</h2>
              <p className="mt-2 text-slate-600">Filter previous reports, reopen analysis, and download polished PDF reports.</p>
            </div>
            <select
              value={riskFilter}
              onChange={(e) => setRiskFilter(e.target.value)}
              className="rounded-md border border-slate-300 bg-white px-4 py-2"
            >
              <option value="">All risk levels</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>

          <section className="mb-6 grid gap-4 md:grid-cols-3">
            <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Total Reports</p>
              <p className="mt-2 text-3xl font-bold text-slate-950">{reports.length}</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Average Trust</p>
              <p className="mt-2 text-3xl font-bold text-blue-700">{averageTrust}%</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">High/Critical</p>
              <p className="mt-2 text-3xl font-bold text-red-700">{reports.filter((r) => ['high', 'critical'].includes(r.risk_level)).length}</p>
            </div>
          </section>

          {loading && <p>Loading reports...</p>}
          {error && <div className="rounded-md bg-red-100 p-4 text-red-700">{error}</div>}

          <div className="space-y-4">
            {reports.map((report) => (
              <div key={report.id} className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                  <div>
                    <p className="text-sm text-slate-500">Report #{report.id}</p>
                    <h3 className="text-xl font-semibold capitalize text-slate-950">{report.risk_level} risk</h3>
                    <p className="mt-1 max-w-3xl text-sm text-slate-600">{report.ai_summary}</p>
                  </div>
                  <div className="flex gap-3">
                    <a href={`/analysis/${report.id}`} className="rounded-md bg-blue-700 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-800">
                      Open
                    </a>
                    <button
                      type="button"
                      onClick={() => handlePdfDownload(report.id)}
                      className="rounded-md border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
                    >
                      Download PDF
                    </button>
                  </div>
                </div>
              </div>
            ))}
            {!loading && !reports.length && (
              <div className="rounded-lg border border-slate-200 bg-white p-8 text-center text-slate-600">
                No reports found for this filter.
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Reports;
