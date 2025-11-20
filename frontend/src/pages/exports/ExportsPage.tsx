import { useEffect, useState } from 'react'
import apiClient from '../../config/apiClient'

interface Export {
  id: string
  format: string
  dataset_name: string
  created_at: string
  download_url: string
  status: string
}

function ExportsPage() {
  const [exports, setExports] = useState<Export[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedFormat, setSelectedFormat] = useState('csv')
  const [exporting, setExporting] = useState(false)

  useEffect(() => {
    fetchExports()
  }, [])

  const fetchExports = async () => {
    try {
      const response = await apiClient.get('/exports')
      setExports(response.data)
    } catch (error) {
      console.error('Failed to fetch exports:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async () => {
    setExporting(true)
    try {
      await apiClient.post('/exports', {
        format: selectedFormat
      })
      alert('تم إنشاء التصدير بنجاح')
      fetchExports()
    } catch (error) {
      alert('فشل إنشاء التصدير')
    } finally {
      setExporting(false)
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
        <h1>تصدير البيانات</h1>
        <p className="page-description">
          صدّر بيانات جهات الاتصال المنظفة بصيغ مختلفة
        </p>
      </div>

      <div className="export-section">
        <h2>إنشاء تصدير جديد</h2>
        <div className="export-formats">
          <label className={`format-card ${selectedFormat === 'csv' ? 'selected' : ''}`}>
            <input
              type="radio"
              value="csv"
              checked={selectedFormat === 'csv'}
              onChange={e => setSelectedFormat(e.target.value)}
            />
            <div className="format-icon">📄</div>
            <div className="format-name">CSV</div>
            <div className="format-description">مثالي للجداول وقواعد البيانات</div>
          </label>

          <label className={`format-card ${selectedFormat === 'xlsx' ? 'selected' : ''}`}>
            <input
              type="radio"
              value="xlsx"
              checked={selectedFormat === 'xlsx'}
              onChange={e => setSelectedFormat(e.target.value)}
            />
            <div className="format-icon">📊</div>
            <div className="format-name">Excel (XLSX)</div>
            <div className="format-description">مع تنسيق وحسابات</div>
          </label>

          <label className={`format-card ${selectedFormat === 'json' ? 'selected' : ''}`}>
            <input
              type="radio"
              value="json"
              checked={selectedFormat === 'json'}
              onChange={e => setSelectedFormat(e.target.value)}
            />
            <div className="format-icon">📦</div>
            <div className="format-name">JSON</div>
            <div className="format-description">للبرمجة والتكامل</div>
          </label>

          <label className={`format-card ${selectedFormat === 'vcard' ? 'selected' : ''}`}>
            <input
              type="radio"
              value="vcard"
              checked={selectedFormat === 'vcard'}
              onChange={e => setSelectedFormat(e.target.value)}
            />
            <div className="format-icon">📇</div>
            <div className="format-name">vCard</div>
            <div className="format-description">لأجهزة الهاتف</div>
          </label>
        </div>

        <button
          onClick={handleExport}
          disabled={exporting}
          className="btn-primary export-btn"
        >
          {exporting ? 'جاري التصدير...' : 'إنشاء التصدير'}
        </button>
      </div>

      <div className="exports-history">
        <h2>التصديرات السابقة</h2>
        <div className="exports-table">
          <table>
            <thead>
              <tr>
                <th>الصيغة</th>
                <th>مجموعة البيانات</th>
                <th>التاريخ</th>
                <th>الحالة</th>
                <th>الإجراء</th>
              </tr>
            </thead>
            <tbody>
              {exports.length === 0 ? (
                <tr>
                  <td colSpan={5} className="no-data">لا توجد تصديرات سابقة</td>
                </tr>
              ) : (
                exports.map(exp => (
                  <tr key={exp.id}>
                    <td>{exp.format.toUpperCase()}</td>
                    <td>{exp.dataset_name}</td>
                    <td>{new Date(exp.created_at).toLocaleDateString('ar-SA')}</td>
                    <td>
                      <span className={`status-badge status-${exp.status}`}>
                        {exp.status === 'ready' ? 'جاهز' : 'جاري الإنشاء'}
                      </span>
                    </td>
                    <td>
                      {exp.status === 'ready' && (
                        <a href={exp.download_url} className="btn-link" download>
                          📥 تنزيل
                        </a>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      <style>{`
        .export-section {
          background: white;
          padding: 2rem;
          border-radius: 12px;
          margin: 2rem 0;
        }

        .export-section h2 {
          margin-bottom: 1.5rem;
        }

        .export-formats {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
          margin-bottom: 1.5rem;
        }

        .format-card {
          border: 2px solid #e5e7eb;
          border-radius: 8px;
          padding: 1.5rem;
          text-align: center;
          cursor: pointer;
          transition: all 0.2s;
        }

        .format-card:hover {
          border-color: #cbd5e1;
        }

        .format-card.selected {
          border-color: #667eea;
          background: #f8f9ff;
        }

        .format-card input {
          display: none;
        }

        .format-icon {
          font-size: 2.5rem;
          margin-bottom: 0.5rem;
        }

        .format-name {
          font-weight: 600;
          color: #1e40af;
          margin-bottom: 0.25rem;
        }

        .format-description {
          font-size: 0.875rem;
          color: #6b7280;
        }

        .export-btn {
          width: 100%;
          padding: 1rem;
          font-size: 1.125rem;
        }

        .exports-history {
          margin-top: 3rem;
        }

        .exports-history h2 {
          margin-bottom: 1.5rem;
        }

        .exports-table {
          background: white;
          border-radius: 12px;
          overflow: hidden;
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

        .status-ready {
          background: #d1fae5;
          color: #065f46;
        }

        .status-processing {
          background: #fef3c7;
          color: #92400e;
        }

        .btn-link {
          color: #667eea;
          text-decoration: none;
        }

        .btn-link:hover {
          text-decoration: underline;
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

export default ExportsPage
