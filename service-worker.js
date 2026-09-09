/* ============================================
   123MiniApps.online v2.0
   File: service-worker.js
   Purpose: Fast repeat loads, always-online tool pages.

   Strategy (intentionally NOT a full offline app):
     - HTML pages: network-only. Every tool opens fresh from
       the server each time, so the page is always current and
       always loads its ads. We do NOT cache pages, so a tool
       cannot be used with no connection. When the user is
       offline we show a friendly "reconnect" page instead.
     - App shell (CSS, JS, data, images): stale-while-revalidate,
       so the page paints fast while the file refreshes in the
       background. These assets carry no ads and rarely change.
     - Cross-origin (fonts): stale-while-revalidate.

   The result: the installed icon behaves like a fast shortcut
   that always connects online, rather than an offline copy.
   ============================================ */

const VERSION = '2.8.6';
const SHELL_CACHE = `123miniapps-shell-v${VERSION}`;
const FONT_CACHE = `123miniapps-fonts-v${VERSION}`;

/** Static assets worth precaching for speed. Deliberately NO HTML
    pages here, so no tool page is ever available offline. */
const SHELL_ASSETS = [
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
   INSTALL — precache the static assets
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
  const keep = new Set([SHELL_CACHE, FONT_CACHE]);

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

  // HTML navigations — network-only (with an offline notice on failure).
  // Pages are never cached, so tools always load fresh and online.
  if (request.mode === 'navigate' || request.headers.get('accept')?.includes('text/html')) {
    event.respondWith(networkOnly(request));
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
 * Always fetch HTML from the network so tools open fresh and load
 * their ads. Nothing is cached. When the user is offline, show the
 * precached "reconnect" page rather than a stale copy of the tool.
 * @param {Request} request
 * @returns {Promise<Response>}
 */
async function networkOnly(request) {
  try {
    return await fetch(request);
  } catch {
    const offline = await caches.match('/offline.html');
    if (offline) return offline;

    return new Response(
      '<!DOCTYPE html><meta charset="utf-8"><title>Offline</title>' +
      '<body style="font-family:system-ui;background:#0B1120;color:#fff;display:grid;place-items:center;height:100vh;margin:0;text-align:center">' +
      '<div><h1>You are offline</h1><p>123MiniApps tools run online. Reconnect to the internet and try again.</p></div>',
      { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' } }
    );
  }
}

/**
 * Return the cached copy immediately while refreshing it in the
 * background — right for static assets and fonts, which change
 * rarely but shouldn't pin forever.
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
