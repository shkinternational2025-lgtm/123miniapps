/* ============================================
   123MiniApps.online v2.0
   File: service-worker.js
   Purpose: Offline support and instant repeat loads.

   Strategy:
     - App shell (CSS, JS, data): stale-while-revalidate, so
       a cached copy loads instantly but is refreshed in the
       background — an updated stylesheet or script propagates
       on the next load instead of being pinned by the cache.
       Caches are versioned so a deploy also invalidates them.
     - HTML pages: network-first with a cache fallback, so
       users always get fresh content when online but keep
       working when they aren't.
     - Cross-origin (fonts): stale-while-revalidate.
   ============================================ */

const VERSION = '2.8.2';
const SHELL_CACHE = `123miniapps-shell-v${VERSION}`;
const PAGE_CACHE = `123miniapps-pages-v${VERSION}`;
const FONT_CACHE = `123miniapps-fonts-v${VERSION}`;

/** Everything needed to render the site with no network. */
const SHELL_ASSETS = [
  '/',
  '/index.html',
  '/offline.html',
  '/manifest.json',
  '/assets/css/animations.css',
  '/assets/css/components.css',
  '/assets/css/design-tokens.css',
  '/assets/css/layout.css',
  '/assets/css/main.min.css',
  '/assets/css/main.css',
  '/assets/css/reset.css',
  '/assets/css/shadows.css',
  '/assets/css/spacing.css',
  '/assets/css/themes.css',
  '/assets/css/typography.css',
  '/assets/js/analytics.js',
  '/assets/js/animations.js',
  '/assets/js/components.js',
  '/assets/js/config.js',
  '/assets/js/main.js',
  '/assets/js/pwa.js',
  '/assets/js/search-engine.js',
  '/assets/js/theme-manager.js',
  '/assets/js/tool-utils.js',
  '/assets/js/vendor/barcode-encoder.js',
  '/assets/js/vendor/qr-encoder.js',
  '/assets/data/categories.js',
  '/assets/data/testimonials.js',
  '/assets/data/tools.js',
  '/assets/images/logo.svg',
  '/favicon.ico'
];

/* ============================================
   INSTALL — precache the shell
   ============================================ */
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE)
      .then((cache) =>
        // addAll rejects wholesale if any single request 404s, which
        // would leave the SW uninstalled. Add individually instead so
        // one missing optional asset can't break the whole install.
        Promise.all(
          SHELL_ASSETS.map((url) =>
            cache.add(new Request(url, { cache: 'reload' })).catch(() => null)
          )
        )
      )
      .then(() => self.skipWaiting())
  );
});

/* ============================================
   ACTIVATE — drop caches from older versions
   ============================================ */
self.addEventListener('activate', (event) => {
  const keep = new Set([SHELL_CACHE, PAGE_CACHE, FONT_CACHE]);

  event.waitUntil(
    caches.keys()
      .then((names) => Promise.all(
        names.filter((name) => !keep.has(name)).map((name) => caches.delete(name))
      ))
      .then(() => self.clients.claim())
  );
});

/* ============================================
   FETCH
   ============================================ */
self.addEventListener('fetch', (event) => {
  const { request } = event;

  // Never interfere with anything but GET
  if (request.method !== 'GET') return;

  const url = new URL(request.url);

  // Google Fonts — stale-while-revalidate
  if (url.origin.includes('fonts.googleapis.com') || url.origin.includes('fonts.gstatic.com')) {
    event.respondWith(staleWhileRevalidate(request, FONT_CACHE));
    return;
  }

  // Anything else off-origin: leave it alone
  if (url.origin !== self.location.origin) return;

  // HTML navigations — network-first
  if (request.mode === 'navigate' || request.headers.get('accept')?.includes('text/html')) {
    event.respondWith(networkFirst(request));
    return;
  }

  // Same-origin assets (CSS, JS, data) — stale-while-revalidate so an
  // updated file is picked up on the next load rather than pinned forever.
  event.respondWith(staleWhileRevalidate(request, SHELL_CACHE));
});

/* ============================================
   Strategies
   ============================================ */

/**
 * Serve from cache, falling back to network and caching the result.
 * @param {Request} request
 * @param {string} cacheName
 * @returns {Promise<Response>}
 */
async function cacheFirst(request, cacheName) {
  const cached = await caches.match(request);
  if (cached) return cached;

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    return new Response('', { status: 504, statusText: 'Offline' });
  }
}

/**
 * Try the network first so online users always see fresh HTML;
 * fall back to cache, then to the offline shell.
 * @param {Request} request
 * @returns {Promise<Response>}
 */
async function networkFirst(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(PAGE_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(request);
    if (cached) return cached;

    // A dedicated, friendly offline page (precached in SHELL_ASSETS)
    const offline = await caches.match('/offline.html');
    if (offline) return offline;

    // Then the homepage, which is always precached
    const home = await caches.match('/index.html');
    if (home) return home;

    return new Response(
      '<!DOCTYPE html><meta charset="utf-8"><title>Offline</title>' +
      '<body style="font-family:system-ui;background:#0B1120;color:#fff;display:grid;place-items:center;height:100vh;margin:0;text-align:center">' +
      '<div><h1>You are offline</h1><p>This page has not been cached yet. Reconnect and try again.</p></div>',
      { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' } }
    );
  }
}

/**
 * Return the cached copy immediately while refreshing it in the
 * background — right for fonts, which change rarely but shouldn't
 * pin forever.
 * @param {Request} request
 * @param {string} cacheName
 * @returns {Promise<Response>}
 */
async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);

  const network = fetch(request)
    .then((response) => {
      if (response.ok) cache.put(request, response.clone());
      return response;
    })
    .catch(() => cached);

  return cached || network;
}

/* Allow the page to trigger an immediate activation after an update. */
self.addEventListener('message', (event) => {
  if (event.data === 'SKIP_WAITING') self.skipWaiting();
});
