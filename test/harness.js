/* ============================================
   123MiniApps.online v2.0
   File: test/harness.js
   Purpose: Boot a tool page in jsdom and expose it
            for assertions.

   Run a suite with:  node test/run.js [phase]

   IMPORTANT — script execution ordering.

   Two jsdom behaviours bite here:
     1. With runScripts:'dangerously', jsdom executes
        inline <script> blocks during parsing but
        cannot fetch local src= files — so page code
        runs before its libraries exist.
     2. jsdom fires its OWN DOMContentLoaded on a
        later tick, regardless of runScripts mode.

   So: jsdom executes nothing ('outside-only'), we
   eval externals then inlines ourselves — which
   registers the page's DOMContentLoaded handler —
   and then we simply wait for jsdom's native
   DOMContentLoaded to fire it. Dispatching one
   manually would double every listener and make each
   button fire twice per click.

   boot() is therefore async.
   ============================================ */

const { JSDOM, VirtualConsole } = require('jsdom');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

/**
 * Load a page and run its scripts.
 * @param {string} relPath - e.g. 'tools/word-counter.html'
 * @returns {Promise<{window: Window, doc: Document, errors: string[], canvasOps: any[]}>}
 */
async function boot(relPath) {
  const errors = [];
  const vc = new VirtualConsole();
  vc.on('jsdomError', (e) => errors.push(e.message));

  const html = fs.readFileSync(path.join(ROOT, relPath), 'utf8');

  const dom = new JSDOM(html, {
    runScripts: 'outside-only',
    virtualConsole: vc,
    url: 'https://www.123miniapps.online/' + relPath.replace(/\\/g, '/'),
    pretendToBeVisual: true
  });

  const { window } = dom;

  /* ---- Stubs for APIs jsdom lacks ---- */
  window.matchMedia = (q) => ({
    matches: false, media: q,
    addEventListener() {}, removeEventListener() {},
    addListener() {}, removeListener() {}
  });
  window.requestAnimationFrame = (cb) => setTimeout(() => cb(Date.now()), 0);
  window.cancelAnimationFrame = clearTimeout;
  window.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
  window.PerformanceObserver = class { observe() {} disconnect() {} };
  // jsdom supplies crypto.getRandomValues but not crypto.subtle, and a
  // plain assignment to window.crypto is silently ignored because jsdom
  // defines it as a non-writable accessor. defineProperty replaces it.
  const nodeCrypto = require('crypto').webcrypto;
  try {
    Object.defineProperty(window, 'crypto', {
      value: nodeCrypto, configurable: true, writable: true
    });
  } catch {
    if (window.crypto && !window.crypto.subtle) window.crypto.subtle = nodeCrypto.subtle;
  }

  window.scrollTo = () => {};

  // Canvas: record draw calls so image/QR tools can be asserted against
  const canvasOps = [];
  window.HTMLCanvasElement.prototype.getContext = function () {
    return {
      canvas: this,
      fillRect: (...a) => canvasOps.push(['fillRect', ...a]),
      clearRect: (...a) => canvasOps.push(['clearRect', ...a]),
      drawImage: (...a) => canvasOps.push(['drawImage', ...a]),
      strokeRect() {}, beginPath() {}, closePath() {}, moveTo() {}, lineTo() {},
      rect() {}, roundRect() {}, quadraticCurveTo() {}, bezierCurveTo() {},
      arc() {}, fill() {}, stroke() {}, save() {}, restore() {}, translate() {},
      rotate() {}, scale() {}, setTransform() {}, clip() {}, measureText: () => ({ width: 42 }),
      fillText: (...a) => canvasOps.push(['fillText', ...a]),
      putImageData() {},
      createImageData: (w, h) => ({ data: new Uint8ClampedArray(w * h * 4), width: w, height: h }),
      getImageData: (x, y, w, h) => ({ data: new Uint8ClampedArray(w * h * 4), width: w, height: h }),
      set fillStyle(v) { this._fill = v; }, get fillStyle() { return this._fill || '#000'; },
      set strokeStyle(v) {}, get strokeStyle() { return '#000'; },
      set lineWidth(v) {}, set font(v) {}, set textAlign(v) {}, set globalAlpha(v) {},
      set filter(v) {}, set textBaseline(v) {}, set lineCap(v) {}, set lineJoin(v) {}
    };
  };
  window.HTMLCanvasElement.prototype.toBlob = function (cb, type) {
    cb(new window.Blob(['fake'], { type: type || 'image/png' }));
  };
  window.HTMLCanvasElement.prototype.toDataURL = () => 'data:image/png;base64,AAAA';

  // Speech synthesis
  window.speechSynthesis = {
    getVoices: () => [],
    speak() {}, cancel() {}, pause() {}, resume() {},
    addEventListener() {}, removeEventListener() {}
  };
  window.SpeechSynthesisUtterance = class {
    constructor(text) { this.text = text; }
    addEventListener() {}
  };

  window.URL.createObjectURL = () => 'blob:fake';
  window.URL.revokeObjectURL = () => {};

  // jsdom does not decode images, so `new Image()` never fires onload and
  // any tool that awaits T.loadImage() would hang. Stub it to resolve
  // immediately with dimensions the test can control via
  // window.__testImageSize.
  window.__testImageSize = { width: 800, height: 600 };
  class StubImage {
    constructor() {
      this.width = 0;
      this.height = 0;
      this.onload = null;
      this.onerror = null;
    }
    set src(value) {
      this._src = value;
      const { width, height } = window.__testImageSize;
      this.width = width;
      this.height = height;
      this.naturalWidth = width;
      this.naturalHeight = height;
      // Resolve asynchronously, as a real decode would
      setTimeout(() => { if (this.onload) this.onload(); }, 0);
    }
    get src() { return this._src; }
  }
  window.Image = StubImage;

  // jsdom's FileReader exposes `result` as a getter-only property, so it
  // cannot be subclassed and assigned. Provide a standalone stub with the
  // small surface these tools actually use.
  window.FileReader = class {
    constructor() {
      this.result = null;
      this.onload = null;
      this.onerror = null;
    }
    readAsDataURL(file) {
      setTimeout(() => {
        this.result = 'data:' + ((file && file.type) || 'image/png') + ';base64,AAAA';
        if (this.onload) this.onload({ target: this });
      }, 0);
    }
    readAsText(file) {
      setTimeout(async () => {
        this.result = file && file.text ? await file.text() : '';
        if (this.onload) this.onload({ target: this });
      }, 0);
    }
    addEventListener(type, handler) {
      if (type === 'load') this.onload = handler;
      if (type === 'error') this.onerror = handler;
    }
  };

  /* ---- 1. External scripts, in document order ---- */
  const base = path.dirname(path.join(ROOT, relPath));
  for (const tag of window.document.querySelectorAll('script[src]')) {
    // Strip any ?v=... cache-busting query string before resolving to a file.
    const src = tag.getAttribute('src').split('?')[0];
    const file = path.resolve(base, src);
    try {
      window.eval(fs.readFileSync(file, 'utf8'));
    } catch (e) {
      errors.push('LOAD ' + tag.getAttribute('src') + ': ' + e.message);
    }
  }

  /* ---- 2. Inline scripts (skipping JSON-LD) ---- */
  for (const tag of window.document.querySelectorAll('script:not([src])')) {
    if ((tag.type || '').includes('ld+json')) continue;
    try {
      window.eval(tag.textContent);
    } catch (e) {
      errors.push('INLINE: ' + e.message);
    }
  }

  /* ---- 3. Let jsdom's own DOMContentLoaded fire the handlers ---- */
  if (window.document.readyState === 'loading') {
    await new Promise((resolve) => {
      window.document.addEventListener('DOMContentLoaded', resolve, { once: true });
      // Safety net in case the event never arrives
      setTimeout(resolve, 500);
    });
  }

  // One extra tick so any handler-scheduled work settles
  await new Promise((r) => setTimeout(r, 0));

  return { window, doc: window.document, errors, canvasOps };
}

