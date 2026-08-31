/* ============================================
 123MiniApps.online v2.0
 File: animations.js
 Purpose: Scroll reveal, hero particle field,
 pointer parallax, count-up stats,
 typewriter, all reduced-motion aware.
 ============================================ */

const Motion = {
 /** @returns {boolean} */
 get reduced() {
 return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 }
};

/* ============================================
 1. SCROLL REVEAL
 ============================================ */

/**
 * Reveal [data-animate] elements as they enter the viewport.
 * Each element is unobserved after firing, so the observer's
 * work shrinks to zero as the user scrolls.
 */
function initScrollReveal() {
 const targets = document.querySelectorAll('[data-animate]');
 if (!targets.length) return;

 if (Motion.reduced || !('IntersectionObserver' in window)) {
 targets.forEach((node) => node.classList.add('is-visible'));
 return;
 }

 const observer = new IntersectionObserver(
 (entries) => {
 entries.forEach((entry) => {
 if (!entry.isIntersecting) return;
 entry.target.classList.add('is-visible');
 observer.unobserve(entry.target);
 });
 },
 { rootMargin: '0px 0px -12% 0px', threshold: 0.08 }
 );

 targets.forEach((node) => observer.observe(node));
}

/* ============================================
 2. COUNT-UP STATS
 ============================================ */

/**
 * Animate [data-count-to] numbers from 0 to their target the
 * first time they scroll into view.
 */
function initCountUp() {
 const counters = document.querySelectorAll('[data-count-to]');
 if (!counters.length) return;

 const render = (node, value) => {
 const suffix = node.dataset.countSuffix || '';
 node.textContent = Math.round(value).toLocaleString() + suffix;
 };

 if (Motion.reduced || !('IntersectionObserver' in window)) {
 counters.forEach((node) => render(node, Number(node.dataset.countTo)));
 return;
 }

 const run = (node) => {
 const target = Number(node.dataset.countTo) || 0;
 const duration = Number(node.dataset.countDuration) || 1400;
 const start = performance.now();

 const step = (now) => {
 const progress = Math.min((now - start) / duration, 1);
 // easeOutExpo, fast start, gentle settle
 const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
 render(node, target * eased);
 if (progress < 1) requestAnimationFrame(step);
 };

 requestAnimationFrame(step);
 };

 const observer = new IntersectionObserver(
 (entries) => {
 entries.forEach((entry) => {
 if (!entry.isIntersecting) return;
 run(entry.target);
 observer.unobserve(entry.target);
 });
 },
 { threshold: 0.5 }
 );

 counters.forEach((node) => observer.observe(node));
}

/* ============================================
 3. TYPEWRITER
 ============================================ */

/**
 * Cycle words in and out of a target element, character by
 * character. Pauses entirely when the tab is hidden so a
 * background tab costs nothing.
 * @param {HTMLElement} node
 * @param {string[]} words
 */
function initTypewriter(node, words) {
 if (!node || !words || !words.length) return;

 if (Motion.reduced) {
 node.textContent = words[0];
 return;
 }

 let wordIndex = 0;
 let charIndex = 0;
 let deleting = false;
 let timer = null;

 const tick = () => {
 if (document.hidden) {
 timer = setTimeout(tick, 500);
 return;
 }

 const word = words[wordIndex];
 charIndex += deleting ? -1 : 1;
 node.textContent = word.slice(0, charIndex);

 let delay = deleting ? 45 : 85;

 if (!deleting && charIndex === word.length) {
 delay = 1600;
 deleting = true;
 } else if (deleting && charIndex === 0) {
 deleting = false;
 wordIndex = (wordIndex + 1) % words.length;
 delay = 350;
 }

 timer = setTimeout(tick, delay);
 };

 tick();

 // Clean up if the element ever leaves the DOM
 return () => clearTimeout(timer);
}

/* ============================================
 4. HERO PARTICLES
 ============================================ */

/**
 * A lightweight canvas particle field. Sized to devicePixelRatio,
 * capped at 60fps, and fully torn down when scrolled out of view
 * so it never burns battery below the fold.
 * @param {HTMLCanvasElement} canvas
 */
