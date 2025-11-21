// Service Worker Registration for DataPurity PWA

export interface SWConfig {
  onSuccess?: (registration: ServiceWorkerRegistration) => void;
  onUpdate?: (registration: ServiceWorkerRegistration) => void;
  onOffline?: () => void;
  onOnline?: () => void;
}

export function registerServiceWorker(config?: SWConfig) {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      const swUrl = '/service-worker.js';

      navigator.serviceWorker
        .register(swUrl)
        .then((registration) => {
          console.log('[PWA] Service Worker registered:', registration);

          // Check for updates periodically
          registration.addEventListener('updatefound', () => {
            const installingWorker = registration.installing;
            if (installingWorker == null) {
              return;
            }

            installingWorker.addEventListener('statechange', () => {
              if (installingWorker.state === 'installed') {
                if (navigator.serviceWorker.controller) {
                  // New update available
                  console.log('[PWA] New content available, please refresh.');
                  if (config?.onUpdate) {
                    config.onUpdate(registration);
                  } else {
                    // Show default update notification
                    showUpdateNotification(registration);
                  }
                } else {
                  // Content cached for offline use
                  console.log('[PWA] Content cached for offline use.');
                  if (config?.onSuccess) {
                    config.onSuccess(registration);
                  }
                }
              }
            });
          });
        })
        .catch((error) => {
          console.error('[PWA] Service Worker registration failed:', error);
        });
    });

    // Online/Offline detection
    window.addEventListener('online', () => {
      console.log('[PWA] Back online');
      if (config?.onOnline) {
        config.onOnline();
      }
    });

    window.addEventListener('offline', () => {
      console.log('[PWA] Gone offline');
      if (config?.onOffline) {
        config.onOffline();
      }
    });
  }
}

function showUpdateNotification(registration: ServiceWorkerRegistration) {
  const updateBanner = document.createElement('div');
  updateBanner.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 16px 24px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 10000;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    display: flex;
    gap: 16px;
    align-items: center;
    animation: slideIn 0.3s ease;
    direction: rtl;
  `;

  updateBanner.innerHTML = `
    <div>
      <strong>تحديث جديد متوفر!</strong>
      <p style="margin: 4px 0 0 0; font-size: 14px; opacity: 0.9;">
        انقر لتحديث التطبيق
      </p>
    </div>
    <button id="update-btn" style="
      background: white;
      color: #667eea;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 600;
      white-space: nowrap;
    ">
      تحديث الآن
    </button>
    <button id="dismiss-btn" style="
      background: transparent;
      color: white;
      border: 1px solid rgba(255,255,255,0.3);
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      white-space: nowrap;
    ">
      لاحقاً
    </button>
  `;

  document.body.appendChild(updateBanner);

  document.getElementById('update-btn')?.addEventListener('click', () => {
    if (registration.waiting) {
      registration.waiting.postMessage({ type: 'SKIP_WAITING' });
      window.location.reload();
    }
  });

  document.getElementById('dismiss-btn')?.addEventListener('click', () => {
    updateBanner.remove();
  });

  // Add animation keyframes
  if (!document.getElementById('pwa-animations')) {
    const style = document.createElement('style');
    style.id = 'pwa-animations';
    style.textContent = `
      @keyframes slideIn {
        from {
          transform: translateX(100%);
          opacity: 0;
        }
        to {
          transform: translateX(0);
          opacity: 1;
        }
      }
    `;
    document.head.appendChild(style);
  }
}

export function unregisterServiceWorker() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.ready
      .then((registration) => {
        registration.unregister();
      })
      .catch((error) => {
        console.error('[PWA] Service Worker unregister failed:', error);
      });
  }
}

// Check if app is running as PWA
export function isPWA(): boolean {
  return window.matchMedia('(display-mode: standalone)').matches ||
         (window.navigator as { standalone?: boolean }).standalone === true ||
         document.referrer.includes('android-app://');
}

// Request notification permission
export async function requestNotificationPermission(): Promise<NotificationPermission> {
  if (!('Notification' in window)) {
    console.log('[PWA] This browser does not support notifications');
    return 'denied';
  }

  const permission = await Notification.requestPermission();
  console.log('[PWA] Notification permission:', permission);
  return permission;
}

// Show install prompt
export function showInstallPrompt() {
  interface BeforeInstallPromptEvent extends Event {
    prompt: () => Promise<void>
    userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>
  }
  
  let deferredPrompt: BeforeInstallPromptEvent | null = null;

  window.addEventListener('beforeinstallprompt', (e: Event) => {
    e.preventDefault();
    deferredPrompt = e as BeforeInstallPromptEvent;
    console.log('[PWA] Install prompt ready');

    // Show custom install button
    const installButton = document.getElementById('install-pwa-btn');
    if (installButton) {
      installButton.style.display = 'block';
      installButton.addEventListener('click', async () => {
        if (deferredPrompt) {
          deferredPrompt.prompt();
          const { outcome } = await deferredPrompt.userChoice;
          console.log('[PWA] User response to install prompt:', outcome);
          deferredPrompt = null;
          installButton.style.display = 'none';
        }
      });
    }
  });

  window.addEventListener('appinstalled', () => {
    console.log('[PWA] App installed successfully');
    deferredPrompt = null;
  });
}
