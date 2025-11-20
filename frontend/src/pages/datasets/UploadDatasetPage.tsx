import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../../config/apiClient'

function UploadDatasetPage() {
  const [file, setFile] = useState<File | null>(null)
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
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
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
            accept=".csv,.xlsx,.xls"
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
              <p>ملفات CSV, Excel (XLSX, XLS)</p>
            </div>
          )}
        </div>

        {file && (
          <button
            onClick={handleUpload}
            disabled={uploading}
            className="btn-primary upload-btn"
          >
            {uploading ? 'جاري الرفع...' : 'رفع وبدء التنظيف'}
          </button>
        )}

        <div className="upload-tips">
          <h3>نصائح لأفضل النتائج:</h3>
          <ul>
            <li>تأكد أن الملف يحتوي على أعمدة واضحة للأسماء والبريد الإلكتروني وأرقام الهواتف</li>
            <li>الحد الأقصى لحجم الملف: 100 ميجابايت</li>
            <li>يدعم النظام اللغة العربية والإنجليزية</li>
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
      `}</style>
    </div>
  )
}

export default UploadDatasetPage
