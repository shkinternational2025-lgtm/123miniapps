/* ============================================
 123MiniApps.online v2.0
 File: components.js
 Purpose: Factory functions that return real DOM
 nodes. No template strings holding user
 data, no innerHTML on untrusted input.
 ============================================ */

/* --------------------------------------------
 Tiny DOM helper, the only "framework" here.
 -------------------------------------------- */

/**
 * Create an element.
 * @param {string} tag
 * @param {Object} [props] - className, text, html, attrs, dataset, on, style
 * @param {(Node|string)[]} [children]
 * @returns {HTMLElement}
 */
function el(tag, props = {}, children = []) {
 const node = document.createElement(tag);

 if (props.className) node.className = props.className;
 if (props.id) node.id = props.id;
 if (props.text != null) node.textContent = props.text;
 if (props.html != null) node.innerHTML = props.html; // only ever used with trusted/escaped markup

 if (props.attrs) {
 for (const [k, v] of Object.entries(props.attrs)) {
 if (v === false || v == null) continue;
 node.setAttribute(k, v === true ? '' : String(v));
 }
 }

 if (props.dataset) {
 for (const [k, v] of Object.entries(props.dataset)) node.dataset[k] = v;
 }

 if (props.style) Object.assign(node.style, props.style);

 if (props.on) {
 for (const [event, handler] of Object.entries(props.on)) {
 node.addEventListener(event, handler);
 }
 }

 for (const child of [].concat(children)) {
 if (child == null || child === false) continue;
 node.append(child instanceof Node ? child : document.createTextNode(String(child)));
 }

 return node;
}

/** Inline SVG icon set, keeps the page request-free. */
const ICONS = {
 search:
 '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
 arrow:
 '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 close:
 '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>',
 up:
 '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 15 6-6 6 6"/></svg>',
 palette:
 '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2Z"/></svg>',
 copy:
 '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>',
 download:
 '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m0 0 4-4m-4 4-4-4M4 19h16"/></svg>',
 refresh:
 '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v6h-6"/></svg>',
 share:
 '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg>'
};

/* ============================================
 BUTTON
 ============================================ */

/**
 * @param {Object} o
 * @param {string} [o.label]
 * @param {'primary'|'secondary'|'ghost'|'danger'|'icon'} [o.variant]
 * @param {'sm'|'md'|'lg'|'xl'} [o.size]
 * @param {string} [o.icon] - key from ICONS or raw emoji
 * @param {Function} [o.onClick]
 * @param {string} [o.href] - renders an <a> instead of a <button>
 * @returns {HTMLElement}
 */
function createButton(o = {}) {
 const {
 label = '',
 variant = 'primary',
 size = 'md',
 icon,
 iconAfter,
 onClick,
 href,
 ariaLabel,
 className = ''
 } = o;

 const tag = href ? 'a' : 'button';
 const classes = ['btn', `btn--${variant}`, `btn--${size}`, className].filter(Boolean).join(' ');

 const node = el(tag, {
 className: classes,
 attrs: {
 ...(href ? { href } : { type: 'button' }),
 ...(ariaLabel ? { 'aria-label': ariaLabel } : {})
 },
 on: onClick ? { click: onClick } : undefined
 });

 if (icon) {
 node.append(
 el('span', { className: 'btn__icon', html: ICONS[icon] || null, text: ICONS[icon] ? null : icon })
 );
 }

 if (label) node.append(el('span', { text: label }));

 if (iconAfter) {
 node.append(
 el('span', {
 className: 'btn__icon btn__icon--arrow',
 html: ICONS[iconAfter] || null,
 text: ICONS[iconAfter] ? null : iconAfter
 })
 );
 }

 return node;
}

/* ============================================
 TOOL CARD
 ============================================ */

/**
 * @param {Object} o
 * @param {Object} o.tool
 * @param {'featured'|'standard'} [o.variant]
 * @param {string} [o.base] - path prefix ('' from root, '../' from /tools)
 * @returns {HTMLElement}
 */
