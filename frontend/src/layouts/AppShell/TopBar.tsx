import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import './TopBar.css'

function TopBar() {
  const { user, logout } = useAuth()
  const [showDropdown, setShowDropdown] = useState(false)
  const navigate = useNavigate()
  
  const handleLogout = () => {
    logout()
    setShowDropdown(false)
  }

  const handleProfile = () => {
    navigate('/app/profile')
    setShowDropdown(false)
  }

  const getUserInitials = () => {
    if (!user?.email) return 'U'
    return user.email.charAt(0).toUpperCase()
  }
  
  return (
    <header className="topbar">
      <div className="topbar-content">
        <div className="topbar-left">
          <div className="topbar-logo">
            <svg width="28" height="28" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M50 10C50 10 25 35 25 55C25 70 35 85 50 85C65 85 75 70 75 55C75 35 50 10 50 10Z" fill="url(#gradient)"/>
              <defs>
                <linearGradient id="gradient" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse">
                  <stop stopColor="#1F7FED"/>
                  <stop offset="1" stopColor="#4FE3C1"/>
                </linearGradient>
              </defs>
            </svg>
            <span className="topbar-brand">DataPurity</span>
          </div>
        </div>
        
        <div className="topbar-right">
          {user && (
            <div className="user-menu-container">
              <button 
                className="user-avatar"
                onClick={() => setShowDropdown(!showDropdown)}
                aria-label="قائمة المستخدم"
              >
                {getUserInitials()}
              </button>
              
              {showDropdown && (
                <>
                  <div className="dropdown-overlay" onClick={() => setShowDropdown(false)} />
                  <div className="user-dropdown">
                    <div className="dropdown-header">
                      <div className="dropdown-email">{user.email}</div>
                    </div>
                    <div className="dropdown-divider" />
                    <button className="dropdown-item" onClick={handleProfile}>
                      <span className="dropdown-icon">👤</span>
                      ملفي الشخصي
                    </button>
                    <button className="dropdown-item" onClick={() => { navigate('/app/settings'); setShowDropdown(false); }}>
                      <span className="dropdown-icon">⚙️</span>
                      الإعدادات
                    </button>
                    <div className="dropdown-divider" />
                    <button className="dropdown-item danger" onClick={handleLogout}>
                      <span className="dropdown-icon">🚪</span>
                      تسجيل الخروج
                    </button>
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </header>
  )
}

export default TopBar
