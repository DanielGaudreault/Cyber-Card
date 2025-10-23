// Service Worker for Capmatic Business Card PWA - Version 3.0.0
const CACHE_NAME = 'capmatic-pwa-v3.0.0';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/service-worker.js',
  '/images/capmatic.png',
  '/images/logo.png',
  '/offline',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@400;500;600;700&display=swap',
  'https://cdn.jsdelivr.net/npm/sweetalert2@11'
];

// Install event
self.addEventListener('install', (event) => {
  console.log('🛠️ Service Worker installing...');
  self.skipWaiting();
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('📦 Opened cache');
        return cache.addAll(urlsToCache);
      })
      .then(() => {
        console.log('✅ All resources cached');
      })
      .catch((error) => {
        console.error('❌ Cache installation failed:', error);
      })
  );
});

// Activate event
self.addEventListener('activate', (event) => {
  console.log('🎯 Service Worker activating...');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('🧹 Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('✅ Service Worker activated');
      return self.clients.claim();
    })
  );
});

// Fetch event
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version
        if (response) {
          return response;
        }

        // Otherwise, fetch from network
        return fetch(event.request)
          .then((response) => {
            // Check if we received a valid response
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clone the response
            const responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache);
              });

            return response;
          })
          .catch(() => {
            // If both fail, show offline page for HTML requests
            if (event.request.headers.get('accept').includes('text/html')) {
              return caches.match('/offline');
            }
          });
      })
  );
});

// Handle app installation
self.addEventListener('beforeinstallprompt', (e) => {
  console.log('📱 beforeinstallprompt event fired');
  e.preventDefault();
  self.deferredPrompt = e;
});

// Handle push notifications
self.addEventListener('push', function(event) {
  console.log('📲 Push message received');
  const options = {
    body: 'New update available from Capmatic',
    icon: '/images/capmatic.png',
    badge: '/images/capmatic.png',
    vibrate: [100, 50, 100],
    data: {
      url: '/'
    }
  };

  event.waitUntil(
    self.registration.showNotification('Capmatic', options)
  );
});

self.addEventListener('notificationclick', function(event) {
  console.log('📲 Notification click received');
  event.notification.close();
  event.waitUntil(
    clients.openWindow('/')
  );
});