function createToolCard({ tool, variant = 'standard', base = '' }) {
 const featured = variant === 'featured';

 const card = el('article', {
 className: `tool-card${featured ? ' tool-card--featured' : ''}`,
 dataset: { toolId: String(tool.id), category: tool.category }
 });

 /* Whole-card link, sits behind the content */
 card.append(
 el('a', {
 className: 'tool-card__overlay-link',
 attrs: { href: base + tool.url, 'aria-label': `Open ${tool.name}` }
 })
 );

 /* Top row: icon + badges */
 const top = el('div', { className: 'tool-card__top' }, [
 el('span', { className: 'tool-card__icon', text: tool.icon, attrs: { 'aria-hidden': 'true' } })
 ]);

 const badges = el('div', { className: 'flex gap-2 items-center' });
 if (tool.premium) badges.append(el('span', { className: 'badge badge--premium', text: 'Premium' }));
 if (!tool.live) badges.append(el('span', { className: 'badge badge--muted', text: 'Soon' }));
 badges.append(createFavoriteButton(tool));
 top.append(badges);

 card.append(top);
 card.append(el('h3', { className: 'tool-card__title', text: tool.name }));
 card.append(el('p', { className: 'tool-card__desc', text: tool.description }));

 if (featured) {
 const list = el('ul', { className: 'flex flex-wrap gap-2' });
 tool.features.slice(0, 3).forEach((f) => {
 list.append(el('li', { className: 'category-card__example', text: f }));
 });
 card.append(list);
 }

 /* Meta row */
 const meta = el('div', { className: 'tool-card__meta' }, [
 el('span', { className: 'tool-card__rating' }, [
 el('span', { text: '★', attrs: { 'aria-hidden': 'true' } }),
 el('span', { text: tool.rating.toFixed(1) }),
 el('span', { className: 'sr-only', text: `out of 5, ${formatCount(tool.usageCount)} uses` })
 ]),
 el('span', { className: 'tool-card__link' }, [
 el('span', { text: featured ? 'Open Tool' : 'Open' }),
 el('span', { html: ICONS.arrow })
 ])
 ]);

 card.append(meta);
 return card;
}

/**
 * Star/favorite toggle. Kept above the overlay link via z-index
 * so it stays independently clickable.
 * @returns {HTMLElement}
 */
function createFavoriteButton(tool) {
 const isFav = Favorites.has(tool.id);

 const btn = el('button', {
 className: `tool-card__fav${isFav ? ' is-active' : ''}`,
 attrs: {
 type: 'button',
 'aria-pressed': String(isFav),
 'aria-label': `${isFav ? 'Remove' : 'Add'} ${tool.name} ${isFav ? 'from' : 'to'} favorites`,
 title: 'Favorite'
 },
 text: isFav ? '★' : '☆',
 on: {
 click: (e) => {
 e.preventDefault();
 e.stopPropagation();
 const nowFav = Favorites.toggle(tool.id);
 btn.classList.toggle('is-active', nowFav);
 btn.textContent = nowFav ? '★' : '☆';
 btn.setAttribute('aria-pressed', String(nowFav));
 btn.setAttribute(
 'aria-label',
 `${nowFav ? 'Remove' : 'Add'} ${tool.name} ${nowFav ? 'from' : 'to'} favorites`
 );
 toast({
 type: 'success',
 title: nowFav ? 'Added to favorites' : 'Removed from favorites',
 message: tool.name
 });
 }
 }
 });

 return btn;
}

/* ============================================
 CATEGORY CARD / CHIP
 ============================================ */

/** @returns {HTMLElement} */
function createCategoryCard({ category, base = '' }) {
 const count = window.getCategoryCount(category.id);

 const card = el('article', { className: 'category-card', dataset: { category: category.id } }, [
 el('a', {
 className: 'category-card__link',
 attrs: { href: `${base}#category-${category.id}`, 'aria-label': `Browse ${category.name}` }
 }),
 el('span', { className: 'badge category-card__count', text: `${count} tools` }),
 el('span', { className: 'category-card__icon', text: category.icon, attrs: { 'aria-hidden': 'true' } }),
 el('h3', { className: 'category-card__title', text: category.name }),
 el('p', { className: 'category-card__desc', text: category.desc })
 ]);

 const examples = el('div', { className: 'category-card__examples' });
 category.examples.forEach((ex) => {
 examples.append(el('span', { className: 'category-card__example', text: ex }));
 });
 card.append(examples);

 return card;
}

/** @returns {HTMLElement} */
function createCategoryChip({ category, base = '' }) {
 const count = window.getCategoryCount(category.id);

 return el('a', {
 className: 'category-chip',
 dataset: { category: category.id },
 attrs: { href: `${base}#category-${category.id}` }
 }, [
 el('span', { className: 'category-chip__icon', text: category.icon, attrs: { 'aria-hidden': 'true' } }),
 el('span', {}, [
 el('span', { className: 'category-chip__name', text: category.name }),
 el('br'),
 el('span', { className: 'category-chip__count', text: `${count} tools` })
 ])
 ]);
}

