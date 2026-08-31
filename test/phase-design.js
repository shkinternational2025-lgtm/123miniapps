/* ============================================
   123MiniApps.online v2.0
   File: test/phase-design.js
   Purpose: Behavioural tests for the 7 design tools.
   ============================================ */

const { boot, Suite, set, click, text, val, wait } = require('./harness');

module.exports = async function run() {
  const s = new Suite('Design tools');

  /* ---------- Palette Generator ---------- */
  {
    const { window: w, errors } = await boot('tools/color-palette-generator.html');

    set(w, 'base', '#00D4FF', 'input');
    set(w, 'scheme', 'complementary', 'change');
    await wait(250);

    let swatches = w.document.querySelectorAll('#palette .swatch');
    s.check('palette: swatches rendered', swatches.length > 0);
    s.check('palette: contrast table renders',
      w.document.querySelector('#contrast table') !== null);

    // Complementary means a hue roughly 180 degrees apart
    const hexes = [...w.document.querySelectorAll('#palette .swatch__hex')]
      .map((n) => n.textContent);
    s.check('palette: all valid hex', hexes.every((h) => /^#[0-9A-F]{6}$/.test(h)), hexes[0]);

    set(w, 'scheme', 'monochromatic', 'change');
    await wait(250);
    const mono = [...w.document.querySelectorAll('#palette .swatch__hex')].map((n) => n.textContent);
    s.check('palette: monochromatic differs from complementary',
      JSON.stringify(mono) !== JSON.stringify(hexes));

    set(w, 'count', '8');
    await wait(250);
    s.eq('palette: honours swatch count',
      w.document.querySelectorAll('#palette .swatch').length, 8);

    // Export formats
    set(w, 'format', 'css', 'change');
    await wait(200);
    s.includes('palette: CSS export', text(w, 'css'), '--colour-1:');

    set(w, 'format', 'scss', 'change');
    await wait(200);
    s.includes('palette: SCSS export', text(w, 'css'), '$colour-1:');

    set(w, 'format', 'tailwind', 'change');
    await wait(200);
    s.includes('palette: Tailwind export', text(w, 'css'), 'module.exports');

    set(w, 'format', 'json', 'change');
    await wait(200);
    s.check('palette: JSON export parses', (() => {
      try { JSON.parse(text(w, 'css')); return true; } catch { return false; }
    })());
    s.noErrors(errors);
  }

  /* ---------- Contrast Checker ---------- */
  {
    const { window: w, errors } = await boot('tools/contrast-checker.html');

    // Black on white is exactly 21:1
    set(w, 'fg', '#000000', 'input');
    set(w, 'bg', '#FFFFFF', 'input');
    await wait(250);
    s.eq('contrast: black on white = 21.00:1', text(w, 'r-ratio'), '21.00:1');
    s.match('contrast: passes AAA', text(w, 'status'), /passes AA and AAA/i);

    // Identical colours are 1:1
    set(w, 'fg', '#808080', 'input');
    set(w, 'bg', '#808080', 'input');
    await wait(250);
    s.eq('contrast: identical colours = 1.00:1', text(w, 'r-ratio'), '1.00:1');
    s.match('contrast: fails AA', text(w, 'status'), /fails AA/i);
    s.check('contrast: suggestions shown on failure',
      w.document.getElementById('suggestions-field').hidden === false);
    s.check('contrast: suggestion swatches rendered',
      w.document.querySelectorAll('#suggestions .swatch').length > 0);

    // Ratio is symmetrical
    set(w, 'fg', '#0B1120', 'input');
    set(w, 'bg', '#FFFFFF', 'input');
    await wait(250);
    const forward = text(w, 'r-ratio');
    click(w, 'swap');
    await wait(250);
    s.eq('contrast: ratio is symmetrical', text(w, 'r-ratio'), forward);

    // Results table lists all five criteria
    s.eq('contrast: five WCAG rows',
      w.document.querySelectorAll('#results tbody tr').length, 5);

    // Hex entry syncs the picker
    set(w, 'fg-hex', '#FF0000');
    await wait(250);
    s.eq('contrast: hex field drives picker', val(w, 'fg').toUpperCase(), '#FF0000');
    s.noErrors(errors);
  }

  /* ---------- Box Shadow ---------- */
  {
    const { window: w, errors } = await boot('tools/box-shadow-generator.html');

    await wait(250);
    s.check('shadow: layers rendered', w.document.querySelectorAll('#layers .info-panel').length >= 1);
    s.match('shadow: CSS generated', text(w, 'css'), /^box-shadow: .*rgba\(/);

    const before = w.document.querySelectorAll('#layers .info-panel').length;
    click(w, 'add');
    await wait(250);
    s.eq('shadow: layer added', w.document.querySelectorAll('#layers .info-panel').length, before + 1);

    click(w, 'preset-material');
    await wait(250);
    s.eq('shadow: material preset has 3 layers',
      w.document.querySelectorAll('#layers .info-panel').length, 3);
    s.check('shadow: three comma-separated shadows',
      (text(w, 'css').match(/rgba\(/g) || []).length === 3);

    click(w, 'preset-hard');
    await wait(250);
    s.eq('shadow: hard preset has 1 layer',
      w.document.querySelectorAll('#layers .info-panel').length, 1);
    s.includes('shadow: hard preset has no blur', text(w, 'css'), '0px 0px');

    // The preview element carries the shadow. Note #box is the colour
    // input; #preview-box is the preview — they used to share an id,
    // which meant the preview never picked up the styling.
    s.includes('shadow: preview styled',
      w.document.getElementById('preview-box').style.boxShadow, 'rgba');
    s.noErrors(errors);
  }

  /* ---------- Border Radius ---------- */
  {
    const { window: w, errors } = await boot('tools/border-radius-generator.html');

    await wait(250);
    s.match('radius: simple CSS generated', text(w, 'css'), /^border-radius: \d+px;$/);

    // Linking corners produces the single-value shorthand
    set(w, 'linked', true, 'change');
    await wait(250);
    s.match('radius: linked gives one value', text(w, 'css'), /^border-radius: \d+px;$/);

    // Elliptical mode uses the slash syntax
    set(w, 'advanced', true, 'change');
    await wait(250);
    s.includes('radius: elliptical uses slash syntax', text(w, 'css'), '/');
    s.match('radius: elliptical uses percentages', text(w, 'css'), /%/);
    s.check('radius: advanced controls shown',
      w.document.getElementById('advanced-controls').hidden === false);

    click(w, 'blob');
    await wait(250);
    s.includes('radius: blob is elliptical', text(w, 'css'), '/');

    click(w, 'reset');
    await wait(250);
    s.eq('radius: reset returns to simple mode',
      w.document.getElementById('advanced').checked, false);
    s.match('radius: reset value', text(w, 'css'), /22px/);
    s.noErrors(errors);
  }

  /* ---------- Font Pairing ---------- */
  {
    const { window: w, errors } = await boot('tools/font-pairing-tool.html');

    await wait(300);
    s.check('fonts: pairings populated',
      w.document.getElementById('pairing').options.length === 20);
    s.includes('fonts: embed code generated', text(w, 'css'), 'fonts.googleapis.com');
    s.includes('fonts: display swap included', text(w, 'css'), 'display=swap');
    s.includes('fonts: CSS includes fallbacks', text(w, 'css'), 'sans-serif');

    // Category filter
    set(w, 'category', 'technical', 'change');
    await wait(300);
    const filtered = w.document.getElementById('pairing').options.length;
    s.check('fonts: filter narrows the list', filtered < 20 && filtered > 0, String(filtered));

    set(w, 'category', 'all', 'change');
    await wait(300);

    // Specimen reflects the selection
    set(w, 'sample-heading', 'Testing the specimen');
    await wait(300);
    s.eq('fonts: specimen uses custom text',
      text(w, 'spec-heading'), 'Testing the specimen');

    set(w, 'heading-size', '64');
    await wait(300);
    s.eq('fonts: heading size applied',
      w.document.getElementById('spec-heading').style.fontSize, '64px');

    set(w, 'weight', '800', 'change');
    await wait(300);
    s.eq('fonts: weight applied',
      w.document.getElementById('spec-heading').style.fontWeight, '800');

    click(w, 'random');
    await wait(300);
    s.includes('fonts: random still generates code', text(w, 'css'), 'font-family');
    s.noErrors(errors);
  }

  /* ---------- CSS Grid ---------- */
  {
    const { window: w, errors } = await boot('tools/css-grid-generator.html');

    set(w, 'cols', '4');
    set(w, 'rows', '3');
    await wait(250);

    s.eq('grid: 12 cells rendered',
      w.document.querySelectorAll('#preview .chip').length, 12);
    s.includes('grid: CSS has display grid', text(w, 'css'), 'display: grid');
    s.includes('grid: 4 columns', text(w, 'css'), 'repeat(4, minmax(0, 1fr))');
    s.includes('grid: HTML generated', text(w, 'html-out'), '<div class="grid">');
    s.eq('grid: HTML has 12 cells',
      (text(w, 'html-out').match(/class="cell"/g) || []).length, 12);

    // Responsive sizing
    set(w, 'col-unit', 'minmax', 'change');
    await wait(250);
    s.includes('grid: auto-fill minmax', text(w, 'css'), 'repeat(auto-fill, minmax(200px, 1fr))');

    set(w, 'col-unit', 'mixed', 'change');
    await wait(250);
    s.includes('grid: sidebar layout', text(w, 'css'), '240px repeat(3');

    // Named areas
    set(w, 'col-unit', '1fr', 'change');
    set(w, 'areas', true, 'change');
    await wait(250);
    s.includes('grid: named areas emitted', text(w, 'css'), 'grid-template-areas:');
    s.includes('grid: header area', text(w, 'css'), 'header');

    // Cell spanning
    set(w, 'areas', false, 'change');
    await wait(250);
    w.document.querySelectorAll('#preview .chip')[0].click();
    await wait(250);
    s.includes('grid: span rule emitted', text(w, 'css'), 'grid-column: span 2');

    click(w, 'reset');
    await wait(250);
    s.check('grid: reset clears spans', !text(w, 'css').includes('span 2'));
    s.noErrors(errors);
  }

  /* ---------- Glassmorphism ---------- */
  {
    const { window: w, errors } = await boot('tools/glassmorphism-generator.html');

    set(w, 'blur', '20');
    set(w, 'transparency', '20');
    set(w, 'saturation', '160');
    set(w, 'backdrop', 'mesh', 'change');
    await wait(250);

    const css = text(w, 'css');
    s.includes('glass: backdrop-filter', css, 'backdrop-filter: blur(20px) saturate(160%)');
    s.includes('glass: webkit prefix for Safari', css, '-webkit-backdrop-filter');
    s.includes('glass: rgba background', css, 'rgba(');
    s.includes('glass: border included', css, 'border: 1px solid');
    s.includes('glass: supports fallback', css, '@supports not');

    set(w, 'blur', '5');
    await wait(250);
    s.includes('glass: blur value updates', text(w, 'css'), 'blur(5px)');

    // Flat backgrounds should trigger the "nothing to blur" warning
    set(w, 'backdrop', 'dark', 'change');
    await wait(250);
    s.match('glass: warns on flat backdrop', text(w, 'status'), /nothing to sample/i);

    set(w, 'backdrop', 'photo', 'change');
    await wait(250);
    s.match('glass: no warning over detail', text(w, 'status'), /Blur \d+px/);

    set(w, 'shadow', false, 'change');
    await wait(250);
    s.check('glass: shadow removed', !text(w, 'css').includes('box-shadow'));

    // The preview element actually carries the effect
    s.includes('glass: preview styled',
      w.document.getElementById('glass').style.background, 'rgba');
    s.noErrors(errors);
  }

  return s;
};
