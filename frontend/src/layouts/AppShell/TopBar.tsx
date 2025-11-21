import { useAuth } from '../../hooks/useAuth'
import './TopBar.css'

function TopBar() {
  const { user, logout } = useAuth()
  
  return (
    <header className="topbar">
      <div className="topbar-content">
        <div className="topbar-left">
          <div className="topbar-logo">
            <svg width="28" height="28" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M50 10C50 10 25 35 25 55C25 70 35 80 50 80C65 80 75 70 75 55C75 35 50 10 50 10Z" fill="url(#gradient-topbar)"/>
              <rect x="35" y="45" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
              <rect x="35" y="53" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
              <rect x="35" y="61" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
              <defs>
                <linearGradient id="gradient-topbar" x1="50" y1="10" x2="50" y2="80" gradientUnits="userSpaceOnUse">
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
            <div className="user-menu">
              <span className="user-email">{user.email}</span>
              <button onClick={logout} className="btn-logout">
                تسجيل الخروج
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}

export default TopBar
