import { useEffect, useState } from 'react'
import apiClient from '../../config/apiClient'

interface Card {
  id: number
  user_id: number
  original_filename: string
  storage_path: string
  ocr_text?: string | null
  ocr_confidence?: number | null
  extracted_name?: string | null
  extracted_company?: string | null
  extracted_phone?: string | null
  extracted_email?: string | null
  extracted_address?: string | null
  is_processed: boolean
  is_reviewed: boolean
  created_at: string
  updated_at?: string | null
}

function CardReviewPage() {
  const [cards, setCards] = useState<Card[]>([])
  const [loading, setLoading] = useState(true)
  const [editingCard, setEditingCard] = useState<string | null>(null)
  const [formData, setFormData] = useState<any>({})

  useEffect(() => {
    fetchCards()
  }, [])

  const fetchCards = async () => {
    try {
      const response = await apiClient.get('/cards')
      setCards(response.data)
    } catch (error) {
      console.error('Failed to fetch cards:', error)
    } finally {
      setLoading(false)
    }
  }

  const startEditing = (card: Card) => {
    setEditingCard(card.id.toString())
    setFormData({
      extracted_name: card.extracted_name || '',
      extracted_company: card.extracted_company || '',
      extracted_phone: card.extracted_phone || '',
      extracted_email: card.extracted_email || '',
      extracted_address: card.extracted_address || ''
    })
  }

  const saveCard = async (cardId: string) => {
    try {
      await apiClient.put(`/cards/${cardId}`, {
        ...formData,
        is_reviewed: true
      })
      setEditingCard(null)
      fetchCards()
    } catch (error) {
      alert('فشل حفظ التعديلات')
    }
  }

  const markAsReviewed = async (cardId: string) => {
    try {
      await apiClient.put(`/cards/${cardId}`, { is_reviewed: true })
      fetchCards()
    } catch (error) {
      alert('فشل تحديث الحالة')
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
        <h1>مراجعة البطاقات</h1>
        <p className="page-description">
          راجع وصحح البيانات المستخرجة من بطاقات الأعمال
        </p>
      </div>

      <div className="cards-grid">
        {cards.length === 0 ? (
          <div className="no-data">لا توجد بطاقات للمراجعة</div>
        ) : (
          cards.map(card => (
            <div key={card.id} className={`card-item ${card.is_reviewed ? 'reviewed' : ''}`}>
              <div className="card-image">
                <img src={card.storage_path} alt={card.original_filename} />
              </div>
              
              {editingCard === card.id.toString() ? (
                <div className="card-form">
                  <input
                    value={formData.extracted_name || ''}
                    onChange={e => setFormData({...formData, extracted_name: e.target.value})}
                    placeholder="الاسم"
                  />
                  <input
                    value={formData.extracted_company || ''}
                    onChange={e => setFormData({...formData, extracted_company: e.target.value})}
                    placeholder="الشركة"
                  />
                  <input
                    value={formData.extracted_email || ''}
                    onChange={e => setFormData({...formData, extracted_email: e.target.value})}
                    placeholder="البريد الإلكتروني"
                  />
                  <input
                    value={formData.extracted_phone || ''}
                    onChange={e => setFormData({...formData, extracted_phone: e.target.value})}
                    placeholder="رقم الهاتف"
                  />
                  <input
                    value={formData.extracted_address || ''}
                    onChange={e => setFormData({...formData, extracted_address: e.target.value})}
                    placeholder="العنوان"
                  />
                  <div className="form-actions">
                    <button onClick={() => saveCard(card.id.toString())} className="btn-primary">حفظ</button>
                    <button onClick={() => setEditingCard(null)} className="btn-secondary">إلغاء</button>
                  </div>
                </div>
              ) : (
                <div className="card-data">
                  <div className="data-row">
                    <strong>الاسم:</strong> {card.extracted_name || '-'}
                  </div>
                  <div className="data-row">
                    <strong>الشركة:</strong> {card.extracted_company || '-'}
                  </div>
                  <div className="data-row">
                    <strong>البريد:</strong> {card.extracted_email || '-'}
                  </div>
                  <div className="data-row">
                    <strong>الهاتف:</strong> {card.extracted_phone || '-'}
                  </div>
                  {card.extracted_address && (
                    <div className="data-row">
                      <strong>العنوان:</strong> {card.extracted_address}
                    </div>
                  )}
                  <div className="card-actions">
                    <button onClick={() => startEditing(card)} className="btn-secondary">✏️ تعديل</button>
                    {!card.is_reviewed && (
                      <button onClick={() => markAsReviewed(card.id.toString())} className="btn-primary">✓ تأكيد</button>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      <style>{`
        .cards-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
          gap: 1.5rem;
          margin-top: 2rem;
        }

        .card-item {
          background: white;
          border-radius: 12px;
          overflow: hidden;
          border: 2px solid #e5e7eb;
        }

        .card-item.reviewed {
          border-color: #10b981;
          opacity: 0.7;
        }

        .card-image {
          width: 100%;
          height: 200px;
          overflow: hidden;
          background: #f3f4f6;
        }

        .card-image img {
          width: 100%;
          height: 100%;
          object-fit: contain;
        }

        .card-data, .card-form {
          padding: 1.5rem;
        }

        .data-row {
          padding: 0.5rem 0;
          border-bottom: 1px solid #f3f4f6;
        }

        .data-row strong {
          color: #6b7280;
          margin-left: 0.5rem;
        }

        .card-actions, .form-actions {
          display: flex;
          gap: 0.5rem;
          margin-top: 1rem;
        }

        .card-actions button, .form-actions button {
          flex: 1;
        }

        .card-form input {
          width: 100%;
          padding: 0.75rem;
          margin-bottom: 0.75rem;
          border: 1px solid #cbd5e1;
          border-radius: 8px;
          font-size: 1rem;
        }

        .card-form input:focus {
          outline: none;
          border-color: #667eea;
        }

        .no-data {
          text-align: center;
          padding: 3rem;
          color: #6b7280;
          grid-column: 1 / -1;
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

export default CardReviewPage
