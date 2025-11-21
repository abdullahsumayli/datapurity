import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { apiClient } from '../../config/apiClient'
import './checkout.css'

interface PlanDetails {
  id: string
  name: string
  nameAr: string
  price: number
  features: string[]
  ocr_cards: number
  cleaning_operations: number
  records_per_file: number
  extra_card_price: number
}

const PLANS: Record<string, PlanDetails> = {
  free: {
    id: 'free',
    name: 'Free',
    nameAr: 'مجاني',
    price: 0,
    ocr_cards: 10,
    cleaning_operations: 1,
    records_per_file: 100,
    extra_card_price: 0.50,
    features: [
      'عملية تنظيف واحدة شهريًا',
      'حتى 100 سجل لكل ملف',
      '10 كروت OCR شهريًا',
      'تصدير إلى Excel/CSV',
      'تقرير Data Health أساسي',
      'دعم عبر البريد الإلكتروني'
    ]
  },
  starter: {
    id: 'starter',
    name: 'Starter',
    nameAr: 'المبتدئ',
    price: 79,
    ocr_cards: 100,
    cleaning_operations: 5,
    records_per_file: 500,
    extra_card_price: 0.40,
    features: [
      '5 عمليات تنظيف شهريًا',
      'حتى 500 سجل لكل ملف',
      '100 كرت OCR شهريًا',
      'تصدير غير محدود',
      'تقارير Data Health متقدمة',
      'كشف التكرار الذكي',
      'دعم ذو أولوية'
    ]
  },
  business: {
    id: 'business',
    name: 'Business',
    nameAr: 'الأعمال',
    price: 199,
    ocr_cards: 500,
    cleaning_operations: 20,
    records_per_file: 2000,
    extra_card_price: 0.30,
    features: [
      '20 عملية تنظيف شهريًا',
      'حتى 2000 سجل لكل ملف',
      '500 كرت OCR شهريًا',
      'تقارير جودة بيانات تفصيلية',
      'تصنيف العملاء (Hot/Warm/Cold)',
      'حتى 5 مستخدمين',
      'دعم WhatsApp مباشر'
    ]
  }
}

function CheckoutPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const planId = searchParams.get('plan') || 'starter'
  
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [paymentMethod, setPaymentMethod] = useState<'mada' | 'visa' | 'applepay'>('mada')
  const [billingInfo, setBillingInfo] = useState({
    fullName: '',
    email: '',
    phone: '',
    company: '',
    vatNumber: '',
    address: '',
    city: '',
    country: 'SA'
  })

  const plan = PLANS[planId] || PLANS.starter

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await apiClient.post('/billing/create-checkout', {
        plan_id: planId,
        payment_method: paymentMethod,
        billing_info: billingInfo
      })

      // Redirect to payment gateway
      if (response.data.checkout_url) {
        window.location.href = response.data.checkout_url
      } else {
        navigate('/app/billing?status=success')
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'حدث خطأ أثناء معالجة الدفع')
      setLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBillingInfo({
      ...billingInfo,
      [e.target.name]: e.target.value
    })
  }

  if (plan.price === 0) {
    return (
      <div className="checkout-page">
        <div className="checkout-container">
          <div className="checkout-card">
            <div className="checkout-header">
              <h1>الباقة المجانية</h1>
              <p>لا تحتاج إلى إدخال معلومات الدفع</p>
            </div>
            <div className="checkout-free-message">
              <div className="free-icon">🎉</div>
              <h2>أنت على وشك الانضمام!</h2>
              <p>الباقة المجانية لا تتطلب أي معلومات دفع</p>
              <button 
                className="btn-primary btn-large"
                onClick={() => navigate('/app')}
              >
                ابدأ الاستخدام الآن
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="checkout-page">
      <div className="checkout-container">
        <div className="checkout-grid">
          {/* Plan Summary */}
          <div className="checkout-summary">
            <h2>ملخص الطلب</h2>
            
            <div className="plan-summary-card">
              <div className="plan-header">
                <h3>{plan.nameAr}</h3>
                <span className="plan-badge">{plan.name}</span>
              </div>
              
              <div className="plan-price">
                <span className="price-amount">{plan.price}</span>
                <span className="price-currency">ريال / شهر</span>
              </div>

              <div className="plan-features">
                <h4>ما تحصل عليه:</h4>
                <ul>
                  {plan.features.map((feature, idx) => (
                    <li key={idx}>
                      <span className="feature-check">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="plan-extra-info">
                <p>💳 الدفع حسب الاستخدام للكروت الإضافية</p>
                <p className="extra-price">{plan.extra_card_price} ريال لكل كرت إضافي</p>
              </div>
            </div>

            <div className="price-breakdown">
              <div className="breakdown-row">
                <span>الاشتراك الشهري</span>
                <span>{plan.price} ريال</span>
              </div>
              <div className="breakdown-row">
                <span>ضريبة القيمة المضافة (15%)</span>
                <span>{(plan.price * 0.15).toFixed(2)} ريال</span>
              </div>
              <div className="breakdown-row total">
                <span>الإجمالي</span>
                <span>{(plan.price * 1.15).toFixed(2)} ريال</span>
              </div>
            </div>
          </div>

          {/* Payment Form */}
          <div className="checkout-form-section">
            <h2>معلومات الدفع</h2>
            
            {error && (
              <div className="error-message">
                <span className="error-icon">⚠️</span>
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit}>
              {/* Payment Method Selection */}
              <div className="form-section">
                <h3>طريقة الدفع</h3>
                <div className="payment-methods">
                  <label className={`payment-method-option ${paymentMethod === 'mada' ? 'selected' : ''}`}>
                    <input
                      type="radio"
                      name="paymentMethod"
                      value="mada"
                      checked={paymentMethod === 'mada'}
                      onChange={(e) => setPaymentMethod(e.target.value as any)}
                    />
                    <div className="method-content">
                      <span className="method-icon">💳</span>
                      <span className="method-name">مدى</span>
                    </div>
                  </label>

                  <label className={`payment-method-option ${paymentMethod === 'visa' ? 'selected' : ''}`}>
                    <input
                      type="radio"
                      name="paymentMethod"
                      value="visa"
                      checked={paymentMethod === 'visa'}
                      onChange={(e) => setPaymentMethod(e.target.value as any)}
                    />
                    <div className="method-content">
                      <span className="method-icon">💳</span>
                      <span className="method-name">Visa / Mastercard</span>
                    </div>
                  </label>

                  <label className={`payment-method-option ${paymentMethod === 'applepay' ? 'selected' : ''}`}>
                    <input
                      type="radio"
                      name="paymentMethod"
                      value="applepay"
                      checked={paymentMethod === 'applepay'}
                      onChange={(e) => setPaymentMethod(e.target.value as any)}
                    />
                    <div className="method-content">
                      <span className="method-icon"></span>
                      <span className="method-name">Apple Pay</span>
                    </div>
                  </label>
                </div>
              </div>

              {/* Billing Information */}
              <div className="form-section">
                <h3>معلومات الفوترة</h3>
                
                <div className="form-grid">
                  <div className="form-group">
                    <label>الاسم الكامل *</label>
                    <input
                      type="text"
                      name="fullName"
                      value={billingInfo.fullName}
                      onChange={handleInputChange}
                      required
                      placeholder="محمد أحمد السعيد"
                    />
                  </div>

                  <div className="form-group">
                    <label>البريد الإلكتروني *</label>
                    <input
                      type="email"
                      name="email"
                      value={billingInfo.email}
                      onChange={handleInputChange}
                      required
                      placeholder="email@example.com"
                    />
                  </div>

                  <div className="form-group">
                    <label>رقم الجوال *</label>
                    <input
                      type="tel"
                      name="phone"
                      value={billingInfo.phone}
                      onChange={handleInputChange}
                      required
                      placeholder="+966 5XX XXX XXX"
                    />
                  </div>

                  <div className="form-group">
                    <label>اسم الشركة</label>
                    <input
                      type="text"
                      name="company"
                      value={billingInfo.company}
                      onChange={handleInputChange}
                      placeholder="اسم الشركة (اختياري)"
                    />
                  </div>

                  <div className="form-group full-width">
                    <label>الرقم الضريبي (اختياري)</label>
                    <input
                      type="text"
                      name="vatNumber"
                      value={billingInfo.vatNumber}
                      onChange={handleInputChange}
                      placeholder="3XXXXXXXXXX"
                    />
                  </div>

                  <div className="form-group full-width">
                    <label>العنوان *</label>
                    <input
                      type="text"
                      name="address"
                      value={billingInfo.address}
                      onChange={handleInputChange}
                      required
                      placeholder="الشارع، الحي"
                    />
                  </div>

                  <div className="form-group">
                    <label>المدينة *</label>
                    <input
                      type="text"
                      name="city"
                      value={billingInfo.city}
                      onChange={handleInputChange}
                      required
                      placeholder="الرياض"
                    />
                  </div>

                  <div className="form-group">
                    <label>الدولة *</label>
                    <select
                      name="country"
                      value={billingInfo.country}
                      onChange={(e) => setBillingInfo({ ...billingInfo, country: e.target.value })}
                      required
                    >
                      <option value="SA">المملكة العربية السعودية</option>
                      <option value="AE">الإمارات العربية المتحدة</option>
                      <option value="BH">البحرين</option>
                      <option value="KW">الكويت</option>
                      <option value="OM">عمان</option>
                      <option value="QA">قطر</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Terms & Submit */}
              <div className="form-section">
                <div className="terms-notice">
                  <p>
                    بالمتابعة، أنت توافق على 
                    <a href="/terms" target="_blank"> شروط الخدمة </a>
                    و
                    <a href="/privacy" target="_blank"> سياسة الخصوصية</a>
                  </p>
                  <p className="secure-notice">
                    🔒 جميع المعاملات مشفرة وآمنة
                  </p>
                </div>

                <button
                  type="submit"
                  className="btn-primary btn-large btn-checkout"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <span className="spinner"></span>
                      جاري المعالجة...
                    </>
                  ) : (
                    <>
                      إتمام الدفع - {(plan.price * 1.15).toFixed(2)} ريال
                    </>
                  )}
                </button>

                <button
                  type="button"
                  className="btn-text btn-large"
                  onClick={() => navigate('/app/billing')}
                  disabled={loading}
                >
                  إلغاء
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CheckoutPage