function initParticles(canvas) {
 if (!canvas) return;
 if (Motion.reduced || !window.CONFIG.performance.enableParticles) return;

 const ctx = canvas.getContext('2d', { alpha: true });
 if (!ctx) return;

 const count = window.CONFIG.performance.particleCount;
 const particles = [];
 let width = 0;
 let height = 0;
 let dpr = 1;
 let rafId = null;
 let running = false;

 const readAccent = () =>
 getComputedStyle(document.documentElement).getPropertyValue('--accent-primary').trim() || '#00d4ff';

 let accent = readAccent();

 const resize = () => {
 dpr = Math.min(window.devicePixelRatio || 1, 2);
 const rect = canvas.getBoundingClientRect();
 width = rect.width;
 height = rect.height;
 canvas.width = Math.floor(width * dpr);
 canvas.height = Math.floor(height * dpr);
 ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
 };

 const seed = () => {
 particles.length = 0;
 for (let i = 0; i < count; i++) {
 particles.push({
 x: Math.random() * width,
 y: Math.random() * height,
 r: Math.random() * 1.8 + 0.6,
 vx: (Math.random() - 0.5) * 0.22,
 vy: (Math.random() - 0.5) * 0.22,
 a: Math.random() * 0.4 + 0.15
 });
 }
 };

 const draw = () => {
 ctx.clearRect(0, 0, width, height);
 ctx.fillStyle = accent;

 for (const p of particles) {
 p.x += p.vx;
 p.y += p.vy;

 // Wrap at the edges rather than bouncing, reads as a drifting field
 if (p.x < -5) p.x = width + 5;
 if (p.x > width + 5) p.x = -5;
 if (p.y < -5) p.y = height + 5;
 if (p.y > height + 5) p.y = -5;

 ctx.globalAlpha = p.a;
 ctx.beginPath();
 ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
 ctx.fill();
 }

 ctx.globalAlpha = 1;
 rafId = requestAnimationFrame(draw);
 };

 const start = () => {
 if (running) return;
 running = true;
 draw();
 };

 const stop = () => {
 running = false;
 if (rafId) cancelAnimationFrame(rafId);
 rafId = null;
 };

 resize();
 seed();
 start();

 window.addEventListener('resize', debounce(() => {
 resize();
 seed();
 }, 200), { passive: true });

 // Stop drawing once the hero scrolls away
 if ('IntersectionObserver' in window) {
 new IntersectionObserver((entries) => {
 entries[0].isIntersecting ? start() : stop();
 }, { threshold: 0 }).observe(canvas);
 }

 document.addEventListener('visibilitychange', () => {
 document.hidden ? stop() : start();
 });

 // Recolor when the theme changes
 document.addEventListener('themechange', () => {
 accent = readAccent();
 });
}

/* ============================================
 5. POINTER PARALLAX
 ============================================ */

/**
 * Nudge the hero's floating cards toward the pointer. Values are
 * written to CSS custom properties so the actual transform stays
 * declarative in CSS and stays on the compositor.
 * @param {HTMLElement} scope
 */
function initParallax(scope) {
 if (!scope) return;
 if (Motion.reduced || !window.CONFIG.performance.enableParallax) return;
 if (!window.matchMedia('(pointer: fine)').matches) return; // skip on touch

 const cards = scope.querySelectorAll('.hero__card');
 if (!cards.length) return;

 const onMove = rafThrottle((e) => {
 const rect = scope.getBoundingClientRect();
 const px = ((e.clientX - rect.left) / rect.width - 0.5) * 24;
 const py = ((e.clientY - rect.top) / rect.height - 0.5) * 24;

 cards.forEach((card) => {
 card.style.setProperty('--px', px.toFixed(2));
 card.style.setProperty('--py', py.toFixed(2));
 });
 });

 const reset = () => {
 cards.forEach((card) => {
 card.style.setProperty('--px', '0');
 card.style.setProperty('--py', '0');
 });
 };

 scope.addEventListener('pointermove', onMove, { passive: true });
 scope.addEventListener('pointerleave', reset, { passive: true });
}

/* ============================================
 6. READING PROGRESS + BACK TO TOP + NAV SCROLL
 ============================================ */

/** Wire all three scroll-driven UI behaviours to one handler. */
function initScrollUI() {
 const nav = document.querySelector('.nav');
 const progress = document.getElementById('progress-bar');
 const backToTop = document.getElementById('back-to-top');

 const onScroll = rafThrottle(() => {
 const y = window.scrollY;

 if (nav) nav.classList.toggle('is-scrolled', y > window.CONFIG.navScrollThreshold);

 if (progress) {
 const max = document.documentElement.scrollHeight - window.innerHeight;
 const ratio = max > 0 ? Math.min(y / max, 1) : 0;
 progress.style.transform = `scaleX(${ratio})`;
 }

 if (backToTop) {
 backToTop.classList.toggle('is-visible', y > window.CONFIG.backToTopThreshold);
 }
 });

 window.addEventListener('scroll', onScroll, { passive: true });
 onScroll();

 if (backToTop) {
 backToTop.addEventListener('click', () => {
 window.scrollTo({
 top: 0,
 behavior: Motion.reduced ? 'auto' : 'smooth'
 });
 });
 }
}

Object.assign(window, {
 Motion,
 initScrollReveal,
 initCountUp,
 initTypewriter,
 initParticles,
 initParallax,
 initScrollUI
});
