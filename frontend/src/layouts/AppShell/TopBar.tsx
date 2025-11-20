import { useAuth } from '../../hooks/useAuth'
import './TopBar.css'

function TopBar() {
  const { user, logout } = useAuth()
  
  return (
    <header className="topbar">
      <div className="topbar-content">
        <div className="topbar-left">
          <h2 style={{ margin: 0, fontSize: '1.125rem', color: '#64748b' }}>
            مرحباً بك في نظام تنقية البيانات ✨
          </h2>
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
