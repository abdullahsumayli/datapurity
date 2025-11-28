import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../../config/apiClient'

function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await apiClient.post('/auth/forgot-password', { email })
      setSuccess(true)
    } catch (err) {
      const error = err as { response?: { data?: { detail?: string } } }
      setError(error.response?.data?.detail || 'حدث خطأ. حاول مرة أخرى.')
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <div className="auth-page">
        <div className="auth-container">
          <div className="success-icon">✅</div>
          <div className="auth-header">
            <h1>تم إرسال رابط إعادة التعيين</h1>
            <p>تحقق من بريدك الإلكتروني ({email}) للحصول على رابط إعادة تعيين كلمة المرور</p>
          </div>
          <div className="success-actions">
            <button 
              onClick={() => navigate('/login')} 
              className="btn-primary"
            >
              العودة لتسجيل الدخول
            </button>
            <button 
              onClick={() => setSuccess(false)} 
              className="btn-secondary"
            >
              إرسال مرة أخرى
            </button>
          </div>

          <style>{`
            .success-icon {
              font-size: 4rem;
              text-align: center;
              margin-bottom: 1.5rem;
            }
            
            .success-actions {
              display: flex;
              flex-direction: column;
              gap: 1rem;
              margin-top: 2rem;
            }
            
            .btn-secondary {
              padding: 0.875rem 2rem;
              border-radius: 12px;
              border: 2px solid #1F7FED;
              background: transparent;
              color: #1F7FED;
              font-size: 1rem;
              font-weight: 600;
              cursor: pointer;
              transition: all 0.3s ease;
            }
            
            .btn-secondary:hover {
              background: #1F7FED;
              color: white;
              transform: translateY(-2px);
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
            <path d="M50 10C50 10 25 35 25 55C25 70 35 80 50 80C65 80 75 70 75 55C75 35 50 10 50 10Z" fill="url(#gradient-forgot)"/>
            <rect x="35" y="45" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
            <rect x="35" y="53" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
            <rect x="35" y="61" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
            <defs>
              <linearGradient id="gradient-forgot" x1="50" y1="10" x2="50" y2="80" gradientUnits="userSpaceOnUse">
                <stop stopColor="#1F7FED"/>
                <stop offset="1" stopColor="#4FE3C1"/>
              </linearGradient>
            </defs>
          </svg>
        </div>

        <div className="auth-header">
          <h1>نسيت كلمة المرور؟ 🔐</h1>
          <p>أدخل بريدك الإلكتروني وسنرسل لك رابط لإعادة تعيين كلمة المرور</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <label htmlFor="email">البريد الإلكتروني</label>
            <div className="input-with-icon">
              <span className="input-icon">📧</span>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="example@email.com"
                disabled={loading}
                required
                autoFocus
              />
            </div>
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner"></span>
                جاري الإرسال...
              </>
            ) : (
              <>
                <span>📨</span>
                إرسال رابط إعادة التعيين
              </>
            )}
          </button>
        </form>

        <p className="auth-footer">
          تذكرت كلمة المرور؟ <a href="/login">تسجيل الدخول</a>
        </p>
      </div>
    </div>
  )
}

export default ForgotPasswordPage
