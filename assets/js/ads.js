/* ============================================
 123MiniApps.online, Ad loader (Adsterra)
 File: assets/js/ads.js

 Your 4 Adsterra banner units are wired in below. Each banner is loaded
 inside its own same-origin iframe (assets/ads/<size>.html) so their
 internal 'atOptions' variables never clash - that is what lets several
 sizes appear on one page.

 Placement (kept moderate on purpose - a clean, fast site keeps visitors
 and rankings, which is what actually grows ad income):
   - In-content banner: fills every <div class="ad-slot"> already built
     into the blog, homepage and (via JS) each tool page.
       * desktop  -> 728x90 leaderboard
       * mobile   -> 300x250 rectangle
   - Side rails: 160x600 skyscrapers in the left and right page gutters,
     shown ONLY when the screen is wide enough that they cannot overlap
     the content, and hidden on laptops/tablets/phones.

 Privacy: these are third-party ad scripts that may set cookies. Your
 Privacy and Cookie pages already mention advertising. consentMode
 'notice' loads ads immediately (the cookie notice is informational);
 'gate' waits for the visitor to Accept; 'off' loads with no notice.

 To turn ads OFF again, set enabled:false below.
 ============================================ */

window.ADSTERRA = window.ADSTERRA || {
	enabled: true,
	consentMode: 'notice',

	// Your Adsterra banner ad-unit keys (safe to be public - they live in
	// the page anyway). Each maps to assets/ads/<width>x<height>.html.
	banners: {
		rect:   { key: '6d10ec0ef7be1d968a2e737f196dbff5', w: 300, h: 250 },
		leader: { key: '82b78bed10155579891e560d7441980f', w: 728, h: 90  },
		mobile: { key: '5fc1d78bcad974346f79cd94f79ad801', w: 320, h: 50  },
		rail:   { key: 'a8a801176b8daa16b1bf43b4846af37e', w: 160, h: 600 }
	},

	// Optional: a site-wide Social Bar / Popunder script SRC. Left empty on
	// purpose (those formats are intrusive; add later once traffic grows).
	siteScriptUrl: ''
};

(function () {
	var cfg = window.ADSTERRA || {};
	if (!cfg.enabled) return;

	// Never show ads on legal / system pages (thin pages; also keeps the
	// door open for stricter networks like AdSense later).
	var path = (location.pathname || '').toLowerCase();
	if (path.indexOf('/pages/') !== -1 ||
		/\/(404|offline|theme-debug)\.html$/.test(path)) return;

	var ADS_BASE = '/assets/ads/';          // same-origin ad documents
	var RAIL_MIN_GUTTER = 176;              // px of side space needed to show a 160 rail
	var started = false;

	function isDesktop() {
		return (window.innerWidth || document.documentElement.clientWidth) >= 760;
	}

	/* Build a same-origin iframe that shows one Adsterra banner size. */
	function adFrame(w, h, extraStyle) {
		var f = document.createElement('iframe');
		f.src = ADS_BASE + w + 'x' + h + '.html';
		f.width = w; f.height = h;
		f.setAttribute('scrolling', 'no');
		f.setAttribute('frameborder', '0');
		f.setAttribute('loading', 'lazy');
		f.setAttribute('title', 'Advertisement');
		f.setAttribute('aria-hidden', 'true');
		f.style.cssText = 'border:0;display:block;overflow:hidden;width:' + w + 'px;height:' + h +
			'px;max-width:100%;' + (extraStyle || '');
		return f;
	}

	/* A small, unobtrusive "Advertisement" label (good practice + some
	   networks require ads to be labelled). */
	function label() {
		var s = document.createElement('span');
		s.textContent = 'Advertisement';
		s.style.cssText = 'display:block;text-align:center;font:600 10px/1.4 Inter,system-ui,sans-serif;' +
			'letter-spacing:.08em;text-transform:uppercase;opacity:.45;margin-bottom:6px';
		return s;
	}

	/* ---- In-content banners: fill every .ad-slot on the page ---- */
	function fillSlots() {
		var slots = document.querySelectorAll('.ad-slot');
		slots.forEach(function (slot) {
			if (slot.getAttribute('data-ad-done')) return;
			slot.setAttribute('data-ad-done', '1');
			slot.hidden = false;
			slot.style.cssText = 'margin:32px auto;display:flex;flex-direction:column;align-items:center;' +
				'justify-content:center;min-height:60px';
			slot.appendChild(label());
			var b = isDesktop() ? cfg.banners.leader : cfg.banners.rect;
			slot.appendChild(adFrame(b.w, b.h));
		});
	}

	/* ---- Tool pages have no .ad-slot in their HTML: add one before
	   the "Related tools" section so the tool itself stays at the top. ---- */
	function ensureToolSlot() {
		if (!document.querySelector('main.tool-page')) return;
		if (document.querySelector('.ad-slot')) return;      // already has one
		var relStrip = document.getElementById('related');
		var host = relStrip ? relStrip.closest('.section') : null;
		var container = document.querySelector('main.tool-page .container');
		if (!container) return;
		var slot = document.createElement('div');
		slot.className = 'ad-slot';
		if (host && host.parentNode) host.parentNode.insertBefore(slot, host);
		else container.appendChild(slot);
	}

	/* ---- Side rails (160x600), only where they fit without overlapping ---- */
	var railLeft, railRight;
	function makeRail(side) {
		var d = document.createElement('div');
		d.className = 'ad-rail ad-rail--' + side;
		d.style.cssText = 'position:fixed;top:110px;z-index:40;' + side + ':8px;' +
			'width:160px;height:600px;display:none';
		d.appendChild(adFrame(cfg.banners.rail.w, cfg.banners.rail.h));
		document.body.appendChild(d);
		return d;
	}
	function positionRails() {
		if (!railLeft) { railLeft = makeRail('left'); railRight = makeRail('right'); }
		// Measure the real content column so rails never sit over the text.
		var col = document.querySelector('main .container') || document.querySelector('.container');
		var gutter = col ? col.getBoundingClientRect().left : 0;
		var show = gutter >= RAIL_MIN_GUTTER;
		[railLeft, railRight].forEach(function (r) {
			r.style.display = show ? 'block' : 'none';
			if (show) {
				var edge = Math.max(8, (gutter - 160) / 2);   // centre the rail in the gutter
				r.style[r.classList.contains('ad-rail--left') ? 'left' : 'right'] = edge + 'px';
			}
		});
	}

	var rz;
	function onResize() { clearTimeout(rz); rz = setTimeout(positionRails, 200); }

	function start() {
		if (started) return;
		started = true;

		if ((cfg.siteScriptUrl || '').trim()) {
			var s = document.createElement('script');
			var u = cfg.siteScriptUrl.trim();
			s.src = /^(https?:)?\/\//.test(u) ? u : '//' + u;
			s.async = true; s.setAttribute('data-cfasync', 'false');
			document.body.appendChild(s);
		}

		ensureToolSlot();
		fillSlots();
		positionRails();
		window.addEventListener('resize', onResize);
	}

	function maybeStart() {
		var gate = (cfg.consentMode || 'notice') === 'gate';
		if (gate && !(window.CONSENT && window.CONSENT.get() === 'accepted')) return;
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
