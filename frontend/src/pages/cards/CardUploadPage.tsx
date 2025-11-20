import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../../config/apiClient'

function CardUploadPage() {
  const [files, setFiles] = useState<File[]>([])
  const [uploading, setUploading] = useState(false)
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
    
    if (e.dataTransfer.files) {
      setFiles(Array.from(e.dataTransfer.files))
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files))
    }
  }

  const handleUpload = async () => {
    if (files.length === 0) return

    setUploading(true)
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))

    try {
      await apiClient.post('/cards/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      navigate('/app/cards/review')
    } catch (error) {
      alert('فشل رفع البطاقات. حاول مرة أخرى.')
    } finally {
      setUploading(false)
    }
  }

  const removeFile = (index: number) => {
    setFiles(files.filter((_, i) => i !== index))
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>رفع بطاقات أعمال</h1>
        <p className="page-description">
          ارفع صور بطاقات الأعمال لاستخراج البيانات تلقائياً
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
          <button
            onClick={handleUpload}
            disabled={uploading}
            className="btn-primary upload-btn"
          >
            {uploading ? 'جاري الرفع...' : `رفع ${files.length} بطاقة`}
          </button>
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
      `}</style>
    </div>
  )
}

export default CardUploadPage
