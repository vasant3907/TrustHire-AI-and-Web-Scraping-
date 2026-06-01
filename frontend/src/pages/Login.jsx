import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import apiService from '../services/apiService';

export const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [forgotMode, setForgotMode] = useState(false);
  const [resetRequested, setResetRequested] = useState(false);
  const [resetToken, setResetToken] = useState('');
  const [resetPassword, setResetPassword] = useState('');
  const [resetConfirm, setResetConfirm] = useState('');

  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');
    try {
      const response = await apiService.login(email, password);
      const { access_token, user_id, name, is_admin } = response.data;
      login({ id: user_id, name, email, is_admin }, access_token, rememberMe);
      navigate(is_admin ? '/admin' : '/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');

    try {
      if (!resetRequested) {
        const response = await apiService.forgotPassword({ email });
        setResetRequested(true);
        setResetToken('');
        setMessage(response.data?.message || 'If this email exists, a reset code has been sent.');
      } else {
        if (resetPassword !== resetConfirm) {
          setError('New password and confirmation do not match.');
          setLoading(false);
          return;
        }
        const response = await apiService.resetPassword({
          reset_token: resetToken,
          new_password: resetPassword,
        });
        setMessage(response.data?.message || 'Password reset completed. You can sign in now.');
        setPassword('');
        setResetToken('');
        setResetPassword('');
        setResetConfirm('');
        setResetRequested(false);
        setForgotMode(false);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Password reset failed');
    } finally {
      setLoading(false);
    }
  };

  const particles = Array.from({ length: 24 }, (_, i) => ({
    id: i,
    left: `${(i * 37) % 100}%`,
    top: `${35 + ((i * 23) % 60)}%`,
    color: ['#378ADD', '#AFA9EC', '#5DCAA5', '#F09595'][i % 4],
    duration: `${6 + ((i * 11) % 10)}s`,
    delay: `${-((i * 7) % 13)}s`,
  }));

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

        @keyframes th-orb1  { 0%,100%{transform:translate(0,0) scale(1)} 50%{transform:translate(28px,-22px) scale(1.07)} }
        @keyframes th-orb2  { 0%,100%{transform:translate(0,0)} 50%{transform:translate(-18px,18px) scale(.93)} }
        @keyframes th-orb3  { 0%,100%{transform:translate(0,0)} 50%{transform:translate(14px,-28px)} }
        @keyframes th-ptcl  { 0%{transform:translateY(0);opacity:0} 15%{opacity:.85} 85%{opacity:.35} 100%{transform:translateY(-140px);opacity:0} }
        @keyframes th-rspin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
        @keyframes th-rspinr{ from{transform:rotate(0deg)} to{transform:rotate(-360deg)} }
        @keyframes th-fade  { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
        @keyframes th-glow  { 0%,100%{box-shadow:0 0 0 0 rgba(55,138,221,.5)} 50%{box-shadow:0 0 0 10px rgba(55,138,221,0)} }
        @keyframes th-shim  { 0%{background-position:-400px 0} 100%{background-position:400px 0} }
        @keyframes th-spin  { from{transform:rotate(0)} to{transform:rotate(360deg)} }

        .th-page {
          font-family: 'Space Grotesk', sans-serif;
          min-height: 100vh; width: 100%;
          background: #060d1c;
          display: flex; align-items: center; justify-content: center;
          position: relative; overflow: hidden; padding: 28px 16px;
        }
        .th-bg { position:absolute;inset:0;pointer-events:none;overflow:hidden }
        .th-grid {
          position:absolute;inset:0;
          background-image: linear-gradient(rgba(55,138,221,.04) 1px,transparent 1px),
                            linear-gradient(90deg,rgba(55,138,221,.04) 1px,transparent 1px);
          background-size: 50px 50px;
        }
        .th-orb { position:absolute;border-radius:50%;filter:blur(80px) }
        .th-o1 { width:400px;height:400px;background:rgba(18,88,158,.3);top:-130px;left:-110px;animation:th-orb1 11s ease-in-out infinite }
        .th-o2 { width:280px;height:280px;background:rgba(75,50,170,.24);bottom:-90px;left:35%;animation:th-orb2 14s ease-in-out infinite }
        .th-o3 { width:220px;height:220px;background:rgba(10,100,75,.2);bottom:-55px;right:-55px;animation:th-orb3 9s ease-in-out infinite }
        .th-pt { position:absolute;width:3px;height:3px;border-radius:50%;opacity:0;animation:th-ptcl var(--d) ease-in-out var(--dl) infinite }

        .th-card {
          position:relative;z-index:5;
          display:flex; width:100%; max-width:860px; min-height:520px;
          background:rgba(9,15,30,.9);
          border:0.5px solid rgba(255,255,255,.1);
          border-radius:20px; overflow:hidden;
          animation:th-fade .55s ease both;
        }
        .th-left {
          flex:1; padding:3rem 2.75rem;
          display:flex; flex-direction:column; justify-content:center;
          border-right:0.5px solid rgba(255,255,255,.07);
          position:relative; overflow:hidden;
        }
        .th-rings { position:absolute;right:-80px;top:50%;transform:translateY(-50%);pointer-events:none;opacity:.08 }
        .th-r1 { animation:th-rspin 30s linear infinite }
        .th-r2 { position:absolute;top:35px;left:35px;animation:th-rspinr 22s linear infinite }

        .th-logo-row { display:flex;align-items:center;gap:13px;margin-bottom:2.25rem }
        .th-logo-box {
          width:46px;height:46px;
          background:linear-gradient(135deg,#185FA5,#378ADD);
          border-radius:13px;display:flex;align-items:center;justify-content:center;
          animation:th-glow 3.5s ease-in-out infinite;flex-shrink:0;
        }
        .th-logo-box i { font-size:22px;color:#fff }
        .th-logo-name { font-size:20px;font-weight:700;color:#fff;letter-spacing:-.02em }

        .th-badge {
          display:inline-flex;align-items:center;gap:6px;
          background:rgba(224,75,74,.15);
          border:0.5px solid rgba(224,75,74,.3);
          border-radius:20px;padding:5px 12px;
          font-size:11.5px;color:#F09595;
          margin-bottom:1.25rem;letter-spacing:.01em;width:fit-content;
        }
        .th-badge i { font-size:13px }

        .th-hero { font-size:30px;font-weight:700;color:#fff;line-height:1.18;margin-bottom:10px;letter-spacing:-.025em }
        .th-hero span { background:linear-gradient(90deg,#378ADD,#AFA9EC);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text }
        .th-sub { font-size:13.5px;color:rgba(255,255,255,.38);line-height:1.65;margin-bottom:2.25rem;max-width:260px }

        .th-feats { display:flex;flex-direction:column;gap:14px }
        .th-feat { display:flex;align-items:center;gap:12px;animation:th-fade .55s ease both }
        .th-feat:nth-child(1){animation-delay:.08s}
        .th-feat:nth-child(2){animation-delay:.16s}
        .th-feat:nth-child(3){animation-delay:.22s}
        .th-feat:nth-child(4){animation-delay:.28s}
        .th-fd { width:32px;height:32px;border-radius:9px;display:flex;align-items:center;justify-content:center;flex-shrink:0 }
        .th-fd i { font-size:16px }
        .th-fd-red   { background:rgba(162,45,45,.28)  } .th-fd-red   i { color:#F09595 }
        .th-fd-blue  { background:rgba(24,95,165,.28)  } .th-fd-blue  i { color:#85B7EB }
        .th-fd-amber { background:rgba(133,79,11,.3)   } .th-fd-amber i { color:#EF9F27 }
        .th-fd-teal  { background:rgba(15,110,86,.28)  } .th-fd-teal  i { color:#5DCAA5 }
        .th-feat-lbl { font-size:13px;color:rgba(255,255,255,.5) }

        .th-right { width:340px;flex-shrink:0;padding:3rem 2.5rem;display:flex;flex-direction:column;justify-content:center }
        .th-form-head { font-size:24px;font-weight:700;color:#fff;margin-bottom:4px;letter-spacing:-.02em }
        .th-form-sub  { font-size:13px;color:rgba(255,255,255,.3);margin-bottom:1.75rem;line-height:1.5 }

        .th-err {
          background:rgba(162,45,45,.2);border:0.5px solid rgba(224,75,74,.3);
          border-radius:9px;padding:9px 13px;font-size:12.5px;color:#F09595;
          margin-bottom:14px;display:flex;align-items:center;gap:7px;
        }
        .th-err i { font-size:14px;flex-shrink:0 }
        .th-ok {
          background:rgba(36,132,94,.18);border:0.5px solid rgba(93,202,165,.35);
          border-radius:9px;padding:9px 13px;font-size:12.5px;color:#8FE0C3;
          margin-bottom:14px;display:flex;align-items:center;gap:7px;
        }
        .th-ok i { font-size:14px;flex-shrink:0 }

        .th-field { margin-bottom:15px }
        .th-lbl { display:block;font-size:11px;color:rgba(255,255,255,.35);letter-spacing:.05em;text-transform:uppercase;margin-bottom:6px }
        .th-iw  { position:relative }
        .th-iw i.ico { position:absolute;left:11px;top:50%;transform:translateY(-50%);font-size:16px;color:rgba(255,255,255,.22);pointer-events:none }
        .th-inp {
          width:100%;box-sizing:border-box;
          background:rgba(255,255,255,.05);border:0.5px solid rgba(255,255,255,.1);
          border-radius:10px;padding:11px 12px 11px 36px;
          font-family:'Space Grotesk',sans-serif;font-size:14px;color:#fff;outline:none;
          transition:border-color .2s,background .2s,box-shadow .2s;
        }
        .th-inp::placeholder { color:rgba(255,255,255,.18) }
        .th-inp:focus { border-color:rgba(55,138,221,.55);background:rgba(55,138,221,.07);box-shadow:0 0 0 3px rgba(55,138,221,.1) }
        .th-eye { position:absolute;right:10px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;padding:0;color:rgba(255,255,255,.22);display:flex;align-items:center }
        .th-eye:hover { color:rgba(255,255,255,.6) }
        .th-eye i { font-size:16px }

        .th-row { display:flex;justify-content:space-between;align-items:center;margin-bottom:1.3rem }
        .th-chk { display:flex;align-items:center;gap:7px }
        .th-chk input { accent-color:#378ADD;width:14px;height:14px;cursor:pointer }
        .th-chk label { font-size:12.5px;color:rgba(255,255,255,.3);cursor:pointer }
        .th-fgt { font-size:12.5px;color:#85B7EB;text-decoration:none;background:none;border:0;padding:0;cursor:pointer;font-family:'Space Grotesk',sans-serif }
        .th-fgt:hover { color:#B5D4F4 }

        .th-sbtn {
          width:100%;padding:12px;
          background:linear-gradient(135deg,#185FA5,#378ADD);
          border:none;border-radius:10px;color:#fff;
          font-family:'Space Grotesk',sans-serif;font-size:14.5px;font-weight:600;
          cursor:pointer;position:relative;overflow:hidden;
          display:flex;align-items:center;justify-content:center;gap:8px;
          transition:opacity .2s,transform .15s;letter-spacing:.01em;
        }
        .th-sbtn:hover:not(:disabled){opacity:.9;transform:translateY(-1px)}
        .th-sbtn:active:not(:disabled){transform:scale(.98)}
        .th-sbtn:disabled{opacity:.55;cursor:not-allowed}
        .th-sbtn::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.14),transparent);background-size:400px 100%;animation:th-shim 2s linear infinite}
        .th-spinner{width:15px;height:15px;border:2px solid rgba(255,255,255,.3);border-top-color:#fff;border-radius:50%;animation:th-spin .7s linear infinite;flex-shrink:0}

        .th-reg { text-align:center;margin-top:1.4rem;font-size:13px;color:rgba(255,255,255,.28) }
        .th-reg a { color:#85B7EB;text-decoration:none;font-weight:600 }
        .th-reg a:hover { color:#B5D4F4 }

        @media(max-width:620px){
          .th-left{display:none}
          .th-card{max-width:380px}
          .th-right{width:100%}
        }
      `}</style>

      <div className="th-page">
        <div className="th-bg">
          <div className="th-grid" />
          <div className="th-orb th-o1" />
          <div className="th-orb th-o2" />
          <div className="th-orb th-o3" />
          {particles.map(p => (
            <div key={p.id} className="th-pt"
              style={{ left: p.left, top: p.top, background: p.color, '--d': p.duration, '--dl': p.delay }}
            />
          ))}
        </div>

        <div className="th-card">
          {/* LEFT — branding, no logic */}
          <div className="th-left">
            <div className="th-rings" aria-hidden="true">
              <svg className="th-r1" width="220" height="220" viewBox="0 0 220 220">
                <circle cx="110" cy="110" r="100" fill="none" stroke="#378ADD" strokeWidth=".7" strokeDasharray="8 6"/>
                <circle cx="110" cy="110" r="72"  fill="none" stroke="#AFA9EC" strokeWidth=".7" strokeDasharray="3 8"/>
                <circle cx="110" cy="10"  r="5.5" fill="#378ADD"/>
                <circle cx="210" cy="110" r="4"   fill="#AFA9EC"/>
                <circle cx="110" cy="210" r="4.5" fill="#5DCAA5"/>
              </svg>
              <svg className="th-r2" width="150" height="150" viewBox="0 0 150 150"
                style={{ position: 'absolute', top: 35, left: 35 }}>
                <circle cx="75" cy="75" r="65" fill="none" stroke="#5DCAA5" strokeWidth=".6" strokeDasharray="5 9"/>
                <circle cx="75" cy="10" r="4"  fill="#5DCAA5"/>
                <circle cx="140" cy="75" r="3" fill="#378ADD"/>
              </svg>
            </div>

            <div className="th-logo-row">
              <div className="th-logo-box" aria-hidden="true">
                <i className="ti ti-shield-check" />
              </div>
              <span className="th-logo-name">TrustHire AI</span>
            </div>

            <div className="th-badge">
              <i className="ti ti-alert-triangle" aria-hidden="true" />
              Job scam &amp; fraud detection
            </div>

            <h1 className="th-hero">Stay safe.<br /><span>Trust smarter.</span></h1>
            <p className="th-sub">
              AI-powered protection for freshers and job seekers against fake postings,
              scam recruiters, and fraudulent companies.
            </p>

            <div className="th-feats">
              <div className="th-feat">
                <div className="th-fd th-fd-red" aria-hidden="true"><i className="ti ti-bug" /></div>
                <span className="th-feat-lbl">Fake job posting detector</span>
              </div>
              <div className="th-feat">
                <div className="th-fd th-fd-blue" aria-hidden="true"><i className="ti ti-mail-search" /></div>
                <span className="th-feat-lbl">Recruiter email verifier</span>
              </div>
              <div className="th-feat">
                <div className="th-fd th-fd-amber" aria-hidden="true"><i className="ti ti-chart-bar" /></div>
                <span className="th-feat-lbl">Company trust score engine</span>
              </div>
              <div className="th-feat">
                <div className="th-fd th-fd-teal" aria-hidden="true"><i className="ti ti-scan" /></div>
                <span className="th-feat-lbl">Screenshot &amp; OCR analysis</span>
              </div>
            </div>
          </div>

          {/* RIGHT — original implementation, untouched */}
          <div className="th-right">
            <p className="th-form-head">{forgotMode ? 'Reset password' : 'Welcome back'}</p>
            <p className="th-form-sub">
              {forgotMode
                ? resetRequested ? 'Check your email, enter the reset code, and choose a new password' : 'Enter your account email to receive a reset code'
                : 'Sign in to keep your job search safe'}
            </p>

            <form onSubmit={forgotMode ? handleForgotPassword : handleSubmit}>
              {error && (
                <div className="th-err" role="alert">
                  <i className="ti ti-alert-circle" aria-hidden="true" />
                  {error}
                </div>
              )}
              {message && (
                <div className="th-ok" role="status">
                  <i className="ti ti-circle-check" aria-hidden="true" />
                  {message}
                </div>
              )}

              <div className="th-field">
                <label className="th-lbl" htmlFor="email">Email</label>
                <div className="th-iw">
                  <i className="ti ti-mail ico" aria-hidden="true" />
                  <input
                    id="email"
                    type="email"
                    placeholder="you@email.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="th-inp"
                    required
                    autoComplete="email"
                  />
                </div>
              </div>

              {!forgotMode && (
              <div className="th-field">
                <label className="th-lbl" htmlFor="password">Password</label>
                <div className="th-iw">
                  <i className="ti ti-lock ico" aria-hidden="true" />
                  <input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="th-inp"
                    required
                    autoComplete="current-password"
                  />
                  <button
                    type="button"
                    className="th-eye"
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                  >
                    <i className={showPassword ? 'ti ti-eye-off' : 'ti ti-eye'} aria-hidden="true" />
                  </button>
                </div>
              </div>
              )}

              {forgotMode && resetRequested && (
                <>
                  <div className="th-field">
                    <label className="th-lbl" htmlFor="resetToken">Reset code</label>
                    <div className="th-iw">
                      <i className="ti ti-key ico" aria-hidden="true" />
                      <input
                        id="resetToken"
                        type="text"
                        placeholder="6 digit code"
                        value={resetToken}
                        onChange={(e) => setResetToken(e.target.value)}
                        className="th-inp"
                        required
                        autoComplete="one-time-code"
                      />
                    </div>
                  </div>

                  <div className="th-field">
                    <label className="th-lbl" htmlFor="resetPassword">New password</label>
                    <div className="th-iw">
                      <i className="ti ti-lock ico" aria-hidden="true" />
                      <input
                        id="resetPassword"
                        type={showPassword ? 'text' : 'password'}
                        placeholder="minimum 8 characters"
                        value={resetPassword}
                        onChange={(e) => setResetPassword(e.target.value)}
                        className="th-inp"
                        minLength={8}
                        required
                        autoComplete="new-password"
                      />
                    </div>
                  </div>

                  <div className="th-field">
                    <label className="th-lbl" htmlFor="resetConfirm">Confirm password</label>
                    <div className="th-iw">
                      <i className="ti ti-lock-check ico" aria-hidden="true" />
                      <input
                        id="resetConfirm"
                        type={showPassword ? 'text' : 'password'}
                        placeholder="repeat new password"
                        value={resetConfirm}
                        onChange={(e) => setResetConfirm(e.target.value)}
                        className="th-inp"
                        minLength={8}
                        required
                        autoComplete="new-password"
                      />
                    </div>
                  </div>
                </>
              )}

              <div className="th-row">
                {!forgotMode ? (
                  <div className="th-chk">
                    <input
                      type="checkbox"
                      id="remember"
                      checked={rememberMe}
                      onChange={(event) => setRememberMe(event.target.checked)}
                    />
                    <label htmlFor="remember">Remember me</label>
                  </div>
                ) : (
                  <span />
                )}
                <button
                  type="button"
                  className="th-fgt"
                  onClick={() => {
                    setForgotMode((value) => !value);
                    setResetRequested(false);
                    setResetToken('');
                    setResetPassword('');
                    setResetConfirm('');
                    setError('');
                    setMessage('');
                  }}
                >
                  {forgotMode ? 'Back to login' : 'Forgot password?'}
                </button>
              </div>

              <button type="submit" disabled={loading} className="th-sbtn">
                {loading && <div className="th-spinner" aria-hidden="true" />}
                {loading
                  ? forgotMode ? 'Working...' : 'Signing in...'
                  : forgotMode ? resetRequested ? 'Reset password' : 'Generate reset code' : 'Sign in'}
              </button>
            </form>

            <p className="th-reg">
              New here? <a href="/register">Create an account</a>
            </p>
          </div>
        </div>
      </div>
    </>
  );
};

export default Login;
