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
              ودّع فوضى الإكسل والكروت… واحصل على{" "}
              <span className="dp-hero-highlight">بيانات نظيفة ودقيقة</span>
              {" "}خلال دقائق.
            </h1>
            <p className="dp-hero-description">
              DataPurity منصة ذكية تنظّف وتنظّم بيانات العملاء من ملفات Excel و CSV وصور الكروت، وتعيدها لك كملف جاهز للاستخدام في أنظمة العمل وفرق التسويق والمبيعات.
            </p>

            <div className="dp-hero-actions">
              <Link to="/login" className="dp-btn dp-btn-primary dp-hero-main-cta">
                ابدأ تنظيف أول 100 سجل مجاناً
              </Link>
              <span className="dp-hero-subtext">
                بدون بطاقة ائتمانية – تجربة كاملة قبل الاشتراك.
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
            <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
              <a href="#example" style={{ color: '#1F7FED', fontWeight: 600, fontSize: '0.95rem', textDecoration: 'none', borderBottom: '2px solid #1F7FED', paddingBottom: '2px' }}>
                شاهد مثالاً حقيقياً قبل/بعد ↓
              </a>
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

          {/* Growth Chart */}
          <div className="dp-hero-chart">
            <div className="dp-chart-container">
              <div className="dp-chart-header">
                <h3>التأثير على أعمالك</h3>
                <p>وفّر الوقت وزد الأرباح مع DataPurity</p>
              </div>
              
              <div className="dp-chart-visual">
                {/* Chart SVG */}
                <svg className="dp-growth-chart" viewBox="0 0 400 250" fill="none" xmlns="http://www.w3.org/2000/svg">
                  {/* Grid lines */}
                  <line x1="50" y1="200" x2="380" y2="200" stroke="#E5E7EB" strokeWidth="1" opacity="0.5"/>
                  <line x1="50" y1="150" x2="380" y2="150" stroke="#E5E7EB" strokeWidth="1" opacity="0.5"/>
                  <line x1="50" y1="100" x2="380" y2="100" stroke="#E5E7EB" strokeWidth="1" opacity="0.5"/>
                  <line x1="50" y1="50" x2="380" y2="50" stroke="#E5E7EB" strokeWidth="1" opacity="0.5"/>
                  
                  {/* Axes */}
                  <line x1="50" y1="30" x2="50" y2="210" stroke="#6B7280" strokeWidth="2"/>
                  <line x1="45" y1="210" x2="385" y2="210" stroke="#6B7280" strokeWidth="2"/>
                  
                  {/* Before DataPurity - Flat/Declining line */}
                  <path d="M 80 180 L 120 185 L 160 180 L 200 190" stroke="#EF4444" strokeWidth="3" strokeDasharray="5,5" opacity="0.6"/>
                  
                  {/* After DataPurity - Growth line */}
                  <path d="M 200 190 L 240 160 L 280 120 L 320 70 L 360 50" stroke="url(#growthGradient)" strokeWidth="4" strokeLinecap="round"/>
                  
                  {/* Growth area fill */}
                  <path d="M 200 210 L 200 190 L 240 160 L 280 120 L 320 70 L 360 50 L 360 210 Z" fill="url(#areaGradient)" opacity="0.2"/>
                  
                  {/* Data points */}
                  <circle cx="80" cy="180" r="4" fill="#EF4444"/>
                  <circle cx="160" cy="180" r="4" fill="#EF4444"/>
                  <circle cx="200" cy="190" r="5" fill="#F59E0B"/>
                  <circle cx="280" cy="120" r="5" fill="#1F7FED"/>
                  <circle cx="360" cy="50" r="6" fill="#10B981"/>
                  
                  {/* Labels */}
                  <text x="80" y="230" fontSize="11" fill="#6B7280" textAnchor="middle">قبل</text>
                  <text x="200" y="230" fontSize="11" fill="#F59E0B" textAnchor="middle" fontWeight="600">البداية</text>
                  <text x="360" y="230" fontSize="11" fill="#10B981" textAnchor="middle" fontWeight="600">بعد</text>
                  
                  {/* Y-axis labels */}
                  <text x="35" y="55" fontSize="10" fill="#6B7280" textAnchor="end">عالي</text>
                  <text x="35" y="155" fontSize="10" fill="#6B7280" textAnchor="end">متوسط</text>
                  <text x="35" y="205" fontSize="10" fill="#6B7280" textAnchor="end">منخفض</text>
                  
                  {/* Annotation */}
                  <text x="280" y="105" fontSize="12" fill="#1F7FED" fontWeight="600">+250%</text>
                  <path d="M 310 70 L 340 55" stroke="#10B981" strokeWidth="2" markerEnd="url(#arrowhead)"/>
                  
                  <defs>
                    <linearGradient id="growthGradient" x1="200" y1="190" x2="360" y2="50">
                      <stop offset="0%" stopColor="#F59E0B"/>
                      <stop offset="50%" stopColor="#1F7FED"/>
                      <stop offset="100%" stopColor="#10B981"/>
                    </linearGradient>
                    <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#1F7FED" stopOpacity="0.3"/>
                      <stop offset="100%" stopColor="#10B981" stopOpacity="0.1"/>
                    </linearGradient>
                    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
                      <polygon points="0 0, 10 3, 0 6" fill="#10B981"/>
                    </marker>
                  </defs>
                </svg>
              </div>

              <div className="dp-chart-stats">
                <div className="dp-stat-item dp-stat-time">
                  <div className="dp-stat-icon">⏱️</div>
                  <div className="dp-stat-content">
                    <div className="dp-stat-value">70%</div>
                    <div className="dp-stat-label">توفير في الوقت</div>
                  </div>
                </div>
                
                <div className="dp-stat-item dp-stat-sales">
                  <div className="dp-stat-icon">📈</div>
                  <div className="dp-stat-content">
                    <div className="dp-stat-value">+250%</div>
                    <div className="dp-stat-label">زيادة في المبيعات</div>
                  </div>
                </div>
                
                <div className="dp-stat-item dp-stat-revenue">
                  <div className="dp-stat-icon">💰</div>
                  <div className="dp-stat-content">
                    <div className="dp-stat-value">+180%</div>
                    <div className="dp-stat-label">نمو في الإيرادات</div>
                  </div>
                </div>
              </div>

              <div className="dp-chart-insight">
                <span className="dp-insight-icon">💡</span>
                <p>بيانات نظيفة = قرارات أسرع = أرباح أعلى</p>
              </div>
            </div>
          </div>
        </section>

        {/* How it works Diagram */}
        <section className="dp-section dp-diagram-section">
          <h2>كيف تعمل المنصة؟</h2>
          <p className="dp-section-subtitle">
            عملية بسيطة من 3 خطوات لتحويل بياناتك الفوضوية إلى بيانات نظيفة وجاهزة للاستخدام.
          </p>
          
          <div className="dp-process-diagram">
            <div className="dp-process-step">
              <div className="dp-process-icon dp-process-input">
                📤
              </div>
              <h3>1. الإدخال</h3>
              <p>ارفع ملفات Excel/CSV أو صور الكروت من جهازك أو جوالك.</p>
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
              <p>يقوم النظام بتنظيف وتصحيح البيانات واكتشاف التكرار والأخطاء تلقائياً.</p>
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
              <p>تحصل على ملف منظّم وجاهز للتصدير إلى Excel أو CRM أو أنظمة عملك.</p>
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
                <circle cx="40" cy="30" r="25" fill="url(#transformGradient)" opacity="0.15"/>
                <circle cx="40" cy="30" r="18" fill="url(#transformGradient)" opacity="0.1"/>
                <path d="M62 24 L22 24 M22 24 L30 16 M22 24 L30 20" stroke="url(#transformGradient)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M62 36 L22 36 M22 36 L30 40 M22 36 L30 44" stroke="url(#transformGradient)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
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
          <h2>ماذا يقدم DataPurity لشركتك؟</h2>
          <p className="dp-section-subtitle">
            ثلاث أدوات أساسية مخصصة لاحتياجات الشركات الحديثة
          </p>

          <div className="dp-features-grid">
            <div className="dp-feature-card">
              <div className="dp-feature-icon">📊</div>
              <h3>تنظيف ملفات Excel و CSV</h3>
              <p>
                أداة متقدمة لمعالجة الأخطاء، توحيد تنسيق البيانات، وإزالة التكرار — بيانات جاهزة للاستخدام فوراً في أنظمة العمل.
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
                ارفع صور الكروت من المعارض أو الاجتماعات — استخراج تلقائي من الصور إلى جدول جاهز يحتوي على الأسماء، الشركات، الأرقام، والإيميلات.
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
                تصدير مباشر إلى CRM وفرق التسويق — البيانات النظيفة جاهزة للدمج مباشرة مع:
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
          <h2>كيف تعمل المنصة؟</h2>
          <p className="dp-section-subtitle">
            عملية بسيطة من 3 خطوات لتحويل بياناتك الفوضوية إلى بيانات نظيفة وجاهزة للاستخدام.
          </p>
          <div className="dp-steps">
            <div className="dp-step">
              <span className="dp-step-number">١</span>
              <h3>ارفع ملفات Excel/CSV أو صور الكروت</h3>
              <p>من جهازك أو جوالك.</p>
            </div>
            <div className="dp-step">
              <span className="dp-step-number">٢</span>
              <h3>يقوم النظام بتنظيف وتصحيح البيانات</h3>
              <p>واكتشاف التكرار والأخطاء تلقائياً.</p>
            </div>
            <div className="dp-step">
              <span className="dp-step-number">٣</span>
              <h3>تحصل على ملف منظّم وجاهز للتصدير</h3>
              <p>إلى Excel أو CRM أو أنظمة عملك.</p>
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
            <div className="dp-price-card dp-price-card-free">
              <div className="dp-free-badge">مجاني للأبد</div>
              <h3>Free</h3>
              <p className="dp-price">
                <span style={{ fontSize: '3rem', fontWeight: 800 }}>0</span>
                <span style={{ fontSize: '1.25rem', marginRight: '0.5rem' }}>ريال</span>
              </p>
              <p style={{ fontSize: '0.9rem', color: '#64748b', marginTop: '-0.5rem', marginBottom: '0.75rem' }}>
                مثالية للتجربة والاستكشاف قبل الانتقال للخطة المدفوعة.
              </p>
              <p style={{ fontSize: '0.85rem', color: '#64748b', fontStyle: 'italic', marginBottom: '1.5rem' }}>
                يمكنك الإلغاء في أي وقت – بدون التزام طويل.
              </p>
              <ul>
                <li>عملية تنظيف واحدة شهريًا</li>
                <li>حتى 100 سجل لكل ملف</li>
                <li>10 كروت OCR شهريًا</li>
                <li>كروت إضافية: 0.50 ريال/كرت</li>
                <li>تصدير إلى Excel/CSV</li>
                <li>تقرير Data Health أساسي</li>
                <li>دعم عبر البريد الإلكتروني</li>
              </ul>
              <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'rgba(79, 227, 193, 0.1)', borderRadius: '0.5rem', border: '1px solid rgba(79, 227, 193, 0.3)' }}>
                <p style={{ margin: 0, fontSize: '0.85rem', color: '#059669', fontWeight: 600, textAlign: 'center' }}>
                  ✨ ابدأ فورًا بدون بطاقة ائتمانية
                </p>
              </div>
              <Link to="/login" className="dp-btn dp-btn-primary" style={{ marginTop: '1.5rem', width: '100%', textAlign: 'center' }}>
                ابدأ مجانًا
              </Link>
            </div>

            <div className="dp-price-card">
              <h3>Starter</h3>
              <p className="dp-price">79 <span style={{ fontSize: '1rem', fontWeight: 500 }}>ريال / شهر</span></p>
              <p style={{ fontSize: '0.9rem', color: '#64748b', marginTop: '-0.5rem', marginBottom: '0.75rem' }}>
                للشركات الناشئة والفرق الصغيرة
              </p>
              <p style={{ fontSize: '0.85rem', color: '#64748b', fontStyle: 'italic', marginBottom: '1.5rem' }}>
                يمكنك الإلغاء في أي وقت – بدون التزام طويل.
              </p>
              <ul>
                <li>5 عمليات تنظيف شهريًا</li>
                <li>حتى 500 سجل لكل ملف</li>
                <li>100 كرت OCR شهريًا</li>
                <li>كروت إضافية: 0.40 ريال/كرت</li>
                <li>تصدير غير محدود</li>
                <li>تقارير Data Health متقدمة</li>
                <li>كشف التكرار الذكي</li>
                <li>دعم ذو أولوية</li>
              </ul>
              <Link to="/checkout?plan=starter" className="dp-btn dp-btn-primary" style={{ marginTop: '1.5rem', width: '100%', textAlign: 'center' }}>
                اشترك الآن
              </Link>
            </div>

            <div className="dp-price-card dp-price-card-main">
              <div className="dp-popular-badge">الأكثر طلبًا</div>
              <h3>Business</h3>
              <p className="dp-price">199 <span style={{ fontSize: '1rem', fontWeight: 500 }}>ريال / شهر</span></p>
              <p style={{ fontSize: '0.9rem', color: '#64748b', marginTop: '-0.5rem', marginBottom: '0.75rem' }}>
                للشركات النامية والفرق المتوسطة
              </p>
              <p style={{ fontSize: '0.85rem', color: '#64748b', fontStyle: 'italic', marginBottom: '1.5rem' }}>
                يمكنك الإلغاء في أي وقت – بدون التزام طويل.
              </p>
              <ul>
                <li>20 عملية تنظيف شهريًا</li>
                <li>حتى 2000 سجل لكل ملف</li>
                <li>500 كرت OCR شهريًا</li>
                <li>كروت إضافية: 0.30 ريال/كرت</li>
                <li>تقارير جودة بيانات تفصيلية</li>
                <li>تصنيف العملاء (Hot/Warm/Cold)</li>
                <li>حتى 5 مستخدمين</li>
                <li>دعم WhatsApp مباشر</li>
              </ul>
              <Link to="/checkout?plan=business" className="dp-btn dp-btn-primary" style={{ marginTop: '1.5rem', width: '100%', textAlign: 'center' }}>
                اشترك الآن
              </Link>
            </div>
          </div>
          <div className="dp-pricing-note" style={{ 
            textAlign: 'center', 
            marginTop: '2rem', 
            padding: '1.5rem', 
            background: 'rgba(31, 127, 237, 0.05)', 
            borderRadius: '1rem',
            border: '1px solid rgba(31, 127, 237, 0.2)',
            maxWidth: '800px',
            margin: '2rem auto 1.5rem'
          }}>
            <p style={{ margin: 0, fontSize: '1rem', color: '#1F7FED', fontWeight: 600, marginBottom: '0.5rem' }}>
              💳 الدفع حسب الاستخدام للكروت
            </p>
            <p style={{ margin: 0, fontSize: '0.9rem', color: '#64748b', lineHeight: 1.6 }}>
              عند انتهاء الكروت المجانية، يمكنك شراء كروت إضافية بأسعار مرنة حسب باقتك.
              <br />
              ادفع فقط مقابل ما تستخدمه — بدون التزامات إضافية.
            </p>
          </div>
          <div className="dp-pricing-cta">
            <Link to="/login" className="dp-btn dp-btn-primary">
              ابدأ الآن — تشغيل فوري من المتصفح
            </Link>
            <span>بدون التزام. بدون تجهيزات.</span>
          </div>
        </section>

        {/* Example Section */}
        <section id="example" className="dp-section">
          <div className="dp-hero-card" style={{ maxWidth: '800px', margin: '0 auto' }}>
            <h2>مثال حقيقي قبل/بعد – هكذا ننظّف بياناتك</h2>
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
            <h2>جاهز لتنظيف بياناتك والبدء الآن؟</h2>
            <p>ابدأ مجاناً اليوم ونظّف حتى 100 سجل بدون أي التزام أو بطاقة ائتمانية.</p>
            <div className="dp-cta-buttons">
              <Link to="/login" className="dp-btn dp-btn-primary dp-btn-large">
                ابدأ مجاناً الآن
              </Link>
              <a href="#pricing" className="dp-btn dp-btn-text">
                اطلع على جميع الباقات
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
