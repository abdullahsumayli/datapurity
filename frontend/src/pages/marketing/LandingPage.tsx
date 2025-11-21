import React from "react";
import { Link } from "react-router-dom";
import PWAInstallButton from "../../components/PWAInstallButton/PWAInstallButton";
import "../../styles/landing.css";

export const LandingPage: React.FC = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  return (
    <div className="dp-landing">
      {/* Top Nav */}
      <header className="dp-landing-nav">
        <div className="dp-landing-logo">
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
          <span>DataPurity</span>
        </div>
        
        <button 
          className="dp-mobile-menu-btn"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="القائمة"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <nav className={`dp-landing-links ${mobileMenuOpen ? 'dp-menu-open' : ''}`}>
          <a href="#features" onClick={() => setMobileMenuOpen(false)}>المزايا</a>
          <a href="#how-it-works" onClick={() => setMobileMenuOpen(false)}>كيف يعمل؟</a>
          <a href="#sectors" onClick={() => setMobileMenuOpen(false)}>القطاعات</a>
          <a href="#pricing" onClick={() => setMobileMenuOpen(false)}>الأسعار</a>
        </nav>
        <div className="dp-landing-cta-nav">
          <Link to="/login" className="dp-btn dp-btn-text">
            دخول
          </Link>
        </div>
      </header>

      {/* Hero */}
      <main className="dp-landing-main">
        <section className="dp-hero">
          <div className="dp-hero-text">
            <div className="dp-badge">🚀 منصة سعودية متقدمة</div>
            <h1>
              حوّل فوضى الإكسل والكروت
              <br />
              إلى{" "}
              <span className="dp-hero-highlight">بيانات جاهزة للاستخدام</span>
            </h1>
            <p className="dp-hero-tagline">
              DataPurity — منصة ذكية لتنظيف وتنظيم بيانات العملاء
            </p>
            <p className="dp-hero-description">
              DataPurity تساعد الشركات على تنظيم بيانات العملاء، تنظيف قوائم Excel، واستخراج بيانات كروت الأعمال من المعارض والزيارات خلال ثوانٍ فقط… مباشرة من المتصفح.
            </p>

            <div className="dp-hero-actions">
              <Link to="/login" className="dp-btn dp-btn-primary dp-hero-main-cta">
                ابدأ بتنظيف أول 100 سجل مجانًا
              </Link>
              <span className="dp-hero-subtext">
                بدون تعقيد. بدون أخطاء. بدون شغل يدوي.
              </span>
            </div>

            <div className="dp-hero-metrics">
              <div>
                <strong>+50,000</strong>
                <span>سجل بيانات تمت معالجته</span>
              </div>
              <div>
                <strong>+20</strong>
                <span>شركة جرّبت المنصة</span>
              </div>
              <div>
                <strong>99٪</strong>
                <span>رضا عن سهولة الاستخدام والنتائج</span>
              </div>
            </div>

            <div className="dp-trust-badges">
              <div className="dp-trust-item">
                <span className="dp-trust-icon">✓</span>
                <span>بيانات آمنة ومشفرة</span>
              </div>
              <div className="dp-trust-item">
                <span className="dp-trust-icon">✓</span>
                <span>استخدام فوري بدون تثبيت</span>
              </div>
              <div className="dp-trust-item">
                <span className="dp-trust-icon">✓</span>
                <span>دعم فني سريع</span>
              </div>
            </div>
          </div>
        </section>

        {/* How it works Diagram */}
        <section className="dp-section dp-diagram-section">
          <h2>كيف تعمل المنصة؟</h2>
          <p className="dp-section-subtitle">
            عملية بسيطة من 3 خطوات لتحويل بياناتك الفوضوية إلى بيانات نظيفة جاهزة للاستخدام
          </p>
          
          <div className="dp-process-diagram">
            <div className="dp-process-step">
              <div className="dp-process-icon dp-process-input">
                📤
              </div>
              <h3>1. الإدخال</h3>
              <p>ارفع ملفات Excel/CSV أو صور كروت الأعمال</p>
              <div className="dp-process-examples">
                <span className="dp-tag">Excel</span>
                <span className="dp-tag">CSV</span>
                <span className="dp-tag">صور</span>
                <span className="dp-tag">ZIP</span>
              </div>
            </div>

            <div className="dp-process-arrow">
              <svg width="60" height="40" viewBox="0 0 60 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 20 L45 20 M45 20 L35 10 M45 20 L35 30" stroke="#1F7FED" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>

            <div className="dp-process-step">
              <div className="dp-process-icon dp-process-processing">
                ⚙️
              </div>
              <h3>2. المعالجة الذكية</h3>
              <p>تنظيف، تصحيح، واستخراج تلقائي للبيانات</p>
              <div className="dp-process-examples">
                <span className="dp-tag">تصحيح الأرقام</span>
                <span className="dp-tag">إزالة التكرار</span>
                <span className="dp-tag">OCR</span>
                <span className="dp-tag">التحقق</span>
              </div>
            </div>

            <div className="dp-process-arrow">
              <svg width="60" height="40" viewBox="0 0 60 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 20 L45 20 M45 20 L35 10 M45 20 L35 30" stroke="#1F7FED" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>

            <div className="dp-process-step">
              <div className="dp-process-icon dp-process-output">
                ✅
              </div>
              <h3>3. النتيجة النظيفة</h3>
              <p>بيانات جاهزة للاستخدام في أنظمتك</p>
              <div className="dp-process-examples">
                <span className="dp-tag">Excel</span>
                <span className="dp-tag">CRM</span>
                <span className="dp-tag">تقارير</span>
                <span className="dp-tag">API</span>
              </div>
            </div>
          </div>

          {/* Visual representation */}
          <div className="dp-visual-flow">
            <div className="dp-visual-box dp-visual-messy">
              <div className="dp-visual-header">قبل التنظيف ❌</div>
              <div className="dp-visual-content">
                <div className="dp-messy-data">
                  <span>05xxxxxxx</span>
                  <span>+966xxxxxxx</span>
                  <span>email@@@</span>
                  <span>تكرار تكرار</span>
                  <span>بيانات فوضوية</span>
                  <span>???</span>
                </div>
              </div>
            </div>

            <div className="dp-visual-transform">
              <svg width="80" height="60" viewBox="0 0 80 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="40" cy="30" r="25" fill="url(#transformGradient)" opacity="0.2"/>
                <path d="M20 30 L55 30 M55 30 L45 20 M55 30 L45 40" stroke="url(#transformGradient)" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round"/>
                <defs>
                  <linearGradient id="transformGradient" x1="0" y1="0" x2="80" y2="60">
                    <stop offset="0%" stopColor="#1F7FED"/>
                    <stop offset="100%" stopColor="#4FE3C1"/>
                  </linearGradient>
                </defs>
              </svg>
              <span className="dp-transform-text">DataPurity</span>
            </div>

            <div className="dp-visual-box dp-visual-clean">
              <div className="dp-visual-header">بعد التنظيف ✓</div>
              <div className="dp-visual-content">
                <div className="dp-clean-data">
                  <div className="dp-data-row">
                    <span className="dp-data-label">الجوال:</span>
                    <span className="dp-data-value">+966 5X XXX XXXX</span>
                  </div>
                  <div className="dp-data-row">
                    <span className="dp-data-label">البريد:</span>
                    <span className="dp-data-value">valid@email.com</span>
                  </div>
                  <div className="dp-data-row">
                    <span className="dp-data-label">الحالة:</span>
                    <span className="dp-data-value dp-status-clean">✓ نظيف</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features */}
        <section id="features" className="dp-section">
          <h2>ماذا يقدم DataPurity؟</h2>
          <p className="dp-section-subtitle">
            ثلاث أدوات أساسية مخصصة لاحتياجات الشركات الحديثة
          </p>

          <div className="dp-features-grid">
            <div className="dp-feature-card">
              <div className="dp-feature-icon">📊</div>
              <h3>تنظيف ملفات Excel و CSV</h3>
              <p>
                أداة متقدمة لمعالجة الأخطاء، توحيد تنسيق البيانات، وإزالة التكرار، لتصبح بياناتك جاهزة للاستخدام داخل الأنظمة التشغيلية.
              </p>
              <p style={{ marginTop: '0.75rem', fontWeight: 600 }}>يشمل:</p>
              <ul>
                <li>تصحيح وتوحيد أرقام الجوال</li>
                <li>اكتشاف السجلات المكررة</li>
                <li>كشف الإيميلات الخاطئة</li>
                <li>حساب Data Health Score</li>
              </ul>
            </div>

            <div className="dp-feature-card">
              <div className="dp-feature-icon">📇</div>
              <h3>استخراج بيانات كروت الأعمال (OCR)</h3>
              <p>
                ارفع صور الكروت من المعارض أو الاجتماعات…
                <br />
                والنظام يستخرج الأسماء، الشركات، الأرقام، والإيميلات تلقائيًا.
              </p>
              <p style={{ marginTop: '0.75rem', fontWeight: 600 }}>يشمل:</p>
              <ul>
                <li>OCR عربي/إنجليزي</li>
                <li>معاينة قبل الحفظ</li>
                <li>تصدير مباشر إلى Excel أو CRM</li>
              </ul>
            </div>

            <div className="dp-feature-card">
              <div className="dp-feature-icon">🎯</div>
              <h3>ملفات جاهزة للاستخدام في أنظمة العمل</h3>
              <p>
                يمكن تصدير البيانات نظيفة وجاهزة للدمج مع:
              </p>
              <ul>
                <li>أنظمة CRM</li>
                <li>فرق التسويق</li>
                <li>فرق المبيعات</li>
                <li>لوحات التحليل والتشغيل</li>
              </ul>
              <p style={{ marginTop: '0.75rem', fontWeight: 600 }}>
                مع تقسيم تلقائي للعملاء إلى:
                <br />
                Hot / Warm / Cold
              </p>
            </div>
          </div>
        </section>

        {/* How it works */}
        <section id="how-it-works" className="dp-section dp-section-alt">
          <h2>كيف يعمل DataPurity؟</h2>
          <div className="dp-steps">
            <div className="dp-step">
              <span className="dp-step-number">١</span>
              <h3>ارفع ملفات Excel أو صور الكروت</h3>
              <p>من الحاسوب أو الجوال.</p>
            </div>
            <div className="dp-step">
              <span className="dp-step-number">٢</span>
              <h3>النظام ينظّف ويفهم البيانات</h3>
              <p>تصحيح – استخراج – تنظيم – تدقيق.</p>
            </div>
            <div className="dp-step">
              <span className="dp-step-number">٣</span>
              <h3>تحصل على ملف نظيف جاهز للاستخدام</h3>
              <p>تصدير فوري إلى Excel أو CRM.</p>
            </div>
          </div>
        </section>

        {/* Sectors */}
        <section id="sectors" className="dp-section">
          <h2>مناسب لعدة قطاعات</h2>
          <div className="dp-sectors-grid">
            <div className="dp-sector-card">
              <h3>شركات التطوير العقاري</h3>
              <p>تنظيم بيانات الزوار والمهتمين بالمشاريع.</p>
            </div>
            <div className="dp-sector-card">
              <h3>شركات تنظيم المعارض</h3>
              <p>تحويل بيانات التسجيل والحضور إلى قوائم عملاء واضحة.</p>
            </div>
            <div className="dp-sector-card">
              <h3>وكالات التسويق</h3>
              <p>تنظيف بيانات العملاء قبل التشغيل.</p>
            </div>
            <div className="dp-sector-card">
              <h3>شركات B2B</h3>
              <p>تنظيم بيانات العملاء والموردين وتحسين جودة السجلات.</p>
            </div>
          </div>
        </section>

        {/* Pricing teaser */}
        <section id="pricing" className="dp-section dp-section-alt">
          <h2>خطط الاشتراك</h2>
          <p className="dp-section-subtitle">
            اختر الخطة المناسبة لحجم عملك
          </p>
          <div className="dp-pricing-grid">
            <div className="dp-price-card">
              <h3>Starter</h3>
              <p className="dp-price">79 / شهر</p>
              <ul>
                <li>3 عمليات تنظيف</li>
                <li>50 كرت شهريًا</li>
                <li>تصدير غير محدود</li>
              </ul>
            </div>
            <div className="dp-price-card dp-price-card-main">
              <div className="dp-popular-badge">الأكثر طلبًا</div>
              <h3>Business</h3>
              <p className="dp-price">199 / شهر</p>
              <ul>
                <li>10 عمليات تنظيف</li>
                <li>300 كرت</li>
                <li>تقارير جودة بيانات</li>
                <li>حتى 3 مستخدمين</li>
              </ul>
            </div>
            <div className="dp-price-card">
              <h3>Pro</h3>
              <p className="dp-price">399 / شهر</p>
              <ul>
                <li>30 عملية تنظيف</li>
                <li>1000 كرت</li>
                <li>وصول إلى API و Webhooks</li>
              </ul>
            </div>
          </div>
          <div className="dp-pricing-cta">
            <Link to="/login" className="dp-btn dp-btn-primary">
              ابدأ الآن — تشغيل فوري من المتصفح
            </Link>
            <span>بدون التزام. بدون تجهيزات.</span>
          </div>
        </section>

        {/* Example Section */}
        <section className="dp-section">
          <div className="dp-hero-card" style={{ maxWidth: '800px', margin: '0 auto' }}>
            <h2>مثال مبسّط</h2>
            <div className="dp-hero-mini-table">
              <div className="dp-hero-mini-header">
                <span>الاسم</span>
                <span>الجوال</span>
                <span>الحالة</span>
              </div>
              <div className="dp-hero-mini-row">
                <span>محمد سعيد أحمد</span>
                <span>+966 5•••• ••••</span>
                <span className="dp-pill dp-pill-good">تم التنظيف</span>
              </div>
              <div className="dp-hero-mini-row">
                <span>شركة تطوير الشرق</span>
                <span>+966 5•••• ••••</span>
                <span className="dp-pill dp-pill-good">جاهز للاستخدام</span>
              </div>
              <div className="dp-hero-mini-row">
                <span>Lead من أحد المعارض</span>
                <span>غير صالح</span>
                <span className="dp-pill dp-pill-bad">رقم غير قابل للمعالجة</span>
              </div>
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section className="dp-section dp-cta-final">
          <div className="dp-cta-content">
            <h2>جاهز لتنظيف بياناتك؟</h2>
            <p>ابدأ مجانًا بتنظيف أول 100 سجل — بدون بطاقة ائتمانية</p>
            <div className="dp-cta-buttons">
              <Link to="/login" className="dp-btn dp-btn-primary dp-btn-large">
                ابدأ الآن مجانًا
              </Link>
              <a href="#pricing" className="dp-btn dp-btn-text">
                اطلع على الأسعار
              </a>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="dp-footer">
          <span>© {new Date().getFullYear()} DataPurity – منصة ذكية لتنظيف وتنظيم بيانات العملاء</span>
          <span>مصممة للشركات الحديثة في المملكة العربية السعودية</span>
        </footer>
      </main>
      
      {/* PWA Install Button */}
      <PWAInstallButton />
    </div>
  );
};
