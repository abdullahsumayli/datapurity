import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './OnboardingBanner.css'

function OnboardingBanner() {
  const [isVisible, setIsVisible] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    // Check if user has seen the banner before
    const hasSeenBanner = localStorage.getItem('hasSeenOnboardingBanner')
    if (!hasSeenBanner) {
      setIsVisible(true)
    }
  }, [])

  const handleDismiss = () => {
    localStorage.setItem('hasSeenOnboardingBanner', 'true')
    setIsVisible(false)
  }

  const handleGetStarted = () => {
    localStorage.setItem('hasSeenOnboardingBanner', 'true')
    navigate('/app/upload')
  }

  if (!isVisible) return null

  return (
    <div className="onboarding-banner">
      <button className="banner-close" onClick={handleDismiss} aria-label="إغلاق">
        ×
      </button>
      
      <div className="banner-content">
        <h2 className="banner-title">ابدأ استخدام DataPurity خلال 3 خطوات</h2>
        
        <div className="banner-steps">
          <div className="banner-step">
            <span className="step-number">1</span>
            <p>ارفع ملف بياناتك (Excel أو CSV)</p>
          </div>
          
          <div className="banner-step">
            <span className="step-number">2</span>
            <p>انتظر المعالجة والتنظيف</p>
          </div>
          
          <div className="banner-step">
            <span className="step-number">3</span>
            <p>قم بتنزيل النسخة المنظّفة أو إضافتها لجهات الاتصال</p>
          </div>
        </div>

        <button className="banner-cta" onClick={handleGetStarted}>
          ابدأ برفع ملف البيانات
        </button>
      </div>
    </div>
  )
}

export default OnboardingBanner