/* ============================================
 FEATURE CARD / TESTIMONIAL
 ============================================ */

/** @returns {HTMLElement} */
function createFeatureCard({ icon, title, desc, delay = 0 }) {
 return el('article', {
 className: 'feature-card',
 dataset: { animate: 'fade-up' },
 style: { '--reveal-delay': `${delay}ms` }
 }, [
 el('div', { className: 'feature-card__icon', text: icon, attrs: { 'aria-hidden': 'true' } }),
 el('h3', { className: 'feature-card__title', text: title }),
 el('p', { className: 'feature-card__desc', text: desc })
 ]);
}

/** @returns {HTMLElement} */
function createTestimonial({ quote, name, role, stars, delay = 0 }) {
 return el('figure', {
 className: 'testimonial',
 dataset: { animate: 'fade-up' },
 style: { '--reveal-delay': `${delay}ms` }
 }, [
 el('div', {
 className: 'testimonial__stars',
 text: '★'.repeat(stars),
 attrs: { 'aria-label': `${stars} out of 5 stars` }
 }),
 el('blockquote', { className: 'testimonial__quote', text: `"${quote}"` }),
 el('figcaption', { className: 'testimonial__author' }, [
 el('div', {
 className: 'testimonial__avatar',
 text: name.split(' ').map((w) => w[0]).slice(0, 2).join(''),
 attrs: { 'aria-hidden': 'true' }
 }),
 el('div', {}, [
 el('div', { className: 'testimonial__name', text: name }),
 el('div', { className: 'testimonial__role', text: role })
 ])
 ])
 ]);
}

/* ============================================
 ACCORDION
 ============================================ */

/**
 * @param {Object} o
 * @param {{q: string, a: string}[]} o.items
 * @param {boolean} [o.single] - only one panel open at a time
 * @returns {HTMLElement}
 */
function createAccordion({ items, single = true }) {
 const root = el('div', { className: 'accordion' });

 items.forEach((item, i) => {
 const panelId = `faq-panel-${i}`;
 const triggerId = `faq-trigger-${i}`;

 const wrapper = el('div', { className: 'accordion__item' });

 const trigger = el('button', {
 className: 'accordion__trigger',
 id: triggerId,
 attrs: { type: 'button', 'aria-expanded': 'false', 'aria-controls': panelId }
 }, [
 el('span', { text: item.q }),
 el('span', { className: 'accordion__icon', text: '+', attrs: { 'aria-hidden': 'true' } })
 ]);

 const panel = el('div', {
 className: 'accordion__panel',
 id: panelId,
 attrs: { role: 'region', 'aria-labelledby': triggerId }
 }, [
 el('div', { className: 'accordion__panel-inner' }, [
 el('div', { className: 'accordion__content', text: item.a })
 ])
 ]);

 trigger.addEventListener('click', () => {
 const isOpen = wrapper.classList.contains('is-open');

 if (single) {
 root.querySelectorAll('.accordion__item.is-open').forEach((openItem) => {
 openItem.classList.remove('is-open');
 openItem.querySelector('.accordion__trigger').setAttribute('aria-expanded', 'false');
 });
 }

 wrapper.classList.toggle('is-open', !isOpen);
 trigger.setAttribute('aria-expanded', String(!isOpen));
 });

 wrapper.append(trigger, panel);
 root.append(wrapper);
 });

 return root;
}

/* ============================================
 TABS
 ============================================ */

/**
 * @param {Object} o
 * @param {{id: string, label: string, render: () => Node}[]} o.tabs
 * @param {number} [o.activeIndex]
 * @returns {HTMLElement}
 */
