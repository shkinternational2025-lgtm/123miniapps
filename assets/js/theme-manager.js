/* ============================================
 123MiniApps.online v2.0
 File: theme-manager.js
 Purpose: Switching, persisting and broadcasting
 the active theme across all 9 options.
 ============================================ */

/**
 * Owns everything about the active theme: detection on first
 * visit, persistence, the 500ms cross-fade, the floating
 * switcher panel, and the `themechange` event other modules
 * can subscribe to.
 */
class ThemeManager {
 /** @param {Object} config - window.CONFIG */
 constructor(config) {
 this.config = config;
 this.themes = config.themes;
 this.storageKey = config.storageKeys.theme;
 this.current = null;
 this.panel = null;
 this.fab = null;
 this._transitionTimer = null;
 }

 /**
 * Resolve and apply the starting theme, then wire up the UI.
 * Safe to call before DOMContentLoaded, UI wiring is deferred.
 */
 init() {
 this.apply(this.resolveInitialTheme(), { animate: false });

 if (document.readyState === 'loading') {
 document.addEventListener('DOMContentLoaded', () => this.mountUI(), { once: true });
 } else {
 this.mountUI();
 }

 this.watchSystemPreference();
 }

 /**
 * Decide which theme to start with:
 * saved choice → system light/dark preference → configured default.
 * @returns {string} theme id
 */
 resolveInitialTheme() {
 // An explicit saved choice always wins.
 const saved = this.read(this.storageKey);
 if (saved && this.isValid(saved)) return saved;

 // Otherwise use the branded default (Indigo Nova) so first-time visitors
 // get the signature dark look rather than a light theme picked from their
 // OS setting. They can still switch to any theme, and that choice sticks.
 return this.config.defaultTheme;
 }

 /**
 * @param {string} id
 * @returns {boolean} whether id names a known theme
 */
 isValid(id) {
 return this.themes.some((t) => t.id === id);
 }

 /**
 * Apply a theme to the document.
 * @param {string} id - theme id
 * @param {{animate?: boolean, persist?: boolean}} [options]
 */
 apply(id, options = {}) {
 const { animate = true, persist = true } = options;
 if (!this.isValid(id) || id === this.current) {
 if (id === this.current) return;
 }

 const theme = this.themes.find((t) => t.id === id) || this.themes[0];
 const root = document.documentElement;

 if (animate && !this.prefersReducedMotion()) {
 root.classList.add('theme-transitioning');
 clearTimeout(this._transitionTimer);
 this._transitionTimer = setTimeout(() => {
 root.classList.remove('theme-transitioning');
 }, 520);
 }

 root.setAttribute('data-theme', theme.id);
 this.current = theme.id;

 this.syncMetaThemeColor(theme.color);
 if (persist) this.write(this.storageKey, theme.id);

 this.refreshPanelState();

 document.dispatchEvent(
 new CustomEvent('themechange', { detail: { theme } })
 );
 }

 /** Keep the browser chrome color in step with the theme. */
 syncMetaThemeColor(color) {
 let meta = document.querySelector('meta[name="theme-color"]');
 if (!meta) {
 meta = document.createElement('meta');
 meta.name = 'theme-color';
 document.head.appendChild(meta);
 }
 meta.content = color;
 }

 /**
 * Follow the OS light/dark setting, but only for visitors who
 * have never made an explicit choice.
 */
 watchSystemPreference() {
 const mq = window.matchMedia('(prefers-color-scheme: light)');
 const handler = (e) => {
 if (this.read(this.storageKey)) return; // user has chosen; don't override
 const pool = this.themes.filter((t) => t.type === (e.matches ? 'light' : 'dark'));
 if (pool.length) this.apply(pool[0].id, { persist: false });
 };

 if (mq.addEventListener) mq.addEventListener('change', handler);
 else if (mq.addListener) mq.addListener(handler);
 }

 /* ------------------------------------------
 UI: floating button + panel
 ------------------------------------------ */

