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
  const [activeTab, setActiveTab] = useState<'overview' | 'analytics' | 'activity'>('overview')
  const [isExpanded, setIsExpanded] = useState(false)

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
      {/* Enhanced Header Section */}
      <div className="dashboard-header">
        <div className="header-top">
          <div className="header-content">
            <h1 className="dashboard-title">
              {greeting} 👋
            </h1>
            <p className="dashboard-subtitle">
              آخر تحديث: {new Date().toLocaleString('ar-SA', { hour: '2-digit', minute: '2-digit' })}
            </p>
          </div>
          <div className="header-actions">
            <button className="action-btn action-btn-secondary" onClick={fetchData}>
              <span className="btn-icon">🔄</span>
              تحديث
            </button>
            <Link to="/app/datasets/upload" className="action-btn action-btn-primary">
              <span className="btn-icon">➕</span>
              إضافة بيانات
            </Link>
          </div>
        </div>
        
        {/* Navigation Tabs */}
        <div className="dashboard-tabs">
          <button 
            className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            <span className="tab-icon">📊</span>
            نظرة عامة
          </button>
          <button 
            className={`tab-btn ${activeTab === 'analytics' ? 'active' : ''}`}
            onClick={() => setActiveTab('analytics')}
          >
            <span className="tab-icon">📈</span>
            التحليلات
          </button>
          <button 
            className={`tab-btn ${activeTab === 'activity' ? 'active' : ''}`}
            onClick={() => setActiveTab('activity')}
          >
            <span className="tab-icon">⚡</span>
            النشاط الأخير
          </button>
        </div>
      </div>

      {/* Enhanced Stats Cards */}
      {activeTab === 'overview' && (
        <div className="stats-grid">
          <div className="stat-card stat-primary">
            <div className="stat-header">
              <div className="stat-icon-wrapper">
                <div className="stat-icon">👥</div>
              </div>
              <div className="stat-meta">
                <p className="stat-label">إجمالي جهات الاتصال</p>
                <span className="stat-info-icon" title="العدد الكلي للجهات المسجلة">ℹ️</span>
              </div>
            </div>
            <div className="stat-body">
              <h3 className="stat-value">{stats?.total_contacts.toLocaleString('ar-SA')}</h3>
              <div className="stat-comparison">
                <span className="comparison-badge positive">
                  <span className="badge-icon">↗</span>
                  <span className="badge-value">+12.5%</span>
                </span>
                <span className="comparison-text">مقارنة بالشهر الماضي</span>
              </div>
            </div>
            <div className="stat-footer">
              <span className="stat-detail">📅 آخر إضافة: منذ ساعتين</span>
            </div>
          </div>

          <div className="stat-card stat-success">
            <div className="stat-header">
              <div className="stat-icon-wrapper">
                <div className="stat-icon">✨</div>
              </div>
              <div className="stat-meta">
                <p className="stat-label">جهات منظفة</p>
                <span className="stat-info-icon" title="البيانات التي تم تنظيفها بنجاح">ℹ️</span>
              </div>
            </div>
            <div className="stat-body">
              <h3 className="stat-value">{stats?.cleaned_contacts.toLocaleString('ar-SA')}</h3>
              <div className="stat-progress-enhanced">
                <div className="progress-info">
                  <span className="progress-label">نسبة الإنجاز</span>
                  <span className="progress-percentage">{cleaningPercentage.toFixed(1)}%</span>
                </div>
                <div className="progress-bar-modern">
                  <div 
                    className="progress-fill-animated"
                    style={{ width: `${cleaningPercentage}%` }}
                  >
                    <span className="progress-glow"></span>
                  </div>
                </div>
                <div className="progress-milestones">
                  <span className="milestone" style={{ left: '50%' }}>50%</span>
                  <span className="milestone" style={{ left: '100%' }}>100%</span>
                </div>
              </div>
            </div>
            <div className="stat-footer">
              <span className="stat-detail">⚡ متوسط الوقت: 2.3 ثانية/جهة</span>
            </div>
          </div>

          <div className="stat-card stat-warning">
            <div className="stat-header">
              <div className="stat-icon-wrapper">
                <div className="stat-icon stat-icon-pulse">⏳</div>
              </div>
              <div className="stat-meta">
                <p className="stat-label">مهام قيد التنفيذ</p>
                <span className="stat-badge live">مباشر</span>
              </div>
            </div>
            <div className="stat-body">
              <h3 className="stat-value">{stats?.pending_jobs.toLocaleString('ar-SA')}</h3>
              <div className="stat-queue">
                <div className="queue-bar">
                  <div className="queue-item"></div>
                  <div className="queue-item"></div>
                  <div className="queue-item active"></div>
                </div>
                <span className="queue-text">معالجة نشطة</span>
              </div>
            </div>
            <div className="stat-footer">
              <span className="stat-detail">⏱️ الوقت المتبقي: ~15 دقيقة</span>
            </div>
          </div>

          <div className="stat-card stat-info">
            <div className="stat-header">
              <div className="stat-icon-wrapper">
                <div className="stat-icon">📊</div>
              </div>
              <div className="stat-meta">
                <p className="stat-label">معدل النجاح</p>
                <span className="stat-quality excellent">ممتاز</span>
              </div>
            </div>
            <div className="stat-body stat-body-chart">
              <div className="chart-container">
                <svg className="circular-chart" width="100" height="100" viewBox="0 0 100 100">
                  <circle
                    cx="50"
                    cy="50"
                    r="40"
                    fill="none"
                    stroke="#e5e7eb"
                    strokeWidth="8"
                  />
                  <circle
                    className="progress-ring"
                    cx="50"
                    cy="50"
                    r="40"
                    fill="none"
                    stroke="url(#gradient)"
                    strokeWidth="8"
                    strokeDasharray={`${(stats?.success_rate || 0) * 2.51} 251.2`}
                    strokeLinecap="round"
                    transform="rotate(-90 50 50)"
                  />
                  <defs>
                    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#667eea" />
                      <stop offset="100%" stopColor="#764ba2" />
                    </linearGradient>
                  </defs>
                </svg>
                <div className="chart-center">
                  <h3 className="chart-value">{stats?.success_rate.toFixed(1)}%</h3>
                </div>
              </div>
            </div>
            <div className="stat-footer">
              <span className="stat-detail">🎯 الهدف: 95%</span>
            </div>
          </div>
        </div>
      )}

      {/* Enhanced Main Content */}
      {activeTab === 'overview' && (
        <div className="dashboard-grid">
          {/* Simplified Quick Actions */}
          <div className="dashboard-card quick-actions-card">
            <div className="card-header">
              <h2 className="card-title">
                <span className="title-icon">⚡</span>
                إجراءات سريعة
              </h2>
            </div>
            <div className="quick-actions-modern">
              <Link to="/app/datasets/upload" className="action-card">
                <div className="action-card-icon">📤</div>
                <h4 className="action-card-title">رفع بيانات</h4>
                <p className="action-card-desc">رفع ملف Excel أو CSV</p>
                <div className="action-card-overlay">
                  <span className="overlay-text">ابدأ الآن ←</span>
                </div>
              </Link>

              <Link to="/app/cards/upload" className="action-card">
                <div className="action-card-icon">📇</div>
                <h4 className="action-card-title">مسح بطاقات</h4>
                <p className="action-card-desc">استخراج من الصور</p>
                <div className="action-card-overlay">
                  <span className="overlay-text">ابدأ الآن ←</span>
                </div>
              </Link>

              <Link to="/app/contacts" className="action-card">
                <div className="action-card-icon">📋</div>
                <h4 className="action-card-title">جهات الاتصال</h4>
                <p className="action-card-desc">عرض وإدارة البيانات</p>
                <div className="action-card-overlay">
                  <span className="overlay-text">عرض الكل ←</span>
                </div>
              </Link>
            </div>
          </div>

          {/* Timeline Activity */}
          <div className="dashboard-card activity-card">
            <div className="card-header">
              <h2 className="card-title">
                <span className="title-icon">📋</span>
                النشاط الأخير
              </h2>
              <button className="expand-btn" onClick={() => setIsExpanded(!isExpanded)}>
                {isExpanded ? 'طي ↑' : 'عرض المزيد ↓'}
              </button>
            </div>
            <div className="activity-timeline">
              {activities.length > 0 ? (
                activities.slice(0, isExpanded ? activities.length : 3).map((activity, index) => {
                  const badge = getStatusBadge(activity.status)
                  return (
                    <div key={activity.id} className="timeline-item">
                      <div className="timeline-marker">
                        <div className={`marker-dot status-${badge.class}`}></div>
                        {index < activities.length - 1 && <div className="marker-line"></div>}
                      </div>
                      <div className="timeline-content">
                        <div className="timeline-header">
                          <span className="timeline-icon">{getActivityIcon(activity.type)}</span>
                          <span className="timeline-time">{formatTimestamp(activity.timestamp)}</span>
                        </div>
                        <p className="timeline-description">{activity.description}</p>
                        <span className={`timeline-badge status-${badge.class}`}>
                          <span className="badge-dot"></span>
                          {badge.text}
                        </span>
                      </div>
                    </div>
                  )
                })
              ) : (
                <div className="empty-state-modern">
                  <div className="empty-illustration">📭</div>
                  <h4>لا توجد أنشطة بعد</h4>
                  <p>ابدأ برفع البيانات لرؤية النشاط هنا</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Analytics Tab */}
      {activeTab === 'analytics' && (
        <div className="analytics-section">
          <div className="dashboard-card chart-card">
            <div className="card-header">
              <h2 className="card-title">
                <span className="title-icon">📈</span>
                نشاط التنظيف الأسبوعي
              </h2>
            </div>
            <div className="chart-placeholder">
              <div className="bar-chart">
                {['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'].map((day, i) => (
                  <div key={day} className="bar-item">
                    <div className="bar" style={{ height: `${Math.random() * 100}%` }}>
                      <span className="bar-value">{Math.floor(Math.random() * 500)}</span>
                    </div>
                    <span className="bar-label">{day}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          <div className="analytics-grid">
            <div className="dashboard-card mini-card">
              <h4>أكثر الأيام نشاطاً</h4>
              <p className="mini-value">الأحد</p>
              <span className="mini-detail">423 عملية</span>
            </div>
            <div className="dashboard-card mini-card">
              <h4>متوسط الوقت</h4>
              <p className="mini-value">2.3 ثانية</p>
              <span className="mini-detail">لكل جهة اتصال</span>
            </div>
            <div className="dashboard-card mini-card">
              <h4>توفير الوقت</h4>
              <p className="mini-value">15 ساعة</p>
              <span className="mini-detail">هذا الأسبوع</span>
            </div>
          </div>
        </div>
      )}

      {/* Activity Tab */}
      {activeTab === 'activity' && (
        <div className="activity-full-section">
          <div className="dashboard-card">
            <div className="card-header">
              <h2 className="card-title">
                <span className="title-icon">⚡</span>
                سجل النشاط الكامل
              </h2>
              <div className="filter-buttons">
                <button className="filter-btn active">الكل</button>
                <button className="filter-btn">نجاح</button>
                <button className="filter-btn">قيد التنفيذ</button>
                <button className="filter-btn">أخطاء</button>
              </div>
            </div>
            <div className="activity-timeline-full">
              {activities.map((activity, index) => {
                const badge = getStatusBadge(activity.status)
                return (
                  <div key={activity.id} className="timeline-item-full">
                    <div className="timeline-marker">
                      <div className={`marker-dot status-${badge.class}`}></div>
                      {index < activities.length - 1 && <div className="marker-line"></div>}
                    </div>
                    <div className="timeline-content-full">
                      <div className="timeline-header">
                        <span className="timeline-icon">{getActivityIcon(activity.type)}</span>
                        <span className="timeline-time">{formatTimestamp(activity.timestamp)}</span>
                      </div>
                      <p className="timeline-description">{activity.description}</p>
                      <span className={`timeline-badge status-${badge.class}`}>
                        <span className="badge-dot"></span>
                        {badge.text}
                      </span>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      )}

      {/* Features Showcase */}
      {activeTab === 'overview' && (
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
      )}
    </div>
  )
}

export default DashboardPage

