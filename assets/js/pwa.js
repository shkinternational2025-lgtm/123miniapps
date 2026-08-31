/* ============================================
 123MiniApps.online v2.0
 File: pwa.js
 Purpose: Service worker registration, update
 prompt, and the A2HS install flow.
 ============================================ */

const PWA = {
 deferredPrompt: null,

 init() {
 this.registerServiceWorker();
 this.watchInstallPrompt();
 this.watchConnectivity();
 },

 /**
 * Register the service worker after load so it never competes
 * with first paint for bandwidth.
 */
 registerServiceWorker() {
 if (!('serviceWorker' in navigator)) return;

 // file:// has no SW support; skip silently during local preview
 if (location.protocol === 'file:') return;

 // When a new service worker takes control, reload once so the page
 // is running the newest CSS/JS instead of whatever was cached before.
 // Without this, an updated stylesheet (e.g. new theme palettes) can be
 // shadowed by a stale cached copy until the user manually hard-refreshes.
 let hasReloaded = false;
 navigator.serviceWorker.addEventListener('controllerchange', () => {
 if (hasReloaded) return;
 hasReloaded = true;
 window.location.reload();
 });

 window.addEventListener('load', () => {
 navigator.serviceWorker
 .register('/service-worker.js', { scope: '/' })
 .then((registration) => {
 registration.addEventListener('updatefound', () => {
 const installing = registration.installing;
 if (!installing) return;

 installing.addEventListener('statechange', () => {
 if (installing.state === 'installed' && navigator.serviceWorker.controller) {
 // A new version is ready. Activate it immediately, the SW
 // handles SKIP_WAITING, which triggers controllerchange
 // above and reloads the page with fresh assets.
 installing.postMessage('SKIP_WAITING');
 }
 });
 });
 })
 .catch(() => {
 /* Registration failure is non-fatal, the site works without it. */
 });
 });
 },

 /** Let the user choose when to take a new version. */
 promptUpdate() {
 if (!window.toast) return;

 const node = window.toast({
 type: 'info',
 title: 'Update available',
 message: 'Reload to get the newest version.',
 duration: 12000
 });

 const reload = window.el('button', {
 className: 'btn btn--ghost btn--sm mt-2',
 attrs: { type: 'button' },
 text: 'Reload now',
 on: { click: () => window.location.reload() }
 });

 const body = node.querySelector('.toast__body');
 if (body) body.append(reload);
 },

 /**
 * Capture the browser's install prompt and re-surface it on our
 * own terms rather than letting it fire unprompted.
 */
 watchInstallPrompt() {
 window.addEventListener('beforeinstallprompt', (e) => {
 e.preventDefault();
 this.deferredPrompt = e;

 const btn = document.getElementById('install-app');
 if (btn) {
 btn.hidden = false;
 btn.addEventListener('click', () => this.promptInstall(), { once: true });
 }
 });

 window.addEventListener('appinstalled', () => {
 this.deferredPrompt = null;
 const btn = document.getElementById('install-app');
 if (btn) btn.hidden = true;
 if (window.toast) {
 window.toast({ type: 'success', title: 'Installed', message: 'Find it with your other apps.' });
 }
 });
 },

 async promptInstall() {
 if (!this.deferredPrompt) return;
 this.deferredPrompt.prompt();
 await this.deferredPrompt.userChoice;
 this.deferredPrompt = null;
 },

 /** Tell the user when they've dropped offline, and when they're back. */
 watchConnectivity() {
 window.addEventListener('offline', () => {
 if (window.toast) {
 window.toast({
 type: 'warning',
 title: 'You are offline',
 message: 'Cached tools still work normally.'
 });
 }
 });

 window.addEventListener('online', () => {
 if (window.toast) {
 window.toast({ type: 'success', title: 'Back online' });
 }
 });
 }
};

window.PWA = PWA;
