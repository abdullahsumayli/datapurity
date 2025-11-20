import { NavLink } from 'react-router-dom'
import './Sidebar.css'

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1 className="logo">DataPurity</h1>
      </div>
      
      <nav className="sidebar-nav">
        <NavLink to="/dashboard" className="nav-item">
          📊 Dashboard
        </NavLink>
        
        <div className="nav-section">
          <div className="nav-section-title">Data Management</div>
          <NavLink to="/datasets/upload" className="nav-item">
            📤 Upload Dataset
          </NavLink>
          <NavLink to="/contacts" className="nav-item">
            👥 Contacts
          </NavLink>
        </div>
        
        <div className="nav-section">
          <div className="nav-section-title">Business Cards</div>
          <NavLink to="/cards/upload" className="nav-item">
            📇 Upload Cards
          </NavLink>
          <NavLink to="/cards/review" className="nav-item">
            ✏️ Review Cards
          </NavLink>
        </div>
        
        <div className="nav-section">
          <div className="nav-section-title">Operations</div>
          <NavLink to="/jobs" className="nav-item">
            ⚙️ Jobs
          </NavLink>
          <NavLink to="/exports" className="nav-item">
            📥 Exports
          </NavLink>
        </div>
        
        <div className="nav-section">
          <NavLink to="/billing" className="nav-item">
            💳 Billing
          </NavLink>
        </div>
      </nav>
    </aside>
  )
}

export default Sidebar
