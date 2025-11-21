import { useEffect, useState } from 'react';
import './PWAInstallButton.css';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

const PWAInstallButton = () => {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [showButton, setShowButton] = useState(false);
  const [isInstalled, setIsInstalled] = useState(false);

  useEffect(() => {
    // Check if already installed
    const isPWA = window.matchMedia('(display-mode: standalone)').matches ||
                  (window.navigator as { standalone?: boolean }).standalone === true;
    
    if (isPWA) {
      setIsInstalled(true);
      return;
    }

    // Listen for install prompt
    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
      setShowButton(true);
      console.log('[PWA] Install prompt ready');
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    // Listen for successful install
    const handleAppInstalled = () => {
      console.log('[PWA] App installed successfully');
      setShowButton(false);
      setIsInstalled(true);
      setDeferredPrompt(null);
    };

    window.addEventListener('appinstalled', handleAppInstalled);

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  const handleInstallClick = async () => {
    if (!deferredPrompt) {
      return;
    }

    // Show install prompt
    await deferredPrompt.prompt();

    // Wait for user response
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`[PWA] User response: ${outcome}`);

    // Clear the prompt
    setDeferredPrompt(null);
    setShowButton(false);
  };

  const handleDismiss = () => {
    setShowButton(false);
    // Save dismissal in localStorage
    localStorage.setItem('pwa-install-dismissed', 'true');
  };

  // Don't show if dismissed or installed
  if (!showButton || isInstalled) {
    return null;
  }

  // Check if previously dismissed (optional: respect for 7 days)
  const dismissed = localStorage.getItem('pwa-install-dismissed');
  if (dismissed) {
    return null;
  }

  return (
    <div className="pwa-install-banner">
      <div className="pwa-install-content">
        <div className="pwa-install-icon">📱</div>
        <div className="pwa-install-text">
          <h3>ثبّت التطبيق</h3>
          <p>استخدم DataPurity كتطبيق على جهازك</p>
        </div>
        <div className="pwa-install-actions">
          <button className="pwa-install-btn" onClick={handleInstallClick}>
            ✓ تثبيت
          </button>
          <button className="pwa-dismiss-btn" onClick={handleDismiss}>
            ✕
          </button>
        </div>
      </div>
    </div>
  );
};

export default PWAInstallButton;
