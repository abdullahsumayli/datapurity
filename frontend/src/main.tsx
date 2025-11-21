import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { registerServiceWorker, showInstallPrompt } from './pwa/registerSW'
import './styles/globals.css'

// Register Service Worker for PWA functionality
registerServiceWorker({
  onSuccess: () => {
    console.log('✅ PWA: Content cached for offline use')
  },
  onUpdate: () => {
    console.log('🔄 PWA: New content available, please refresh')
  },
  onOffline: () => {
    console.log('📴 PWA: You are offline')
    // Show offline notification
    const offlineBanner = document.createElement('div')
    offlineBanner.id = 'offline-banner'
    offlineBanner.style.cssText = `
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: #ef4444;
      color: white;
      padding: 12px 24px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      z-index: 10000;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    `
    offlineBanner.textContent = '⚠️ أنت غير متصل بالإنترنت'
    document.body.appendChild(offlineBanner)
  },
  onOnline: () => {
    console.log('✅ PWA: You are back online')
    const banner = document.getElementById('offline-banner')
    if (banner) {
      banner.style.background = '#10b981'
      banner.textContent = '✓ تم الاتصال بالإنترنت'
      setTimeout(() => banner.remove(), 3000)
    }
  }
})

// Show install prompt when available
showInstallPrompt()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
