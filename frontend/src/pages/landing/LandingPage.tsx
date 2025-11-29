import { useNavigate } from 'react-router-dom'
import './LandingPage.css'

function LandingPage() {
  const navigate = useNavigate()
  const plans = [
    {
      id: 'free',
      title: 'الخطة المجانية',
      price: '0',
      period: 'ريال/شهر',
      description: 'مناسبة للتجربة السريعة وعدد محدود من عمليات التنظيف.',
      features: [
        'تنظيف ملف واحد حتى 100 سجل',
        '10 بطاقات أعمال OCR',
        'تقارير جودة أساسية'
      ],
      cta: 'ابدأ مجاناً'
    },
    {
      id: 'starter',
      title: 'خطة الشركات الناشئة',
      price: '79',
      period: 'ريال/شهر',
      description: 'أفضل خيار للفرق الصغيرة التي تحتاج معالجة منتظمة للبيانات.',
      features: [
        '5 عمليات تنظيف لكل شهر',
        'حتى 500 سجل في الملف الواحد',
        '100 بطاقة أعمال OCR',
        'تقارير وتصدير CSV/Excel'
      ],
      popular: true,
      cta: 'جرّب الخطة'
    },
    {
      id: 'business',
      title: 'خطة الأعمال',
      price: '199',
      period: 'ريال/شهر',
      description: 'قدرات متقدمة مع دعم الأولوية وفريق متعدد المستخدمين.',
      features: [
        '20 عملية تنظيف + كشف مكرر ذكي',
        '2000 سجل لكل ملف',
        '500 بطاقة أعمال OCR',
        'دعم WhatsApp + وصول API'
      ],
      cta: 'احجز عرضاً'
    }
  ]

  return (
    <div className="landing-page">
      {/* Header */}
      <header className="landing-header">
        <div className="container">
          <div className="header-content">
            <div className="logo">
              <svg width="32" height="32" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M50 10C50 10 25 35 25 55C25 70 35 80 50 80C65 80 75 70 75 55C75 35 50 10 50 10Z" fill="url(#gradient-landing)"/>
                <rect x="35" y="45" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
                <rect x="35" y="53" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
                <rect x="35" y="61" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
                <defs>
                  <linearGradient id="gradient-landing" x1="50" y1="10" x2="50" y2="80" gradientUnits="userSpaceOnUse">
                    <stop stopColor="#1F7FED"/>
                    <stop offset="1" stopColor="#4FE3C1"/>
                  </linearGradient>
                </defs>
              </svg>
              <span className="brand">DataPurity</span>
            </div>
            
            <div className="header-actions">
              <button className="btn-secondary" onClick={() => navigate('/login')}>
                تسجيل الدخول
              </button>
              <button className="btn-primary" onClick={() => navigate('/signup')}>
                إنشاء حساب
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <h1 className="hero-title">
              تنظيف ذكي للبيانات
              <br />
              <span className="gradient-text">بتقنية الذكاء الاصطناعي</span>
            </h1>
            <p className="hero-description">
              منصة احترافية لتنظيف البيانات، معالجة بطاقات الأعمال بتقنية OCR المتقدمة،
              وإدارة جهات الاتصال بكفاءة عالية
            </p>
            <div className="hero-actions">
              <button className="btn-hero-primary" onClick={() => navigate('/signup')}>
                ابدأ مجاناً
              </button>
              <button className="btn-hero-secondary" onClick={() => navigate('/login')}>
                تسجيل الدخول
              </button>
            </div>
          </div>
          
          <div className="hero-image">
            <div className="floating-card card-1">
              <div className="card-icon">📊</div>
              <div className="card-text">تنظيف تلقائي</div>
            </div>
            <div className="floating-card card-2">
              <div className="card-icon">🎯</div>
              <div className="card-text">دقة 99%</div>
            </div>
            <div className="floating-card card-3">
              <div className="card-icon">⚡</div>
              <div className="card-text">معالجة فورية</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="container">
          <h2 className="section-title">ميزات DataPurity</h2>
          <p className="section-subtitle">
            كل ما تحتاجه لإدارة بياناتك باحترافية
          </p>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🔍</div>
              <h3 className="feature-title">OCR متقدم</h3>
              <p className="feature-description">
                استخراج ذكي للبيانات من بطاقات الأعمال باستخدام Google Cloud Vision
                بدقة عالية ودعم كامل للغة العربية والإنجليزية
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">✨</div>
              <h3 className="feature-title">تنظيف تلقائي</h3>
              <p className="feature-description">
                تنظيف البيانات تلقائياً، إزالة التكرارات، تصحيح الأخطاء،
                وتوحيد الصيغ بضغطة زر واحدة
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📱</div>
              <h3 className="feature-title">معالجة جماعية</h3>
              <p className="feature-description">
                معالجة مئات البطاقات دفعة واحدة، توفير الوقت والجهد
                مع ضمان الدقة والجودة
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3 className="feature-title">تقارير تفصيلية</h3>
              <p className="feature-description">
                تقارير شاملة عن جودة البيانات، الإحصائيات، والتحليلات
                لاتخاذ قرارات أفضل
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🔒</div>
              <h3 className="feature-title">أمان عالي</h3>
              <p className="feature-description">
                حماية متقدمة للبيانات، تشفير شامل، ونسخ احتياطي تلقائي
                لضمان سلامة معلوماتك
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">💾</div>
              <h3 className="feature-title">تصدير سهل</h3>
              <p className="feature-description">
                تصدير البيانات بصيغ متعددة (Excel, CSV, JSON)
                مع دعم كامل للأحرف العربية
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="pricing" id="pricing">
        <div className="container">
          <h2 className="section-title">خطط الاشتراك</h2>
          <p className="section-subtitle">
            اختر الخطة المناسبة لفريقك وابدأ بتنظيف البيانات خلال دقائق.
          </p>

          <div className="pricing-grid">
            {plans.map(plan => (
              <div
                key={plan.id}
                className={`pricing-card ${plan.popular ? 'pricing-card-popular' : ''}`}
              >
                {plan.popular && <div className="plan-badge">الأكثر طلباً</div>}
                <h3 className="plan-title">{plan.title}</h3>
                <p className="plan-description">{plan.description}</p>
                <div className="plan-price">
                  <span className="price-number">{plan.price}</span>
                  <span className="price-period">{plan.period}</span>
                </div>

                <ul className="plan-features">
                  {plan.features.map(feature => (
                    <li key={feature}>
                      <span>✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>

                <button
                  className="btn-plan"
                  onClick={() => navigate(`/checkout?plan=${plan.id}`)}
                >
                  {plan.cta}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta">
        <div className="container">
          <div className="cta-content">
            <h2 className="cta-title">جاهز لتحسين إدارة بياناتك؟</h2>
            <p className="cta-description">
              ابدأ الآن مع DataPurity واستمتع بتجربة تنظيف البيانات الاحترافية
            </p>
            <button className="btn-cta" onClick={() => navigate('/signup')}>
              إنشاء حساب مجاني
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-brand">
              <div className="logo">
                <svg width="28" height="28" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M50 10C50 10 25 35 25 55C25 70 35 80 50 80C65 80 75 70 75 55C75 35 50 10 50 10Z" fill="url(#gradient-footer)"/>
                  <rect x="35" y="45" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
                  <rect x="35" y="53" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
                  <rect x="35" y="61" width="30" height="4" rx="2" fill="white" opacity="0.9"/>
                  <defs>
                    <linearGradient id="gradient-footer" x1="50" y1="10" x2="50" y2="80" gradientUnits="userSpaceOnUse">
                      <stop stopColor="#1F7FED"/>
                      <stop offset="1" stopColor="#4FE3C1"/>
                    </linearGradient>
                  </defs>
                </svg>
                <span className="brand">DataPurity</span>
              </div>
              <p className="footer-tagline">تنظيف ذكي للبيانات بتقنية الذكاء الاصطناعي</p>
            </div>
            
            <div className="footer-copyright">
              <p>© 2025 DataPurity. جميع الحقوق محفوظة</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage
