import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import apiClient from '../../config/apiClient'
import './dashboard.css'

interface Stats {
  total_contacts: number
  cleaned_contacts: number
  pending_jobs: number
  success_rate: number
}

interface Activity {
  id: number
  type: string
  description: string
  timestamp: string
  status: 'success' | 'pending' | 'error'
}

function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [activities, setActivities] = useState<Activity[]>([])
  const [loading, setLoading] = useState(true)
  const [greeting, setGreeting] = useState('')

  useEffect(() => {
    fetchData()
    updateGreeting()
  }, [])

  const updateGreeting = () => {
    const hour = new Date().getHours()
    if (hour < 12) setGreeting('صباح الخير')
    else if (hour < 18) setGreeting('مساء الخير')
    else setGreeting('مساء الخير')
  }

  const fetchData = async () => {
    try {
      const [statsResponse] = await Promise.all([
        apiClient.get('/dashboard/stats').catch(() => ({ data: {
          total_contacts: 0,
          cleaned_contacts: 0,
          pending_jobs: 0,
          success_rate: 0
        }}))
      ])
      
      setStats(statsResponse.data)
      
      // Mock activities for demonstration
      setActivities([
        {
          id: 1,
          type: 'upload',
          description: 'تم رفع ملف جهات اتصال جديد',
          timestamp: new Date(Date.now() - 3600000).toISOString(),
          status: 'success'
        },
        {
          id: 2,
          type: 'clean',
          description: 'جاري تنظيف البيانات',
          timestamp: new Date(Date.now() - 7200000).toISOString(),
          status: 'pending'
        },
        {
          id: 3,
          type: 'export',
          description: 'تم تصدير 150 جهة اتصال',
          timestamp: new Date(Date.now() - 10800000).toISOString(),
          status: 'success'
        }
      ])
    } catch (error) {
      console.error('Failed to fetch data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getActivityIcon = (type: string) => {
    const icons: Record<string, string> = {
      upload: '📤',
      clean: '✨',
      export: '📥',
      scan: '📷'
    }
    return icons[type] || '📋'
  }

  const getStatusBadge = (status: string) => {
    const badges: Record<string, { text: string; class: string }> = {
      success: { text: 'مكتمل', class: 'success' },
      pending: { text: 'قيد التنفيذ', class: 'pending' },
      error: { text: 'فشل', class: 'error' }
    }
    return badges[status] || badges.success
  }

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const hours = Math.floor(diff / 3600000)
    
    if (hours < 1) return 'منذ لحظات'
    if (hours === 1) return 'منذ ساعة'
    if (hours < 24) return `منذ ${hours} ساعات`
    return date.toLocaleDateString('ar-SA')
  }

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>جاري تحميل البيانات...</p>
        </div>
      </div>
    )
  }

  const cleaningPercentage = stats?.total_contacts ? 
    (stats.cleaned_contacts / stats.total_contacts * 100) : 0

  return (
    <div className="dashboard-container">
      {/* Header Section */}
      <div className="dashboard-header">
        <div className="header-content">
          <h1 className="dashboard-title">
            {greeting} 👋
          </h1>
          <p className="dashboard-subtitle">
            مرحباً بك في لوحة التحكم. هنا يمكنك متابعة جميع عمليات تنظيف البيانات
          </p>
        </div>
        <div className="header-actions">
          <button className="refresh-btn" onClick={fetchData}>
            🔄 تحديث
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card stat-primary">
          <div className="stat-icon-wrapper">
            <div className="stat-icon">👥</div>
          </div>
          <div className="stat-details">
            <p className="stat-label">إجمالي جهات الاتصال</p>
            <h3 className="stat-value">{stats?.total_contacts.toLocaleString('ar-SA')}</h3>
            <div className="stat-trend positive">↗ زيادة عن الشهر الماضي</div>
          </div>
        </div>

        <div className="stat-card stat-success">
          <div className="stat-icon-wrapper">
            <div className="stat-icon">✨</div>
          </div>
          <div className="stat-details">
            <p className="stat-label">جهات منظفة</p>
            <h3 className="stat-value">{stats?.cleaned_contacts.toLocaleString('ar-SA')}</h3>
            <div className="stat-progress">
              <div className="progress-bar">
                <div 
                  className="progress-fill"
                  style={{ width: `${cleaningPercentage}%` }}
                ></div>
              </div>
              <span className="progress-text">{cleaningPercentage.toFixed(1)}%</span>
            </div>
          </div>
        </div>

        <div className="stat-card stat-warning">
          <div className="stat-icon-wrapper">
            <div className="stat-icon">⏳</div>
          </div>
          <div className="stat-details">
            <p className="stat-label">مهام قيد التنفيذ</p>
            <h3 className="stat-value">{stats?.pending_jobs.toLocaleString('ar-SA')}</h3>
            <div className="stat-trend neutral">جاري المعالجة</div>
          </div>
        </div>

        <div className="stat-card stat-info">
          <div className="stat-icon-wrapper">
            <div className="stat-icon">📊</div>
          </div>
          <div className="stat-details">
            <p className="stat-label">معدل النجاح</p>
            <h3 className="stat-value">{stats?.success_rate.toFixed(1)}%</h3>
            <div className="circular-progress">
              <svg width="60" height="60" viewBox="0 0 60 60">
                <circle
                  cx="30"
                  cy="30"
                  r="25"
                  fill="none"
                  stroke="#e5e7eb"
                  strokeWidth="6"
                />
                <circle
                  cx="30"
                  cy="30"
                  r="25"
                  fill="none"
                  stroke="#667eea"
                  strokeWidth="6"
                  strokeDasharray={`${(stats?.success_rate || 0) * 1.57} 157`}
                  strokeLinecap="round"
                  transform="rotate(-90 30 30)"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="dashboard-grid">
        {/* Quick Actions */}
        <div className="dashboard-card quick-actions-card">
          <div className="card-header">
            <h2 className="card-title">إجراءات سريعة</h2>
            <span className="card-badge">3</span>
          </div>
          <div className="quick-actions">
            <Link to="/app/datasets/upload" className="action-item action-upload">
              <div className="action-icon">📤</div>
              <div className="action-content">
                <h4>رفع بيانات</h4>
                <p>رفع ملف Excel أو CSV</p>
              </div>
              <div className="action-arrow">←</div>
            </Link>

            <Link to="/app/cards/upload" className="action-item action-scan">
              <div className="action-icon">📇</div>
              <div className="action-content">
                <h4>مسح بطاقات</h4>
                <p>استخراج البيانات من الصور</p>
              </div>
              <div className="action-arrow">←</div>
            </Link>

            <Link to="/app/contacts" className="action-item action-view">
              <div className="action-icon">📋</div>
              <div className="action-content">
                <h4>جهات الاتصال</h4>
                <p>عرض وإدارة البيانات</p>
              </div>
              <div className="action-arrow">←</div>
            </Link>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="dashboard-card activity-card">
          <div className="card-header">
            <h2 className="card-title">النشاط الأخير</h2>
            <Link to="#" className="view-all-link">عرض الكل</Link>
          </div>
          <div className="activity-list">
            {activities.length > 0 ? (
              activities.map((activity) => {
                const badge = getStatusBadge(activity.status)
                return (
                  <div key={activity.id} className="activity-item">
                    <div className="activity-icon">
                      {getActivityIcon(activity.type)}
                    </div>
                    <div className="activity-content">
                      <p className="activity-description">{activity.description}</p>
                      <span className="activity-time">{formatTimestamp(activity.timestamp)}</span>
                    </div>
                    <span className={`activity-status status-${badge.class}`}>
                      {badge.text}
                    </span>
                  </div>
                )
              })
            ) : (
              <div className="empty-state">
                <div className="empty-icon">📭</div>
                <p>لا توجد أنشطة حالياً</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Features Showcase */}
      <div className="features-section">
        <h2 className="section-title">ميزات DataPurity</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>تنظيف ذكي</h3>
            <p>استخدام الذكاء الاصطناعي لتنظيف وتنظيم البيانات تلقائياً</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>معالجة سريعة</h3>
            <p>معالجة آلاف السجلات في ثوانٍ معدودة</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <h3>أمان عالي</h3>
            <p>حماية بياناتك بأعلى معايير الأمان</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>تقارير تفصيلية</h3>
            <p>احصل على تقارير شاملة عن جودة بياناتك</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage

