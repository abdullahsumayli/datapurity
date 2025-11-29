import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { disableWeb3 } from './utils/web3Guard'
// import { registerServiceWorker, showInstallPrompt } from './pwa/registerSW'
// تعليق تسجيل service worker مؤقتاً لمنع أخطاء الكونسول
// registerServiceWorker({
//   onSuccess: () => console.log('Service worker registered'),
//   onUpdate: () => console.log('Service worker update available'),
// })
// Show install prompt when available
// showInstallPrompt()
import './styles/globals.css'

// Disable any injected Web3 providers (e.g., MetaMask)
disableWeb3()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
