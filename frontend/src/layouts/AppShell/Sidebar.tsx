import { NavLink } from 'react-router-dom'
import './Sidebar.css'

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1 className="logo">DataPurity</h1>
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
