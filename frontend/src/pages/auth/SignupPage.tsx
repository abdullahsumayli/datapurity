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
    
    // Validate required fields
    if (!fullName.trim()) {
      setError('الرجاء إدخال الاسم الكامل')
      return
    }
    
    if (!email.trim()) {
      setError('الرجاء إدخال البريد الإلكتروني')
      return
    }
    
    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      setError('البريد الإلكتروني غير صحيح')
      return
    }
    
    // Validate password if provided
    if (password && password.length < 8) {
      setError('إذا أدخلت كلمة مرور، يجب أن تكون 8 أحرف على الأقل')
      return
    }
    
    // Generate random password if not provided
    const finalPassword = password || `DP${Math.random().toString(36).slice(2, 10).toUpperCase()}!`
    
    setLoading(true)
    
    try {
      await signup({ email, password: finalPassword, full_name: fullName })
      
      // Show success message with password if auto-generated
      if (!password) {
        alert(`تم إنشاء حسابك بنجاح!\n\nكلمة المرور المؤقتة: ${finalPassword}\n\nيمكنك تغييرها من الملف الشخصي`)
      }
      
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
        <div className="auth-logo">
          <svg width="64" height="64" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M50 10C50 10 25 35 25 55C25 70 35 80 50 80C65 80 75 70 75 55C75 35 50 10 50 10Z" fill="url(#gradient1)"/>
            <rect x="35" y="45" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
            <rect x="35" y="53" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
            <rect x="35" y="61" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
            <defs>
              <linearGradient id="gradient1" x1="50" y1="10" x2="50" y2="80" gradientUnits="userSpaceOnUse">
                <stop stopColor="#1F7FED"/>
                <stop offset="1" stopColor="#4FE3C1"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <div className="auth-header">
          <h1>انضم إلى DataPurity 🚀</h1>
          <p>أنشئ حسابك في 30 ثانية فقط</p>
        </div>
        
        <form onSubmit={handleSubmit} className="auth-form">
          {error && <div className="error-message">{error}</div>}
          
          <div className="form-group">
            <label htmlFor="fullName">الاسم الكامل</label>
            <div className="input-with-icon">
              <span className="input-icon">👤</span>
              <input
                type="text"
                id="fullName"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="أدخل اسمك الكامل"
                disabled={loading}
                autoComplete="name"
              />
            </div>
          </div>
          
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
                autoComplete="email"
              />
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="password">كلمة المرور (اختيارية)</label>
            <div className="input-with-icon">
              <span className="input-icon">🔒</span>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="اتركها فارغة لكلمة مرور تلقائية"
                disabled={loading}
                autoComplete="new-password"
              />
            </div>
            <small className="form-hint">💡 يمكنك تركها فارغة وسنرسل لك كلمة مرور مؤقتة</small>
          </div>
          
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner"></span>
                جاري إنشاء الحساب...
              </>
            ) : (
              <>
                <span>✨</span>
                إنشاء حساب مجاني
              </>
            )}
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
