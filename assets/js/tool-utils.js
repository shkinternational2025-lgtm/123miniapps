/* ============================================
 123MiniApps.online v2.0
 File: tool-utils.js
 Purpose: Helpers shared by every tool page.

 Loaded after components.js, so it can rely on
 el(), toast(), copyToClipboard(), downloadFile()
 and shareLink() already existing.
 ============================================ */

const T = (() => {
 'use strict';

 /* ============================================
 DOM
 ============================================ */

 /** @returns {HTMLElement} */
 const $ = (id) => document.getElementById(id);

 /** @returns {HTMLElement[]} */
 const $$ = (sel, scope = document) => Array.from(scope.querySelectorAll(sel));

 /**
 * Write a status line with semantic coloring.
 * @param {string|HTMLElement} target - element or its id
 * @param {string} message
 * @param {'ok'|'error'|'warn'|'muted'} [kind]
 */
 function status(target, message, kind = 'muted') {
 const node = typeof target === 'string' ? $(target) : target;
 if (!node) return;
 node.textContent = message;
 node.style.color = {
 ok: 'var(--success)',
 error: 'var(--danger)',
 warn: 'var(--warning)',
 muted: 'var(--text-muted)'
 }[kind] || 'var(--text-muted)';
 }

 /**
 * Render into an output box, toggling the empty state.
 * @param {string} id
 * @param {string} text
 * @param {string} [emptyMessage]
 */
 function setOutput(id, text, emptyMessage = 'Result will appear here.') {
 const node = $(id);
 if (!node) return;
 const has = text !== '' && text != null;
 node.textContent = has ? text : emptyMessage;
 node.classList.toggle('output--empty', !has);
 }

 /**
 * Render trusted HTML into an output box.
 * Callers are responsible for escaping any user data first, 
 * use T.esc() for that.
 */
 function setOutputHTML(id, html, emptyMessage = 'Result will appear here.') {
 const node = $(id);
 if (!node) return;
 const has = Boolean(html);
 node.innerHTML = has ? html : esc(emptyMessage);
 node.classList.toggle('output--empty', !has);
 }

 /** Escape HTML-significant characters. */
 const esc = (s) =>
 String(s).replace(/[&<>"']/g, (c) => ({
 '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
 }[c]));

 /* ============================================
 Events
 ============================================ */

 /**
 * Attach the same handler to many controls at once.
 * @param {string[]} ids
 * @param {Function} handler
 * @param {string} [event]
 */
 function on(ids, handler, event = 'input') {
 ids.forEach((id) => {
 const node = $(id);
 if (node) node.addEventListener(event, handler);
 });
 }

 /**
 * Wire the standard Copy / Download / Share button trio.
 * @param {Object} o
 * @param {string} o.slug - tool slug, for local usage counting
 * @param {() => string} o.getResult - returns the current result text
 * @param {string} [o.filename]
 * @param {string} [o.mime]
 * @param {string} [o.name] - display name for the share sheet
 */
 function wireActions({ slug, getResult, filename = 'output.txt', mime = 'text/plain;charset=utf-8', name = document.title }) {
 const copy = $('copy');
 const dl = $('download');
 const share = $('share');

 if (copy) {
 copy.addEventListener('click', () => copyToClipboard(getResult(), 'Result copied'));
 }

 if (dl) {
 dl.addEventListener('click', () => {
 const result = getResult();
 if (!result) {
 toast({ type: 'warning', title: 'Nothing to download', message: 'Produce a result first.' });
 return;
 }
 downloadFile(result, filename, mime);
 });
 }

 if (share) {
 share.addEventListener('click', () => shareLink({ title: name }));
 }

 if (slug && window.Analytics) Analytics.trackToolUse(slug);
 }

 /**
 * Wire the static FAQ accordion on tool pages.
 *
 * Unlike the homepage FAQ, this markup is rendered at build time
 * rather than by createAccordion(), it has to be in the HTML source
 * so that Google can match it against the FAQPage structured data.
 * That means it ships without event handlers, so attach them here.
 */
 function initFaq() {
 const root = $('tool-faq');
 if (!root) return;

 $$('.accordion__trigger', root).forEach((trigger) => {
 trigger.addEventListener('click', () => {
 const item = trigger.closest('.accordion__item');
 const isOpen = item.classList.contains('is-open');

 // One open at a time keeps the page from growing unmanageably
 $$('.accordion__item.is-open', root).forEach((openItem) => {
 openItem.classList.remove('is-open');
 openItem.querySelector('.accordion__trigger').setAttribute('aria-expanded', 'false');
 });

 item.classList.toggle('is-open', !isOpen);
 trigger.setAttribute('aria-expanded', String(!isOpen));
 });
 });
 }

 /**
 * Render the "related tools" strip at the bottom of a tool page.
 * @param {string} slug
 */
 function related(slug) {
 const mount = $('related');
 const tool = window.getToolBySlug && window.getToolBySlug(slug);
 if (!mount || !tool) return;
 window.getRelatedTools(tool, 4).forEach((t) => {
 mount.append(createToolCard({ tool: t, base: '../' }));
 });
 }

 /* ============================================
 Numbers
 ============================================ */

 /** Parse a user-entered number, returning NaN for blanks. */
 const num = (v) => {
 const s = String(v).trim().replace(/,/g, '');
 return s === '' ? NaN : Number(s);
 };

 const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));

 /**
 * Round to a set number of decimals without floating-point noise.
 * @param {number} n
 * @param {number} [places]
 */
 function round(n, places = 2) {
 const f = Math.pow(10, places);
 return Math.round((n + Number.EPSILON) * f) / f;
 }

 /** Format a number with thousands separators. */
 const fmt = (n, places = 2) =>
 Number(n).toLocaleString(undefined, {
 minimumFractionDigits: places,
 maximumFractionDigits: places
 });

 /** Format as currency without assuming a locale's symbol placement. */
 const money = (n, currency = 'USD') => {
 try {
 return Number(n).toLocaleString(undefined, { style: 'currency', currency });
 } catch {
 return fmt(n, 2);
 }
 };

 /* ============================================
 Randomness (CSPRNG-backed)
 ============================================ */

 /**
 * Uniform random integer in [0, max). Rejection-sampled to remove
 * the modulo bias a plain `% max` would introduce.
 */
 function randomBelow(max) {
 if (max <= 0) return 0;
 const limit = Math.floor(0xffffffff / max) * max;
 const buf = new Uint32Array(1);
 let v;
 do {
 crypto.getRandomValues(buf);
 v = buf[0];
 } while (v >= limit);
 return v % max;
 }

 /** Random integer in [min, max] inclusive. */
 const randomInt = (min, max) => min + randomBelow(max - min + 1);

 /** Pick one random element. */
 const pick = (arr) => arr[randomBelow(arr.length)];

 /** Fisher-Yates shuffle, in place. */
 function shuffle(arr) {
 for (let i = arr.length - 1; i > 0; i--) {
 const j = randomBelow(i + 1);
 [arr[i], arr[j]] = [arr[j], arr[i]];
 }
 return arr;
 }

 /* ============================================
 Colour
 ============================================ */

 function hexToRgb(hex) {
 let h = String(hex).trim().replace(/^#/, '');
 if (h.length === 3) h = h.split('').map((c) => c + c).join('');
 if (!/^[0-9a-f]{6}$/i.test(h)) return null;
 return {
 r: parseInt(h.slice(0, 2), 16),
 g: parseInt(h.slice(2, 4), 16),
 b: parseInt(h.slice(4, 6), 16)
 };
 }

 function rgbToHex(r, g, b) {
 const c = (n) => clamp(Math.round(n), 0, 255).toString(16).padStart(2, '0');
 return ('#' + c(r) + c(g) + c(b)).toUpperCase();
 }

 function rgbToHsl(r, g, b) {
 r /= 255; g /= 255; b /= 255;
 const max = Math.max(r, g, b), min = Math.min(r, g, b), d = max - min;
 let h = 0;
 if (d) {
 if (max === r) h = ((g - b) / d) % 6;
 else if (max === g) h = (b - r) / d + 2;
 else h = (r - g) / d + 4;
 h = (h * 60 + 360) % 360;
 }
 const l = (max + min) / 2;
 const s = d === 0 ? 0 : d / (1 - Math.abs(2 * l - 1));
 return { h: Math.round(h), s: Math.round(s * 100), l: Math.round(l * 100) };
 }

 function hslToRgb(h, s, l) {
 h = ((h % 360) + 360) % 360; s /= 100; l /= 100;
 const c = (1 - Math.abs(2 * l - 1)) * s;
 const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
 const m = l - c / 2;
 const seg = [[c,x,0],[x,c,0],[0,c,x],[0,x,c],[x,0,c],[c,0,x]][Math.floor(h / 60) % 6];
 return { r: (seg[0]+m)*255, g: (seg[1]+m)*255, b: (seg[2]+m)*255 };
 }

 /** WCAG relative luminance. */
 function luminance(rgb) {
 const ch = (c) => {
 const s = c / 255;
 return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
 };
 return 0.2126 * ch(rgb.r) + 0.7152 * ch(rgb.g) + 0.0722 * ch(rgb.b);
 }

 /** WCAG contrast ratio between two rgb objects, 1-21. */
 function contrast(a, b) {
 const l1 = luminance(a), l2 = luminance(b);
 return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
 }

 /* ============================================
 Files and images
 ============================================ */

 /**
 * Open a file picker and resolve with the chosen File.
 * @param {string} [accept]
 * @returns {Promise<File|null>}
 */
 function pickFile(accept = '*/*') {
 return new Promise((resolve) => {
 const input = document.createElement('input');
 input.type = 'file';
 input.accept = accept;
 input.addEventListener('change', () => resolve(input.files[0] || null), { once: true });
 input.click();
 });
 }

 /** @returns {Promise<string>} data URL */
 function readAsDataURL(file) {
 return new Promise((resolve, reject) => {
 const r = new FileReader();
 r.onload = () => resolve(String(r.result));
 r.onerror = () => reject(new Error('Could not read that file.'));
 r.readAsDataURL(file);
 });
 }

 /** @returns {Promise<string>} text */
 function readAsText(file) {
 return new Promise((resolve, reject) => {
 const r = new FileReader();
 r.onload = () => resolve(String(r.result));
 r.onerror = () => reject(new Error('Could not read that file.'));
 r.readAsText(file);
 });
 }

 /** @returns {Promise<HTMLImageElement>} */
 function loadImage(src) {
 return new Promise((resolve, reject) => {
 const img = new Image();
 img.onload = () => resolve(img);
 img.onerror = () => reject(new Error('Could not decode that image.'));
 img.src = src;
 });
 }

 /** Human-readable byte size. */
 function bytes(n) {
 if (n < 1024) return n + ' B';
 const units = ['KB', 'MB', 'GB'];
 let i = -1;
 do { n /= 1024; i++; } while (n >= 1024 && i < units.length - 1);
 return n.toFixed(n < 10 ? 1 : 0) + ' ' + units[i];
 }

 /**
 * Wire a drag-and-drop + click-to-browse dropzone.
 * @param {string} zoneId
 * @param {(file: File) => void} onFile
 * @param {string} [accept]
 */
 function dropzone(zoneId, onFile, accept = 'image/*') {
 const zone = $(zoneId);
 if (!zone) return;

 const handle = (file) => {
 if (!file) return;
 if (accept.startsWith('image/') && !file.type.startsWith('image/')) {
 toast({ type: 'error', title: 'Not an image', message: 'Choose a PNG, JPG, WebP or GIF.' });
 return;
 }
 onFile(file);
 };

 zone.addEventListener('click', async () => handle(await pickFile(accept)));

 zone.addEventListener('keydown', async (e) => {
 if (e.key === 'Enter' || e.key === ' ') {
 e.preventDefault();
 handle(await pickFile(accept));
 }
 });

 ['dragenter', 'dragover'].forEach((ev) =>
 zone.addEventListener(ev, (e) => {
 e.preventDefault();
 zone.classList.add('is-dragover');
 })
 );

 ['dragleave', 'drop'].forEach((ev) =>
 zone.addEventListener(ev, (e) => {
 e.preventDefault();
 zone.classList.remove('is-dragover');
 })
 );

 zone.addEventListener('drop', (e) => handle(e.dataTransfer.files[0]));
 }

 /* ============================================
 Persistence, namespaced, failure-tolerant
 ============================================ */

 const store = {
 get(key, fallback = null) {
 try {
 const raw = localStorage.getItem('123ma:' + key);
 return raw === null ? fallback : JSON.parse(raw);
 } catch {
 return fallback;
 }
 },
 set(key, value) {
 try {
 localStorage.setItem('123ma:' + key, JSON.stringify(value));
 return true;
 } catch {
 return false;
 }
 },
 remove(key) {
 try { localStorage.removeItem('123ma:' + key); } catch { /* no-op */ }
 }
 };

 /* ============================================
 Text
 ============================================ */

 /** Split into words, Unicode-aware enough for Latin scripts. */
 const words = (s) => (String(s).trim().match(/[\p{L}\p{N}'’-]+/gu) || []);

 /** Split into sentences on terminal punctuation. */
 const sentences = (s) =>
 String(s).split(/[.!?…]+[\s"')\]]*/u).map((x) => x.trim()).filter(Boolean);

 /** Approximate syllable count, used by the readability scores. */
 function syllables(word) {
 const w = String(word).toLowerCase().replace(/[^a-z]/g, '');
 if (!w) return 0;
 if (w.length <= 3) return 1;
 const trimmed = w
 .replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/, '')
 .replace(/^y/, '');
 const groups = trimmed.match(/[aeiouy]{1,2}/g);
 return Math.max(1, groups ? groups.length : 1);
 }

 const titleCase = (s) =>
 String(s).replace(/\w\S*/g, (t) => t[0].toUpperCase() + t.slice(1).toLowerCase());

 /** Convert a string to a URL-safe slug. */
 const slugify = (s, sep = '-') =>
 String(s)
 .normalize('NFD')
 .replace(/[\u0300-\u036f]/g, '')
 .toLowerCase()
 .replace(/[^a-z0-9]+/g, sep)
 .replace(new RegExp(`^${sep}+|${sep}+$`, 'g'), '');

 /* ============================================
 Dates
 ============================================ */

 const pad2 = (n) => String(n).padStart(2, '0');

 /** Seconds → H:MM:SS (or M:SS under an hour). */
 function duration(totalSeconds) {
 const s = Math.max(0, Math.floor(totalSeconds));
 const h = Math.floor(s / 3600);
 const m = Math.floor((s % 3600) / 60);
 const sec = s % 60;
 return h ? `${h}:${pad2(m)}:${pad2(sec)}` : `${m}:${pad2(sec)}`;
 }

 /** Build a table element from headers and rows. */
 function table(headers, rows) {
 const t = el('table', { className: 'data-table' });
 const thead = el('thead');
 const hr = el('tr');
 headers.forEach((h) => hr.append(el('th', { text: h })));
 thead.append(hr);

 const tbody = el('tbody');
 rows.forEach((row) => {
 const tr = el('tr');
 row.forEach((cell) => tr.append(el('td', { text: String(cell) })));
 tbody.append(tr);
 });

 t.append(thead, tbody);
 return t;
 }

 return {
 $, $$, status, setOutput, setOutputHTML, esc, on, wireActions, related, initFaq,
 num, clamp, round, fmt, money,
 randomBelow, randomInt, pick, shuffle,
 hexToRgb, rgbToHex, rgbToHsl, hslToRgb, luminance, contrast,
 pickFile, readAsDataURL, readAsText, loadImage, bytes, dropzone,
 store,
 words, sentences, syllables, titleCase, slugify,
 pad2, duration, table
 };
})();

window.T = T;

// Every tool page carries a build-time FAQ accordion, so wire it once
// here rather than in each of the 95 tool scripts.
if (document.readyState === 'loading') {
 document.addEventListener('DOMContentLoaded', () => T.initFaq(), { once: true });
} else {
 T.initFaq();
}
