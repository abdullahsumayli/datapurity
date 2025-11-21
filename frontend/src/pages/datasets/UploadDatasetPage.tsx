import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../../config/apiClient'
import { ProcessedData, exportToCSV, exportToExcel, processFile } from '../../utils/fileProcessor'

function UploadDatasetPage() {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [processing, setProcessing] = useState(false)
  const [processedData, setProcessedData] = useState<ProcessedData | null>(null)
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setProcessedData(null) // إعادة تعيين البيانات المعالجة
    }
  }

  const handleProcessFile = async () => {
    if (!file) return

    setProcessing(true)
    try {
      const result = await processFile(file)
      setProcessedData(result)
    } catch (error) {
      alert(`فشل معالجة الملف: ${error instanceof Error ? error.message : 'خطأ غير معروف'}`)
    } finally {
      setProcessing(false)
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await apiClient.post('/datasets/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      navigate(`/app/datasets/${response.data.id}`)
    } catch (error) {
      alert('فشل رفع الملف. حاول مرة أخرى.')
    } finally {
      setUploading(false)
    }
  }

  const handleExportExcel = () => {
    if (!processedData) return
    const timestamp = new Date().toISOString().slice(0, 10)
    exportToExcel(processedData.cleanedData, `cleaned_data_${timestamp}.xlsx`)
  }

  const handleExportCSV = () => {
    if (!processedData) return
    const timestamp = new Date().toISOString().slice(0, 10)
    exportToCSV(processedData.cleanedData, `cleaned_data_${timestamp}.csv`)
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>رفع ملف بيانات</h1>
        <p className="page-description">
          ارفع ملف Excel أو CSV لتنظيف وتوحيد بيانات جهات الاتصال
        </p>
      </div>

      <div className="upload-container">
        <div
          className={`dropzone ${dragActive ? 'active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv,.xlsx,.xls,.zip"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          
          {file ? (
            <div className="file-selected">
              <div className="file-icon">📄</div>
              <div className="file-name">{file.name}</div>
              <div className="file-size">{(file.size / 1024 / 1024).toFixed(2)} ميجابايت</div>
            </div>
          ) : (
            <div className="dropzone-content">
              <div className="upload-icon">📤</div>
              <h3>اسحب الملف هنا أو اضغط للاختيار</h3>
              <p>ملفات CSV, Excel (XLSX, XLS), ZIP</p>
            </div>
          )}
        </div>

        {file && !processedData && (
          <button
            onClick={handleProcessFile}
            disabled={processing}
            className="btn-primary upload-btn"
          >
            {processing ? 'جاري المعالجة...' : '🔍 معالجة وتنظيف البيانات'}
          </button>
        )}

        {processedData && (
          <div className="processing-results">
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">{processedData.totalRows}</div>
                <div className="stat-label">إجمالي الصفوف</div>
              </div>
              <div className="stat-card success">
                <div className="stat-value">
                  {processedData.cleanedData.filter(c => c.status === 'valid').length}
                </div>
                <div className="stat-label">بيانات صحيحة</div>
              </div>
              <div className="stat-card warning">
                <div className="stat-value">
                  {processedData.cleanedData.filter(c => c.status === 'warning').length}
                </div>
                <div className="stat-label">تحذيرات</div>
              </div>
              <div className="stat-card error">
                <div className="stat-value">
                  {processedData.cleanedData.filter(c => c.status === 'error').length}
                </div>
                <div className="stat-label">أخطاء</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{processedData.duplicates}</div>
                <div className="stat-label">تكرارات</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{processedData.emptyRows}</div>
                <div className="stat-label">صفوف فارغة</div>
              </div>
            </div>

            <div className="action-buttons">
              <button onClick={handleExportExcel} className="btn-success">
                📗 تصدير Excel
              </button>
              <button onClick={handleExportCSV} className="btn-secondary">
                📄 تصدير CSV
              </button>
              <button
                onClick={handleUpload}
                disabled={uploading}
                className="btn-primary"
              >
                {uploading ? 'جاري الرفع...' : '☁️ رفع إلى النظام'}
              </button>
            </div>

            {/* Data Preview */}
            <div className="data-preview">
              <h3>معاينة البيانات المنظفة ({processedData.cleanedData.length} جهة اتصال)</h3>
              <div className="table-container">
                <table>
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>الاسم</th>
                      <th>البريد الإلكتروني</th>
                      <th>الهاتف</th>
                      <th>الشركة</th>
                      <th>الحالة</th>
                      <th>المشاكل</th>
                    </tr>
                  </thead>
                  <tbody>
                    {processedData.cleanedData.slice(0, 10).map((contact) => (
                      <tr key={contact.id} className={`row-${contact.status}`}>
                        <td>{contact.id}</td>
                        <td>{contact.name}</td>
                        <td>{contact.email}</td>
                        <td>{contact.phone}</td>
                        <td>{contact.company || '-'}</td>
                        <td>
                          <span className={`status-badge ${contact.status}`}>
                            {contact.status === 'valid' ? '✓ صحيح' : 
                             contact.status === 'warning' ? '⚠ تحذير' : '✗ خطأ'}
                          </span>
                        </td>
                        <td className="issues">
                          {contact.issues.length > 0 ? contact.issues.join(', ') : '-'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {processedData.cleanedData.length > 10 && (
                  <p className="preview-note">
                    معاينة أول 10 صفوف من {processedData.cleanedData.length}
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        {!processedData && (
          <div className="upload-tips">
            <h3>نصائح لأفضل النتائج:</h3>
            <ul>
              <li>تأكد أن الملف يحتوي على أعمدة واضحة للأسماء والبريد الإلكتروني وأرقام الهواتف</li>
              <li>الحد الأقصى لحجم الملف: 100 ميجابايت</li>
              <li>يدعم النظام اللغة العربية والإنجليزية</li>
              <li>يمكنك رفع ملفات مضغوطة (ZIP) تحتوي على عدة ملفات</li>
              <li>سيتم تنظيف البيانات تلقائياً وإزالة التكرارات</li>
            </ul>
          </div>
        )}
      </div>

      <style>{`
        .upload-container {
          max-width: 1200px;
          margin: 2rem auto;
        }

        .dropzone {
          border: 2px dashed #cbd5e1;
          border-radius: 12px;
          padding: 3rem;
          text-align: center;
          cursor: pointer;
          transition: all 0.3s;
          background: white;
        }

        .dropzone:hover,
        .dropzone.active {
          border-color: #667eea;
          background: #f8f9ff;
        }

        .upload-icon {
          font-size: 4rem;
          margin-bottom: 1rem;
        }

        .dropzone h3 {
          color: #1e40af;
          margin-bottom: 0.5rem;
        }

        .dropzone p {
          color: #6b7280;
          font-size: 0.875rem;
        }

        .file-selected {
          padding: 2rem;
        }

        .file-icon {
          font-size: 3rem;
          margin-bottom: 1rem;
        }

        .file-name {
          font-size: 1.125rem;
          font-weight: 600;
          color: #1e40af;
          margin-bottom: 0.5rem;
        }

        .file-size {
          color: #6b7280;
          font-size: 0.875rem;
        }

        .upload-btn {
          width: 100%;
          margin-top: 1.5rem;
          padding: 1rem;
          font-size: 1.125rem;
        }

        .upload-tips {
          margin-top: 2rem;
          padding: 1.5rem;
          background: #f8f9ff;
          border-radius: 8px;
        }

        .upload-tips h3 {
          color: #1e40af;
          margin-bottom: 1rem;
        }

        .upload-tips ul {
          list-style: none;
          padding: 0;
        }

        .upload-tips li {
          padding: 0.5rem 0;
          color: #4b5563;
          padding-right: 1.5rem;
          position: relative;
        }

        .upload-tips li::before {
          content: "✓";
          position: absolute;
          right: 0;
          color: #10b981;
          font-weight: bold;
        }

        .processing-results {
          margin-top: 2rem;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 1rem;
          margin-bottom: 2rem;
        }

        .stat-card {
          background: white;
          padding: 1.5rem;
          border-radius: 12px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
          text-align: center;
          border: 2px solid #e5e7eb;
        }

        .stat-card.success {
          border-color: #10b981;
          background: linear-gradient(135deg, #f0fdf4, white);
        }

        .stat-card.warning {
          border-color: #f59e0b;
          background: linear-gradient(135deg, #fffbeb, white);
        }

        .stat-card.error {
          border-color: #ef4444;
          background: linear-gradient(135deg, #fef2f2, white);
        }

        .stat-value {
          font-size: 2rem;
          font-weight: bold;
          color: #1e40af;
          margin-bottom: 0.5rem;
        }

        .stat-label {
          color: #6b7280;
          font-size: 0.875rem;
        }

        .action-buttons {
          display: flex;
          gap: 1rem;
          margin-bottom: 2rem;
          flex-wrap: wrap;
        }

        .action-buttons button {
          flex: 1;
          min-width: 150px;
          padding: 0.875rem 1.5rem;
          border: none;
          border-radius: 8px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
          font-size: 1rem;
        }

        .btn-success {
          background: linear-gradient(135deg, #10b981, #059669);
          color: white;
        }

        .btn-success:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        }

        .btn-secondary {
          background: #f3f4f6;
          color: #1f2937;
        }

        .btn-secondary:hover {
          background: #e5e7eb;
        }

        .data-preview {
          background: white;
          border-radius: 12px;
          padding: 1.5rem;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .data-preview h3 {
          color: #1e40af;
          margin-bottom: 1rem;
        }

        .table-container {
          overflow-x: auto;
        }

        table {
          width: 100%;
          border-collapse: collapse;
          font-size: 0.875rem;
        }

        th {
          background: #f3f4f6;
          padding: 0.75rem;
          text-align: right;
          font-weight: 600;
          color: #374151;
          border-bottom: 2px solid #e5e7eb;
        }

        td {
          padding: 0.75rem;
          border-bottom: 1px solid #f3f4f6;
        }

        tr:hover {
          background: #f9fafb;
        }

        .row-valid {
          background: #f0fdf4;
        }

        .row-warning {
          background: #fffbeb;
        }

        .row-error {
          background: #fef2f2;
        }

        .status-badge {
          padding: 0.25rem 0.75rem;
          border-radius: 12px;
          font-size: 0.75rem;
          font-weight: 600;
          display: inline-block;
        }

        .status-badge.valid {
          background: #d1fae5;
          color: #065f46;
        }

        .status-badge.warning {
          background: #fef3c7;
          color: #92400e;
        }

        .status-badge.error {
          background: #fee2e2;
          color: #991b1b;
        }

        .issues {
          color: #6b7280;
          font-size: 0.8rem;
          max-width: 200px;
        }

        .preview-note {
          text-align: center;
          color: #6b7280;
          margin-top: 1rem;
          font-size: 0.875rem;
        }

        @media (max-width: 768px) {
          .upload-container {
            padding: 0 1rem;
          }

          .stats-grid {
            grid-template-columns: repeat(2, 1fr);
          }

          .action-buttons {
            flex-direction: column;
          }

          .action-buttons button {
            width: 100%;
          }

          table {
            font-size: 0.75rem;
          }

          th, td {
            padding: 0.5rem;
          }
        }
      `}</style>
    </div>
  )
}

export default UploadDatasetPage
