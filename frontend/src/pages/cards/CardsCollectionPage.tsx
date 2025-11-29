import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import * as XLSX from 'xlsx'
import './CardsCollectionPage.css'

interface Contact {
  id: number
  name: string
  company: string
  phone: string
  email: string
  position: string
  source: 'bulk-upload' | 'single-scan' | 'manual'
  addedAt: string
}

export default function CardsCollectionPage() {
  const navigate = useNavigate()
  const [contacts, setContacts] = useState<Contact[]>([])
  const [filteredContacts, setFilteredContacts] = useState<Contact[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [filterSource, setFilterSource] = useState<'all' | 'bulk-upload' | 'single-scan' | 'manual'>('all')
  const [selectedContacts, setSelectedContacts] = useState<Set<number>>(new Set())

  useEffect(() => {
    loadContacts()
  }, [])

  useEffect(() => {
    applyFilters()
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [contacts, searchQuery, filterSource])

  const loadContacts = () => {
    const stored = localStorage.getItem('cards_collection')
    if (stored) {
      const loaded: Contact[] = JSON.parse(stored)
      setContacts(loaded)
    }
  }

  const applyFilters = () => {
    let filtered = [...contacts]

    // Filter by source
    if (filterSource !== 'all') {
      filtered = filtered.filter(c => c.source === filterSource)
    }

    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(c =>
        c.name.toLowerCase().includes(query) ||
        c.company.toLowerCase().includes(query) ||
        c.phone.includes(query) ||
        c.email.toLowerCase().includes(query)
      )
    }

    setFilteredContacts(filtered)
  }

  const handleSelectAll = () => {
    if (selectedContacts.size === filteredContacts.length && filteredContacts.length > 0) {
      setSelectedContacts(new Set())
    } else {
      setSelectedContacts(new Set(filteredContacts.map(c => c.id)))
    }
  }

  const handleSelectContact = (id: number) => {
    const newSelected = new Set(selectedContacts)
    if (newSelected.has(id)) {
      newSelected.delete(id)
    } else {
      newSelected.add(id)
    }
    setSelectedContacts(newSelected)
  }

  const handleDeleteSelected = () => {
    if (selectedContacts.size === 0) return
    
    if (confirm(`هل تريد حذف ${selectedContacts.size} جهة اتصال؟`)) {
      const remaining = contacts.filter(c => !selectedContacts.has(c.id))
      setContacts(remaining)
      localStorage.setItem('cards_collection', JSON.stringify(remaining))
      setSelectedContacts(new Set())
    }
  }

  const handleExportExcel = () => {
    const dataToExport = selectedContacts.size > 0
      ? contacts.filter(c => selectedContacts.has(c.id))
      : filteredContacts

    if (dataToExport.length === 0) {
      alert('لا توجد جهات اتصال للتصدير')
      return
    }

    const worksheet = XLSX.utils.json_to_sheet(dataToExport.map(c => ({
      'الاسم': c.name,
      'الشركة': c.company,
      'الهاتف': c.phone,
      'البريد الإلكتروني': c.email,
      'المنصب': c.position,
      'المصدر': c.source === 'bulk-upload' ? 'رفع متعدد' : c.source === 'single-scan' ? 'مسح فردي' : 'يدوي',
      'تاريخ الإضافة': new Date(c.addedAt).toLocaleString('ar-SA')
    })))

    const workbook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workbook, worksheet, 'جهات الاتصال')
    XLSX.writeFile(workbook, `contacts_${Date.now()}.xlsx`)
  }

  const handleExportCSV = () => {
    const dataToExport = selectedContacts.size > 0
      ? contacts.filter(c => selectedContacts.has(c.id))
      : filteredContacts

    if (dataToExport.length === 0) {
      alert('لا توجد جهات اتصال للتصدير')
      return
    }

    const csvContent = [
      ['الاسم', 'الشركة', 'الهاتف', 'البريد الإلكتروني', 'المنصب', 'المصدر', 'تاريخ الإضافة'].join(','),
      ...dataToExport.map(c => [
        c.name,
        c.company,
        c.phone,
        c.email,
        c.position,
        c.source === 'bulk-upload' ? 'رفع متعدد' : c.source === 'single-scan' ? 'مسح فردي' : 'يدوي',
        new Date(c.addedAt).toLocaleString('ar-SA')
      ].join(','))
    ].join('\n')

    const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `contacts_${Date.now()}.csv`
    link.click()
  }

  const handleClearAll = () => {
    if (confirm('هل تريد حذف جميع جهات الاتصال من المجموعة؟')) {
      setContacts([])
      localStorage.removeItem('cards_collection')
      setSelectedContacts(new Set())
    }
  }

  const getSourceLabel = (source: string) => {
    switch (source) {
      case 'bulk-upload': return 'رفع متعدد'
      case 'single-scan': return 'مسح فردي'
      case 'manual': return 'يدوي'
      default: return source
    }
  }

  return (
    <div className="cards-collection-page">
      <div className="collection-header">
        <div className="header-top">
          <h1>📇 مجموعة الكروت</h1>
          <button onClick={() => navigate('/app/cards/upload')} className="btn-back">
            ← العودة
          </button>
        </div>
        <p className="subtitle">جميع جهات الاتصال المستخرجة من الكروت في مكان واحد</p>
      </div>

      <div className="collection-stats">
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-info">
            <div className="stat-value">{contacts.length}</div>
            <div className="stat-label">إجمالي الكروت</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📤</div>
          <div className="stat-info">
            <div className="stat-value">{contacts.filter(c => c.source === 'bulk-upload').length}</div>
            <div className="stat-label">رفع متعدد</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🔍</div>
          <div className="stat-info">
            <div className="stat-value">{contacts.filter(c => c.source === 'single-scan').length}</div>
            <div className="stat-label">مسح فردي</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">✍️</div>
          <div className="stat-info">
            <div className="stat-value">{contacts.filter(c => c.source === 'manual').length}</div>
            <div className="stat-label">يدوي</div>
          </div>
        </div>
      </div>

      <div className="collection-controls">
        <div className="search-filter-section">
          <div className="search-box">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="بحث بالاسم، الشركة، الهاتف، أو البريد..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="filter-buttons">
            <button
              className={`filter-btn ${filterSource === 'all' ? 'active' : ''}`}
              onClick={() => setFilterSource('all')}
            >
              الكل ({contacts.length})
            </button>
            <button
              className={`filter-btn ${filterSource === 'bulk-upload' ? 'active' : ''}`}
              onClick={() => setFilterSource('bulk-upload')}
            >
              رفع متعدد ({contacts.filter(c => c.source === 'bulk-upload').length})
            </button>
            <button
              className={`filter-btn ${filterSource === 'single-scan' ? 'active' : ''}`}
              onClick={() => setFilterSource('single-scan')}
            >
              مسح فردي ({contacts.filter(c => c.source === 'single-scan').length})
            </button>
            <button
              className={`filter-btn ${filterSource === 'manual' ? 'active' : ''}`}
              onClick={() => setFilterSource('manual')}
            >
              يدوي ({contacts.filter(c => c.source === 'manual').length})
            </button>
          </div>
        </div>

        <div className="action-buttons">
          <button onClick={handleSelectAll} className="btn-select-all">
            {selectedContacts.size === filteredContacts.length ? '❌ إلغاء التحديد' : '✅ تحديد الكل'}
          </button>
          <button onClick={handleExportExcel} className="btn-export-excel">
            📊 تصدير Excel
          </button>
          <button onClick={handleExportCSV} className="btn-export-csv">
            📄 تصدير CSV
          </button>
          {selectedContacts.size > 0 && (
            <button onClick={handleDeleteSelected} className="btn-delete">
              🗑️ حذف المحدد ({selectedContacts.size})
            </button>
          )}
          {contacts.length > 0 && (
            <button onClick={handleClearAll} className="btn-clear-all">
              🗑️ حذف الكل
            </button>
          )}
        </div>
      </div>

      {filteredContacts.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📭</div>
          <h3>لا توجد جهات اتصال</h3>
          <p>
            {contacts.length === 0
              ? 'ابدأ بإضافة كروت من خلال صفحات الاستخراج'
              : 'لا توجد نتائج تطابق البحث أو الفلتر'}
          </p>
          <button onClick={() => navigate('/app/cards/upload')} className="btn-add-cards">
            + إضافة كروت جديدة
          </button>
        </div>
      ) : (
        <div className="contacts-table-container">
          <table className="contacts-table">
            <thead>
              <tr>
                <th>
                  <input
                    type="checkbox"
                    checked={selectedContacts.size === filteredContacts.length && filteredContacts.length > 0}
                    onChange={handleSelectAll}
                  />
                </th>
                <th>الاسم</th>
                <th>الشركة</th>
                <th>الهاتف</th>
                <th>البريد الإلكتروني</th>
                <th>المنصب</th>
                <th>المصدر</th>
                <th>تاريخ الإضافة</th>
              </tr>
            </thead>
            <tbody>
              {filteredContacts.map(contact => (
                <tr key={contact.id} className={selectedContacts.has(contact.id) ? 'selected' : ''}>
                  <td>
                    <input
                      type="checkbox"
                      checked={selectedContacts.has(contact.id)}
                      onChange={() => handleSelectContact(contact.id)}
                    />
                  </td>
                  <td className="contact-name">{contact.name}</td>
                  <td>{contact.company}</td>
                  <td className="contact-phone">{contact.phone}</td>
                  <td className="contact-email">{contact.email}</td>
                  <td>{contact.position}</td>
                  <td>
                    <span className={`source-badge source-${contact.source}`}>
                      {getSourceLabel(contact.source)}
                    </span>
                  </td>
                  <td className="contact-date">
                    {new Date(contact.addedAt).toLocaleDateString('ar-SA')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
