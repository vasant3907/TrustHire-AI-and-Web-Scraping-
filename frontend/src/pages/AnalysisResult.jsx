import React, { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import apiService from '../services/apiService';

const parseJson = (value, fallback) => {
  try {
    return value ? JSON.parse(value) : fallback;
  } catch {
    return fallback;
  }
};

const riskStyles = {
  low: 'bg-emerald-100 text-emerald-800 border-emerald-200',
  medium: 'bg-amber-100 text-amber-800 border-amber-200',
  high: 'bg-orange-100 text-orange-800 border-orange-200',
  critical: 'bg-red-100 text-red-800 border-red-200',
};

export const AnalysisResult = () => {
  const { reportId } = useParams();
  const [report, setReport] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [note, setNote] = useState('');
  const [bookmarked, setBookmarked] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [noteMessage, setNoteMessage] = useState('');

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const response = await apiService.getReport(reportId);
        setReport(response.data);
        const timelineResponse = await apiService.getReportTimeline(reportId);
        setTimeline(timelineResponse.data);
        const noteResponse = await apiService.getReportNote(response.data.id);
        setNote(noteResponse.data.note || '');
        setBookmarked(Boolean(noteResponse.data.bookmarked));
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load report');
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, [reportId]);

  const keywords = useMemo(() => parseJson(report?.suspicious_keywords, []), [report]);
  const intelligence = useMemo(() => parseJson(report?.company_intelligence, {}), [report]);

  const handlePdfDownload = async () => {
    const response = await apiService.downloadReportPdf(report.id);
    const url = URL.createObjectURL(response.data);
    const link = document.createElement('a');
    link.href = url;
    link.download = `trusthire-report-${report.id}.pdf`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const saveNote = async () => {
    setNoteMessage('');
    try {
      const response = await apiService.saveReportNote(report.id, { note, bookmarked });
      setBookmarked(Boolean(response.data.bookmarked));
      setNoteMessage('Saved successfully.');
    } catch (err) {
      setNoteMessage(err.response?.data?.detail || 'Unable to save note.');
    }
  };

  if (loading) {
    return (
      <div>
        <Navbar />
        <div className="container mx-auto p-6">Loading analysis...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <Navbar />
        <div className="container mx-auto p-6">
          <div className="rounded-md bg-red-100 p-4 text-red-700">{error}</div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Navbar />
      <main className="min-h-screen bg-slate-50">
        <div className="container mx-auto px-6 py-8">
          <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-wide text-blue-700">Analysis Report</p>
              <h2 className="text-3xl font-bold text-slate-950">Trust and scam risk summary</h2>
            </div>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={handlePdfDownload}
                className="rounded-md bg-blue-700 px-4 py-2 text-center text-sm font-semibold text-white hover:bg-blue-800"
              >
                Download PDF
              </button>
            </div>
          </div>

          <section className="grid gap-4 md:grid-cols-4">
            <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Trust Score</p>
              <p className="mt-2 text-4xl font-bold text-blue-700">{Math.round(report.trust_score)}%</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Scam Probability</p>
              <p className="mt-2 text-4xl font-bold text-red-700">{Math.round(report.scam_probability || 0)}%</p>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Risk Level</p>
              <span className={`mt-3 inline-flex rounded-full border px-3 py-1 text-sm font-semibold capitalize ${riskStyles[report.risk_level] || riskStyles.medium}`}>
                {report.risk_level}
              </span>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Company Presence</p>
              <p className="mt-2 text-4xl font-bold text-slate-900">{Math.round(report.company_presence_score)}%</p>
            </div>
          </section>

          <section className="mt-6 grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
            <div className="space-y-6">
              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-slate-950">AI Explanation</h3>
                <p className="mt-3 text-slate-700">{report.ai_summary}</p>
              </div>

              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-slate-950">Recommendation</h3>
                <p className="mt-3 text-slate-700">{report.recommendation}</p>
              </div>

              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-slate-950">AI Review Summarizer</h3>
                <p className="mt-3 text-slate-700">{report.review_summary || 'No public review summary available.'}</p>
              </div>

              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-slate-950">Risk Explanation Timeline</h3>
                <div className="mt-4 space-y-4">
                  {timeline.map((item) => (
                    <div key={item.step} className="border-l-4 border-blue-600 pl-4">
                      <p className="font-semibold text-slate-900">{item.step}</p>
                      <p className="text-sm text-slate-600">{item.detail}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-slate-950">Notes and Bookmark</h3>
                <textarea
                  value={note}
                  onChange={(e) => setNote(e.target.value)}
                  className="mt-3 w-full rounded-md border border-slate-300 px-4 py-2"
                  rows="3"
                  placeholder="Add personal notes about this opportunity..."
                />
                <label className="mt-3 flex items-center gap-2 text-sm text-slate-700">
                  <input type="checkbox" checked={bookmarked} onChange={(e) => setBookmarked(e.target.checked)} />
                  Bookmark this report
                </label>
                <button type="button" onClick={saveNote} className="mt-3 rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white">
                  Save Note
                </button>
                {noteMessage && <p className="mt-3 text-sm text-slate-600">{noteMessage}</p>}
              </div>
            </div>

            <div className="space-y-6">
              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-slate-950">Suspicious Signals</h3>
                <div className="mt-3 flex flex-wrap gap-2">
                  {keywords.length ? keywords.map((keyword) => (
                    <span key={keyword} className="rounded-full bg-red-50 px-3 py-1 text-sm font-medium text-red-700">
                      {keyword}
                    </span>
                  )) : <p className="text-slate-600">No suspicious keywords found.</p>}
                </div>
              </div>

              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-slate-950">Company Web Intelligence</h3>
                <div className="mt-3 space-y-2 text-sm text-slate-700">
                  <p><span className="font-semibold">Website:</span> {intelligence.website || 'Not found'}</p>
                  <p><span className="font-semibold">LinkedIn:</span> {intelligence.linkedin_url || 'Public listing not found'}</p>
                  <p><span className="font-semibold">Naukri:</span> {intelligence.naukri_url || 'Public listing not found'}</p>
                  <p><span className="font-semibold">Salary:</span> {report.salary_validity}</p>
                  <p><span className="font-semibold">Email:</span> {report.email_validity}</p>
                </div>
              </div>

              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-slate-950">Public Review Links</h3>
                <div className="mt-3 space-y-3">
                  {(intelligence.reviews || []).slice(0, 5).map((review) => (
                    <a key={review.url} href={review.url} target="_blank" rel="noreferrer" className="block rounded-md border border-slate-200 p-3 hover:border-blue-300">
                      <p className="font-medium text-slate-900">{review.review_source || 'Review'}: {review.title}</p>
                      <p className="mt-1 text-sm text-slate-600">{review.snippet}</p>
                    </a>
                  ))}
                  {!(intelligence.reviews || []).length && <p className="text-sm text-slate-600">No reachable public review snippets were found.</p>}
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
};

export default AnalysisResult;
