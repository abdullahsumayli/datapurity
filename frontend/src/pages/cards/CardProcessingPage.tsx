import { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import * as XLSX from 'xlsx'
import apiClient from '../../config/apiClient'

interface ExtractedContact {
  id: number
  name: string
  company: string
  phone: string
  email: string
  address?: string
  position?: string
  confidence: number
  image_url?: string
}

interface ProcessingState {
  total: number
  processed: number
  failed: number
  status: 'processing' | 'completed' | 'failed'
}

function CardProcessingPage() {
  const [contacts, setContacts] = useState<ExtractedContact[]>([])
  const [processing, setProcessing] = useState<ProcessingState>({
    total: 0,
    processed: 0,
    failed: 0,
    status: 'processing'
  })
  const [exporting, setExporting] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const navigate = useNavigate()
  const location = useLocation()
  const uploadedFiles = location.state?.files || []

  useEffect(() => {
    if (uploadedFiles.length > 0) {
      processCards()
    } else {
      navigate('/app/cards/upload')
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const processCards = async () => {
    setProcessing(prev => ({ ...prev, total: uploadedFiles.length }))

    const formData = new FormData()
    uploadedFiles.forEach((file: File) => formData.append('files', file))

    try {
      await apiClient.post('/cards/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      // Simulate OCR processing (في الإنتاج سيكون هناك معالجة حقيقية)
      const extractedData: ExtractedContact[] = uploadedFiles.map((file: File, index: number) => ({
        id: index + 1,
        name: `جهة اتصال ${index + 1}`,
        company: `شركة ${index + 1}`,
        phone: `+966 50 123 ${String(1000 + index).slice(-4)}`,
        email: `contact${index + 1}@company.com`,
        address: 'الرياض، المملكة العربية السعودية',
        position: 'مدير',
        confidence: Math.round(85 + Math.random() * 15),
        image_url: URL.createObjectURL(file)
      }))

      setContacts(extractedData)
      setProcessing({
        total: uploadedFiles.length,
        processed: uploadedFiles.length,
        failed: 0,
        status: 'completed'
      })
    } catch (error) {
      console.error('Processing failed:', error)
      setProcessing(prev => ({
        ...prev,
        failed: prev.total,
        status: 'failed'
      }))
    }
  }

  const downloadExcel = () => {
    if (contacts.length === 0) return
    setExporting(true)

    try {
      // تحضير البيانات للـ Excel
      const excelData = contacts.map(contact => ({
        'الاسم': contact.name,
        'الشركة': contact.company,
        'رقم الهاتف': contact.phone,
        'البريد الإلكتروني': contact.email,
        'العنوان': contact.address || '',
        'الوظيفة': contact.position || '',
        'نسبة الدقة': `${contact.confidence}%`
      }))

      // إنشاء Workbook
      const wb = XLSX.utils.book_new()
      const ws = XLSX.utils.json_to_sheet(excelData)

      // تنسيق الأعمدة
      const colWidths = [
        { wch: 20 }, // الاسم
        { wch: 25 }, // الشركة
        { wch: 18 }, // رقم الهاتف
        { wch: 30 }, // البريد الإلكتروني
        { wch: 35 }, // العنوان
        { wch: 20 }, // الوظيفة
        { wch: 12 }  // نسبة الدقة
      ]
      ws['!cols'] = colWidths

      // إضافة الورقة للـ Workbook
      XLSX.utils.book_append_sheet(wb, ws, 'جهات الاتصال')

      // تنزيل الملف
      const timestamp = new Date().toISOString().slice(0, 10)
      XLSX.writeFile(wb, `business_cards_${timestamp}.xlsx`)

      setTimeout(() => setExporting(false), 1000)
    } catch (error) {
      console.error('Export failed:', error)
      alert('فشل تصدير الملف. حاول مرة أخرى.')
      setExporting(false)
    }
  }

  const downloadCSV = () => {
    if (contacts.length === 0) return

    const csvContent = [
      // Headers
      ['الاسم', 'الشركة', 'رقم الهاتف', 'البريد الإلكتروني', 'العنوان', 'الوظيفة', 'نسبة الدقة'].join(','),
      // Data
      ...contacts.map(c => [
        c.name,
        c.company,
        c.phone,
        c.email,
        c.address || '',
        c.position || '',
        `${c.confidence}%`
      ].join(','))
    ].join('\n')

    const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    
    const timestamp = new Date().toISOString().slice(0, 10)
    link.setAttribute('href', url)
    link.setAttribute('download', `business_cards_${timestamp}.csv`)
    link.click()
  }

  const updateContact = (id: number, field: keyof ExtractedContact, value: string | number) => {
    setContacts(prev => prev.map(contact => 
      contact.id === id ? { ...contact, [field]: value } : contact
    ))
  }

  const saveToContacts = async () => {
    try {
      // في الإنتاج: حفظ إلى قاعدة البيانات
      alert(`تم حفظ ${contacts.length} جهة اتصال بنجاح!`)
      navigate('/app/contacts')
    } catch (error) {
      console.error('Save failed:', error)
      alert('فشل الحفظ. حاول مرة أخرى.')
    }
  }

  if (processing.status === 'processing') {
    return (
      <div className="page-container">
        <div className="processing-container">
          <div className="processing-animation">
            <div className="scanner"></div>
            <h2>جاري معالجة البطاقات...</h2>
            <p>استخدام الذكاء الاصطناعي لاستخراج البيانات</p>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${(processing.processed / processing.total) * 100}%` }}
              ></div>
            </div>
            <p className="progress-text">
              {processing.processed} من {processing.total}
            </p>
          </div>
        </div>
        <style>{processingStyles}</style>
      </div>
    )
  }

  if (processing.status === 'failed') {
    return (
      <div className="page-container">
        <div className="error-container">
          <div className="error-icon">❌</div>
          <h2>فشلت المعالجة</h2>
          <p>حدث خطأ أثناء معالجة البطاقات</p>
          <button 
            className="btn-primary" 
            onClick={() => navigate('/app/cards/upload')}
          >
            حاول مرة أخرى
          </button>
        </div>
        <style>{processingStyles}</style>
      </div>
    )
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <button className="btn-back" onClick={() => navigate('/app')}>
          ← العودة إلى الرئيسية
        </button>
        <h1>نتائج المعالجة</h1>
        <p className="page-description">
          تم استخراج {contacts.length} جهة اتصال من البطاقات
        </p>
      </div>

      <div className="results-container">
        {/* Export Actions */}
        <div className="actions-bar">
          <button 
            className="btn-success"
            onClick={downloadExcel}
            disabled={exporting}
          >
            📗 {exporting ? 'جاري التصدير...' : 'تنزيل Excel'}
          </button>
          <button 
            className="btn-secondary"
            onClick={downloadCSV}
          >
            📄 تنزيل CSV
          </button>
          <button 
            className="btn-primary"
            onClick={saveToContacts}
          >
            💾 حفظ في جهات الاتصال
          </button>
        </div>

        {/* Contacts Grid */}
        <div className="contacts-grid">
          {contacts.map(contact => (
            <div key={contact.id} className="contact-card">
              {contact.image_url && (
                <div className="card-preview">
                  <img src={contact.image_url} alt={contact.name} />
                </div>
              )}
              <div className="card-details">
                <div className="edit-controls">
                  <button 
                    className="btn-edit"
                    onClick={() => setEditingId(editingId === contact.id ? null : contact.id)}
                  >
                    {editingId === contact.id ? '✓ حفظ' : '✏️ تعديل'}
                  </button>
                </div>
                
                <div className="detail-row">
                  <span className="label">الاسم:</span>
                  {editingId === contact.id ? (
                    <input
                      type="text"
                      className="edit-input"
                      value={contact.name}
                      onChange={(e) => updateContact(contact.id, 'name', e.target.value)}
                    />
                  ) : (
                    <span className="value">{contact.name}</span>
                  )}
                </div>
                
                <div className="detail-row">
                  <span className="label">الشركة:</span>
                  {editingId === contact.id ? (
                    <input
                      type="text"
                      className="edit-input"
                      value={contact.company}
                      onChange={(e) => updateContact(contact.id, 'company', e.target.value)}
                    />
                  ) : (
                    <span className="value">{contact.company}</span>
                  )}
                </div>
                
                <div className="detail-row">
                  <span className="label">الهاتف:</span>
                  {editingId === contact.id ? (
                    <input
                      type="text"
                      className="edit-input"
                      value={contact.phone}
                      onChange={(e) => updateContact(contact.id, 'phone', e.target.value)}
                    />
                  ) : (
                    <span className="value">{contact.phone}</span>
                  )}
                </div>
                
                <div className="detail-row">
                  <span className="label">البريد:</span>
                  {editingId === contact.id ? (
                    <input
                      type="email"
                      className="edit-input"
                      value={contact.email}
                      onChange={(e) => updateContact(contact.id, 'email', e.target.value)}
                    />
                  ) : (
                    <span className="value">{contact.email}</span>
                  )}
                </div>
                
                <div className="detail-row">
                  <span className="label">العنوان:</span>
                  {editingId === contact.id ? (
                    <input
                      type="text"
                      className="edit-input"
                      value={contact.address || ''}
                      onChange={(e) => updateContact(contact.id, 'address', e.target.value)}
                    />
                  ) : (
                    <span className="value">{contact.address || '-'}</span>
                  )}
                </div>
                
                <div className="detail-row">
                  <span className="label">الوظيفة:</span>
                  {editingId === contact.id ? (
                    <input
                      type="text"
                      className="edit-input"
                      value={contact.position || ''}
                      onChange={(e) => updateContact(contact.id, 'position', e.target.value)}
                    />
                  ) : (
                    <span className="value">{contact.position || '-'}</span>
                  )}
                </div>
                
                <div className="confidence-badge">
                  دقة: {contact.confidence}%
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <style>{resultsStyles}</style>
    </div>
  )
}

const processingStyles = `
  .processing-container,
  .error-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 60vh;
  }

  .processing-animation {
    text-align: center;
    max-width: 400px;
  }

  .scanner {
    width: 120px;
    height: 120px;
    margin: 0 auto 2rem;
    border: 4px solid #667eea;
    border-radius: 12px;
    position: relative;
    overflow: hidden;
  }

  .scanner::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #667eea, transparent);
    animation: scan 2s linear infinite;
  }

  @keyframes scan {
    from { transform: translateY(0); }
    to { transform: translateY(120px); }
  }

  .processing-animation h2 {
    color: #1e40af;
    margin-bottom: 0.5rem;
  }

  .processing-animation p {
    color: #6b7280;
    margin-bottom: 2rem;
  }

  .progress-bar {
    width: 100%;
    height: 8px;
    background: #e5e7eb;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 0.5rem;
  }

  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea, #764ba2);
    transition: width 0.3s ease;
  }

  .progress-text {
    color: #4b5563;
    font-size: 0.875rem;
  }

  .error-container {
    text-align: center;
  }

  .error-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
  }

  .error-container h2 {
    color: #ef4444;
    margin-bottom: 0.5rem;
  }

  .error-container p {
    color: #6b7280;
    margin-bottom: 2rem;
  }
`

const resultsStyles = `
  .results-container {
    max-width: 1200px;
    margin: 0 auto;
  }

  .actions-bar {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
  }

  .actions-bar button {
    padding: 0.75rem 1.5rem;
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

  .btn-success:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .btn-secondary {
    background: #f3f4f6;
    color: #1f2937;
  }

  .btn-secondary:hover {
    background: #e5e7eb;
  }

  .btn-primary {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
  }

  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  }

  .contacts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1.5rem;
  }

  .contact-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.3s;
  }

  .contact-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  }

  .card-preview {
    width: 100%;
    height: 180px;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 1rem;
    background: #f3f4f6;
  }

  .card-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .card-details {
    text-align: right;
  }

  .edit-controls {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
  }

  .btn-edit {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 6px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    font-weight: 600;
    cursor: pointer;
    font-size: 0.875rem;
    transition: all 0.3s;
  }

  .btn-edit:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  }

  .detail-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f3f4f6;
    gap: 1rem;
  }

  .detail-row:last-of-type {
    border-bottom: none;
  }

  .label {
    font-weight: 600;
    color: #6b7280;
    font-size: 0.875rem;
    min-width: 80px;
  }

  .value {
    color: #1f2937;
    font-weight: 500;
    flex: 1;
  }

  .edit-input {
    flex: 1;
    padding: 0.5rem;
    border: 2px solid #667eea;
    border-radius: 6px;
    font-size: 0.875rem;
    font-family: inherit;
    transition: all 0.3s;
    text-align: right;
  }

  .edit-input:focus {
    outline: none;
    border-color: #764ba2;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }

  .confidence-badge {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    border-radius: 20px;
    text-align: center;
    font-weight: 600;
    font-size: 0.875rem;
  }

  @media (max-width: 768px) {
    .contacts-grid {
      grid-template-columns: 1fr;
    }

    .actions-bar {
      flex-direction: column;
    }

    .actions-bar button {
      width: 100%;
    }
  }
`

export default CardProcessingPage
