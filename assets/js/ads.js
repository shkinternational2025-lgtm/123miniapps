/* ============================================
 123MiniApps.online, Ad loader (Adsterra)
 File: assets/js/ads.js

 Four Adsterra banner units, each in its own same-origin iframe
 (assets/ads/<size>.html) so their internal 'atOptions' never clash.

 Layout model (desktop >= 1280px):
   - The page content is capped so a fixed gutter (~212px) opens on each
     side. The 160x600 side rails sit in those gutters, hugging the content
     edge, so there is no large empty band. Content stays as wide as the
     viewport allows, up to a sensible max.
   - Below 1280px there is no room for rails, so a dismissible 320x50
     bottom anchor is shown instead.
 ============================================ */

window.ADSTERRA = window.ADSTERRA || {
	enabled: true,
	consentMode: 'notice',
	banners: {
		rect:   { key: '6d10ec0ef7be1d968a2e737f196dbff5', w: 300, h: 250 },
		leader: { key: '82b78bed10155579891e560d7441980f', w: 728, h: 90  },
		mobile: { key: '5fc1d78bcad974346f79cd94f79ad801', w: 320, h: 50  },
		rail:   { key: 'a8a801176b8daa16b1bf43b4846af37e', w: 160, h: 600 }
	},
	siteScriptUrl: ''
};

