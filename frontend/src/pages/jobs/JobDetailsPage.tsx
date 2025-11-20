import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import apiClient from '../../config/apiClient'

interface JobDetail {
  id: string
  type: string
  status: string
  progress: number
  created_at: string
  completed_at?: string
  error_message?: string
  result?: {
    total_processed: number
    successful: number
    failed: number
  }
}

function JobDetailsPage() {
  const { id } = useParams()
  const [job, setJob] = useState<JobDetail | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchJob()
    const interval = setInterval(fetchJob, 3000)
    return () => clearInterval(interval)
  }, [id])

  const fetchJob = async () => {
    try {
      const response = await apiClient.get(`/jobs/${id}`)
      setJob(response.data)
    } catch (error) {
      console.error('Failed to fetch job:', error)
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

  if (!job) {
    return (
      <div className="page-container">
        <div className="error">لم يتم العثور على المهمة</div>
      </div>
    )
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>تفاصيل المهمة #{job.id.slice(0, 8)}</h1>
        <p className="page-description">
          تم الإنشاء في {new Date(job.created_at).toLocaleDateString('ar-SA')}
        </p>
      </div>

      <div className="status-section">
        <div className={`status-card status-${job.status}`}>
          <h3>الحالة: {job.status}</h3>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${job.progress}%` }} />
            <span className="progress-text">{job.progress}%</span>
          </div>
        </div>
      </div>

      {job.result && (
        <div className="results-section">
          <h2>نتائج المعالجة</h2>
          <div className="results-grid">
            <div className="result-card">
              <div className="result-icon">📊</div>
              <div className="result-value">{job.result.total_processed}</div>
              <div className="result-label">إجمالي المعالجة</div>
            </div>
            <div className="result-card success">
              <div className="result-icon">✅</div>
              <div className="result-value">{job.result.successful}</div>
              <div className="result-label">نجح</div>
            </div>
            <div className="result-card error">
              <div className="result-icon">❌</div>
              <div className="result-value">{job.result.failed}</div>
              <div className="result-label">فشل</div>
            </div>
          </div>
        </div>
      )}

      {job.error_message && (
        <div className="error-section">
          <h3>رسالة الخطأ</h3>
          <div className="error-message">{job.error_message}</div>
        </div>
      )}

      {job.completed_at && (
        <div className="completion-info">
          اكتمل في {new Date(job.completed_at).toLocaleString('ar-SA')}
        </div>
      )}

      <style>{`
        .status-section {
          margin: 2rem 0;
        }

        .status-card {
          background: white;
          padding: 2rem;
          border-radius: 12px;
          border: 2px solid #e5e7eb;
        }

        .status-card.status-completed {
          border-color: #10b981;
        }

        .status-card.status-failed {
          border-color: #ef4444;
        }

        .status-card h3 {
          margin-bottom: 1rem;
          color: #1e40af;
        }

        .progress-bar {
          position: relative;
          width: 100%;
          height: 32px;
          background: #f3f4f6;
          border-radius: 16px;
          overflow: hidden;
        }

        .progress-fill {
          position: absolute;
          right: 0;
          top: 0;
          height: 100%;
          background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
          transition: width 0.5s;
        }

        .progress-text {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
          font-weight: 600;
          color: #1f2937;
          z-index: 1;
        }

        .results-section {
          margin: 2rem 0;
        }

        .results-section h2 {
          margin-bottom: 1rem;
        }

        .results-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1.5rem;
        }

        .result-card {
          background: white;
          padding: 1.5rem;
          border-radius: 12px;
          text-align: center;
          border: 2px solid #e5e7eb;
        }

        .result-card.success {
          border-color: #10b981;
        }

        .result-card.error {
          border-color: #ef4444;
        }

        .result-icon {
          font-size: 2rem;
          margin-bottom: 0.5rem;
        }

        .result-value {
          font-size: 2rem;
          font-weight: bold;
          color: #1e40af;
        }

        .result-label {
          color: #6b7280;
          margin-top: 0.5rem;
        }

        .error-section {
          background: #fee2e2;
          padding: 1.5rem;
          border-radius: 8px;
          margin: 2rem 0;
        }

        .error-section h3 {
          color: #991b1b;
          margin-bottom: 0.5rem;
        }

        .error-message {
          color: #7f1d1d;
          font-family: monospace;
        }

        .completion-info {
          text-align: center;
          color: #6b7280;
          margin-top: 2rem;
        }

        .loading, .error {
          text-align: center;
          padding: 3rem;
          font-size: 1.25rem;
          color: #6b7280;
        }
      `}</style>
    </div>
  )
}

export default JobDetailsPage
