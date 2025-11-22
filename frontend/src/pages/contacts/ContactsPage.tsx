import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import apiClient from '../../config/apiClient'

interface Contact {
  id: number
  full_name: string | null
  email: string | null
  phone: string | null
  company?: string | null
  overall_quality_score: number | null
  dataset_id: number
  created_at: string
}

function ContactsPage() {
  const [contacts, setContacts] = useState<Contact[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterDataset, setFilterDataset] = useState<number | 'all'>('all')
  const navigate = useNavigate()

  useEffect(() => {
    fetchContacts()
  }, [])

  const fetchContacts = async () => {
    try {
      const response = await apiClient.get('/contacts')
      setContacts(response.data)
    } catch (error) {
      console.error('Failed to fetch contacts:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredContacts = contacts.filter(contact => {
    const matchesSearch = !searchTerm || 
      (contact.full_name && contact.full_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (contact.email && contact.email.toLowerCase().includes(searchTerm.toLowerCase()))
    
    const matchesFilter = filterDataset === 'all' || contact.dataset_id === filterDataset
    
    return matchesSearch && matchesFilter
  })

  const getQualityBadge = (score: number) => {
    if (score >= 90) return { label: 'ممتاز', className: 'excellent' }
    if (score >= 70) return { label: 'جيد', className: 'good' }
    if (score >= 50) return { label: 'مقبول', className: 'fair' }
    return { label: 'ضعيف', className: 'poor' }
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
        <h1>جهات الاتصال</h1>
        <p className="page-description">
          تصفح وابحث وإدارة بيانات جهات الاتصال المنظفة
        </p>
      </div>

      <div className="filters-section">
        <div className="search-box">
          <input
            type="text"
            placeholder="بحث عن اسم أو بريد إلكتروني..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
          />
        </div>
        <select 
          value={filterDataset} 
          onChange={e => setFilterDataset(e.target.value === 'all' ? 'all' : Number(e.target.value))}
          className="filter-select"
        >
          <option value="all">كل مجموعات البيانات</option>
        </select>
      </div>

      <div className="contacts-table">
        <table>
          <thead>
            <tr>
              <th>الاسم</th>
              <th>البريد الإلكتروني</th>
              <th>الهاتف</th>
              <th>الشركة</th>
              <th>درجة الجودة</th>
              <th>المصدر</th>
            </tr>
          </thead>
          <tbody>
            {filteredContacts.length === 0 && contacts.length === 0 ? (
              <tr>
                <td colSpan={6} className="empty-state">
                  <div className="empty-state-content">
                    <div className="empty-state-icon">📭</div>
                    <h3>لا توجد بيانات حتى الآن</h3>
                    <p>ارفع أول ملف بيانات لبدء التنظيف</p>
                    <button 
                      className="empty-state-btn"
                      onClick={() => navigate('/app/upload')}
                    >
                      رفع ملف بيانات
                    </button>
                  </div>
                </td>
              </tr>
            ) : filteredContacts.length === 0 ? (
              <tr>
                <td colSpan={6} className="no-data">
                  لم يتم العثور على نتائج مطابقة
                </td>
              </tr>
            ) : (
              filteredContacts.map(contact => {
                const score = contact.overall_quality_score || 0
                const quality = getQualityBadge(score)
                return (
                  <tr key={contact.id}>
                    <td>{contact.full_name || '-'}</td>
                    <td>{contact.email || '-'}</td>
                    <td>{contact.phone || '-'}</td>
                    <td>{contact.company || '-'}</td>
                    <td>
                      <span className={`quality-badge quality-${quality.className}`}>
                        {score.toFixed(0)}% {quality.label}
                      </span>
                    </td>
                    <td>Dataset #{contact.dataset_id}</td>
                  </tr>
                )
              })
            )}
          </tbody>
        </table>
      </div>

      <div className="contacts-summary">
        إجمالي {filteredContacts.length} جهة اتصال
      </div>

      <style>{`
        .filters-section {
          display: flex;
          gap: 1rem;
          margin: 2rem 0;
        }

        .search-box {
          flex: 1;
        }

        .search-box input {
          width: 100%;
          padding: 0.75rem 1rem;
          border: 1px solid #cbd5e1;
          border-radius: 8px;
          font-size: 1rem;
        }

        .search-box input:focus {
          outline: none;
          border-color: #667eea;
        }

        .filter-select {
          padding: 0.75rem 1rem;
          border: 1px solid #cbd5e1;
          border-radius: 8px;
          font-size: 1rem;
          background: white;
        }

        .contacts-table {
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

        .empty-state {
          text-align: center;
          padding: 0;
        }

        .empty-state-content {
          padding: 4rem 2rem;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 1rem;
        }

        .empty-state-icon {
          font-size: 4rem;
          opacity: 0.6;
        }

        .empty-state-content h3 {
          font-size: 1.5rem;
          color: #1f2937;
          margin: 0;
        }

        .empty-state-content p {
          color: #6b7280;
          font-size: 1rem;
          margin: 0;
        }

        .empty-state-btn {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          padding: 0.875rem 2rem;
          font-size: 1rem;
          font-weight: 600;
          border-radius: 12px;
          cursor: pointer;
          transition: all 0.3s;
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }

        .empty-state-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
        }

        .quality-badge {
          display: inline-block;
          padding: 0.25rem 0.75rem;
          border-radius: 12px;
          font-size: 0.875rem;
          font-weight: 600;
        }

        .quality-excellent {
          background: #d1fae5;
          color: #065f46;
        }

        .quality-good {
          background: #dbeafe;
          color: #1e40af;
        }

        .quality-fair {
          background: #fef3c7;
          color: #92400e;
        }

        .quality-poor {
          background: #fee2e2;
          color: #991b1b;
        }

        .contacts-summary {
          text-align: center;
          color: #6b7280;
          margin-top: 1.5rem;
          padding: 1rem;
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

export default ContactsPage
