import { useEffect, useState } from 'react'
import apiClient from '../../config/apiClient'

interface Card {
  id: string
  image_url: string
  extracted_data: {
    name?: string
    title?: string
    company?: string
    email?: string
    phone?: string
  }
  reviewed: boolean
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
    setEditingCard(card.id)
    setFormData(card.extracted_data)
  }

  const saveCard = async (cardId: string) => {
    try {
      await apiClient.put(`/cards/${cardId}`, {
        extracted_data: formData,
        reviewed: true
      })
      setEditingCard(null)
      fetchCards()
    } catch (error) {
      alert('فشل حفظ التعديلات')
    }
  }

  const markAsReviewed = async (cardId: string) => {
    try {
      await apiClient.put(`/cards/${cardId}`, { reviewed: true })
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
            <div key={card.id} className={`card-item ${card.reviewed ? 'reviewed' : ''}`}>
              <div className="card-image">
                <img src={card.image_url} alt="Business card" />
              </div>
              
              {editingCard === card.id ? (
                <div className="card-form">
                  <input
                    value={formData.name || ''}
                    onChange={e => setFormData({...formData, name: e.target.value})}
                    placeholder="الاسم"
                  />
                  <input
                    value={formData.title || ''}
                    onChange={e => setFormData({...formData, title: e.target.value})}
                    placeholder="المسمى الوظيفي"
                  />
                  <input
                    value={formData.company || ''}
                    onChange={e => setFormData({...formData, company: e.target.value})}
                    placeholder="الشركة"
                  />
                  <input
                    value={formData.email || ''}
                    onChange={e => setFormData({...formData, email: e.target.value})}
                    placeholder="البريد الإلكتروني"
                  />
                  <input
                    value={formData.phone || ''}
                    onChange={e => setFormData({...formData, phone: e.target.value})}
                    placeholder="رقم الهاتف"
                  />
                  <div className="form-actions">
                    <button onClick={() => saveCard(card.id)} className="btn-primary">حفظ</button>
                    <button onClick={() => setEditingCard(null)} className="btn-secondary">إلغاء</button>
                  </div>
                </div>
              ) : (
                <div className="card-data">
                  <div className="data-row">
                    <strong>الاسم:</strong> {card.extracted_data.name || '-'}
                  </div>
                  <div className="data-row">
                    <strong>المسمى:</strong> {card.extracted_data.title || '-'}
                  </div>
                  <div className="data-row">
                    <strong>الشركة:</strong> {card.extracted_data.company || '-'}
                  </div>
                  <div className="data-row">
                    <strong>البريد:</strong> {card.extracted_data.email || '-'}
                  </div>
                  <div className="data-row">
                    <strong>الهاتف:</strong> {card.extracted_data.phone || '-'}
                  </div>
                  <div className="card-actions">
                    <button onClick={() => startEditing(card)} className="btn-secondary">✏️ تعديل</button>
                    {!card.reviewed && (
                      <button onClick={() => markAsReviewed(card.id)} className="btn-primary">✓ تأكيد</button>
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
