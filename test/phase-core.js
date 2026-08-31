/* ============================================
   123MiniApps.online v2.0
   File: test/phase-core.js
   Purpose: Site-wide checks — the homepage, the
            shared chrome, and a smoke test that
            boots every one of the 95 tool pages.
   ============================================ */

const { boot, Suite, set, click, text, wait } = require('./harness');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

module.exports = async function run() {
  const s = new Suite('Core site');

  /* ---------- Homepage ---------- */
  {
    const { window: w, errors } = await boot('index.html');
    await wait(300);

    const q = (sel) => w.document.querySelectorAll(sel).length;

    s.eq('home: 95 tools loaded', w.TOOLS.length, 95);
    s.eq('home: 11 categories', w.CATEGORIES.length, 11);
    s.eq('home: every tool marked live', w.TOOLS.filter((t) => t.live).length, 95);
    s.eq('home: no "Soon" badges remain', q('.badge--muted'), 0);

    s.eq('home: theme applied', w.document.documentElement.getAttribute('data-theme'), 'indigo-nova');
    s.eq('home: ten theme swatches', q('.theme-swatch'), 10);
    s.eq('home: six category cards', q('#category-grid .category-card'), 6);
    s.eq('home: five category chips', q('#category-row .category-chip'), 5);
    s.eq('home: six featured tools', q('#featured-grid .tool-card--featured'), 6);
    s.eq('home: twelve category tabs', q('#all-tools [role="tab"]'), 12);
    s.eq('home: all 95 cards in the directory', q('#tabpanel-all .tool-card'), 95);
    s.eq('home: four feature cards', q('#features-grid .feature-card'), 4);
    s.eq('home: no fabricated testimonials', q('.testimonial'), 0);
    s.eq('home: three "why" value cards', q('[aria-labelledby="why-heading"] .info-panel'), 3);
    s.eq('home: five FAQ items', q('#faq .accordion__item'), 5);

    // Search
    const se = w.searchEngine;
    s.eq('search: exact name', se.search('password generator')[0].name, 'Password Generator');
    s.eq('search: prefix', se.search('json')[0].name, 'JSON Formatter');
    s.check('search: typo tolerance', se.search('passwrd').length > 0);
    s.eq('search: by tag', se.search('sha256')[0].name, 'Hash Generator');
    s.eq('search: by description', se.search('amortization')[0].name, 'Loan Calculator');
    s.eq('search: nonsense returns nothing', se.search('zzzqqqxxx').length, 0);

    // Every tool must be findable by its own name
    const unfindable = w.TOOLS.filter((t) => {
      const results = se.search(t.name, 5);
      return !results.some((r) => r.id === t.id);
    });
    s.eq('search: every tool findable by name', unfindable.length, 0,
      unfindable.slice(0, 3).map((t) => t.name).join(', '));

    // Category counts must match the data
    const mismatched = w.CATEGORIES.filter(
      (c) => w.getToolsByCategory(c.id).length !== w.getCategoryCount(c.id));
    s.eq('data: category counts consistent', mismatched.length, 0);

    s.noErrors(errors);
  }

  /* ---------- Data integrity ---------- */
  {
    // tools.js assigns to `window`, so give it one rather than
    // require()ing it into a bare Node context.
    const sandbox = { window: {} };
    const vm = require('vm');
    vm.createContext(sandbox);
    vm.runInContext(fs.readFileSync(path.join(ROOT, 'assets/data/tools.js'), 'utf8'), sandbox);
    const all = sandbox.window.TOOLS;

    s.eq('data: 95 tools', all.length, 95);
    s.eq('data: unique ids', new Set(all.map((t) => t.id)).size, 95);
    s.eq('data: unique slugs', new Set(all.map((t) => t.slug)).size, 95);
    s.eq('data: unique names', new Set(all.map((t) => t.name)).size, 95);
    s.check('data: every tool has features', all.every((t) => t.features.length >= 3));
    s.check('data: every rating in range', all.every((t) => t.rating >= 1 && t.rating <= 5));
    s.check('data: every url points at tools/', all.every((t) => t.url.startsWith('tools/')));
  }

  /* ---------- Every tool page boots cleanly ---------- */
  {
    const pages = fs.readdirSync(path.join(ROOT, 'tools'))
      .filter((f) => f.endsWith('.html') && !f.startsWith('_'))
      .sort();

    s.eq('pages: 95 tool pages on disk', pages.length, 95);

    const broken = [];
    let booted = 0;

    for (const page of pages) {
      try {
        const { window: w, errors } = await boot('tools/' + page);
        await wait(30);

        // The shared chrome must be present and wired on every page
        const problems = [];
        if (!w.document.querySelector('.nav')) problems.push('no nav');
        if (!w.document.getElementById('theme-panel')) problems.push('no theme panel');
        if (!w.document.getElementById('search-modal')) problems.push('no search modal');
        if (w.document.querySelectorAll('.theme-swatch').length !== 10) problems.push('theme swatches');
        if (!w.document.querySelector('h1')) problems.push('no h1');
        if (!w.document.querySelector('.workspace')) problems.push('no workspace');
        if (w.document.querySelectorAll('#related .tool-card').length !== 4) problems.push('related tools');
        if (errors.length) problems.push('errors: ' + errors[0]);

        if (problems.length) broken.push(`${page}: ${problems.join(', ')}`);
        else booted++;

        w.close();
      } catch (e) {
        broken.push(`${page}: threw ${e.message}`);
      }
    }

    s.eq('pages: all 95 boot with no errors', broken.length, 0,
      broken.slice(0, 5).join(' | '));
    s.check('pages: booted count', booted === 95, String(booted));
  }

  return s;
};
