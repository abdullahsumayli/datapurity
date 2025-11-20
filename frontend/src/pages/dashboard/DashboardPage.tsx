import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import apiClient from '../../config/apiClient'

interface Stats {
  total_contacts: number
  cleaned_contacts: number
  pending_jobs: number
  success_rate: number
}

function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await apiClient.get('/dashboard/stats')
      setStats(response.data)
    } catch (error) {
      console.error('Failed to fetch stats:', error)
      // Set default stats if API fails
      setStats({
        total_contacts: 0,
        cleaned_contacts: 0,
        pending_jobs: 0,
        success_rate: 0
      })
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading">جاري التحميل...</div>
      </div>
    )
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>لوحة التحكم</h1>
        <p className="page-description">
          مرحباً في DataPurity. اطلع على إحصائيات جودة البيانات والنشاطات الأخيرة.
        </p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <div className="stat-value">{stats?.total_contacts.toLocaleString('ar-SA')}</div>
            <div className="stat-label">إجمالي جهات الاتصال</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">✨</div>
          <div className="stat-content">
            <div className="stat-value">{stats?.cleaned_contacts.toLocaleString('ar-SA')}</div>
            <div className="stat-label">جهات اتصال منظفة</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⏳</div>
          <div className="stat-content">
            <div className="stat-value">{stats?.pending_jobs.toLocaleString('ar-SA')}</div>
            <div className="stat-label">مهام قيد التنفيذ</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <div className="stat-value">{stats?.success_rate.toFixed(1)}%</div>
            <div className="stat-label">معدل النجاح</div>
          </div>
        </div>
      </div>

      <div className="dashboard-section">
        <h2>البدء السريع</h2>
        <div className="quick-actions">
          <Link to="/app/datasets/upload" className="action-card">
            <div className="action-icon">📤</div>
            <h3>رفع بيانات جديدة</h3>
            <p>ارفع ملف Excel أو CSV لتنظيف البيانات</p>
          </Link>

          <Link to="/app/cards/upload" className="action-card">
            <div className="action-icon">📇</div>
            <h3>مسح بطاقات أعمال</h3>
            <p>استخرج البيانات من صور البطاقات</p>
          </Link>

          <Link to="/app/contacts" className="action-card">
            <div className="action-icon">📋</div>
            <h3>عرض جهات الاتصال</h3>
            <p>تصفح وإدارة جهات الاتصال المحفوظة</p>
          </Link>
        </div>
      </div>

      <style>{`
        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 1.5rem;
          margin: 2rem 0;
        }

        .stat-card {
          background: white;
          border-radius: 12px;
          padding: 1.5rem;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
          display: flex;
          align-items: center;
          gap: 1rem;
          transition: transform 0.2s;
        }

        .stat-card:hover {
          transform: translateY(-4px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .stat-icon {
          font-size: 2.5rem;
        }

        .stat-content {
          flex: 1;
        }

        .stat-value {
          font-size: 2rem;
          font-weight: bold;
          color: #1e40af;
          margin-bottom: 0.25rem;
        }

        .stat-label {
          color: #6b7280;
          font-size: 0.875rem;
        }

        .dashboard-section {
          margin-top: 3rem;
        }

        .dashboard-section h2 {
          font-size: 1.5rem;
          margin-bottom: 1.5rem;
          color: #111827;
        }

        .quick-actions {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 1.5rem;
        }

        .action-card {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 2rem;
          border-radius: 12px;
          text-decoration: none;
          transition: transform 0.2s;
        }

        .action-card:hover {
          transform: translateY(-4px);
        }

        .action-icon {
          font-size: 3rem;
          margin-bottom: 1rem;
        }

        .action-card h3 {
          font-size: 1.25rem;
          margin-bottom: 0.5rem;
          color: white;
        }

        .action-card p {
          color: rgba(255, 255, 255, 0.9);
          font-size: 0.875rem;
        }

        .loading {
          text-align: center;
          padding: 3rem;
          font-size: 1.25rem;
          color: #6b7280;
        }
      `}</style>
    </div>
  )
}

export default DashboardPage

