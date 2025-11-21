import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'

function CardUploadPage() {
  const [files, setFiles] = useState<File[]>([])
  const [uploading, setUploading] = useState(false)
  const [totalSize, setTotalSize] = useState(0)
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()

  const MAX_FILES = 100
  const MAX_FILE_SIZE = 10 * 1024 * 1024 // 10MB per file

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
    
    if (e.dataTransfer.files) {
      const newFiles = Array.from(e.dataTransfer.files)
      const validFiles = newFiles.filter(file => {
        if (file.size > MAX_FILE_SIZE) {
          alert(`الملف ${file.name} كبير جداً (الحد الأقصى 10MB)`)
          return false
        }
        return true
      })

      const combined = [...files, ...validFiles]
      if (combined.length > MAX_FILES) {
        alert(`الحد الأقصى ${MAX_FILES} ملف في المرة الواحدة`)
        setFiles(combined.slice(0, MAX_FILES))
      } else {
        setFiles(combined)
      }

      const size = combined.reduce((sum, f) => sum + f.size, 0)
      setTotalSize(size)
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const newFiles = Array.from(e.target.files)
      
      // Filter valid files
      const validFiles = newFiles.filter(file => {
        if (file.size > MAX_FILE_SIZE) {
          alert(`الملف ${file.name} كبير جداً (الحد الأقصى 10MB)`)
          return false
        }
        return true
      })

      // Limit total number of files
      const combined = [...files, ...validFiles]
      if (combined.length > MAX_FILES) {
        alert(`الحد الأقصى ${MAX_FILES} ملف في المرة الواحدة`)
        setFiles(combined.slice(0, MAX_FILES))
      } else {
        setFiles(combined)
      }

      // Calculate total size
      const size = combined.reduce((sum, f) => sum + f.size, 0)
      setTotalSize(size)
    }
  }

  const handleUpload = async () => {
    if (files.length === 0) return

    setUploading(true)
    
    // الانتقال مباشرة لصفحة المعالجة مع الملفات
    navigate('/app/cards/processing', { state: { files } })
  }

  const removeFile = (index: number) => {
    const newFiles = files.filter((_, i) => i !== index)
    setFiles(newFiles)
    const size = newFiles.reduce((sum, f) => sum + f.size, 0)
    setTotalSize(size)
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button className="btn-back" onClick={() => navigate('/app')}>
            ← العودة إلى الرئيسية
          </button>
          <button 
            className="btn-collection" 
            onClick={() => navigate('/app/cards/collection')}
            style={{
              padding: '0.75rem 1.5rem',
              background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '1rem',
              transition: 'all 0.3s'
            }}
          >
            📇 مجموعة الكروت
          </button>
        </div>
        <h1>رفع بطاقات أعمال</h1>
        <p className="page-description">
          ارفع صور بطاقات الأعمال لاستخراج البيانات تلقائياً
        </p>
        
        <div className="upload-modes">
          <div className="mode-card active">
            <span className="mode-icon">📇</span>
            <h3>رفع ملفات متعددة</h3>
            <p>ارفع عدة صور منفصلة (الوضع الحالي)</p>
          </div>
          <div 
            className="mode-card" 
            onClick={() => navigate('/app/cards/bulk-scan')}
          >
            <span className="mode-icon">📷</span>
            <h3>مسح صورة واحدة</h3>
            <p>صورة بها عدة كروت - اكتشاف تلقائي</p>
            <span className="mode-badge">جديد</span>
          </div>
        </div>
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
            accept=".jpg,.jpeg,.png,.pdf"
            multiple
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          
          {files.length === 0 ? (
            <div className="dropzone-content">
              <div className="upload-icon">📇</div>
              <h3>اسحب البطاقات هنا أو اضغط للاختيار</h3>
              <p>صور JPG, PNG أو ملفات PDF</p>
              <p>يمكنك رفع عدة بطاقات دفعة واحدة</p>
            </div>
          ) : (
            <div className="files-list">
              <h3>{files.length} بطاقة محددة</h3>
              {files.map((file, index) => (
                <div key={index} className="file-item">
                  <span>📄 {file.name}</span>
                  <button 
                    onClick={(e) => {
                      e.stopPropagation()
                      removeFile(index)
                    }}
                    className="remove-btn"
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {files.length > 0 && (
          <div className="upload-actions">
            <div className="upload-stats">
              <div className="stat-item">
                <span className="stat-label">📁 عدد الملفات:</span>
                <span className="stat-value">{files.length}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">📦 الحجم الإجمالي:</span>
                <span className="stat-value">{(totalSize / (1024 * 1024)).toFixed(2)} MB</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">⚡ معالجة متوقعة:</span>
                <span className="stat-value">~{Math.ceil(files.length * 3)} ثانية</span>
              </div>
            </div>
            <button
              onClick={handleUpload}
              disabled={uploading}
              className="btn-primary upload-btn"
            >
              {uploading ? (
                <>
                  <span className="spinner"></span>
                  جاري الرفع...
                </>
              ) : (
                `رفع ومعالجة ${files.length} بطاقة`
              )}
            </button>
            <button
              onClick={() => { setFiles([]); setTotalSize(0) }}
              className="btn-secondary"
              disabled={uploading}
            >
              مسح الكل
            </button>
          </div>
        )}

        <div className="upload-tips">
          <h3>نصائح للحصول على أفضل النتائج:</h3>
          <ul>
            <li>تأكد من وضوح الصورة وجودتها العالية</li>
            <li>تجنب الظلال والانعكاسات</li>
            <li>يفضل التصوير على خلفية بيضاء أو فاتحة</li>
            <li>يدعم النظام اللغتين العربية والإنجليزية</li>
          </ul>
        </div>
      </div>

      <style>{`
        .upload-container {
          max-width: 600px;
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
          margin: 0.25rem 0;
        }

        .files-list {
          text-align: right;
        }

        .files-list h3 {
          margin-bottom: 1rem;
          color: #1e40af;
        }

        .file-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.75rem;
          background: #f8f9ff;
          border-radius: 8px;
          margin-bottom: 0.5rem;
        }

        .remove-btn {
          background: #ef4444;
          color: white;
          border: none;
          width: 24px;
          height: 24px;
          border-radius: 50%;
          cursor: pointer;
          font-size: 0.75rem;
        }

        .remove-btn:hover {
          background: #dc2626;
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

        .upload-actions {
          margin-top: 2rem;
        }

        .upload-stats {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 1rem;
          margin-bottom: 1.5rem;
          padding: 1.5rem;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          border-radius: 12px;
          color: white;
        }

        .stat-item {
          text-align: center;
        }

        .stat-label {
          display: block;
          font-size: 0.875rem;
          opacity: 0.9;
          margin-bottom: 0.5rem;
        }

        .stat-value {
          display: block;
          font-size: 1.5rem;
          font-weight: 700;
        }

        .btn-secondary {
          width: 100%;
          margin-top: 0.75rem;
          padding: 0.875rem;
          background: #6b7280;
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          font-size: 1rem;
          transition: all 0.3s;
        }

        .btn-secondary:hover:not(:disabled) {
          background: #4b5563;
        }

        .btn-secondary:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .upload-modes {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 1rem;
          margin-top: 1.5rem;
        }

        .mode-card {
          background: white;
          border: 2px solid #e5e7eb;
          border-radius: 12px;
          padding: 1.5rem;
          cursor: pointer;
          transition: all 0.3s;
          position: relative;
          overflow: hidden;
        }

        .mode-card:hover {
          border-color: #667eea;
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }

        .mode-card.active {
          border-color: #667eea;
          background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
        }

        .mode-card .mode-icon {
          font-size: 2.5rem;
          display: block;
          margin-bottom: 0.75rem;
        }

        .mode-card h3 {
          color: #1e40af;
          font-size: 1.125rem;
          margin-bottom: 0.5rem;
        }

        .mode-card p {
          color: #6b7280;
          font-size: 0.875rem;
          margin: 0;
        }

        .mode-badge {
          position: absolute;
          top: 12px;
          left: 12px;
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          color: white;
          padding: 0.25rem 0.75rem;
          border-radius: 12px;
          font-size: 0.75rem;
          font-weight: 700;
        }

        @media (max-width: 768px) {
          .upload-modes {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  )
}

export default CardUploadPage
