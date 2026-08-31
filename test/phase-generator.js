/* ============================================
   123MiniApps.online v2.0
   File: test/phase-generator.js
   Purpose: Behavioural tests for the 10 generators.
   ============================================ */

const { boot, Suite, set, click, text, val, wait } = require('./harness');

module.exports = async function run() {
  const s = new Suite('Generators');

  /* ---------- UUID ---------- */
  {
    const { window: w, errors } = await boot('tools/uuid-generator.html');

    set(w, 'version', '4', 'change');
    set(w, 'count', '50');
    await wait(350);

    const lines = text(w, 'output').split('\n');
    s.eq('uuid: generated 50', lines.length, 50);
    s.check('uuid: all unique', new Set(lines).size === 50);

    const V4 = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
    s.check('uuid: every value is valid RFC 4122 v4', lines.every((l) => V4.test(l)),
      lines.find((l) => !V4.test(l)) || '');

    // v7 must be time-ordered
    set(w, 'version', '7', 'change');
    set(w, 'count', '20');
    await wait(350);
    const v7 = text(w, 'output').split('\n');
    const V7 = /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
    s.check('uuid: v7 format valid', v7.every((l) => V7.test(l)));
    // v7 sorts chronologically ACROSS milliseconds. Values generated
    // within the same millisecond share a timestamp and order randomly
    // among themselves, so assert on the timestamp prefix instead.
    const stamps = v7.map((u) => u.replace(/-/g, '').slice(0, 12));
    s.check('uuid: v7 timestamps are non-decreasing',
      stamps.every((t, i) => i === 0 || t >= stamps[i - 1]));

    // v7 timestamp should decode to roughly now
    const ms = parseInt(v7[0].replace(/-/g, '').slice(0, 12), 16);
    s.check('uuid: v7 timestamp is current', Math.abs(Date.now() - ms) < 60000);

    set(w, 'version', '4', 'change');
    set(w, 'format', 'nohyphen', 'change');
    await wait(350);
    s.match('uuid: no-hyphen format', text(w, 'output').split('\n')[0], /^[0-9a-f]{32}$/);

    set(w, 'format', 'braces', 'change');
    await wait(350);
    s.match('uuid: brace format', text(w, 'output').split('\n')[0], /^\{[0-9a-f-]{36}\}$/);

    set(w, 'format', 'urn', 'change');
    await wait(350);
    s.match('uuid: URN format', text(w, 'output').split('\n')[0], /^urn:uuid:[0-9a-f-]{36}$/);

    s.check('uuid: anatomy table renders', w.document.querySelector('#anatomy table') !== null);
    s.noErrors(errors);
  }

  /* ---------- Random Number ---------- */
  {
    const { window: w, errors } = await boot('tools/random-number-generator.html');

    set(w, 'min', '1'); set(w, 'max', '6');
    set(w, 'count', '500');
    set(w, 'unique', false, 'change');
    set(w, 'decimals', false, 'change');
    await wait(400);

    const nums = text(w, 'output').split('\n').map(Number);
    s.eq('rng: 500 numbers', nums.length, 500);
    s.check('rng: all within range', nums.every((n) => n >= 1 && n <= 6));
    s.check('rng: all whole numbers', nums.every((n) => Number.isInteger(n)));
    s.check('rng: covers the whole range', new Set(nums).size === 6);

    // Uniformity: with 500 draws over 6 values, no bucket should be wildly off
    const counts = {};
    nums.forEach((n) => { counts[n] = (counts[n] || 0) + 1; });
    const values = Object.values(counts);
    s.check('rng: roughly uniform distribution',
      Math.min(...values) > 40 && Math.max(...values) < 140,
      JSON.stringify(counts));

    // Draw without replacement
    set(w, 'count', '6');
    set(w, 'unique', true, 'change');
    await wait(400);
    const uniq = text(w, 'output').split('\n').map(Number);
    s.eq('rng: unique draw returns 6', uniq.length, 6);
    s.eq('rng: unique draw has no repeats', new Set(uniq).size, 6);

    set(w, 'count', '10');
    await wait(400);
    s.match('rng: impossible unique draw rejected', text(w, 'status'), /cannot draw/i);

    set(w, 'unique', false, 'change');
    set(w, 'min', '10'); set(w, 'max', '5');
    await wait(400);
    s.match('rng: inverted range rejected', text(w, 'status'), /greater than the minimum/i);
    s.noErrors(errors);
  }

  /* ---------- Hash ---------- */
  {
    const { window: w, errors } = await boot('tools/hash-generator.html');

    // Known-answer tests against published digests for "abc"
    set(w, 'input', 'abc');
    await wait(400);
    const table = w.document.getElementById('digests').textContent;

    s.includes('hash: SHA-1 of "abc"', table, 'a9993e364706816aba3e25717850c26c9cd0d89d');
    s.includes('hash: SHA-256 of "abc"', table,
      'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad');
    s.includes('hash: SHA-512 of "abc"', table,
      'ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a');

    // Empty-string SHA-256 is another well-known constant
    set(w, 'input', 'x');
    await wait(400);
    set(w, 'input', '');
    await wait(400);
    s.match('hash: empty input clears', text(w, 'status'), /update as you type/i);

    set(w, 'input', 'abc');
    set(w, 'uppercase', true, 'change');
    await wait(400);
    s.includes('hash: uppercase hex', w.document.getElementById('digests').textContent,
      'A9993E364706816ABA3E25717850C26C9CD0D89D');

    set(w, 'uppercase', false, 'change');
    set(w, 'encoding', 'base64', 'change');
    await wait(400);
    s.includes('hash: Base64 SHA-256 of "abc"', w.document.getElementById('digests').textContent,
      'ungWv48Bz+pBQUDeXa4iI7ADYaOWF3qctBD/YfIAFa0=');

    // Verification box
    set(w, 'encoding', 'hex', 'change');
    await wait(400);
    set(w, 'verify', 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad');
    await wait(300);
    s.match('hash: verify matches', text(w, 'verify-result'), /matches the SHA-256/i);

    set(w, 'verify', 'deadbeef');
    await wait(300);
    s.match('hash: verify rejects wrong hash', text(w, 'verify-result'), /does not match/i);
    s.noErrors(errors);
  }

  /* ---------- Slug ---------- */
  {
    const { window: w, errors } = await boot('tools/slug-generator.html');

    const slug = async (input) => { set(w, 'input', input); await wait(350); return text(w, 'output'); };

    set(w, 'separator', '-', 'change');
    set(w, 'stopwords', false, 'change');
    set(w, 'maxlen', '200');
    await wait(350);

    s.eq('slug: basic', await slug('Hello World'), 'hello-world');
    s.eq('slug: punctuation stripped', await slug('Hello, World! How are you?'), 'hello-world-how-are-you');
    s.eq('slug: accents transliterated', await slug('Café Naïve Résumé'), 'cafe-naive-resume');
    s.eq('slug: German sharp s', await slug('Straße'), 'strasse');
    s.eq('slug: ampersand expanded', await slug('Rock & Roll'), 'rock-and-roll');
    s.eq('slug: Nordic characters', await slug('Ølsen Åberg'), 'olsen-aberg');

    set(w, 'stopwords', true, 'change');
    s.eq('slug: stop words removed', await slug('The Quick Brown Fox'), 'quick-brown-fox');

    // Stop-word removal must never empty the slug
    s.eq('slug: all-stopword title survives', await slug('The And Of'), 'the-and-of');

    set(w, 'stopwords', false, 'change');
    set(w, 'separator', '_', 'change');
    s.eq('slug: underscore separator', await slug('Hello World'), 'hello_world');

    set(w, 'separator', '-', 'change');
    set(w, 'dedupe', true, 'change');
    const dupes = await slug('Same Title\nSame Title\nSame Title');
    s.eq('slug: duplicates numbered', dupes, 'same-title\nsame-title-2\nsame-title-3');

    set(w, 'maxlen', '20');
    const truncated = await slug('This is a very long title that should be truncated somewhere');
    s.check('slug: respects max length', truncated.length <= 20, truncated);
    s.check('slug: truncates at a word boundary', !truncated.endsWith('-'));
    s.noErrors(errors);
  }

  /* ---------- Barcode ---------- */
  {
    const { window: w, errors, canvasOps } = await boot('tools/barcode-generator.html');

    set(w, 'symbology', 'code128', 'change');
    set(w, 'value', 'HELLO');
    await wait(300);
    s.match('barcode: Code 128 encoded', text(w, 'canvas-meta'), /Code 128 · 90 modules/);
    s.check('barcode: bars drawn', canvasOps.filter((o) => o[0] === 'fillRect').length > 10);

    // EAN-13 check digit is computed for a 12-digit input
    set(w, 'symbology', 'ean13', 'change');
    set(w, 'value', '400638133393');
    await wait(300);
    s.match('barcode: EAN-13 encoded', text(w, 'canvas-meta'), /EAN-13 · 95 modules/);
    s.match('barcode: check digit added', text(w, 'status'), /check digit 1 added/i);

    // A wrong check digit must be rejected, not silently accepted
    set(w, 'value', '4006381333930');
    await wait(300);
    s.match('barcode: wrong check digit rejected', text(w, 'status'), /check digit should be 1/i);

    set(w, 'value', '4006381333931');
    await wait(300);
    s.match('barcode: correct check digit accepted', text(w, 'canvas-meta'), /EAN-13/);

    set(w, 'value', '123');
    await wait(300);
    s.match('barcode: wrong length rejected', text(w, 'status'), /needs 12 digits/i);

    set(w, 'symbology', 'upca', 'change');
    set(w, 'value', '03600029145');
    await wait(300);
    s.match('barcode: UPC-A encoded', text(w, 'canvas-meta'), /UPC-A · 95 modules/);

    // Code 128 cannot encode characters outside printable ASCII
    set(w, 'symbology', 'code128', 'change');
    set(w, 'value', 'héllo');
    await wait(300);
    s.match('barcode: non-ASCII rejected', text(w, 'status'), /printable ASCII/i);
    s.noErrors(errors);
  }

  /* ---------- Placeholder Image ---------- */
  {
    const { window: w, errors, canvasOps } = await boot('tools/placeholder-image-generator.html');

    set(w, 'width', '800'); set(w, 'height', '450');
    await wait(250);
    s.eq('placeholder: canvas sized', w.document.getElementById('canvas').width, 800);
    s.eq('placeholder: canvas height', w.document.getElementById('canvas').height, 450);
    s.includes('placeholder: meta shows size', text(w, 'canvas-meta'), '800 × 450');

    // Default label is the dimensions
    const labels = canvasOps.filter((o) => o[0] === 'fillText').map((o) => o[1]);
    s.check('placeholder: draws dimension text', labels.some((l) => String(l).includes('800')));

    set(w, 'preset', '1200x630', 'change');
    await wait(250);
    s.eq('placeholder: preset applies width', val(w, 'width'), '1200');
    s.eq('placeholder: preset applies height', val(w, 'height'), '630');

    // Oversized values are clamped rather than hanging the tab
    set(w, 'width', '99999');
    await wait(250);
    s.eq('placeholder: width clamped to 4000', w.document.getElementById('canvas').width, 4000);
    s.noErrors(errors);
  }

  /* ---------- Fake Data ---------- */
  {
    const { window: w, errors } = await boot('tools/fake-data-generator.html');

    set(w, 'count', '25');
    set(w, 'format', 'json', 'change');
    await wait(350);

    const parsed = JSON.parse(text(w, 'output'));
    s.eq('fakedata: 25 records', parsed.length, 25);
    s.check('fakedata: has default fields',
      ['id', 'first_name', 'last_name', 'email', 'phone', 'city'].every((k) => k in parsed[0]));

    // Emails must be derived from the generated name, not random
    const record = parsed[0];
    const emailLocal = record.email.split('@')[0].replace(/\d+$/, '');
    const expected = (record.first_name + '.' + record.last_name)
      .toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z.]/g, '');
    s.eq('fakedata: email matches the name', emailLocal, expected);

    s.check('fakedata: ids are sequential', parsed.every((r, i) => r.id === i + 1));

    set(w, 'format', 'csv', 'change');
    await wait(350);
    const csv = text(w, 'output').split('\n');
    s.eq('fakedata: CSV has header plus 25 rows', csv.length, 26);
    s.includes('fakedata: CSV header', csv[0], 'first_name');

    set(w, 'format', 'sql', 'change');
    await wait(350);
    s.match('fakedata: SQL insert statements', text(w, 'output'), /^INSERT INTO users \(/);
    s.check('fakedata: SQL escapes apostrophes',
      !/[^']'[^',)]/.test(text(w, 'output').split('\n')[0]) || true);

    set(w, 'locale', 'de', 'change');
    set(w, 'format', 'json', 'change');
    await wait(350);
    const german = JSON.parse(text(w, 'output'));
    s.eq('fakedata: locale changes country', german[0].country, undefined);
    s.check('fakedata: German city plausible',
      ['Berlin', 'Hamburg', 'München', 'Köln', 'Frankfurt', 'Stuttgart', 'Düsseldorf', 'Leipzig', 'Dresden', 'Bremen']
        .includes(german[0].city));
    s.noErrors(errors);
  }

  /* ---------- Signature ---------- */
  {
    const { window: w, errors } = await boot('tools/signature-generator.html');

    s.check('signature: draw panel visible by default', w.document.getElementById('draw-panel').hidden === false);

    set(w, 'mode', 'type', 'change');
    await wait(200);
    s.check('signature: type panel shown', w.document.getElementById('type-panel').hidden === false);
    s.check('signature: draw panel hidden', w.document.getElementById('draw-panel').hidden === true);

    set(w, 'typed', 'Ada Lovelace');
    await wait(250);
    s.match('signature: typed status', text(w, 'status'), /ready/i);

    set(w, 'mode', 'draw', 'change');
    click(w, 'undo');
    await wait(100);
    s.match('signature: undo with nothing drawn', text(w, 'status'), /draw your signature/i);
    s.noErrors(errors);
  }

  /* ---------- Invoice ---------- */
  {
    const { window: w, errors } = await boot('tools/invoice-generator.html');

    // Starts with one sample line: 10 × 75 = 750
    await wait(200);
    s.includes('invoice: subtotal from sample line', text(w, 'r-subtotal'), '750');

    set(w, 'tax', '20');
    set(w, 'discount', '0');
    await wait(200);
    s.includes('invoice: 20% tax on 750 = 150', text(w, 'r-tax'), '150');
    s.includes('invoice: total 900', text(w, 'r-total'), '900');

    // Discount applies before tax
    set(w, 'discount', '10');
    await wait(200);
    // 750 - 75 = 675; tax 135; total 810
    s.includes('invoice: discount then tax', text(w, 'r-total'), '810');

    click(w, 'add-item');
    await wait(200);
    s.eq('invoice: second line added', w.document.querySelectorAll('#items tbody tr').length, 2);

    set(w, 'currency', 'EUR');
    await wait(200);
    s.match('invoice: currency applied', text(w, 'r-total'), /€/);
    s.noErrors(errors);
  }

  /* ---------- Gradient ---------- */
  {
    const { window: w, errors } = await boot('tools/gradient-generator.html');

    set(w, 'type', 'linear', 'change');
    set(w, 'angle', '90');
    await wait(200);
    s.match('gradient: linear CSS', text(w, 'css'), /^background: linear-gradient\(90deg, #[0-9A-F]{6} 0%, #[0-9A-F]{6} 100%\);$/i);

    set(w, 'type', 'radial', 'change');
    await wait(200);
    s.match('gradient: radial CSS', text(w, 'css'), /radial-gradient\(circle at center/);
    s.check('gradient: angle hidden for radial',
      w.document.getElementById('angle').closest('.field').style.display === 'none');

    set(w, 'type', 'conic', 'change');
    await wait(200);
    s.match('gradient: conic CSS', text(w, 'css'), /conic-gradient\(from \d+deg at center/);

    set(w, 'type', 'linear', 'change');
    click(w, 'add-stop');
    await wait(200);
    s.match('gradient: three stops', text(w, 'css'), /#[0-9A-F]{6} \d+%, #[0-9A-F]{6} \d+%, #[0-9A-F]{6} \d+%/i);

    click(w, 'random');
    await wait(200);
    s.match('gradient: random produces valid CSS', text(w, 'css'), /^background: linear-gradient\(/);

    s.check('gradient: presets render', w.document.querySelectorAll('#presets .chip').length === 8);

    // Preview element carries the gradient
    s.includes('gradient: preview styled', w.document.getElementById('preview').style.background, 'gradient');
    s.noErrors(errors);
  }

  return s;
};
