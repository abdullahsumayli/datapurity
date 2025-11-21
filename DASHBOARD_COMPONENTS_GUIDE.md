# 🎨 دليل المكونات - Dashboard UI Components

## 📋 جدول المحتويات

1. [Stats Cards](#stats-cards)
2. [Action Cards](#action-cards)
3. [Timeline Items](#timeline-items)
4. [Charts & Visualizations](#charts)
5. [Buttons & CTAs](#buttons)
6. [Tabs Navigation](#tabs)
7. [Badges & Pills](#badges)
8. [Empty States](#empty-states)

---

## Stats Cards

### 1. Basic Stat Card

```tsx
<div className="stat-card stat-primary">
  <div className="stat-header">
    <div className="stat-icon-wrapper">
      <div className="stat-icon">👥</div>
    </div>
    <div className="stat-meta">
      <p className="stat-label">إجمالي المستخدمين</p>
      <span className="stat-info-icon" title="معلومات إضافية">
        ℹ️
      </span>
    </div>
  </div>
  <div className="stat-body">
    <h3 className="stat-value">15,234</h3>
    <div className="stat-comparison">
      <span className="comparison-badge positive">
        <span className="badge-icon">↗</span>
        <span className="badge-value">+12.5%</span>
      </span>
      <span className="comparison-text">مقارنة بالشهر الماضي</span>
    </div>
  </div>
  <div className="stat-footer">
    <span className="stat-detail">📅 آخر تحديث: منذ ساعتين</span>
  </div>
</div>
```

**الألوان المتاحة:**

- `stat-primary` - أزرق
- `stat-success` - أخضر
- `stat-warning` - أصفر
- `stat-info` - بنفسجي

---

### 2. Stat Card with Progress

```tsx
<div className="stat-card stat-success">
  <div className="stat-header">
    <div className="stat-icon-wrapper">
      <div className="stat-icon">✨</div>
    </div>
    <div className="stat-meta">
      <p className="stat-label">نسبة الإنجاز</p>
    </div>
  </div>
  <div className="stat-body">
    <h3 className="stat-value">75.3%</h3>
    <div className="stat-progress-enhanced">
      <div className="progress-info">
        <span className="progress-label">نسبة الإنجاز</span>
        <span className="progress-percentage">75.3%</span>
      </div>
      <div className="progress-bar-modern">
        <div className="progress-fill-animated" style={{ width: "75.3%" }}>
          <span className="progress-glow"></span>
        </div>
      </div>
      <div className="progress-milestones">
        <span className="milestone" style={{ left: "50%" }}>
          50%
        </span>
        <span className="milestone" style={{ left: "100%" }}>
          100%
        </span>
      </div>
    </div>
  </div>
  <div className="stat-footer">
    <span className="stat-detail">⚡ متوسط الوقت: 2.3 ثانية</span>
  </div>
</div>
```

---

### 3. Stat Card with Live Status

```tsx
<div className="stat-card stat-warning">
  <div className="stat-header">
    <div className="stat-icon-wrapper">
      <div className="stat-icon stat-icon-pulse">⏳</div>
    </div>
    <div className="stat-meta">
      <p className="stat-label">عمليات نشطة</p>
      <span className="stat-badge live">مباشر</span>
    </div>
  </div>
  <div className="stat-body">
    <h3 className="stat-value">23</h3>
    <div className="stat-queue">
      <div className="queue-bar">
        <div className="queue-item"></div>
        <div className="queue-item"></div>
        <div className="queue-item active"></div>
      </div>
      <span className="queue-text">معالجة نشطة</span>
    </div>
  </div>
  <div className="stat-footer">
    <span className="stat-detail">⏱️ الوقت المتبقي: ~15 دقيقة</span>
  </div>
</div>
```

---

### 4. Stat Card with Circular Chart

```tsx
<div className="stat-card stat-info">
  <div className="stat-header">
    <div className="stat-icon-wrapper">
      <div className="stat-icon">📊</div>
    </div>
    <div className="stat-meta">
      <p className="stat-label">معدل النجاح</p>
      <span className="stat-quality excellent">ممتاز</span>
    </div>
  </div>
  <div className="stat-body stat-body-chart">
    <div className="chart-container">
      <svg
        className="circular-chart"
        width="100"
        height="100"
        viewBox="0 0 100 100"
      >
        <circle
          cx="50"
          cy="50"
          r="40"
          fill="none"
          stroke="#e5e7eb"
          strokeWidth="8"
        />
        <circle
          className="progress-ring"
          cx="50"
          cy="50"
          r="40"
          fill="none"
          stroke="url(#gradient)"
          strokeWidth="8"
          strokeDasharray="226.2 251.2"
          strokeLinecap="round"
          transform="rotate(-90 50 50)"
        />
        <defs>
          <linearGradient id="gradient">
            <stop offset="0%" stopColor="#667eea" />
            <stop offset="100%" stopColor="#764ba2" />
          </linearGradient>
        </defs>
      </svg>
      <div className="chart-center">
        <h3 className="chart-value">90%</h3>
      </div>
    </div>
  </div>
  <div className="stat-footer">
    <span className="stat-detail">🎯 الهدف: 95%</span>
  </div>
</div>
```

---

## Action Cards

### Modern Action Card

```tsx
<Link to="/path" className="action-card">
  <div className="action-card-icon">📤</div>
  <h4 className="action-card-title">رفع بيانات</h4>
  <p className="action-card-desc">رفع ملف Excel أو CSV</p>
  <div className="action-card-overlay">
    <span className="overlay-text">ابدأ الآن ←</span>
  </div>
</Link>
```

**الحالات:**

- Default: خلفية رمادية فاتحة
- Hover: تحريك للأعلى + ظل + overlay بـ gradient
- Focus: outline بنفسجي

---

## Timeline Items

### Success Timeline Item

```tsx
<div className="timeline-item">
  <div className="timeline-marker">
    <div className="marker-dot status-success"></div>
    <div className="marker-line"></div>
  </div>
  <div className="timeline-content">
    <div className="timeline-header">
      <span className="timeline-icon">📤</span>
      <span className="timeline-time">منذ ساعتين</span>
    </div>
    <p className="timeline-description">تم رفع ملف جهات اتصال جديد</p>
    <span className="timeline-badge status-success">
      <span className="badge-dot"></span>
      مكتمل
    </span>
  </div>
</div>
```

### Pending Timeline Item

```tsx
<div className="timeline-item">
  <div className="timeline-marker">
    <div className="marker-dot status-pending"></div>
    <div className="marker-line"></div>
  </div>
  <div className="timeline-content">
    <div className="timeline-header">
      <span className="timeline-icon">✨</span>
      <span className="timeline-time">الآن</span>
    </div>
    <p className="timeline-description">جاري تنظيف 500 جهة اتصال</p>
    <span className="timeline-badge status-pending">
      <span className="badge-dot"></span>
      قيد التنفيذ
    </span>
  </div>
</div>
```

### Error Timeline Item

```tsx
<div className="timeline-item">
  <div className="timeline-marker">
    <div className="marker-dot status-error"></div>
    <div className="marker-line"></div>
  </div>
  <div className="timeline-content">
    <div className="timeline-header">
      <span className="timeline-icon">❌</span>
      <span className="timeline-time">منذ 10 دقائق</span>
    </div>
    <p className="timeline-description">فشل في معالجة الملف</p>
    <span className="timeline-badge status-error">
      <span className="badge-dot"></span>
      فشل
    </span>
  </div>
</div>
```

---

## Charts & Visualizations

### Bar Chart

```tsx
<div className="bar-chart">
  {[
    "السبت",
    "الأحد",
    "الاثنين",
    "الثلاثاء",
    "الأربعاء",
    "الخميس",
    "الجمعة",
  ].map((day, i) => (
    <div key={day} className="bar-item">
      <div className="bar" style={{ height: `${values[i]}%` }}>
        <span className="bar-value">{values[i]}</span>
      </div>
      <span className="bar-label">{day}</span>
    </div>
  ))}
</div>
```

---

## Buttons & CTAs

### Primary Button

```tsx
<button className="action-btn action-btn-primary">
  <span className="btn-icon">➕</span>
  إضافة بيانات
</button>
```

### Secondary Button

```tsx
<button className="action-btn action-btn-secondary">
  <span className="btn-icon">🔄</span>
  تحديث
</button>
```

---

## Tabs Navigation

```tsx
<div className="dashboard-tabs">
  <button className={`tab-btn ${activeTab === "overview" ? "active" : ""}`}>
    <span className="tab-icon">📊</span>
    نظرة عامة
  </button>
  <button className={`tab-btn ${activeTab === "analytics" ? "active" : ""}`}>
    <span className="tab-icon">📈</span>
    التحليلات
  </button>
  <button className={`tab-btn ${activeTab === "activity" ? "active" : ""}`}>
    <span className="tab-icon">⚡</span>
    النشاط
  </button>
</div>
```

---

## Badges & Pills

### Comparison Badge

```tsx
<span className="comparison-badge positive">
  <span className="badge-icon">↗</span>
  <span className="badge-value">+12.5%</span>
</span>
```

### Status Badge

```tsx
<span className="stat-badge live">مباشر</span>
```

### Quality Badge

```tsx
<span className="stat-quality excellent">ممتاز</span>
```

---

## Empty States

### Modern Empty State

```tsx
<div className="empty-state-modern">
  <div className="empty-illustration">📭</div>
  <h4>لا توجد أنشطة بعد</h4>
  <p>ابدأ برفع البيانات لرؤية النشاط هنا</p>
</div>
```

---

## 🎨 Color Classes

### Text Colors

- `.text-primary` - #111827
- `.text-secondary` - #6b7280
- `.text-tertiary` - #9ca3af

### Background Colors

- `.bg-primary` - #ffffff
- `.bg-secondary` - #f9fafb
- `.bg-tertiary` - #f3f4f6

### Status Colors

- `.status-success` - #10b981 (أخضر)
- `.status-warning` - #f59e0b (أصفر)
- `.status-error` - #ef4444 (أحمر)
- `.status-info` - #667eea (بنفسجي)

---

## ⚡ Animation Classes

### Fade In

```css
.fade-in {
  animation: fadeIn 0.5s ease-in;
}
```

### Pulse

```css
.pulse {
  animation: pulse 2s ease-in-out infinite;
}
```

### Float

```css
.float {
  animation: float 3s ease-in-out infinite;
}
```

---

## 📱 Responsive Breakpoints

```css
/* Small Mobile */
@media (max-width: 480px) {
}

/* Mobile */
@media (max-width: 768px) {
}

/* Tablet */
@media (max-width: 1024px) {
}

/* Desktop */
@media (min-width: 1025px) {
}
```

---

## 🌙 Dark Mode

تلقائياً يكتشف تفضيلات النظام:

```css
@media (prefers-color-scheme: dark) {
  /* Dark theme styles */
}
```

---

## ♿ Accessibility

### Focus States

جميع العناصر التفاعلية لديها focus visible واضح

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  /* Disable animations */
}
```

### High Contrast

```css
@media (prefers-contrast: high) {
  /* Enhanced borders */
}
```

---

## 🚀 Best Practices

1. ✅ استخدم CSS Variables للألوان
2. ✅ احترم Spacing Scale (8px grid)
3. ✅ استخدم Semantic HTML
4. ✅ أضف ARIA labels
5. ✅ اختبر على Mobile
6. ✅ تحقق من Contrast Ratio
7. ✅ استخدم Progressive Enhancement

---

## 📚 المزيد من الأمثلة

للمزيد من الأمثلة والتفاصيل، راجع:

- `DASHBOARD_UX_IMPROVEMENTS.md` - التحسينات الكاملة
- `dashboard.css` - جميع الأنماط
- `DashboardPage.tsx` - التطبيق العملي
