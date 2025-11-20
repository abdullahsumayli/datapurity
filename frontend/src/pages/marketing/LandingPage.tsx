import React from "react";
import { Link } from "react-router-dom";
import "../../styles/landing.css";

export const LandingPage: React.FC = () => {
  return (
    <div className="dp-landing">
      {/* Top Nav */}
      <header className="dp-landing-nav">
        <div className="dp-landing-logo">
          <span className="dp-logo-dot" />
          <span>DataPurity</span>
        </div>
        <nav className="dp-landing-links">
          <a href="#features">المزايا</a>
          <a href="#how-it-works">كيف يعمل؟</a>
          <a href="#sectors">القطاعات</a>
          <a href="#pricing">الأسعار</a>
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
            <h1>
              حوِّل فوضى الإكسل والكروت
              <br />
              إلى{" "}
              <span className="dp-hero-highlight">داتا نظيفة جاهزة للبيع</span>
            </h1>
            <p>
              DataPurity منصة سعودية تنظّف بيانات عملائك، وتحوّل كروت الأعمال
              من المعارض والزيارات إلى ملفات Excel جاهزة للتسويق والمبيعات –
              من المتصفح أو كتطبيق PWA على جوالك.
            </p>

            <div className="dp-hero-actions">
              <Link to="/login" className="dp-btn dp-btn-primary dp-hero-main-cta">
                جرّب تنظيف أول ١٠٠ سجل مجاناً
              </Link>
              <span className="dp-hero-subtext">
                بدون كود – بدون تعقيد – تركيز كامل على الشركات في السعودية.
              </span>
            </div>

            <div className="dp-hero-metrics">
              <div>
                <strong>+50k</strong>
                <span>سجل بيانات تم تنظيفه</span>
              </div>
              <div>
                <strong>+20</strong>
                <span>شركة سعودية جرّبت DataPurity</span>
              </div>
              <div>
                <strong>99٪</strong>
                <span>نسبة رضا عن سهولة الاستخدام</span>
              </div>
            </div>
          </div>

          <div className="dp-hero-card">
            <div className="dp-hero-card-header">
              <span>تشغيل فوري</span>
              <span className="dp-pill">PWA</span>
            </div>
            <h2>مثال عملي</h2>
            <ul className="dp-hero-steps">
              <li>١. ترفع ملف Excel أو صور كروت من المعرض.</li>
              <li>٢. النظام ينظّف الأرقام ويزيل التكرار ويكتشف الأخطاء.</li>
              <li>٣. تحصل على ملف جاهز للتسويق (واتساب / إعلانات).</li>
            </ul>
            <div className="dp-hero-mini-table">
              <div className="dp-hero-mini-header">
                <span>الاسم</span>
                <span>الجوال</span>
                <span>الحالة</span>
              </div>
              <div className="dp-hero-mini-row">
                <span>محمد القحطاني</span>
                <span>+966 5•••• ••••</span>
                <span className="dp-pill dp-pill-good">تم التنظيف</span>
              </div>
              <div className="dp-hero-mini-row">
                <span>شركة تطوير الرياض</span>
                <span>+966 5•••• ••••</span>
                <span className="dp-pill dp-pill-good">جاهز للتصدير</span>
              </div>
              <div className="dp-hero-mini-row">
                <span>Lead من معرض جدة</span>
                <span>غير صالح</span>
                <span className="dp-pill dp-pill-bad">رقم مرفوض</span>
              </div>
            </div>
          </div>
        </section>

        {/* Features */}
        <section id="features" className="dp-section">
          <h2>ماذا يفعل DataPurity بالضبط؟</h2>
          <p className="dp-section-subtitle">
            ثلاث أدوات أساسية، مبنية خصيصاً للشركات في السعودية.
          </p>

          <div className="dp-features-grid">
            <div className="dp-feature-card">
              <h3>تنظيف ملفات Excel و CSV</h3>
              <p>
                يزيل التكرار، يصحّح أرقام الجوال السعودية، يكتشف الإيميلات
                الخاطئة، ويعطيك ملفاً واحداً نظيفاً جاهزاً للاستخدام.
              </p>
              <ul>
                <li>تنسيق أرقام 05 و +966 تلقائياً</li>
                <li>كشف ودمج السجلات المكررة</li>
                <li>حساب Health Score لقائمة العملاء</li>
              </ul>
            </div>

            <div className="dp-feature-card">
              <h3>تحويل كروت الأعمال إلى بيانات</h3>
              <p>
                ارفع صور الكروت من المعارض والزيارات الميدانية، ودع المنصة
                تستخرج الأسماء، الشركات، الأرقام، والإيميلات تلقائياً.
              </p>
              <ul>
                <li>OCR عربي / إنجليزي</li>
                <li>معاينة قبل الحفظ</li>
                <li>تصدير مباشر إلى Excel أو CRM</li>
              </ul>
            </div>

            <div className="dp-feature-card">
              <h3>تصدير جاهز للتسويق والمبيعات</h3>
              <p>
                ملف واحد جاهز للرفع إلى واتساب، حملات Meta، أو أدوات البريد،
                بدون شغل يدوي مرهق على الإكسل.
              </p>
              <ul>
                <li>قوائم واتساب Marketing</li>
                <li>قوائم إعلانات Meta / Google</li>
                <li>تقسيم عملاء Hot / Warm / Cold</li>
              </ul>
            </div>
          </div>
        </section>

        {/* How it works */}
        <section id="how-it-works" className="dp-section dp-section-alt">
          <h2>كيف يعمل DataPurity؟</h2>
          <div className="dp-steps">
            <div className="dp-step">
              <span className="dp-step-number">١</span>
              <h3>ترفع ملفاتك أو صور الكروت</h3>
              <p>ملفات Excel/CSV أو صور كروت من المعارض والزيارات.</p>
            </div>
            <div className="dp-step">
              <span className="dp-step-number">٢</span>
              <h3>النظام ينظّف ويفهم البيانات</h3>
              <p>تنظيف أرقام، إزالة تكرار، فهم الأسماء والعناوين بالعربي.</p>
            </div>
            <div className="dp-step">
              <span className="dp-step-number">٣</span>
              <h3>تحصل على ملف نظيف جاهز للاستخدام</h3>
              <p>تصدير إلى Excel أو تكامل مع أدوات التسويق والـ CRM.</p>
            </div>
          </div>
        </section>

        {/* Sectors */}
        <section id="sectors" className="dp-section">
          <h2>مصمّم لواقع الشركات في السعودية</h2>
          <div className="dp-sectors-grid">
            <div className="dp-sector-card">
              <h3>شركات التطوير العقاري</h3>
              <p>تنظيم بيانات زوّار المعارض والمشاريع وحملات الوسيط.</p>
            </div>
            <div className="dp-sector-card">
              <h3>شركات تنظيم المعارض والفعاليات</h3>
              <p>تحويل بيانات التسجيل والحضور إلى قوائم عملاء منظّمة.</p>
            </div>
            <div className="dp-sector-card">
              <h3>وكالات التسويق الرقمي</h3>
              <p>تنظيف قوائم العملاء قبل أي حملة Ads أو رسائل جماعية.</p>
            </div>
            <div className="dp-sector-card">
              <h3>شركات B2B والتوريد</h3>
              <p>حفظ تاريخ العملاء والموردين بشكل نظيف يسهل تحليله.</p>
            </div>
          </div>
        </section>

        {/* Pricing teaser */}
        <section id="pricing" className="dp-section dp-section-alt">
          <h2>خطط بسيطة تناسب الشركات الصغيرة والمتوسطة</h2>
          <p className="dp-section-subtitle">
            ابدأ بخطة صغيرة، ووسّع لاحقاً مع نمو فريق المبيعات عندك.
          </p>
          <div className="dp-pricing-grid">
            <div className="dp-price-card">
              <h3>Starter</h3>
              <p className="dp-price">79 ر.س / شهر</p>
              <ul>
                <li>٣ عمليات تنظيف شهرياً</li>
                <li>٥٠ كرت شهرياً</li>
                <li>تصدير غير محدود للملفات</li>
              </ul>
            </div>
            <div className="dp-price-card dp-price-card-main">
              <h3>Business</h3>
              <p className="dp-price">199 ر.س / شهر</p>
              <ul>
                <li>١٠ عمليات تنظيف شهرياً</li>
                <li>٣٠٠ كرت شهرياً</li>
                <li>تقارير جودة بيانات PDF</li>
                <li>٣ مستخدمين</li>
              </ul>
            </div>
            <div className="dp-price-card">
              <h3>Pro</h3>
              <p className="dp-price">399 ر.س / شهر</p>
              <ul>
                <li>٣٠ عملية تنظيف</li>
                <li>١٠٠٠ كرت شهرياً</li>
                <li>وصول إلى API و Webhooks</li>
              </ul>
            </div>
          </div>
          <div className="dp-pricing-cta">
            <Link to="/login" className="dp-btn dp-btn-primary">
              أنشئ حسابك وابدأ التجربة
            </Link>
            <span>إمكانك الإلغاء في أي وقت.</span>
          </div>
        </section>

        {/* Footer */}
        <footer className="dp-footer">
          <span>© {new Date().getFullYear()} DataPurity – منصة سعودية لتنظيف البيانات.</span>
          <span>صمِّم لتخدم الشركات الصغيرة والمتوسطة في المملكة.</span>
        </footer>
      </main>
    </div>
  );
};
