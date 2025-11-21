import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'

interface DetectedCard {
  id: number
  x: number
  y: number
  width: number
  height: number
  imageData: string
}

function BulkCardScanPage() {
  const [image, setImage] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string>('')
  const [detectedCards, setDetectedCards] = useState<DetectedCard[]>([])
  const [detecting, setDetecting] = useState(false)
  const [processing, setProcessing] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const navigate = useNavigate()

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setImage(file)
      const reader = new FileReader()
      reader.onload = (event) => {
        setImagePreview(event.target?.result as string)
        setDetectedCards([])
      }
      reader.readAsDataURL(file)
    }
  }

  const detectCards = async () => {
    if (!image || !imagePreview) return

    setDetecting(true)
    
    // محاكاة اكتشاف البطاقات (في الإنتاج سيكون هناك AI حقيقي)
    setTimeout(() => {
      // محاكاة اكتشاف 4 بطاقات في الصورة
      const mockCards: DetectedCard[] = [
        { id: 1, x: 50, y: 50, width: 300, height: 180, imageData: imagePreview },
        { id: 2, x: 400, y: 50, width: 300, height: 180, imageData: imagePreview },
        { id: 3, x: 50, y: 280, width: 300, height: 180, imageData: imagePreview },
        { id: 4, x: 400, y: 280, width: 300, height: 180, imageData: imagePreview },
      ]
      setDetectedCards(mockCards)
      setDetecting(false)
    }, 2000)
  }

  const processAllCards = async () => {
    if (detectedCards.length === 0) return

    setProcessing(true)
    
    // محاكاة معالجة OCR لكل بطاقة
    setTimeout(() => {
      const contacts = detectedCards.map((card, index) => ({
        id: card.id,
        name: `جهة اتصال ${index + 1}`,
        company: `شركة ${index + 1}`,
        phone: `+966 50 123 ${String(1000 + index).slice(-4)}`,
        email: `contact${index + 1}@company.com`,
        address: 'الرياض، المملكة العربية السعودية',
        position: 'مدير',
        confidence: Math.round(85 + Math.random() * 15),
        imageUrl: card.imageData
      }))

      navigate('/app/cards/processing', { 
        state: { 
          contacts,
          fromBulkScan: true 
        } 
      })
    }, 1500)
  }

  const removeCard = (id: number) => {
    setDetectedCards(detectedCards.filter(card => card.id !== id))
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <button className="btn-back" onClick={() => navigate('/app/cards/upload')}>
          ← العودة
        </button>
        <h1>📷 مسح صورة تحتوي على عدة كروت</h1>
        <p className="page-description">
          ارفع صورة واحدة بها عدة بطاقات أعمال وسنكتشفها ونستخرج بياناتها تلقائياً
        </p>
      </div>

      <div className="bulk-scan-container">
        {!image ? (
          <div 
            className="upload-zone"
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              style={{ display: 'none' }}
            />
            <div className="upload-icon">🖼️</div>
            <h3>اختر صورة تحتوي على عدة بطاقات</h3>
            <p>JPG, PNG أو أي صيغة صورة</p>
            <p className="hint">مثال: صورة لعدة كروت على طاولة أو من ماسح ضوئي</p>
          </div>
        ) : (
          <>
            <div className="image-preview-section">
              <div className="image-container">
                <img src={imagePreview} alt="Uploaded" />
                <canvas ref={canvasRef} className="detection-canvas" />
                {detectedCards.length > 0 && (
                  <div className="detection-overlay">
                    {detectedCards.map(card => (
                      <div
                        key={card.id}
                        className="card-box"
                        style={{
                          left: `${(card.x / 800) * 100}%`,
                          top: `${(card.y / 600) * 100}%`,
                          width: `${(card.width / 800) * 100}%`,
                          height: `${(card.height / 600) * 100}%`,
                        }}
                      >
                        <span className="card-number">#{card.id}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="action-buttons">
                {detectedCards.length === 0 ? (
                  <>
                    <button
                      onClick={detectCards}
                      disabled={detecting}
                      className="btn-primary"
                    >
                      {detecting ? (
                        <>
                          <span className="spinner"></span>
                          جاري اكتشاف البطاقات...
                        </>
                      ) : (
                        '🔍 اكتشاف البطاقات تلقائياً'
                      )}
                    </button>
                    <button
                      onClick={() => {
                        setImage(null)
                        setImagePreview('')
                      }}
                      className="btn-secondary"
                    >
                      اختيار صورة أخرى
                    </button>
                  </>
                ) : (
                  <>
                    <div className="detection-info">
                      <span className="info-icon">✅</span>
                      <span>تم اكتشاف {detectedCards.length} بطاقة</span>
                    </div>
                    <button
                      onClick={processAllCards}
                      disabled={processing}
                      className="btn-primary"
                    >
                      {processing ? (
                        <>
                          <span className="spinner"></span>
                          جاري المعالجة...
                        </>
                      ) : (
                        `⚡ استخراج البيانات من ${detectedCards.length} بطاقة`
                      )}
                    </button>
                    <button
                      onClick={() => setDetectedCards([])}
                      className="btn-secondary"
                    >
                      إعادة الاكتشاف
                    </button>
                  </>
                )}
              </div>
            </div>

            {detectedCards.length > 0 && (
              <div className="detected-cards-grid">
                <h3>البطاقات المكتشفة:</h3>
                <div className="cards-grid">
                  {detectedCards.map((card) => (
                    <div key={card.id} className="detected-card-item">
                      <div className="card-preview">
                        <img src={card.imageData} alt={`Card ${card.id}`} />
                        <span className="card-badge">#{card.id}</span>
                      </div>
                      <button
                        onClick={() => removeCard(card.id)}
                        className="remove-card-btn"
                      >
                        ❌ استبعاد
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}

        <div className="features-info">
          <h3>🎯 كيف يعمل النظام؟</h3>
          <div className="features-grid">
            <div className="feature-item">
              <span className="feature-icon">🤖</span>
              <h4>اكتشاف ذكي</h4>
              <p>يستخدم AI للتعرف على البطاقات في الصورة تلقائياً</p>
            </div>
            <div className="feature-item">
              <span className="feature-icon">✂️</span>
              <h4>قص تلقائي</h4>
              <p>يقوم بقص كل بطاقة على حدة لتحسين دقة OCR</p>
            </div>
            <div className="feature-item">
              <span className="feature-icon">⚡</span>
              <h4>معالجة سريعة</h4>
              <p>معالجة متوازية لجميع البطاقات في نفس الوقت</p>
            </div>
            <div className="feature-item">
              <span className="feature-icon">📊</span>
              <h4>استخراج شامل</h4>
              <p>استخراج الأسماء، الشركات، الهواتف، والإيميلات</p>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        .bulk-scan-container {
          max-width: 1200px;
          margin: 2rem auto;
        }

        .upload-zone {
          border: 3px dashed #cbd5e1;
          border-radius: 16px;
          padding: 4rem 2rem;
          text-align: center;
          cursor: pointer;
          transition: all 0.3s;
          background: white;
          margin-bottom: 2rem;
        }

        .upload-zone:hover {
          border-color: #667eea;
          background: #f8f9ff;
          transform: translateY(-2px);
        }

        .upload-icon {
          font-size: 5rem;
          margin-bottom: 1rem;
        }

        .upload-zone h3 {
          color: #1e40af;
          margin-bottom: 0.5rem;
          font-size: 1.5rem;
        }

        .upload-zone p {
          color: #6b7280;
          font-size: 1rem;
          margin: 0.5rem 0;
        }

        .hint {
          font-size: 0.875rem !important;
          font-style: italic;
          color: #9ca3af !important;
        }

        .image-preview-section {
          background: white;
          border-radius: 12px;
          padding: 2rem;
          margin-bottom: 2rem;
        }

        .image-container {
          position: relative;
          max-width: 100%;
          margin-bottom: 1.5rem;
          border-radius: 8px;
          overflow: hidden;
        }

        .image-container img {
          width: 100%;
          display: block;
          border-radius: 8px;
        }

        .detection-overlay {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          pointer-events: none;
        }

        .card-box {
          position: absolute;
          border: 3px solid #10b981;
          background: rgba(16, 185, 129, 0.1);
          border-radius: 4px;
          animation: pulse 2s infinite;
        }

        .card-number {
          position: absolute;
          top: -12px;
          left: -12px;
          background: #10b981;
          color: white;
          width: 28px;
          height: 28px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 700;
          font-size: 0.875rem;
          pointer-events: all;
        }

        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.6; }
        }

        .action-buttons {
          display: flex;
          gap: 1rem;
          flex-wrap: wrap;
        }

        .action-buttons .btn-primary,
        .action-buttons .btn-secondary {
          flex: 1;
          min-width: 200px;
        }

        .detection-info {
          flex: 1;
          display: flex;
          align-items: center;
          gap: 0.75rem;
          padding: 1rem 1.5rem;
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          color: white;
          border-radius: 8px;
          font-size: 1.125rem;
          font-weight: 600;
        }

        .info-icon {
          font-size: 1.5rem;
        }

        .detected-cards-grid {
          background: white;
          border-radius: 12px;
          padding: 2rem;
          margin-bottom: 2rem;
        }

        .detected-cards-grid h3 {
          color: #1e40af;
          margin-bottom: 1.5rem;
        }

        .cards-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
          gap: 1.5rem;
        }

        .detected-card-item {
          border: 2px solid #e5e7eb;
          border-radius: 8px;
          overflow: hidden;
          transition: all 0.3s;
        }

        .detected-card-item:hover {
          transform: translateY(-4px);
          box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }

        .card-preview {
          position: relative;
          padding-bottom: 62.5%; /* 16:10 aspect ratio */
          background: #f3f4f6;
          overflow: hidden;
        }

        .card-preview img {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .card-badge {
          position: absolute;
          top: 8px;
          left: 8px;
          background: rgba(16, 185, 129, 0.9);
          color: white;
          padding: 0.25rem 0.75rem;
          border-radius: 12px;
          font-weight: 700;
          font-size: 0.875rem;
        }

        .remove-card-btn {
          width: 100%;
          padding: 0.75rem;
          background: #ef4444;
          color: white;
          border: none;
          font-size: 0.875rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
        }

        .remove-card-btn:hover {
          background: #dc2626;
        }

        .features-info {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          border-radius: 16px;
          padding: 2.5rem;
          color: white;
        }

        .features-info h3 {
          text-align: center;
          font-size: 1.75rem;
          margin-bottom: 2rem;
        }

        .features-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 2rem;
        }

        .feature-item {
          text-align: center;
        }

        .feature-icon {
          font-size: 3rem;
          display: block;
          margin-bottom: 1rem;
        }

        .feature-item h4 {
          font-size: 1.25rem;
          margin-bottom: 0.5rem;
          color: white;
        }

        .feature-item p {
          font-size: 0.9375rem;
          opacity: 0.95;
          line-height: 1.6;
        }

        @media (max-width: 768px) {
          .action-buttons {
            flex-direction: column;
          }

          .action-buttons .btn-primary,
          .action-buttons .btn-secondary {
            width: 100%;
          }

          .features-grid {
            grid-template-columns: 1fr;
            gap: 1.5rem;
          }
        }
      `}</style>
    </div>
  )
}

export default BulkCardScanPage
