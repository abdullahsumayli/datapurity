import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../../config/apiClient'
import { useAuth } from '../../contexts/AuthContext'
import './admin.css'

interface User {
  id: number
  email: string
  full_name: string
  is_active: boolean
  is_superuser: boolean
  created_at: string
  total_contacts: number
  total_jobs: number
}

interface AdminStats {
  total_users: number
  active_users: number
  total_contacts: number
  total_jobs: number
  completed_jobs: number
}

function AdminDashboard() {
  const navigate = useNavigate()
  const { isAuthenticated, user } = useAuth()
  const [users, setUsers] = useState<User[]>([])
  const [stats, setStats] = useState<AdminStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchAdminData = async () => {
    try {
      setError(null)
      console.log('Fetching admin data...')
      const [usersRes, statsRes] = await Promise.all([
        apiClient.get('/users/admin/users'),
        apiClient.get('/users/admin/stats')
      ])
      
      setUsers(usersRes.data)
      setStats(statsRes.data)
      console.log('Admin data loaded successfully')
    } catch (error: any) {
      console.error('Failed to fetch admin data:', error)
      console.error('Error response:', error.response)
      if (error.response?.status === 403) {
        setError('ليس لديك صلاحيات الوصول إلى لوحة التحكم - تأكد من أنك مسجل دخول كمستخدم superuser')
      } else if (error.response?.status === 401) {
        setError('يجب تسجيل الدخول أولاً')
      } else {
        setError(`فشل تحميل البيانات: ${error.response?.data?.detail || error.message}`)
      }
    } finally {
      setLoading(false)
    }
  }

  // فحص تسجيل الدخول
  useEffect(() => {
    console.log('AdminDashboard: isAuthenticated=', isAuthenticated, 'user=', user)
    if (!isAuthenticated) {
      console.log('Not authenticated, redirecting to login')
      navigate('/login')
      return
    }
    console.log('User authenticated, fetching admin data')
    fetchAdminData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated])

  const changePlan = async (userId: number, newPlan: string) => {
    if (!confirm(`هل تريد تغيير باقة هذا المستخدم إلى ${newPlan}؟`)) {
      return
    }

    try {
      await apiClient.post(`/users/admin/users/${userId}/change-plan`, {
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
    navigate('/app/dashboard')
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ar-SA')
  }

  if (loading) {
    return (
      <div className="admin-container">
        <div className="loading">جاري التحميل...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="admin-container">
        <div className="error-banner">
          <span className="error-icon">⚠️</span>
          {error}
        </div>
      </div>
    )
  }

  return (
    <div className="admin-container">
      <div className="admin-header">
        <div>
          <h1>لوحة التحكم الإدارية</h1>
          <p>إدارة المستخدمين والنظام</p>
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
              <h3>مستخدمون نشطون</h3>
              <p className="stat-value">{stats.active_users}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">👤</div>
            <div className="stat-content">
              <h3>جهات الاتصال</h3>
              <p className="stat-value">{stats.total_contacts}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-content">
              <h3>إجمالي المهام</h3>
              <p className="stat-value">{stats.total_jobs}</p>
            </div>
          </div>

          <div className="stat-card stat-card-success">
            <div className="stat-icon">✓</div>
            <div className="stat-content">
              <h3>مهام مكتملة</h3>
              <p className="stat-value">{stats.completed_jobs}</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📈</div>
            <div className="stat-content">
              <h3>معدل النجاح</h3>
              <p className="stat-value">
                {stats.total_jobs > 0 
                  ? Math.round((stats.completed_jobs / stats.total_jobs) * 100) 
                  : 0}%
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Users Table */}
      <div className="users-table-container">
        <h2>المستخدمون</h2>
        <table className="users-table">
          <thead>
            <tr>
              <th>المعرف</th>
              <th>البريد الإلكتروني</th>
              <th>الاسم</th>
              <th>جهات الاتصال</th>
              <th>المهام</th>
              <th>الحالة</th>
              <th>صلاحية الإدارة</th>
              <th>تاريخ التسجيل</th>
              <th>إجراءات</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td>{user.id}</td>
                <td>{user.email}</td>
                <td className="user-name">{user.full_name || 'غير محدد'}</td>
                <td>{user.total_contacts}</td>
                <td>{user.total_jobs}</td>
                <td>
                  <span className={`status-badge status-${user.is_active ? 'active' : 'inactive'}`}>
                    {user.is_active ? 'نشط' : 'غير نشط'}
                  </span>
                </td>
                <td>
                  <span className={`status-badge ${user.is_superuser ? 'admin-badge' : ''}`}>
                    {user.is_superuser ? 'مدير' : 'مستخدم عادي'}
                  </span>
                </td>
                <td>{formatDate(user.created_at)}</td>
                <td>
                  <div className="action-btns">
                    <select 
                      onChange={(e) => changePlan(user.id, e.target.value)}
                      className="plan-select"
                      defaultValue=""
                    >
                      <option value="" disabled>تغيير الباقة</option>
                      <option value="free">مجاني</option>
                      <option value="pro">احترافي</option>
                      <option value="enterprise">مؤسسي</option>
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