 /** Build and attach the switcher FAB and panel. */
 mountUI() {
 this.fab = document.getElementById('theme-fab');
 this.panel = document.getElementById('theme-panel');
 if (!this.fab || !this.panel) return;

 this.renderSwatches();

 this.fab.addEventListener('click', () => this.togglePanel());

 // Close on outside click
 document.addEventListener('click', (e) => {
 if (!this.panel.classList.contains('is-open')) return;
 if (this.panel.contains(e.target) || this.fab.contains(e.target)) return;
 this.closePanel();
 });

 // Close on Escape, returning focus to the trigger
 document.addEventListener('keydown', (e) => {
 if (e.key === 'Escape' && this.panel.classList.contains('is-open')) {
 this.closePanel();
 this.fab.focus();
 }
 });

 // Arrow-key roving focus inside the 3x3 grid
 this.panel.addEventListener('keydown', (e) => this.handleGridKeys(e));
 }

 /** Render the 9 preview swatches into the panel grid. */
 renderSwatches() {
 const grid = this.panel.querySelector('.theme-panel__grid');
 if (!grid) return;

 grid.innerHTML = '';

 this.themes.forEach((theme) => {
 const btn = document.createElement('button');
 btn.type = 'button';
 btn.className = 'theme-swatch';
 btn.setAttribute('role', 'radio');
 btn.setAttribute('aria-checked', String(theme.id === this.current));
 btn.setAttribute('aria-label', `${theme.name} theme (${theme.type})`);
 btn.dataset.themeId = theme.id;
 btn.title = theme.name;

 btn.innerHTML = `
 <span class="theme-swatch__dot" data-preview="${theme.id}">
 <span class="theme-swatch__check" aria-hidden="true">✓</span>
 </span>
 <span class="theme-swatch__label">${theme.name}</span>
 `;

 btn.addEventListener('click', () => {
 this.apply(theme.id);
 if (window.toast) {
 window.toast({
 type: 'success',
 title: theme.name,
 message: 'Theme applied.'
 });
 }
 });

 grid.appendChild(btn);
 });
 }

 /** Update aria-checked on every swatch after a theme change. */
 refreshPanelState() {
 if (!this.panel) return;
 this.panel.querySelectorAll('.theme-swatch').forEach((el) => {
 el.setAttribute('aria-checked', String(el.dataset.themeId === this.current));
 });
 }

 /**
 * Roving arrow-key navigation across the swatch grid (3 columns).
 * @param {KeyboardEvent} e
 */
 handleGridKeys(e) {
 const keys = ['ArrowRight', 'ArrowLeft', 'ArrowDown', 'ArrowUp'];
 if (!keys.includes(e.key)) return;

 const items = Array.from(this.panel.querySelectorAll('.theme-swatch'));
 const index = items.indexOf(document.activeElement);
 if (index === -1) return;

 e.preventDefault();
 const cols = 3;
 let next = index;

 if (e.key === 'ArrowRight') next = (index + 1) % items.length;
 if (e.key === 'ArrowLeft') next = (index - 1 + items.length) % items.length;
 if (e.key === 'ArrowDown') next = (index + cols) % items.length;
 if (e.key === 'ArrowUp') next = (index - cols + items.length) % items.length;

 items[next].focus();
 }

 togglePanel() {
 this.panel.classList.contains('is-open') ? this.closePanel() : this.openPanel();
 }

 openPanel() {
 this.panel.classList.add('is-open');
 this.panel.removeAttribute('inert');
 this.fab.setAttribute('aria-expanded', 'true');
 const active = this.panel.querySelector('[aria-checked="true"]') ||
 this.panel.querySelector('.theme-swatch');
 if (active) active.focus();
 }

 closePanel() {
 this.panel.classList.remove('is-open');
 this.panel.setAttribute('inert', '');
 this.fab.setAttribute('aria-expanded', 'false');
 }

 /* ------------------------------------------
 Utilities
 ------------------------------------------ */

 prefersReducedMotion() {
 return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 }

 /**
 * localStorage can throw in private mode or when disabled, 
 * never let a storage failure break the page.
 */
 read(key) {
 try {
 return localStorage.getItem(key);
 } catch {
 return null;
 }
 }

 write(key, value) {
 try {
 localStorage.setItem(key, value);
 } catch {
 /* storage unavailable, theme still applies for this session */
 }
 }
}

window.ThemeManager = ThemeManager;

/* Instantiate immediately so the correct theme is on <html>
 before first paint, avoiding a flash of the default theme. */
window.themeManager = new ThemeManager(window.CONFIG);
window.themeManager.init();
