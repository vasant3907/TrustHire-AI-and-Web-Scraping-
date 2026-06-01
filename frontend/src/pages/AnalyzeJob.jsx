import React, { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import apiService from '../services/apiService';

export const AnalyzeJob = () => {
  const [jdText, setJdText] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [screenshot, setScreenshot] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const canSubmit = useMemo(() => jdText.trim() || screenshot, [jdText, screenshot]);

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];
    setScreenshot(file || null);
    setPreviewUrl(file ? URL.createObjectURL(file) : '');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('Extracting text, collecting public company intelligence, and running AI analysis...');

    try {
      const formData = new FormData();
      formData.append('company_name', companyName || 'Unknown Company');
      formData.append('job_description', jdText);
      if (screenshot) {
        formData.append('screenshot', screenshot);
      }

      const response = await apiService.analyzeUpload(formData);
      setMessage('Analysis complete. Opening your report...');
      navigate(`/analysis/${response.data.id}`);
    } catch (err) {
      const detail = err.response?.data?.detail
        || (err.request ? 'Backend is not reachable. Use http://127.0.0.1:5174 or restart the backend on port 8001.' : err.message);
      setMessage('Error analyzing job: ' + detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Navbar />
      <main className="min-h-screen bg-slate-50">
        <div className="container mx-auto px-6 py-8">
          <div className="mb-8 flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-wide text-blue-700">TrustHire Analyzer</p>
              <h2 className="text-3xl font-bold text-slate-950">Analyze a job post or screenshot</h2>
              <p className="mt-2 max-w-3xl text-slate-600">
                Paste text, upload a screenshot, or use both. The system extracts text with AI OCR, checks public web intelligence, summarizes reviews, and generates a scam probability.
              </p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="grid gap-6 lg:grid-cols-[1.25fr_0.75fr]">
            <section className="space-y-6">
              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <label className="block text-sm font-semibold text-slate-700">Company or recruiter name</label>
                <input
                  type="text"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  placeholder="Example: Google, Infosys, ABC Recruiters"
                  className="mt-2 w-full rounded-md border border-slate-300 px-4 py-3 outline-none focus:border-blue-600"
                />
              </div>

              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <label className="block text-sm font-semibold text-slate-700">Job description text</label>
                <textarea
                  value={jdText}
                  onChange={(e) => setJdText(e.target.value)}
                  placeholder="Paste job post, email, WhatsApp message, salary details, recruiter contact, links, or offer text..."
                  rows="12"
                  className="mt-2 w-full rounded-md border border-slate-300 px-4 py-3 outline-none focus:border-blue-600"
                />
              </div>
            </section>

            <aside className="space-y-6">
              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
                <label className="block text-sm font-semibold text-slate-700">Screenshot OCR upload</label>
                <div className="mt-3 rounded-lg border-2 border-dashed border-slate-300 bg-slate-50 p-5 text-center">
                  <input
                    id="screenshot"
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                  <label htmlFor="screenshot" className="inline-flex cursor-pointer rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-700">
                    Choose Screenshot
                  </label>
                  <p className="mt-3 text-sm text-slate-600">{screenshot ? screenshot.name : 'PNG, JPG, or mobile screenshot'}</p>
                </div>
                {previewUrl && (
                  <img src={previewUrl} alt="Screenshot preview" className="mt-4 max-h-72 w-full rounded-md border border-slate-200 object-contain" />
                )}
              </div>

              <div className="rounded-lg border border-blue-200 bg-blue-50 p-5">
                <h3 className="font-semibold text-blue-950">Analysis includes</h3>
                <div className="mt-3 grid grid-cols-2 gap-3 text-sm text-blue-900">
                  <span>AI OCR</span>
                  <span>Scam probability</span>
                  <span>Public reviews</span>
                  <span>Company web data</span>
                  <span>LinkedIn/Naukri signals</span>
                  <span>Report download</span>
                </div>
              </div>

              {message && (
                <div className={`rounded-md p-4 text-sm ${message.includes('Error') ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-800'}`}>
                  {message}
                </div>
              )}

              <button
                type="submit"
                disabled={loading || !canSubmit}
                className="w-full rounded-md bg-blue-700 px-6 py-3 font-semibold text-white hover:bg-blue-800 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? 'Analyzing with AI...' : 'Analyze Job'}
              </button>
            </aside>
          </form>
        </div>
      </main>
    </div>
  );
};

export default AnalyzeJob;
