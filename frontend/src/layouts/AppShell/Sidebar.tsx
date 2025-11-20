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
          <span>📊</span> لوحة التحكم
        </NavLink>
        
        <div className="nav-section">
          <div className="nav-section-title">إدارة البيانات</div>
          <NavLink to="/app/datasets/upload" className="nav-item">
            <span>📤</span> رفع ملف بيانات
          </NavLink>
          <NavLink to="/app/contacts" className="nav-item">
            <span>👥</span> جهات الاتصال
          </NavLink>
        </div>
        
        <div className="nav-section">
          <div className="nav-section-title">بطاقات الأعمال</div>
          <NavLink to="/app/cards/upload" className="nav-item">
            <span>📇</span> رفع البطاقات
          </NavLink>
          <NavLink to="/app/cards/review" className="nav-item">
            <span>✏️</span> مراجعة البطاقات
          </NavLink>
        </div>
        
        <div className="nav-section">
          <div className="nav-section-title">العمليات</div>
          <NavLink to="/app/jobs" className="nav-item">
            <span>⚙️</span> المهام الخلفية
          </NavLink>
          <NavLink to="/app/exports" className="nav-item">
            <span>📥</span> التصديرات
          </NavLink>
        </div>
        
        <div className="nav-section">
          <NavLink to="/app/billing" className="nav-item">
            <span>💳</span> الفوترة والاشتراك
          </NavLink>
          <NavLink to="/app/profile" className="nav-item">
            <span>👤</span> الملف الشخصي
          </NavLink>
        </div>
      </nav>
    </aside>
  )
}

export default Sidebar