/* ============================================
   Assertion helpers
   ============================================ */

class Suite {
  constructor(name) {
    this.name = name;
    this.results = [];
  }

  /** @param {string} label @param {boolean} ok @param {string} [detail] */
  check(label, ok, detail = '') {
    this.results.push({ label, ok: Boolean(ok), detail });
    return Boolean(ok);
  }

  eq(label, actual, expected) {
    const ok = actual === expected;
    return this.check(label, ok, ok ? '' : `got ${JSON.stringify(actual)} want ${JSON.stringify(expected)}`);
  }

  near(label, actual, expected, tolerance = 0.01) {
    const ok = Math.abs(Number(actual) - Number(expected)) <= tolerance;
    return this.check(label, ok, ok ? '' : `got ${actual} want ~${expected}`);
  }

  match(label, actual, regex) {
    const ok = regex.test(String(actual));
    return this.check(label, ok, ok ? '' : `${JSON.stringify(String(actual).slice(0, 80))} !~ ${regex}`);
  }

  includes(label, haystack, needle) {
    const ok = String(haystack).includes(needle);
    return this.check(label, ok, ok ? '' : `${JSON.stringify(String(haystack).slice(0, 80))} missing ${JSON.stringify(needle)}`);
  }

  noErrors(errors) {
    return this.check('no runtime errors', errors.length === 0, errors.slice(0, 2).join(' | '));
  }

  get passed() { return this.results.filter((r) => r.ok).length; }
  get failed() { return this.results.filter((r) => !r.ok).length; }
}

/* ============================================
   Interaction helpers
   ============================================ */

/** Set a value and fire the matching event. */
function set(win, id, value, event = 'input') {
  const node = win.document.getElementById(id);
  if (!node) throw new Error('no element #' + id);
  if (node.type === 'checkbox') node.checked = Boolean(value);
  else node.value = value;
  node.dispatchEvent(new win.Event(event, { bubbles: true }));
  return node;
}

/** Click a button by id. */
function click(win, id) {
  const node = win.document.getElementById(id);
  if (!node) throw new Error('no element #' + id);
  node.click();
  return node;
}

/** Read an element's trimmed text. */
function text(win, id) {
  const node = win.document.getElementById(id);
  return node ? node.textContent.trim() : null;
}

/** Read an input's value. */
function val(win, id) {
  const node = win.document.getElementById(id);
  return node ? node.value : null;
}

/** Wait for debounced handlers to settle. */
const wait = (ms = 350) => new Promise((r) => setTimeout(r, ms));

module.exports = { boot, Suite, set, click, text, val, wait, ROOT };