function createTabs({ tabs, activeIndex = 0 }) {
 const root = el('div', { className: 'tabs' });
 const list = el('div', { className: 'tabs__list', attrs: { role: 'tablist', 'aria-label': 'Tool categories' } });
 const panels = el('div');

 const tabEls = [];
 const panelEls = [];

 const activate = (index) => {
 tabEls.forEach((t, i) => {
 const selected = i === index;
 t.setAttribute('aria-selected', String(selected));
 t.setAttribute('tabindex', selected ? '0' : '-1');
 panelEls[i].hidden = !selected;
 });
 };

 tabs.forEach((tab, i) => {
 const tabId = `tab-${tab.id}`;
 const panelId = `tabpanel-${tab.id}`;

 const tabEl = el('button', {
 className: 'tabs__tab',
 id: tabId,
 attrs: {
 type: 'button',
 role: 'tab',
 'aria-selected': 'false',
 'aria-controls': panelId,
 tabindex: '-1'
 },
 text: tab.label,
 on: { click: () => activate(i) }
 });

 const panelEl = el('div', {
 className: 'tabs__panel',
 id: panelId,
 attrs: { role: 'tabpanel', 'aria-labelledby': tabId, tabindex: '0' }
 }, [tab.render()]);

 panelEl.hidden = true;

 tabEls.push(tabEl);
 panelEls.push(panelEl);
 list.append(tabEl);
 panels.append(panelEl);
 });

 /* Left/right arrow navigation, per the WAI-ARIA tabs pattern */
 list.addEventListener('keydown', (e) => {
 const current = tabEls.indexOf(document.activeElement);
 if (current === -1) return;

 let next = null;
 if (e.key === 'ArrowRight') next = (current + 1) % tabEls.length;
 if (e.key === 'ArrowLeft') next = (current - 1 + tabEls.length) % tabEls.length;
 if (e.key === 'Home') next = 0;
 if (e.key === 'End') next = tabEls.length - 1;

 if (next !== null) {
 e.preventDefault();
 tabEls[next].focus();
 activate(next);
 }
 });

 root.append(list, panels);
 activate(activeIndex);
 return root;
}

/* ============================================
 TOASTS
 ============================================ */

/**
 * Show a toast notification.
 * @param {Object} o
 * @param {'success'|'error'|'warning'|'info'} [o.type]
 * @param {string} o.title
 * @param {string} [o.message]
 * @param {number} [o.duration]
 */
function toast({ type = 'info', title, message = '', duration = window.CONFIG.toastDurationMs }) {
 let region = document.getElementById('toast-region');

 if (!region) {
 region = el('div', {
 id: 'toast-region',
 className: 'toast-region',
 attrs: { role: 'status', 'aria-live': 'polite', 'aria-atomic': 'false' }
 });
 document.body.append(region);
 }

 const icons = { success: '✓', error: '✕', warning: '!', info: 'i' };

 const node = el('div', { className: `toast toast--${type}` }, [
 el('span', { className: 'toast__icon', text: icons[type], attrs: { 'aria-hidden': 'true' } }),
 el('div', { className: 'toast__body' }, [
 el('div', { className: 'toast__title', text: title }),
 message ? el('div', { className: 'toast__message', text: message }) : null
 ]),
 el('button', {
 className: 'toast__close',
 attrs: { type: 'button', 'aria-label': 'Dismiss notification' },
 html: ICONS.close,
 on: { click: () => dismiss() }
 }),
 el('div', {
 className: 'toast__progress',
 style: { animationDuration: `${duration}ms` },
 attrs: { 'aria-hidden': 'true' }
 })
 ]);

 let timer;
 const dismiss = () => {
 clearTimeout(timer);
 node.classList.add('is-leaving');
 node.addEventListener('animationend', () => node.remove(), { once: true });
 };

 region.append(node);
 timer = setTimeout(dismiss, duration);

 /* Pause the countdown while hovered, respects Success Criterion 2.2.1 */
 node.addEventListener('mouseenter', () => clearTimeout(timer));
 node.addEventListener('mouseleave', () => {
 timer = setTimeout(dismiss, 1500);
 });

 return node;
}

/* ============================================
 FAVORITES (localStorage)
 ============================================ */

const Favorites = {
 /** @returns {number[]} */
 all() {
 try {
 const raw = localStorage.getItem(window.CONFIG.storageKeys.favorites);
 const parsed = raw ? JSON.parse(raw) : [];
 return Array.isArray(parsed) ? parsed : [];
 } catch {
 return [];
 }
 },

 has(id) {
 return this.all().includes(Number(id));
 },

 /** @returns {boolean} the new state */
 toggle(id) {
 const numId = Number(id);
 const list = this.all();
 const index = list.indexOf(numId);

 if (index === -1) list.push(numId);
 else list.splice(index, 1);

 try {
 localStorage.setItem(window.CONFIG.storageKeys.favorites, JSON.stringify(list));
 } catch {
 /* storage unavailable */
 }

 document.dispatchEvent(new CustomEvent('favoriteschange', { detail: { favorites: list } }));
 return index === -1;
 }
};

/* ============================================
 UTILITIES shared by tool pages
 ============================================ */

