import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'

function SignupPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { signup } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    // Validate password length
    if (password.length < 8) {
      setError('يجب أن تكون كلمة المرور 8 أحرف على الأقل')
      return
    }
    
    setLoading(true)
    
    try {
      await signup({ email, password, full_name: fullName })
      navigate('/app/dashboard')
    } catch (err) {
      const error = err as { response?: { data?: { detail?: string } } }
      setError(error.response?.data?.detail || 'فشل إنشاء الحساب. حاول مرة أخرى.')
    } finally {
      setLoading(false)
    }
  }

  const handleGoogleSignup = () => {
    // استخدام مسار نسبي للـ OAuth
    window.location.href = '/api/v1/auth/google/login'
  }

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-header">
          <h1>انضم إلى DataPurity 🚀</h1>
          <p>أنشئ حسابك الآن وابدأ بتنظيم بياناتك</p>
        </div>
        
        <form onSubmit={handleSubmit} className="auth-form">
          {error && <div className="error-message">{error}</div>}
          
          <div className="form-group">
            <label htmlFor="fullName">الاسم الكامل</label>
            <input
              type="text"
              id="fullName"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="أدخل اسمك الكامل"
              disabled={loading}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="email">البريد الإلكتروني</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="example@email.com"
              disabled={loading}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">كلمة المرور</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="8 أحرف على الأقل"
              disabled={loading}
              required
              minLength={8}
            />
            <small className="form-hint">يجب أن تحتوي على 8 أحرف على الأقل</small>
          </div>
          
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'جاري إنشاء الحساب...' : 'إنشاء حساب'}
          </button>
          
          <div className="auth-divider">
            <span>أو</span>
          </div>
          
          <button 
            type="button" 
            onClick={handleGoogleSignup}
            className="btn-google"
          >
            <svg width="18" height="18" viewBox="0 0 18 18" style={{ marginLeft: '8px' }}>
              <path fill="#4285F4" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z"/>
              <path fill="#34A853" d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z"/>
              <path fill="#FBBC05" d="M3.964 10.707c-.18-.54-.282-1.117-.282-1.707s.102-1.167.282-1.707V4.961H.957C.347 6.175 0 7.55 0 9s.348 2.825.957 4.039l3.007-2.332z"/>
              <path fill="#EA4335" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.961L3.964 7.293C4.672 5.163 6.656 3.58 9 3.58z"/>
            </svg>
            التسجيل بحساب Google
          </button>
        </form>
        
        <p className="auth-footer">
          لديك حساب بالفعل؟ <a href="/login">تسجيل الدخول</a>
        </p>
      </div>
    </div>
  )
}

export default SignupPage
