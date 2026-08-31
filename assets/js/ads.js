/* ============================================
 123MiniApps.online, Ad loader (Adsterra-ready)
 File: assets/js/ads.js

 Ads are OFF by default. Nothing loads and nothing tracks until YOU
 paste your own Adsterra code below. See ADSTERRA-SETUP.md for the
 exact steps and where to get each code.

 IMPORTANT: enabling ads means third-party ad scripts will run and may
 set cookies / track visitors. Before you switch ads on, keep your
 Privacy and Cookie pages accurate (they already mention advertising).
 ============================================ */

window.ADSTERRA = window.ADSTERRA || {
 // 1) SITE-WIDE SCRIPT (easiest + highest-earning: "Social Bar" or "Popunder").
 // In Adsterra, create that ad unit, copy the script SRC it gives you
 // (looks like //pl00000.effectivegatecpm.com/xx/yy/zz/invoke.js),
 // and paste it between the quotes. Leave '' to keep it off.
 siteScriptUrl: '',

 // 2) IN-CONTENT BANNER (optional). Adsterra "Native Banner" / "Banner"
 // gives you a script SRC plus a container id. Paste both here to fill
 // the <div class="ad-slot"> placeholders in the blog and homepage.
 bannerScriptUrl: '',
 bannerContainerId: '', // e.g. 'container-abc123'

 // 3) CONSENT behaviour:
 //   'notice' (default) - ads load immediately; a small dismissible cookie
 //                        notice is shown. Recommended for Adsterra.
 //   'gate'             - ads do NOT load until the visitor clicks Accept.
 //   'off'              - ads load immediately, no notice shown at all.
 consentMode: 'notice'
};

(function () {
 var cfg = window.ADSTERRA || {};

 function loadScript(url, attrs) {
 if (!url) return;
 var src = (/^(https?:)?\/\//.test(url)) ? url : '//' + url;
 var s = document.createElement('script');
 s.src = src;
 s.async = true;
 s.setAttribute('data-cfasync', 'false');
 if (attrs) Object.keys(attrs).forEach(function (k) { s.setAttribute(k, attrs[k]); });
 document.body.appendChild(s);
 }

 var started = false;
 function start() {
 if (started) return;
 started = true;

 // Site-wide unit (social bar / popunder)
 loadScript((cfg.siteScriptUrl || '').trim());

 // In-content banner into every .ad-slot on the page
 var url = (cfg.bannerScriptUrl || '').trim();
 var cid = (cfg.bannerContainerId || '').trim();
 if (url && cid) {
 document.querySelectorAll('.ad-slot').forEach(function (slot) {
 slot.hidden = false;
 var box = document.createElement('div');
 box.id = cid;
 slot.appendChild(box);
 loadScript(url);
 });
 }
 }

 // Decide whether we may load ad scripts yet. If a consent banner is in play
 // (consent.js present + ads configured), wait for an explicit "accepted".
 // Rejecting means nothing loads. With no consent layer, load as before.
 function maybeStart() {
 var hasAds = (cfg.siteScriptUrl || '').trim() || (cfg.bannerScriptUrl || '').trim();
 if (!hasAds) return;

 // Only hold ads back when consentMode is 'gate'. In 'notice'/'off' modes
 // (the default) ads load immediately; the banner, if any, is informational.
 var gate = (cfg.consentMode || 'notice') === 'gate';
 if (gate && !(window.CONSENT && window.CONSENT.get() === 'accepted')) {
 return; // wait for the visitor to Accept (consentchange handler starts it)
 }
 start();
 }

 document.addEventListener('consentchange', function (e) {
 if (e.detail && e.detail.value === 'accepted') start();
 });

 if (document.readyState === 'loading') {
 document.addEventListener('DOMContentLoaded', maybeStart, { once: true });
 } else {
 maybeStart();
 }
})();
