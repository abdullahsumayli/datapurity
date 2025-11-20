import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../../config/apiClient'

interface Job {
  id: string
  type: string
  status: string
  created_at: string
  completed_at?: string
  progress: number
}

function JobsListPage() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    fetchJobs()
    const interval = setInterval(fetchJobs, 5000) // تحديث كل 5 ثواني
    return () => clearInterval(interval)
  }, [])

  const fetchJobs = async () => {
    try {
      const response = await apiClient.get('/jobs')
      setJobs(response.data)
    } catch (error) {
      console.error('Failed to fetch jobs:', error)
    } finally {
      setLoading(false)
    }
  }

  const getJobTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      'dataset_cleaning': 'تنظيف البيانات',
      'card_ocr': 'استخراج من البطاقات',
      'export': 'تصدير البيانات'
    }
    return labels[type] || type
  }

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      'pending': 'قيد الانتظار',
      'processing': 'جاري المعالجة',
      'completed': 'مكتمل',
      'failed': 'فشل'
    }
    return labels[status] || status
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
        <h1>المهام الخلفية</h1>
        <p className="page-description">
          راقب حالة مهام معالجة البيانات
        </p>
      </div>

      <div className="jobs-table">
        <table>
          <thead>
            <tr>
              <th>النوع</th>
              <th>الحالة</th>
              <th>التقدم</th>
              <th>تاريخ الإنشاء</th>
              <th>الإجراءات</th>
            </tr>
          </thead>
          <tbody>
            {jobs.length === 0 ? (
              <tr>
                <td colSpan={5} className="no-data">لا توجد مهام</td>
              </tr>
            ) : (
              jobs.map(job => (
                <tr key={job.id}>
                  <td>{getJobTypeLabel(job.type)}</td>
                  <td>
                    <span className={`status-badge status-${job.status}`}>
                      {getStatusLabel(job.status)}
                    </span>
                  </td>
                  <td>
                    <div className="progress-bar">
                      <div 
                        className="progress-fill" 
                        style={{ width: `${job.progress}%` }}
                      />
                      <span className="progress-text">{job.progress}%</span>
                    </div>
                  </td>
                  <td>{new Date(job.created_at).toLocaleDateString('ar-SA')}</td>
                  <td>
                    <button 
                      className="btn-link"
                      onClick={() => navigate(`/app/jobs/${job.id}`)}
                    >
                      عرض التفاصيل
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <style>{`
        .jobs-table {
          background: white;
          border-radius: 12px;
          overflow: hidden;
          margin-top: 2rem;
        }

        table {
          width: 100%;
          border-collapse: collapse;
        }

        thead {
          background: #f8f9ff;
        }

        th {
          padding: 1rem;
          text-align: right;
          font-weight: 600;
          color: #1e40af;
        }

        td {
          padding: 1rem;
          border-top: 1px solid #e5e7eb;
        }

        .no-data {
          text-align: center;
          color: #6b7280;
          padding: 3rem;
        }

        .status-badge {
          display: inline-block;
          padding: 0.25rem 0.75rem;
          border-radius: 12px;
          font-size: 0.875rem;
          font-weight: 600;
        }

        .status-pending {
          background: #fef3c7;
          color: #92400e;
        }

        .status-processing {
          background: #dbeafe;
          color: #1e40af;
        }

        .status-completed {
          background: #d1fae5;
          color: #065f46;
        }

        .status-failed {
          background: #fee2e2;
          color: #991b1b;
        }

        .progress-bar {
          position: relative;
          width: 100%;
          height: 24px;
          background: #f3f4f6;
          border-radius: 12px;
          overflow: hidden;
        }

        .progress-fill {
          position: absolute;
          right: 0;
          top: 0;
          height: 100%;
          background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
          transition: width 0.3s;
        }

        .progress-text {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
          font-size: 0.75rem;
          font-weight: 600;
          color: #1f2937;
          z-index: 1;
        }

        .btn-link {
          background: none;
          border: none;
          color: #667eea;
          cursor: pointer;
          text-decoration: underline;
        }

        .btn-link:hover {
          color: #764ba2;
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

export default JobsListPage
