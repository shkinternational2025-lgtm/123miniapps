/* ============================================
 123MiniApps.online v2.0
 File: analytics.js
 Purpose: Local-only performance and usage
 instrumentation.

 IMPORTANT: Nothing here transmits anything. Every
 metric is held in memory for the session and, at
 most, written to this browser's localStorage. The
 privacy claim on the homepage is only credible if
 this file stays that way, if you ever add a
 network sink, update the privacy policy first.
 ============================================ */

const Analytics = {
 metrics: {},
 enabled: true,

 init() {
 // Honour Do Not Track / Global Privacy Control even though
 // we collect nothing, cheap consistency.
 if (navigator.doNotTrack === '1' || navigator.globalPrivacyControl) {
 this.enabled = false;
 return;
 }

 this.observeWebVitals();
 this.logStartup();
 },

 /**
 * Record Core Web Vitals using PerformanceObserver.
 * Values land in Analytics.metrics for inspection via
 * `Analytics.report()` in the console.
 */
 observeWebVitals() {
 if (!('PerformanceObserver' in window)) return;

 const safeObserve = (type, callback, options = {}) => {
 try {
 const observer = new PerformanceObserver(callback);
 observer.observe({ type, buffered: true, ...options });
 return observer;
 } catch {
 return null; // entry type unsupported in this browser
 }
 };

 // Largest Contentful Paint
 safeObserve('largest-contentful-paint', (list) => {
 const entries = list.getEntries();
 const last = entries[entries.length - 1];
 if (last) this.metrics.lcp = Math.round(last.startTime);
 });

 // First Contentful Paint
 safeObserve('paint', (list) => {
 list.getEntries().forEach((entry) => {
 if (entry.name === 'first-contentful-paint') {
 this.metrics.fcp = Math.round(entry.startTime);
 }
 });
 });

 // Cumulative Layout Shift, ignore shifts caused by user input
 let cls = 0;
 safeObserve('layout-shift', (list) => {
 list.getEntries().forEach((entry) => {
 if (!entry.hadRecentInput) cls += entry.value;
 });
 this.metrics.cls = Number(cls.toFixed(4));
 });

 // Long tasks feed an approximate Total Blocking Time
 let tbt = 0;
 safeObserve('longtask', (list) => {
 list.getEntries().forEach((entry) => {
 tbt += Math.max(0, entry.duration - 50);
 });
 this.metrics.tbt = Math.round(tbt);
 });

 // Interaction to Next Paint
 safeObserve('event', (list) => {
 list.getEntries().forEach((entry) => {
 const d = entry.duration || 0;
 if (d > (this.metrics.inp || 0)) this.metrics.inp = Math.round(d);
 });
 }, { durationThreshold: 40 });
 },

 logStartup() {
 // getEntriesByType is missing in some embedded/test environments,
 // so feature-detect the method rather than the `performance` object.
 if (typeof performance === 'undefined' || typeof performance.getEntriesByType !== 'function') return;

 window.addEventListener('load', () => {
 requestIdleCallbackShim(() => {
 try {
 const nav = performance.getEntriesByType('navigation')[0];
 if (nav) {
 this.metrics.domInteractive = Math.round(nav.domInteractive);
 this.metrics.loadComplete = Math.round(nav.loadEventEnd);
 }
 this.metrics.resources = performance.getEntriesByType('resource').length;
 } catch {
 /* metrics are diagnostic only, never let them break the page */
 }
 });
 });
 },

 /**
 * Increment a local counter for a tool. Used to show the user
 * their own usage, never aggregated or sent anywhere.
 * @param {string} toolSlug
 */
 trackToolUse(toolSlug) {
 if (!this.enabled) return;

 try {
 const key = '123miniapps-local-usage';
 const raw = localStorage.getItem(key);
 const data = raw ? JSON.parse(raw) : {};
 data[toolSlug] = (data[toolSlug] || 0) + 1;
 localStorage.setItem(key, JSON.stringify(data));
 } catch {
 /* storage unavailable */
 }
 },

 /**
 * Print collected metrics. Handy during a Lighthouse pass.
 * @returns {Object}
 */
 report() {
 // eslint-disable-next-line no-console
 console.table(this.metrics);
 return this.metrics;
 }
};

/** requestIdleCallback with a setTimeout fallback for Safari. */
function requestIdleCallbackShim(fn, timeout = 2000) {
 if ('requestIdleCallback' in window) {
 return window.requestIdleCallback(fn, { timeout });
 }
 return setTimeout(fn, 200);
}

window.Analytics = Analytics;
window.requestIdleCallbackShim = requestIdleCallbackShim;

/* ============================================
   OPTIONAL external analytics — OFF by default.

   Both supported options are COOKIELESS and collect no personal data, so they
   need no consent banner and keep the site's privacy promise intact. To enable,
   put ONE value below (leave the other ''), then re-deploy:

     plausibleDomain  — your domain, e.g. '123miniapps.online' (Plausible.io)
     cloudflareToken  — the token from Cloudflare Web Analytics

   Note: the nginx CSP already allows plausible.io and cloudflareinsights.com.
   ============================================ */
window.ANALYTICS_CONFIG = window.ANALYTICS_CONFIG || {
  plausibleDomain: '',
  cloudflareToken: ''
};

(function () {
  if (navigator.doNotTrack === '1' || navigator.globalPrivacyControl) return;
  var c = window.ANALYTICS_CONFIG || {};

  var pd = (c.plausibleDomain || '').trim();
  if (pd) {
    var s = document.createElement('script');
    s.defer = true;
    s.setAttribute('data-domain', pd);
    s.src = 'https://plausible.io/js/script.js';
    document.head.appendChild(s);
  }

  var cf = (c.cloudflareToken || '').trim();
  if (cf) {
    var b = document.createElement('script');
    b.defer = true;
    b.src = 'https://static.cloudflareinsights.com/beacon.min.js';
    b.setAttribute('data-cf-beacon', JSON.stringify({ token: cf }));
    document.head.appendChild(b);
  }
})();
