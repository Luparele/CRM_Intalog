const CACHE_NAME = 'crm-intalog-v1';
const urlsToCache = [
  '/',
  '/static/app/css/print.css',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
];

// Instalação do Service Worker
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Instalando...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Cache aberto');
        return cache.addAll(urlsToCache);
      })
  );
  self.skipWaiting();
});

// Ativação do Service Worker
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Ativando...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Removendo cache antigo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Estratégia de cache: Network First
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  
  if (event.request.url.includes('/admin/') || 
      event.request.url.includes('brasilapi.com.br') ||
      event.request.url.includes('cdnjs.cloudflare.com') ||
      event.request.url.includes('cdn.jsdelivr.net')) {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        if (response && response.status === 200) {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return response;
      })
      .catch(() => {
        return caches.match(event.request).then((response) => {
          if (response) return response;
          if (event.request.headers.get('accept').includes('text/html')) {
            return caches.match('/');
          }
        });
      })
  );
});

self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-data') {
    console.log('[Service Worker] Sincronizando dados...');
  }
});

self.addEventListener('push', (event) => {
  const options = {
    body: event.data ? event.data.text() : 'Nova atualização disponível!',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png',
    vibrate: [200, 100, 200],
    tag: 'crm-intalog-notification',
    requireInteraction: true,
  };
  event.waitUntil(
    self.registration.showNotification('CRM - INTALOG', options)
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(clients.openWindow('/'));
});
