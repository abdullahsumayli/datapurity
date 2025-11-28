import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import apiClient from '../../config/apiClient'

function ResetPasswordPage() {
  const [searchParams] = useSearchParams()
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')
  const [tokenValid, setTokenValid] = useState(true)
  const navigate = useNavigate()

  const token = searchParams.get('token')

  useEffect(() => {
    if (!token) {
      setTokenValid(false)
      setError('رابط غير صالح. الرجاء طلب رابط جديد.')
    }
  }, [token])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    // Validate passwords match
    if (password !== confirmPassword) {
      setError('كلمتا المرور غير متطابقتين')
      return
    }

    // Validate password strength
    if (password.length < 8) {
      setError('كلمة المرور يجب أن تكون 8 أحرف على الأقل')
      return
    }

    setLoading(true)

    try {
      await apiClient.post('/auth/reset-password', {
        token,
        new_password: password,
      })
      setSuccess(true)
      setTimeout(() => navigate('/login'), 3000)
    } catch (err) {
      const error = err as { response?: { data?: { detail?: string } } }
      setError(error.response?.data?.detail || 'حدث خطأ. الرجاء المحاولة مرة أخرى.')
    } finally {
      setLoading(false)
    }
  }

  if (!tokenValid) {
    return (
      <div className="auth-page">
        <div className="auth-container">
          <div className="error-icon">❌</div>
          <div className="auth-header">
            <h1>رابط غير صالح</h1>
            <p>هذا الرابط غير صالح أو منتهي الصلاحية</p>
          </div>
          <button onClick={() => navigate('/forgot-password')} className="btn-primary">
            طلب رابط جديد
          </button>

          <style>{`
            .error-icon {
              font-size: 4rem;
              text-align: center;
              margin-bottom: 1.5rem;
            }
          `}</style>
        </div>
      </div>
    )
  }

  if (success) {
    return (
      <div className="auth-page">
        <div className="auth-container">
          <div className="success-icon">✅</div>
          <div className="auth-header">
            <h1>تم تغيير كلمة المرور بنجاح!</h1>
            <p>سيتم تحويلك لصفحة تسجيل الدخول...</p>
          </div>

          <style>{`
            .success-icon {
              font-size: 4rem;
              text-align: center;
              margin-bottom: 1.5rem;
              animation: scaleIn 0.5s ease;
            }
            
            @keyframes scaleIn {
              from {
                transform: scale(0);
              }
              to {
                transform: scale(1);
              }
            }
          `}</style>
        </div>
      </div>
    )
  }

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-logo">
          <svg width="64" height="64" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M50 10C50 10 25 35 25 55C25 70 35 80 50 80C65 80 75 70 75 55C75 35 50 10 50 10Z" fill="url(#gradient-reset)"/>
            <rect x="35" y="45" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
            <rect x="35" y="53" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
            <rect x="35" y="61" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
            <defs>
              <linearGradient id="gradient-reset" x1="50" y1="10" x2="50" y2="80" gradientUnits="userSpaceOnUse">
                <stop stopColor="#1F7FED"/>
                <stop offset="1" stopColor="#4FE3C1"/>
              </linearGradient>
            </defs>
          </svg>
        </div>

        <div className="auth-header">
          <h1>إعادة تعيين كلمة المرور 🔑</h1>
          <p>أدخل كلمة مرور جديدة لحسابك</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <label htmlFor="password">كلمة المرور الجديدة</label>
            <div className="input-with-icon">
              <span className="input-icon">🔒</span>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="8 أحرف على الأقل"
                disabled={loading}
                required
                autoFocus
                minLength={8}
              />
            </div>
            <small className="password-hint">
              يجب أن تحتوي على 8 أحرف على الأقل
            </small>
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">تأكيد كلمة المرور</label>
            <div className="input-with-icon">
              <span className="input-icon">🔒</span>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="أعد إدخال كلمة المرور"
                disabled={loading}
                required
                minLength={8}
              />
            </div>
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner"></span>
                جاري التحديث...
              </>
            ) : (
              <>
                <span>✨</span>
                تحديث كلمة المرور
              </>
            )}
          </button>
        </form>

        <p className="auth-footer">
          تذكرت كلمة المرور؟ <a href="/login">تسجيل الدخول</a>
        </p>

        <style>{`
          .password-hint {
            display: block;
            margin-top: 0.5rem;
            color: #6b7280;
            font-size: 0.875rem;
          }
        `}</style>
      </div>
    </div>
  )
}

export default ResetPasswordPage
