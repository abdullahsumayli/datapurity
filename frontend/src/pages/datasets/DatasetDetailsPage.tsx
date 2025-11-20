import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import apiClient from '../../config/apiClient'

interface Dataset {
  id: string
  filename: string
  uploaded_at: string
  total_rows: number
  cleaned_rows: number
  duplicates: number
  invalid_emails: number
  invalid_phones: number
  status: string
}

function DatasetDetailsPage() {
  const { id } = useParams()
  const [dataset, setDataset] = useState<Dataset | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDataset()
  }, [id])

  const fetchDataset = async () => {
    try {
      const response = await apiClient.get(`/datasets/${id}`)
      setDataset(response.data)
    } catch (error) {
      console.error('Failed to fetch dataset:', error)
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

  if (!dataset) {
    return (
      <div className="page-container">
        <div className="error">لم يتم العثور على البيانات</div>
      </div>
    )
  }

  const qualityScore = dataset.total_rows > 0
    ? ((dataset.cleaned_rows / dataset.total_rows) * 100).toFixed(1)
    : 0

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>{dataset.filename}</h1>
        <p className="page-description">
          تم الرفع في {new Date(dataset.uploaded_at).toLocaleDateString('ar-SA')}
        </p>
      </div>

      <div className={`status-badge status-${dataset.status}`}>
        {dataset.status === 'completed' ? '✓ مكتمل' : '⏳ قيد المعالجة'}
      </div>

      <div className="quality-section">
        <h2>درجة الجودة</h2>
        <div className="quality-gauge">
          <div className="gauge-value">{qualityScore}%</div>
          <div className="gauge-label">جودة البيانات</div>
        </div>
      </div>

      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon">📊</div>
          <div className="metric-value">{dataset.total_rows.toLocaleString('ar-SA')}</div>
          <div className="metric-label">إجمالي السجلات</div>
        </div>

        <div className="metric-card success">
          <div className="metric-icon">✨</div>
          <div className="metric-value">{dataset.cleaned_rows.toLocaleString('ar-SA')}</div>
          <div className="metric-label">سجلات منظفة</div>
        </div>

        <div className="metric-card warning">
          <div className="metric-icon">🔁</div>
          <div className="metric-value">{dataset.duplicates.toLocaleString('ar-SA')}</div>
          <div className="metric-label">تكرارات</div>
        </div>

        <div className="metric-card error">
          <div className="metric-icon">📧</div>
          <div className="metric-value">{dataset.invalid_emails.toLocaleString('ar-SA')}</div>
          <div className="metric-label">بريد غير صالح</div>
        </div>

        <div className="metric-card error">
          <div className="metric-icon">📱</div>
          <div className="metric-value">{dataset.invalid_phones.toLocaleString('ar-SA')}</div>
          <div className="metric-label">هواتف غير صالحة</div>
        </div>
      </div>

      <div className="actions-section">
        <Link to={`/app/exports?dataset=${id}`} className="btn-primary">
          📥 تصدير البيانات المنظفة
        </Link>
        <Link to="/app/datasets/upload" className="btn-secondary">
          📤 رفع ملف جديد
        </Link>
      </div>

      <style>{`
        .status-badge {
          display: inline-block;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-weight: 600;
          margin: 1rem 0;
        }

        .status-completed {
          background: #d1fae5;
          color: #065f46;
        }

        .status-processing {
          background: #fef3c7;
          color: #92400e;
        }

        .quality-section {
          background: white;
          padding: 2rem;
          border-radius: 12px;
          margin: 2rem 0;
          text-align: center;
        }

        .quality-gauge {
          margin-top: 1.5rem;
        }

        .gauge-value {
          font-size: 4rem;
          font-weight: bold;
          color: #1e40af;
        }

        .gauge-label {
          color: #6b7280;
          margin-top: 0.5rem;
        }

        .metrics-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1.5rem;
          margin: 2rem 0;
        }

        .metric-card {
          background: white;
          padding: 1.5rem;
          border-radius: 12px;
          text-align: center;
          border: 2px solid #e5e7eb;
        }

        .metric-card.success {
          border-color: #10b981;
        }

        .metric-card.warning {
          border-color: #f59e0b;
        }

        .metric-card.error {
          border-color: #ef4444;
        }

        .metric-icon {
          font-size: 2rem;
          margin-bottom: 0.5rem;
        }

        .metric-value {
          font-size: 2rem;
          font-weight: bold;
          color: #1e40af;
        }

        .metric-label {
          color: #6b7280;
          font-size: 0.875rem;
          margin-top: 0.5rem;
        }

        .actions-section {
          display: flex;
          gap: 1rem;
          margin-top: 2rem;
        }

        .btn-secondary {
          background: #f3f4f6;
          color: #1f2937;
        }

        .btn-secondary:hover {
          background: #e5e7eb;
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

export default DatasetDetailsPage