/**
 * Copy text to the clipboard with a graceful fallback for
 * insecure contexts, then confirm via toast.
 * @param {string} text
 * @param {string} [label]
 * @returns {Promise<boolean>}
 */
async function copyToClipboard(text, label = 'Copied to clipboard') {
 if (!text) {
 toast({ type: 'warning', title: 'Nothing to copy', message: 'Generate a result first.' });
 return false;
 }

 try {
 if (navigator.clipboard && window.isSecureContext) {
 await navigator.clipboard.writeText(text);
 } else {
 // file:// and http:// origins don't get the async Clipboard API
 const ta = el('textarea', { attrs: { readonly: true } });
 ta.value = text;
 ta.style.cssText = 'position:fixed;top:-1000px;opacity:0';
 document.body.append(ta);
 ta.select();
 document.execCommand('copy');
 ta.remove();
 }

 toast({ type: 'success', title: label });
 return true;
 } catch {
 toast({ type: 'error', title: 'Copy failed', message: 'Select the text and copy manually.' });
 return false;
 }
}

/**
 * Trigger a client-side file download.
 * @param {string|Blob} content
 * @param {string} filename
 * @param {string} [mime]
 */
function downloadFile(content, filename, mime = 'text/plain;charset=utf-8') {
 const blob = content instanceof Blob ? content : new Blob([content], { type: mime });
 const url = URL.createObjectURL(blob);

 const link = el('a', { attrs: { href: url, download: filename } });
 document.body.append(link);
 link.click();
 link.remove();

 // Revoke on the next tick so Safari has time to start the download
 setTimeout(() => URL.revokeObjectURL(url), 1000);
 toast({ type: 'success', title: 'Download started', message: filename });
}

/**
 * Share via the Web Share API, falling back to copying the URL.
 * @param {{title?: string, text?: string, url?: string}} data
 */
async function shareLink(data = {}) {
 const payload = {
 title: data.title || document.title,
 text: data.text || '',
 url: data.url || window.location.href
 };

 if (navigator.share) {
 try {
 await navigator.share(payload);
 return;
 } catch (err) {
 if (err && err.name === 'AbortError') return; // user cancelled, not an error
 }
 }

 copyToClipboard(payload.url, 'Link copied to clipboard');
}

/**
 * Format a large number compactly (184200 → "184.2K").
 * @param {number} n
 * @returns {string}
 */
function formatCount(n) {
 if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
 if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
 return String(n);
}

/**
 * Trailing-edge debounce.
 * @param {Function} fn
 * @param {number} wait
 * @returns {Function}
 */
function debounce(fn, wait = 200) {
 let timer;
 return function debounced(...args) {
 clearTimeout(timer);
 timer = setTimeout(() => fn.apply(this, args), wait);
 };
}

/**
 * rAF-throttle, for scroll and pointermove handlers.
 * @param {Function} fn
 * @returns {Function}
 */
function rafThrottle(fn) {
 let queued = false;
 return function throttled(...args) {
 if (queued) return;
 queued = true;
 requestAnimationFrame(() => {
 queued = false;
 fn.apply(this, args);
 });
 };
}

/**
 * Trap Tab focus inside a container while a modal is open.
 * @param {HTMLElement} container
 * @returns {Function} cleanup
 */
function trapFocus(container) {
 const selector =
 'a[href], button:not([disabled]), input:not([disabled]), select, textarea, [tabindex]:not([tabindex="-1"])';

 const handler = (e) => {
 if (e.key !== 'Tab') return;

 const focusable = Array.from(container.querySelectorAll(selector)).filter(
 (node) => node.offsetParent !== null
 );
 if (!focusable.length) return;

 const first = focusable[0];
 const last = focusable[focusable.length - 1];

 if (e.shiftKey && document.activeElement === first) {
 e.preventDefault();
 last.focus();
 } else if (!e.shiftKey && document.activeElement === last) {
 e.preventDefault();
 first.focus();
 }
 };

 container.addEventListener('keydown', handler);
 return () => container.removeEventListener('keydown', handler);
}

/* Expose the public surface */
Object.assign(window, {
 el,
 ICONS,
 createButton,
 createToolCard,
 createCategoryCard,
 createCategoryChip,
 createFeatureCard,
 createTestimonial,
 createAccordion,
 createTabs,
 toast,
 Favorites,
 copyToClipboard,
 downloadFile,
 shareLink,
 formatCount,
 debounce,
 rafThrottle,
 trapFocus
});
