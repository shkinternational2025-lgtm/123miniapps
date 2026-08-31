/* ============================================
   123MiniApps.online — Cookie consent / notice controller
   File: assets/js/consent.js

   MODE is set in ads.js via window.ADSTERRA.consentMode:
     'notice' (default) — ads load immediately; a small dismissible bar just
                          INFORMS the visitor that cookies are used. Best for
                          Adsterra, which does not require opt-in consent.
     'gate'             — ads do NOT load until the visitor clicks Accept.
                          Reject means no ad scripts load. Use for strict
                          GDPR/AdSense-style opt-in.
     'off'              — no banner at all; ads load immediately.

   The banner only ever appears when advertising is actually configured
   (window.ADSTERRA has a script URL). With ads off, the site sets no cookies,
   so nothing shows and the site stays cookieless.
   ============================================ */

window.CONSENT = (function () {
  var KEY = '123miniapps-consent';

  function mode() {
    return (window.ADSTERRA && window.ADSTERRA.consentMode) || 'notice';
  }
  function read() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function write(v) {
    try { localStorage.setItem(KEY, v); } catch (e) {}
    document.dispatchEvent(new CustomEvent('consentchange', { detail: { value: v } }));
  }
  function required() {
    var a = window.ADSTERRA || {};
    return !!((a.siteScriptUrl || '').trim() || (a.bannerScriptUrl || '').trim());
  }

  function cookiePolicyHref() {
    var p = location.pathname;
    if (p.indexOf('/pages/') > -1) return 'cookies.html';
    if (p.indexOf('/tools/') > -1 || p.indexOf('/blog/') > -1) return '../pages/cookies.html';
    return 'pages/cookies.html';
  }

  function render(gate) {
    if (document.querySelector('.consent-banner')) return;
    var bar = document.createElement('div');
    bar.className = 'consent-banner';
    bar.setAttribute('role', gate ? 'dialog' : 'region');
    bar.setAttribute('aria-label', 'Cookie notice');
    bar.setAttribute('aria-live', 'polite');

    var link = '<a href="' + cookiePolicyHref() + '">Cookie Policy</a>';
    if (gate) {
      bar.innerHTML =
        '<div class="consent-banner__text">This site uses cookies from our advertising partner to keep the '
        + 'tools free. Your tool data always stays on your device. Read our ' + link + '.</div>'
        + '<div class="consent-banner__actions">'
        + '<button class="btn btn--secondary btn--sm" type="button" data-consent="rejected">Reject</button>'
        + '<button class="btn btn--primary btn--sm" type="button" data-consent="accepted">Accept</button>'
        + '</div>';
    } else {
      bar.innerHTML =
        '<div class="consent-banner__text">We use cookies, including from our advertising partner, to keep '
        + 'these tools free. Your tool data always stays on your device. See our ' + link + '.</div>'
        + '<div class="consent-banner__actions">'
        + '<button class="btn btn--primary btn--sm" type="button" data-consent="accepted">Got it</button>'
        + '</div>';
    }

    bar.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-consent]');
      if (!btn) return;
      write(btn.getAttribute('data-consent'));
      bar.remove();
    });
    document.body.appendChild(bar);
  }

  function init() {
    if (!required()) return;      // ads off -> no cookies -> no banner
    if (mode() === 'off') return; // ads show, no notice
    if (read()) return;           // already dismissed / chose
    render(mode() === 'gate');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }

  return { get: read, set: write, required: required, mode: mode };
})();
