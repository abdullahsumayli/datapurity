import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../../config/apiClient'
import './admin.css'

interface User {
  id: number
  email: string
  full_name: string
  created_at: string
  subscription?: {
    plan: string
    status: string
    current_period_end: string
    usage: {
      cleaning?: { used: number; limit: number }
      ocr?: { used: number; limit: number }
    }
  }
}

interface PlanStats {
  total_users: number
  active_subscriptions: number
  free_users: number
  starter_users: number
  business_users: number
  monthly_revenue: number
}

function AdminDashboard() {
  const navigate = useNavigate()
  const [users, setUsers] = useState<User[]>([])
  const [stats, setStats] = useState<PlanStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedPlan, setSelectedPlan] = useState<string>('all')

  const fetchAdminData = async () => {
    try {
      // Note: هذه الـ endpoints تحتاج إلى إضافتها في الـ backend
      const [usersRes, statsRes] = await Promise.all([
        apiClient.get('/admin/users', {
          params: { plan: selectedPlan !== 'all' ? selectedPlan : undefined }
        }),
        apiClient.get('/admin/stats')
      ])
      
      setUsers(usersRes.data)
      setStats(statsRes.data)
    } catch (error) {
      console.error('Failed to fetch admin data:', error)
    } finally {
      setLoading(false)
    }
  }

  // فحص تسجيل الدخول
  useEffect(() => {
    const isAuthenticated = sessionStorage.getItem('adminAuthenticated')
    if (!isAuthenticated) {
      navigate('/admin/login')
      return
    }
    fetchAdminData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    fetchAdminData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedPlan])

  const changePlan = async (userId: number, newPlan: string) => {
    if (!confirm(`هل تريد تغيير باقة هذا المستخدم إلى ${newPlan}؟`)) {
      return
    }

    try {
      await apiClient.post(`/admin/users/${userId}/change-plan`, {
        plan: newPlan
      })
      
      alert('تم تغيير الباقة بنجاح')
      fetchAdminData()
    } catch (error) {
      alert('فشل تغيير الباقة')
      console.error(error)
    }
  }

  const handleLogout = () => {
    sessionStorage.removeItem('adminAuthenticated')
    sessionStorage.removeItem('adminLoginTime')
    navigate('/admin/login')
  }

  const getPlanBadgeClass = (plan: string) => {
    const classes: Record<string, string> = {
      free: 'plan-badge-free',
      starter: 'plan-badge-starter',
      business: 'plan-badge-business'
    }
    return classes[plan] || 'plan-badge-default'
  }

  const getPlanName = (plan: string) => {
    const names: Record<string, string> = {
      free: 'مجاني',
      starter: 'مبتدئ',
      business: 'أعمال'
    }
    return names[plan] || plan
  }

  if (loading) {
    return (
      <div className="admin-container">
        <div className="loading">جاري التحميل...</div>
      </div>
    )
  }

  return (
    <div className="admin-container">
      <div className="admin-header">
        <div>
          <h1>لوحة التحكم الإدارية</h1>
          <p>إدارة المستخدمين والباقات</p>
        </div>
        <button onClick={handleLogout} className="logout-btn">
          <span>🚪</span>
          تسجيل الخروج
        </button>
      </div>

      {/* Statistics Cards */}
      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">👥</div>
            <div className="stat-content">
              <h3>إجمالي المستخدمين</h3>
              <p className="stat-value">{stats.total_users}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">✅</div>
            <div className="stat-content">
              <h3>اشتراكات نشطة</h3>
              <p className="stat-value">{stats.active_subscriptions}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🆓</div>
            <div className="stat-content">
              <h3>باقة مجانية</h3>
              <p className="stat-value">{stats.free_users}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🚀</div>
            <div className="stat-content">
              <h3>باقة مبتدئ</h3>
              <p className="stat-value">{stats.starter_users}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">💼</div>
            <div className="stat-content">
              <h3>باقة أعمال</h3>
              <p className="stat-value">{stats.business_users}</p>
            </div>
          </div>

          <div className="stat-card stat-card-revenue">
            <div className="stat-icon">💰</div>
            <div className="stat-content">
              <h3>الإيرادات الشهرية</h3>
              <p className="stat-value">{stats.monthly_revenue.toFixed(2)} ريال</p>
            </div>
          </div>
        </div>
      )}

      {/* Filter */}
      <div className="filter-section">
        <label>تصفية حسب الباقة:</label>
        <select 
          value={selectedPlan} 
          onChange={(e) => setSelectedPlan(e.target.value)}
          className="plan-filter"
        >
          <option value="all">جميع الباقات</option>
          <option value="free">مجاني</option>
          <option value="starter">مبتدئ</option>
          <option value="business">أعمال</option>
        </select>
      </div>

      {/* Users Table */}
      <div className="users-table-container">
        <h2>المستخدمون</h2>
        <table className="users-table">
          <thead>
            <tr>
              <th>المستخدم</th>
              <th>البريد الإلكتروني</th>
              <th>الباقة</th>
              <th>الحالة</th>
              <th>الاستخدام</th>
              <th>تاريخ الانتهاء</th>
              <th>إجراءات</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td className="user-name">{user.full_name || 'غير محدد'}</td>
                <td>{user.email}</td>
                <td>
                  <span className={`plan-badge ${getPlanBadgeClass(user.subscription?.plan || 'free')}`}>
                    {getPlanName(user.subscription?.plan || 'free')}
                  </span>
                </td>
                <td>
                  <span className={`status-badge status-${user.subscription?.status || 'inactive'}`}>
                    {user.subscription?.status === 'active' ? 'نشط' : 'غير نشط'}
                  </span>
                </td>
                <td>
                  {user.subscription?.usage && (
                    <div className="usage-mini">
                      <small>
                        تنظيف: {user.subscription.usage.cleaning?.used}/{user.subscription.usage.cleaning?.limit}
                        <br />
                        كروت: {user.subscription.usage.ocr?.used}/{user.subscription.usage.ocr?.limit}
                      </small>
                    </div>
                  )}
                </td>
                <td>
                  {user.subscription?.current_period_end ? (
                    new Date(user.subscription.current_period_end).toLocaleDateString('ar-SA')
                  ) : '-'}
                </td>
                <td>
                  <div className="action-buttons">
                    <select
                      onChange={(e) => changePlan(user.id, e.target.value)}
                      defaultValue=""
                      className="plan-change-select"
                    >
                      <option value="" disabled>تغيير الباقة</option>
                      <option value="free">مجاني</option>
                      <option value="starter">مبتدئ</option>
                      <option value="business">أعمال</option>
                    </select>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default AdminDashboard
