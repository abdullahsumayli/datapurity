import { NavLink } from 'react-router-dom'
import './Sidebar.css'

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <svg width="32" height="32" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
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
          <span>DataPurity</span>
        </div>
      </div>
      
      <nav className="sidebar-nav">
        <NavLink to="/app/dashboard" className="nav-item">
          <span className="nav-icon">📊</span>
          <span className="nav-text">لوحة التحكم</span>
        </NavLink>
        
        <NavLink to="/app/datasets/upload" className="nav-item">
          <span className="nav-icon">📤</span>
          <span className="nav-text">رفع ملف بيانات</span>
        </NavLink>
        
        <NavLink to="/app/contacts" className="nav-item">
          <span className="nav-icon">👥</span>
          <span className="nav-text">جهات الاتصال</span>
        </NavLink>
        
        <NavLink to="/app/cards/upload" className="nav-item">
          <span className="nav-icon">📇</span>
          <span className="nav-text">رفع البطاقات</span>
        </NavLink>
        
        <NavLink to="/app/cards/review" className="nav-item">
          <span className="nav-icon">✏️</span>
          <span className="nav-text">مراجعة البطاقات</span>
        </NavLink>
        
        <NavLink to="/app/jobs" className="nav-item">
          <span className="nav-icon">⚙️</span>
          <span className="nav-text">المهام الخلفية</span>
        </NavLink>
        
        <NavLink to="/app/exports" className="nav-item">
          <span className="nav-icon">📥</span>
          <span className="nav-text">التصديرات</span>
        </NavLink>
        
        <NavLink to="/app/billing" className="nav-item">
          <span className="nav-icon">💳</span>
          <span className="nav-text">الفوترة والاشتراك</span>
        </NavLink>
        
        <NavLink to="/app/profile" className="nav-item">
          <span className="nav-icon">👤</span>
          <span className="nav-text">الملف الشخصي</span>
        </NavLink>
      </nav>
    </aside>
  )
}

export default Sidebar
