import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'

function GoogleCallbackPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()

  useEffect(() => {
    const token = searchParams.get('token')
    
    if (token) {
      // Save token to localStorage
      localStorage.setItem('access_token', token)
      
      // Redirect to dashboard
      navigate('/app/dashboard', { replace: true })
    } else {
      // No token, redirect to login
      navigate('/login', { replace: true })
    }
  }, [searchParams, navigate])

  return (
    <div className="auth-page">
      <div className="auth-container">
        <h2>جاري تسجيل الدخول...</h2>
        <p>الرجاء الانتظار</p>
      </div>
    </div>
  )
}

export default GoogleCallbackPage
