import { useAuth } from '../../hooks/useAuth'
import './TopBar.css'

function TopBar() {
  const { user, logout } = useAuth()
  
  return (
    <header className="topbar">
      <div className="topbar-content">
        <div className="topbar-left">
          {/* Breadcrumb or page title could go here */}
        </div>
        
        <div className="topbar-right">
          {user && (
            <div className="user-menu">
              <span className="user-email">{user.email}</span>
              <button onClick={logout} className="btn-logout">
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}

export default TopBar
