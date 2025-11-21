import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './admin-login.css'

// بيانات الدخول الافتراضية للمدير
const ADMIN_CREDENTIALS = {
  username: 'admin',
  password: 'DataPurity@2025'
}

function AdminLogin() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    // محاكاة تأخير الشبكة
    setTimeout(() => {
      if (username === ADMIN_CREDENTIALS.username && password === ADMIN_CREDENTIALS.password) {
        // حفظ حالة تسجيل الدخول
        sessionStorage.setItem('adminAuthenticated', 'true')
        sessionStorage.setItem('adminLoginTime', new Date().toISOString())
        
        // الانتقال للوحة الإدارة
        navigate('/app/admin')
      } else {
        setError('اسم المستخدم أو كلمة المرور غير صحيحة')
        setLoading(false)
      }
    }, 500)
  }

  return (
    <div className="admin-login-page">
      <div className="admin-login-container">
        <div className="admin-login-header">
          <div className="admin-logo">
            <svg width="48" height="48" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
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
          <h1>لوحة إدارة DataPurity</h1>
          <p>تسجيل الدخول كمسؤول</p>
        </div>

        <form onSubmit={handleLogin} className="admin-login-form">
          {error && (
            <div className="admin-error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="username">اسم المستخدم</label>
            <div className="input-wrapper">
              <span className="input-icon">👤</span>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="أدخل اسم المستخدم"
                required
                autoComplete="username"
                autoFocus
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password">كلمة المرور</label>
            <div className="input-wrapper">
              <span className="input-icon">🔒</span>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="أدخل كلمة المرور"
                required
                autoComplete="current-password"
              />
            </div>
          </div>

          <button 
            type="submit" 
            className="admin-login-btn"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                جاري التحقق...
              </>
            ) : (
              <>
                <span>🔑</span>
                تسجيل الدخول
              </>
            )}
          </button>
        </form>

        <div className="admin-login-footer">
          <p>
            <span className="security-icon">🔐</span>
            صفحة محمية - الوصول للمسؤولين فقط
          </p>
          <button 
            onClick={() => navigate('/')}
            className="back-to-home"
          >
            ← العودة للصفحة الرئيسية
          </button>
        </div>

        {/* معلومات تسجيل الدخول للتطوير - احذفها في الإنتاج */}
        {process.env.NODE_ENV === 'development' && (
          <div className="dev-credentials">
            <strong>🔧 بيانات التطوير:</strong>
            <br />
            Username: <code>admin</code>
            <br />
            Password: <code>DataPurity@2025</code>
          </div>
        )}
      </div>
    </div>
  )
}

export default AdminLogin