(function () {
	var cfg = window.ADSTERRA || {};
	if (!cfg.enabled) return;

	// System / thin pages never show ads. Inside /pages/ only the two
	// content pages (services, insights) run ads; legal/about/contact do not.
	var path = (location.pathname || '').toLowerCase();
	if (/\/(404|offline|theme-debug)\.html$/.test(path)) return;
	if (path.indexOf('/pages/') !== -1 &&
		!/\/pages\/(services|insights)\.html$/.test(path)) return;

	var ADS_BASE = '/assets/ads/';
	var RAIL = 160, RAIL_H = 600;
	var GAP = 24;              // space between a rail and the content column
	var MIN_EDGE = 8;          // smallest margin from a rail to the screen edge
	var RAIL_BREAKPOINT = 1280;// >= this width: side rails. Below: bottom anchor.
	var started = false;

	function isDesktop() {
		return (window.innerWidth || document.documentElement.clientWidth) >= 760;
	}

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

	/* ---- Tool pages have no .ad-slot: add one before "Related tools" ---- */
	function ensureToolSlot() {
		if (!document.querySelector('main.tool-page')) return;
		if (document.querySelector('.ad-slot')) return;
		var relStrip = document.getElementById('related');
		var host = relStrip ? relStrip.closest('.section') : null;
		var container = document.querySelector('main.tool-page .container');
		if (!container) return;
		var slot = document.createElement('div');
		slot.className = 'ad-slot';
		if (host && host.parentNode) host.parentNode.insertBefore(slot, host);
		else container.appendChild(slot);
	}

	/* ---- Find the real content column (never the nav/footer) ---- */
	function contentCol() {
		var c = document.querySelector('main .container');
		if (c) return c;
		var all = [].slice.call(document.querySelectorAll('.container'));
		for (var i = 0; i < all.length; i++) {
			if (!all[i].closest('header, nav, footer')) return all[i];
		}
		return document.querySelector('.container');
	}

	/* ---- Side rails (160x600), hugging the content edges ---- */
	var railLeft, railRight;
	function makeRail(side) {
		var d = document.createElement('div');
		d.className = 'ad-rail ad-rail--' + side;
		d.style.cssText = 'position:fixed;top:110px;z-index:40;width:' + RAIL + 'px;height:' + RAIL_H + 'px;display:none';
		d.appendChild(adFrame(cfg.banners.rail.w, cfg.banners.rail.h));
		document.body.appendChild(d);
		return d;
	}
	function positionRails() {
		var vw = document.documentElement.clientWidth || window.innerWidth;
		if (vw < RAIL_BREAKPOINT) {
			if (railLeft) { railLeft.style.display = 'none'; railRight.style.display = 'none'; }
			return;
		}
		if (!railLeft) { railLeft = makeRail('left'); railRight = makeRail('right'); }
		var col = contentCol();
		var rect = col ? col.getBoundingClientRect() : null;
		var leftGutter = rect ? rect.left : 0;
		var rightGutter = rect ? (vw - rect.right) : 0;
		var need = RAIL + GAP + MIN_EDGE;
		var show = rect && leftGutter >= need && rightGutter >= need;
		if (!show) {
			railLeft.style.display = 'none';
			railRight.style.display = 'none';
			return;
		}
		railLeft.style.display = 'block';
		railRight.style.display = 'block';
		// Hug the content: rail sits GAP px from the content edge.
		railLeft.style.right = 'auto';
		railLeft.style.left = Math.max(MIN_EDGE, rect.left - GAP - RAIL) + 'px';
		railRight.style.left = 'auto';
		railRight.style.right = Math.max(MIN_EDGE, (vw - rect.right) - GAP - RAIL) + 'px';
	}

	/* ---- Ad layout CSS: cap content so the rail gutters exist, and keep the
	   content as wide as the viewport allows. Injected at parse time so the
	   width is set before first paint (minimises reflow). ---- */
	function injectAdStyles() {
		if (document.getElementById('ad-layout-style')) return;
		var st = document.createElement('style');
		st.id = 'ad-layout-style';
		// 424 = 2 x (rail 160 + gap 24 + edge 28). Leaves ~212px gutter each side.
		st.textContent =
			'@media (min-width:1280px){' +
			':root{--container-max:min(1600px,calc(100vw - 424px)) !important;' +
			'--container-wide:min(1600px,calc(100vw - 424px)) !important}' +
			'.container--narrow{max-width:min(1100px,calc(100vw - 424px)) !important}' +
			'main.tool-page .prose{max-width:none}' +
			'main.tool-page article figure{text-align:center}' +
			'main.tool-page article figure img{margin-inline:auto}}' +
			'body.has-anchor-ad{padding-bottom:66px}' +
			'.ad-anchor{position:fixed;left:0;right:0;bottom:0;z-index:50;display:flex;' +
			'align-items:center;justify-content:center;gap:8px;padding:6px 44px;' +
			'background:rgba(11,17,32,.94);backdrop-filter:blur(6px);' +
			'-webkit-backdrop-filter:blur(6px);border-top:1px solid rgba(255,255,255,.08)}' +
			'.ad-anchor__x{position:absolute;top:50%;right:8px;transform:translateY(-50%);' +
			'width:28px;height:28px;border:0;border-radius:50%;background:rgba(255,255,255,.14);' +
			'color:#fff;font-size:18px;line-height:1;cursor:pointer}' +
			'body.has-anchor-ad .theme-fab,body.has-anchor-ad .back-to-top{' +
			'bottom:calc(var(--space-8,2rem) + 62px)}' +
			'@media(max-width:560px){body.has-anchor-ad .theme-fab,' +
			'body.has-anchor-ad .back-to-top{bottom:calc(var(--space-4,1rem) + 62px)}}';
		document.head.appendChild(st);
	}

	function hideAnchor() {
		var bar = document.querySelector('.ad-anchor');
		if (bar) bar.remove();
		document.body.classList.remove('has-anchor-ad');
	}
	function mountAnchor() {
		try { if (sessionStorage.getItem('anchorAdClosed') === '1') return; } catch (e) {}
		if (window.innerWidth >= RAIL_BREAKPOINT) return;
		if (document.querySelector('.ad-anchor')) return;
		var bar = document.createElement('div');
		bar.className = 'ad-anchor';
		bar.setAttribute('aria-label', 'Advertisement');
		bar.appendChild(adFrame(cfg.banners.mobile.w, cfg.banners.mobile.h));
		var x = document.createElement('button');
		x.type = 'button';
		x.className = 'ad-anchor__x';
		x.setAttribute('aria-label', 'Close ad');
		x.innerHTML = '&times;';
		x.addEventListener('click', function () {
			hideAnchor();
			try { sessionStorage.setItem('anchorAdClosed', '1'); } catch (e) {}
		});
		bar.appendChild(x);
		document.body.appendChild(bar);
		document.body.classList.add('has-anchor-ad');
	}

	function syncAds() {
		positionRails();
		if (window.innerWidth >= RAIL_BREAKPOINT) hideAnchor();
		else mountAnchor();
	}

	var rz;
	function onResize() { clearTimeout(rz); rz = setTimeout(syncAds, 150); }

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
		syncAds();
		window.addEventListener('resize', onResize);
		window.addEventListener('load', syncAds);
	}

	function maybeStart() {
		var gate = (cfg.consentMode || 'notice') === 'gate';
		if (gate && !(window.CONSENT && window.CONSENT.get() === 'accepted')) return;
		start();
	}

	document.addEventListener('consentchange', function (e) {
		if (e.detail && e.detail.value === 'accepted') start();
	});

	injectAdStyles();

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', maybeStart, { once: true });
	} else {
		maybeStart();
	}
})();
