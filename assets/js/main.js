/* ============================================
 123MiniApps.online v2.0
 File: main.js
 Purpose: Application bootstrap. Wires the nav,
 search, homepage sections, cookie banner
 and newsletter, then hands off to the
 animation and PWA modules.
 ============================================ */

const App = {
 search: null,

 init() {
 this.search = new SearchEngine(window.TOOLS, window.CONFIG);
 window.searchEngine = this.search;

 this.initNav();
 this.initSearch();
 this.initHomepage();
 this.initCookieBanner();
 this.initNewsletter();
 this.initFeedback();

 initScrollUI();
 initScrollReveal();
 initCountUp();

 const hero = document.querySelector('.hero');
 if (hero) {
 initParticles(document.getElementById('hero-particles'));
 initParallax(hero.querySelector('.hero__visual'));
 initTypewriter(document.getElementById('typewriter'), window.CONFIG.rotatingWords);
 }

 PWA.init();
 Analytics.init();

 this.markActiveNavLink();
 },

 /* ============================================
 NAVIGATION
 ============================================ */

 initNav() {
 const toggle = document.getElementById('nav-toggle');
 const drawer = document.getElementById('nav-drawer');
 if (!toggle || !drawer) return;

 const close = () => {
 drawer.classList.remove('is-open');
 toggle.setAttribute('aria-expanded', 'false');
 document.body.style.overflow = '';
 };

 const open = () => {
 drawer.classList.add('is-open');
 toggle.setAttribute('aria-expanded', 'true');
 document.body.style.overflow = 'hidden';
 };

 toggle.addEventListener('click', () => {
 drawer.classList.contains('is-open') ? close() : open();
 });

 // Any link tap closes the drawer
 drawer.addEventListener('click', (e) => {
 if (e.target.closest('a')) close();
 });

 document.addEventListener('keydown', (e) => {
 if (e.key === 'Escape' && drawer.classList.contains('is-open')) {
 close();
 toggle.focus();
 }
 });

 // Returning to desktop width should never leave a stuck drawer
 window.addEventListener('resize', debounce(() => {
 if (window.innerWidth > 900) close();
 }, 200), { passive: true });
 },

 /** Highlight the nav link matching the current page. */
 markActiveNavLink() {
 const path = window.location.pathname.split('/').pop() || 'index.html';
 document.querySelectorAll('.nav__link').forEach((link) => {
 const href = link.getAttribute('href') || '';
 const target = href.split('/').pop().split('#')[0];
 if (target && target === path) {
 link.classList.add('is-active');
 link.setAttribute('aria-current', 'page');
 }
 });
 },

 /* ============================================
 SEARCH, inline bar + full modal
 ============================================ */

 initSearch() {
 const modal = document.getElementById('search-modal');
 const openBtns = document.querySelectorAll('[data-open-search]');
 const inlineInput = document.getElementById('search-input');

 if (modal) this.initSearchModal(modal, openBtns);

 // The homepage's inline bar hands off to the modal on focus, 
 // one search implementation, two entry points.
 if (inlineInput && modal) {
 inlineInput.addEventListener('focus', () => {
 this.openSearchModal(modal, inlineInput.value);
 inlineInput.blur();
 });
 }
 },

 initSearchModal(modal, openBtns) {
 const input = modal.querySelector('#search-modal-input');
 const results = modal.querySelector('#search-results');
 const closeBtn = modal.querySelector('[data-close-search]');

 let releaseFocus = null;
 let highlighted = -1;

 const render = (query) => {
 results.innerHTML = '';
 highlighted = -1;

 if (!query.trim()) {
 this.renderRecentSearches(results, (q) => {
 input.value = q;
 render(q);
 });
 return;
 }

 const matches = this.search.search(query);

 if (!matches.length) {
 results.append(this.renderNoResults(query));
 return;
 }

 const groups = this.search.groupByCategory(matches);

 groups.forEach((group) => {
 results.append(
 el('div', {
 className: 'search-results__group-label',
 text: `${group.category.icon} ${group.category.name}`
 })
 );

 group.tools.forEach((tool) => {
 results.append(this.renderSearchResult(tool, query));
 });
 });

 // Announce count to screen readers
 const status = modal.querySelector('#search-status');
 if (status) {
 status.textContent = `${matches.length} tool${matches.length === 1 ? '' : 's'} found.`;
 }
 };

 const onInput = debounce((e) => render(e.target.value), window.CONFIG.searchDebounceMs);
 input.addEventListener('input', onInput);

 /* Keyboard navigation through results */
 input.addEventListener('keydown', (e) => {
 const items = Array.from(results.querySelectorAll('.search-result'));
 if (!items.length) return;

 if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
 e.preventDefault();
 items.forEach((i) => i.classList.remove('is-highlighted'));
 highlighted =
 e.key === 'ArrowDown'
 ? (highlighted + 1) % items.length
 : (highlighted - 1 + items.length) % items.length;
 items[highlighted].classList.add('is-highlighted');
 items[highlighted].scrollIntoView({ block: 'nearest' });
 }

 if (e.key === 'Enter' && highlighted >= 0) {
 e.preventDefault();
 this.search.addRecent(input.value);
 items[highlighted].click();
 }
 });

 const open = (seed = '') => {
 modal.classList.add('is-open');
 modal.removeAttribute('aria-hidden');
 document.body.style.overflow = 'hidden';
 input.value = seed;
 render(seed);
 setTimeout(() => input.focus(), 60);
 releaseFocus = trapFocus(modal);
 };

 const close = () => {
 if (input.value.trim()) this.search.addRecent(input.value);
 modal.classList.remove('is-open');
 modal.setAttribute('aria-hidden', 'true');
 document.body.style.overflow = '';
 if (releaseFocus) releaseFocus();
 releaseFocus = null;
 };

 this.openSearchModal = (m, seed) => open(seed);

 openBtns.forEach((btn) => btn.addEventListener('click', () => open()));
 if (closeBtn) closeBtn.addEventListener('click', close);

 modal.addEventListener('click', (e) => {
 if (e.target === modal) close();
 });

 document.addEventListener('keydown', (e) => {
 // Ctrl/Cmd+K opens from anywhere
 if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
 e.preventDefault();
 modal.classList.contains('is-open') ? close() : open();
 }
 if (e.key === 'Escape' && modal.classList.contains('is-open')) close();
 });
 },

 /** @returns {HTMLElement} */
 renderSearchResult(tool, query) {
 const link = el('a', {
 className: 'search-result',
 attrs: { href: tool.url }
 });

 link.append(
 el('span', { className: 'search-result__icon', text: tool.icon, attrs: { 'aria-hidden': 'true' } })
 );

 const body = el('span', { className: 'flex-1' });
 body.append(
 el('span', {
 className: 'search-result__name',
 html: this.search.highlight(tool.name, query)
 })
 );
 body.append(el('span', { className: 'search-result__desc', text: tool.description }));
 link.append(body);

 if (tool.premium) {
 link.append(el('span', { className: 'badge badge--premium', text: 'Premium' }));
 }

 return link;
 },

 renderRecentSearches(container, onPick) {
 const recent = this.search.getRecent();

 if (recent.length) {
 container.append(el('div', { className: 'search-results__group-label', text: 'Recent searches' }));
 recent.forEach((q) => {
 container.append(
 el('button', {
 className: 'search-result',
 attrs: { type: 'button' },
 on: { click: () => onPick(q) }
 }, [
 el('span', { className: 'search-result__icon', text: '🕘', attrs: { 'aria-hidden': 'true' } }),
 el('span', { className: 'search-result__name', text: q })
 ])
 );
 });
 }

 container.append(el('div', { className: 'search-results__group-label', text: 'Most popular' }));
 window.getPopularTools(5).forEach((tool) => {
 container.append(this.renderSearchResult(tool, ''));
 });
 },

 /** @returns {HTMLElement} */
 renderNoResults(query) {
 const wrap = el('div', { className: 'search-empty' }, [
 el('div', { className: 'search-empty__icon', text: '🔍', attrs: { 'aria-hidden': 'true' } }),
 el('p', { className: 'font-semibold text-primary', text: `No tools match "${query}"` }),
 el('p', { className: 'text-sm mt-2', text: 'Try one of these instead:' })
 ]);

 const suggestions = el('div', { className: 'flex flex-wrap gap-2 justify-center mt-4' });
 this.search.suggestions(4).forEach((tool) => {
 suggestions.append(
 el('a', { className: 'badge', attrs: { href: tool.url }, text: `${tool.icon} ${tool.name}` })
 );
 });

 wrap.append(suggestions);
 return wrap;
 },

 /* ============================================
 HOMEPAGE SECTION RENDERING
 ============================================ */

 initHomepage() {
 if (!document.getElementById('category-grid')) return;

 this.renderCategories();
 this.renderFeaturedTools();
 this.renderAllTools();
 this.renderFeatures();
 this.renderTestimonials();
 this.renderFAQ();
 this.renderStats();
 },

 renderCategories() {
 const grid = document.getElementById('category-grid');
 const row = document.getElementById('category-row');

 if (grid) {
 const frag = document.createDocumentFragment();
 window.CATEGORIES.filter((c) => c.primary).forEach((category, i) => {
 const card = createCategoryCard({ category });
 card.dataset.animate = 'fade-up';
 card.style.setProperty('--reveal-delay', `${i * 60}ms`);
 frag.append(card);
 });
 grid.append(frag);
 }

 if (row) {
 const frag = document.createDocumentFragment();
 window.CATEGORIES.filter((c) => !c.primary).forEach((category) => {
 frag.append(createCategoryChip({ category }));
 });
 row.append(frag);
 }
 },

 renderFeaturedTools() {
 const grid = document.getElementById('featured-grid');
 if (!grid) return;

 const frag = document.createDocumentFragment();
 window.getPopularTools(6).forEach((tool, i) => {
 const card = createToolCard({ tool, variant: 'featured' });
 card.dataset.animate = 'fade-up';
 card.style.setProperty('--reveal-delay', `${i * 60}ms`);
 frag.append(card);
 });
 grid.append(frag);
 },

 /**
 * The full directory, tabbed by category. Each panel's cards are
 * built lazily on first activation so the initial render only
 * pays for one category instead of all 95 tools.
 */
 renderAllTools() {
 const mount = document.getElementById('all-tools');
 if (!mount) return;

 const buildGrid = (tools) => {
 const grid = el('div', { className: 'grid-auto' });
 tools.forEach((tool) => grid.append(createToolCard({ tool })));
 return grid;
 };

 const tabs = [
 {
 id: 'all',
 label: `All (${window.TOOLS.length})`,
 render: () => buildGrid(window.TOOLS)
 },
 ...window.CATEGORIES.map((category) => ({
 id: category.id,
 label: `${category.icon} ${category.name.replace(' Tools', '')} (${window.getCategoryCount(category.id)})`,
 render: () => {
 const panel = el('div');
 panel.id = `category-${category.id}`;
 panel.append(buildGrid(window.getToolsByCategory(category.id)));
 return panel;
 }
 }))
 ];

 mount.append(createTabs({ tabs, activeIndex: 0 }));
 },

 renderFeatures() {
 const grid = document.getElementById('features-grid');
 if (!grid) return;

 const features = [
 {
 icon: '🔒',
 title: 'Nothing leaves your device',
 desc: 'Every tool runs as JavaScript in your tab. There is no server to send your data to, because there is no server. Check the Network tab and see for yourself.'
 },
 {
 icon: '⚡',
 title: 'Loads in under a second',
 desc: 'No frameworks, no tracking scripts, no ad networks. Just hand-written HTML, CSS and JavaScript, cached aggressively after your first visit.'
 },
 {
 icon: '📱',
 title: 'Built for every screen',
 desc: 'Fluid layouts from 320px up, 44px touch targets, and full keyboard navigation. Install it to your home screen and it behaves like an app.'
 },
 {
 icon: '∞',
 title: 'Free, with no catch',
 desc: 'No account, no usage limits, no upsell. The Premium badge marks depth of features, not a paywall, everything here costs nothing.'
 }
 ];

 const frag = document.createDocumentFragment();
 features.forEach((f, i) => frag.append(createFeatureCard({ ...f, delay: i * 70 })));
 grid.append(frag);
 },

 renderTestimonials() {
 const grid = document.getElementById('testimonials-grid');
 if (!grid) return;

 const frag = document.createDocumentFragment();
 window.TESTIMONIALS.forEach((t, i) => frag.append(createTestimonial({ ...t, delay: i * 90 })));
 grid.append(frag);
 },

 renderFAQ() {
 const mount = document.getElementById('faq');
 if (!mount) return;
 mount.append(createAccordion({ items: window.FAQS, single: true }));
 },

 /** Fill the hero stat counters from live data rather than hardcoding. */
 renderStats() {
 const toolCount = document.querySelector('[data-stat="tools"]');
 const catCount = document.querySelector('[data-stat="categories"]');

 if (toolCount) toolCount.dataset.countTo = String(window.TOOLS.length);
 if (catCount) catCount.dataset.countTo = String(window.CATEGORIES.length);
 },

 /* ============================================
 COOKIE BANNER
 ============================================ */

 initCookieBanner() {
 const banner = document.getElementById('cookie-banner');
 if (!banner) return;

 let consent = null;
 try {
 consent = localStorage.getItem(window.CONFIG.storageKeys.cookieConsent);
 } catch {
 /* storage unavailable, show the banner but don't persist dismissal */
 }

 if (consent) {
 banner.remove();
 return;
 }

 banner.hidden = false;

 const dismiss = (value) => {
 try {
 localStorage.setItem(window.CONFIG.storageKeys.cookieConsent, value);
 } catch {
 /* no-op */
 }
 banner.remove();
 };

 banner.querySelector('[data-consent="all"]')?.addEventListener('click', () => dismiss('all'));
 banner.querySelector('[data-consent="essential"]')?.addEventListener('click', () => dismiss('essential'));
 },

 /* ============================================
 NEWSLETTER
 ============================================ */

 initNewsletter() {
 const form = document.getElementById('newsletter-form');
 if (!form) return;

 form.addEventListener('submit', (e) => {
 e.preventDefault();

 const input = form.querySelector('input[type="email"]');
 const email = input.value.trim();

 if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
 input.setAttribute('aria-invalid', 'true');
 toast({ type: 'error', title: 'Check that address', message: 'That does not look like a valid email.' });
 return;
 }

 input.removeAttribute('aria-invalid');

 // Stored locally only, there is no mailing list backend in this build.
 try {
 localStorage.setItem(window.CONFIG.storageKeys.newsletter, email);
 } catch {
 /* no-op */
 }

 const success = document.getElementById('newsletter-success');
 if (success) {
 success.hidden = false;
 success.textContent = 'Saved to this browser. Connect a mail provider to make it live.';
 }

 form.reset();
 toast({ type: 'success', title: 'Noted', message: 'Stored locally on this device.' });
 });
 },

 /* ============================================
 FEEDBACK WIDGET
 ============================================ */

 initFeedback() {
 const widget = document.getElementById('feedback');
 if (!widget) return;

 widget.querySelectorAll('.feedback__btn').forEach((btn) => {
 btn.addEventListener('click', () => {
 widget.querySelectorAll('.feedback__btn').forEach((b) => {
 b.classList.remove('is-selected');
 b.setAttribute('aria-pressed', 'false');
 });

 btn.classList.add('is-selected');
 btn.setAttribute('aria-pressed', 'true');

 try {
 localStorage.setItem(
 window.CONFIG.storageKeys.feedback,
 JSON.stringify({ page: location.pathname, value: btn.dataset.value, at: Date.now() })
 );
 } catch {
 /* no-op */
 }

 toast({ type: 'success', title: 'Thanks for the signal', message: 'Saved on your device only.' });
 });
 });
 }
};

window.App = App;

if (document.readyState === 'loading') {
 document.addEventListener('DOMContentLoaded', () => App.init(), { once: true });
} else {
 App.init();
}
