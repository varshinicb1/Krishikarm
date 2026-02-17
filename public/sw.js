// Krishikarm Service Worker — Offline Cache Strategy
const CACHE_NAME = 'krishikarm-v7';
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/style.css',
    '/main.js',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
    'https://cdn.jsdelivr.net/npm/chart.js',
    'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.17.0',
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Noto+Sans+Devanagari:wght@400;600;700&family=Outfit:wght@400;500;600;700;800&display=swap',
];

// Install — cache static assets
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(STATIC_ASSETS).catch(err => {
                console.warn('SW: Some assets failed to cache', err);
            });
        })
    );
    self.skipWaiting();
});

// Activate — clean old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        )
    );
    self.clients.claim();
});

// Fetch — Network first, fallback to cache
self.addEventListener('fetch', event => {
    const url = new URL(event.request.url);

    // For API calls — try network, cache response for offline
    if (url.hostname.includes('api.open-meteo.com') ||
        url.hostname.includes('power.larc.nasa.gov') ||
        url.hostname.includes('archive-api.open-meteo.com')) {
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    const clone = response.clone();
                    caches.open(CACHE_NAME + '-api').then(cache => cache.put(event.request, clone));
                    return response;
                })
                .catch(() => caches.match(event.request))
        );
        return;
    }

    // For satellite tiles — cache aggressively
    if (url.hostname.includes('gibs.earthdata.nasa.gov') ||
        url.hostname.includes('basemaps.cartocdn.com')) {
        event.respondWith(
            caches.match(event.request).then(cached => {
                if (cached) return cached;
                return fetch(event.request).then(response => {
                    const clone = response.clone();
                    caches.open(CACHE_NAME + '-tiles').then(cache => cache.put(event.request, clone));
                    return response;
                }).catch(() => new Response('', { status: 408 }));
            })
        );
        return;
    }

    // Static assets — cache first, network fallback
    event.respondWith(
        caches.match(event.request).then(cached => cached || fetch(event.request))
    );
});
