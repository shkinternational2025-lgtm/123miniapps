/* ============================================
   123MiniApps.online v2.0
   File: test/phase-converter.js
   Purpose: Behavioural tests for the 10 converters.
   ============================================ */

const { boot, Suite, set, click, text, val, wait } = require('./harness');

module.exports = async function run() {
  const s = new Suite('Converters');

  /* ---------- Unit Converter ---------- */
  {
    const { window: w, errors } = await boot('tools/unit-converter.html');

    // Exact definitional conversions
    set(w, 'from-unit', 'm', 'change');
    set(w, 'to-unit', 'ft', 'change');
    set(w, 'from-value', '1');
    await wait(80);
    s.near('unit: 1 m → ft', Number(val(w, 'to-value')), 3.280839895, 1e-6);

    set(w, 'from-unit', 'in', 'change');
    set(w, 'to-unit', 'mm', 'change');
    set(w, 'from-value', '1');
    await wait(80);
    s.near('unit: 1 in = 25.4 mm exactly', Number(val(w, 'to-value')), 25.4, 1e-9);

    set(w, 'from-unit', 'mi', 'change');
    set(w, 'to-unit', 'km', 'change');
    set(w, 'from-value', '1');
    await wait(80);
    s.near('unit: 1 mi = 1.609344 km', Number(val(w, 'to-value')), 1.609344, 1e-9);

    // Reverse direction
    set(w, 'to-value', '1');
    await wait(80);
    s.near('unit: reverse 1 km → mi', Number(val(w, 'from-value')), 0.621371192, 1e-6);

    // Mass
    set(w, 'family', 'mass', 'change');
    await wait(80);
    set(w, 'from-unit', 'lb', 'change');
    set(w, 'to-unit', 'kg', 'change');
    set(w, 'from-value', '1');
    await wait(80);
    s.near('unit: 1 lb = 0.45359237 kg', Number(val(w, 'to-value')), 0.45359237, 1e-9);

    // US vs imperial gallon must differ
    set(w, 'family', 'volume', 'change');
    await wait(80);
    set(w, 'from-unit', 'gal', 'change');
    set(w, 'to-unit', 'l', 'change');
    set(w, 'from-value', '1');
    await wait(80);
    const usGal = Number(val(w, 'to-value'));
    set(w, 'from-unit', 'igal', 'change');
    set(w, 'from-value', '1');
    await wait(80);
    const impGal = Number(val(w, 'to-value'));
    s.near('unit: US gallon 3.785 L', usGal, 3.785411784, 1e-6);
    s.near('unit: imperial gallon 4.546 L', impGal, 4.54609, 1e-6);
    s.check('unit: gallons differ', Math.abs(usGal - impGal) > 0.7);

    // Data
    set(w, 'family', 'data', 'change');
    await wait(80);
    set(w, 'from-unit', 'MiB', 'change');
    set(w, 'to-unit', 'B', 'change');
    set(w, 'from-value', '1');
    await wait(80);
    s.eq('unit: 1 MiB = 1048576 B', Number(val(w, 'to-value')), 1048576);

    s.check('unit: all-units table renders', w.document.querySelector('#all-units table') !== null);

    click(w, 'swap');
    await wait(80);
    s.eq('unit: swap exchanges units', val(w, 'from-unit'), 'B');
    s.noErrors(errors);
  }

  /* ---------- Temperature ---------- */
  {
    const { window: w, errors } = await boot('tools/temperature-converter.html');

    set(w, 'celsius', '100');
    await wait(80);
    s.eq('temp: 100 C = 212 F', Number(val(w, 'fahrenheit')), 212);
    s.eq('temp: 100 C = 373.15 K', Number(val(w, 'kelvin')), 373.15);

    set(w, 'celsius', '0');
    await wait(80);
    s.eq('temp: 0 C = 32 F', Number(val(w, 'fahrenheit')), 32);

    // The scales cross at -40
    set(w, 'celsius', '-40');
    await wait(80);
    s.eq('temp: -40 C = -40 F', Number(val(w, 'fahrenheit')), -40);

    set(w, 'fahrenheit', '98.6');
    await wait(80);
    s.near('temp: 98.6 F = 37 C', Number(val(w, 'celsius')), 37, 0.01);

    set(w, 'kelvin', '0');
    await wait(80);
    s.near('temp: 0 K = -273.15 C', Number(val(w, 'celsius')), -273.15, 0.001);

    set(w, 'celsius', '-300');
    await wait(80);
    s.match('temp: below absolute zero warns', text(w, 'status'), /below absolute zero/i);

    set(w, 'celsius', '20');
    await wait(80);
    s.match('temp: context describes 20 C', text(w, 'context'), /comfortable|room/i);
    s.check('temp: reference table renders', w.document.querySelector('#reference table') !== null);
    s.noErrors(errors);
  }

  /* ---------- CSV to JSON ---------- */
  {
    const { window: w, errors } = await boot('tools/csv-to-json.html');

    set(w, 'input', 'name,age\nAda,36\nAlan,41');
    await wait(450);
    let parsed = JSON.parse(text(w, 'output'));
    s.eq('csv: 2 records', parsed.length, 2);
    s.eq('csv: field value', parsed[0].name, 'Ada');
    s.eq('csv: numeric typing', parsed[0].age, 36);

    // The critical case — a quoted field containing a comma
    set(w, 'input', 'name,city\nAlan,"Wilmslow, Cheshire"');
    await wait(450);
    parsed = JSON.parse(text(w, 'output'));
    s.eq('csv: quoted comma stays one field', parsed[0].city, 'Wilmslow, Cheshire');

    // Escaped quotes
    set(w, 'input', 'quote\n"She said ""hi"""');
    await wait(450);
    parsed = JSON.parse(text(w, 'output'));
    s.eq('csv: escaped quotes', parsed[0].quote, 'She said "hi"');

    // Leading zeros must survive when typing is off
    set(w, 'input', 'zip\n02134');
    set(w, 'typed', false, 'change');
    await wait(450);
    parsed = JSON.parse(text(w, 'output'));
    s.eq('csv: leading zero preserved untyped', parsed[0].zip, '02134');
    set(w, 'typed', true, 'change');
    await wait(450);
    parsed = JSON.parse(text(w, 'output'));
    s.eq('csv: leading zero kept as string when typed', parsed[0].zip, '02134');

    // Booleans
    set(w, 'input', 'ok\ntrue\nfalse');
    await wait(450);
    parsed = JSON.parse(text(w, 'output'));
    s.eq('csv: boolean typing', parsed[0].ok, true);

    // Reverse direction
    set(w, 'direction', 'json2csv', 'change');
    set(w, 'input', '[{"a":1,"b":"x, y"},{"a":2,"b":"z"}]');
    await wait(450);
    s.includes('json→csv: header row', text(w, 'output'), 'a,b');
    s.includes('json→csv: quotes embedded comma', text(w, 'output'), '"x, y"');

    // Semicolon delimiter
    set(w, 'direction', 'csv2json', 'change');
    set(w, 'delimiter', ';', 'change');
    set(w, 'input', 'a;b\n1;2');
    await wait(450);
    parsed = JSON.parse(text(w, 'output'));
    s.eq('csv: semicolon delimiter', parsed[0].b, 2);

    // Headerless
    set(w, 'delimiter', ',', 'change');
    set(w, 'header', false, 'change');
    set(w, 'input', '1,2\n3,4');
    await wait(450);
    parsed = JSON.parse(text(w, 'output'));
    s.eq('csv: headerless gives arrays', Array.isArray(parsed[0]), true);

    // Malformed JSON reports cleanly
    set(w, 'direction', 'json2csv', 'change');
    set(w, 'input', '{not json');
    await wait(450);
    s.match('csv: bad JSON reported', text(w, 'status'), /could not convert/i);
    s.noErrors(errors);
  }

  /* ---------- Timestamp ---------- */
  {
    const { window: w, errors } = await boot('tools/timestamp-converter.html');

    set(w, 'timestamp', '0');
    await wait(80);
    s.includes('ts: epoch renders 1970', w.document.getElementById('formats').textContent, '1970-01-01');

    set(w, 'timestamp', '1735689600');
    await wait(80);
    s.includes('ts: 2025-01-01 UTC', w.document.getElementById('formats').textContent, '2025-01-01T00:00:00.000Z');

    // Auto-detection of milliseconds
    set(w, 'timestamp', '1735689600000');
    await wait(80);
    s.includes('ts: ms auto-detected', w.document.getElementById('formats').textContent, '2025-01-01');

    // Forcing seconds on a ms value pushes far into the future
    set(w, 'unit', 's', 'change');
    await wait(80);
    s.check('ts: forced seconds yields far future',
      !w.document.getElementById('formats').textContent.includes('2025-01-01'));

    set(w, 'unit', 'auto', 'change');
    click(w, 'use-now');
    await wait(80);
    s.match('ts: current timestamp is 10 digits', val(w, 'timestamp'), /^\d{10}$/);
    s.match('ts: live clock ticking', text(w, 'now-ms'), /^\d{13}$/);
    s.noErrors(errors);
  }

  /* ---------- Number Base ---------- */
  {
    const { window: w, errors } = await boot('tools/number-base-converter.html');

    set(w, 'dec', '255');
    await wait(80);
    s.eq('base: 255 → hex FF', val(w, 'hex'), 'FF');
    s.eq('base: 255 → oct 377', val(w, 'oct'), '377');
    s.eq('base: 255 → bin 11111111', val(w, 'bin'), '11111111');
    s.eq('base: 255 needs 8 bits', text(w, 'r-bits'), '8');
    s.eq('base: smallest type uint8', text(w, 'r-fits'), 'uint8');

    set(w, 'hex', 'DEADBEEF');
    await wait(80);
    s.eq('base: DEADBEEF → decimal', val(w, 'dec'), '3735928559');
    s.eq('base: DEADBEEF needs 32 bits', text(w, 'r-bits'), '32');

    set(w, 'bin', '1010');
    await wait(80);
    s.eq('base: 1010b = 10', val(w, 'dec'), '10');

    // Invalid digit for the base
    set(w, 'bin', '1012');
    await wait(80);
    s.match('base: rejects invalid binary digit', text(w, 'status'), /not a valid base-2/i);

    // BigInt path — beyond Number.MAX_SAFE_INTEGER
    set(w, 'dec', '18446744073709551615');
    await wait(80);
    s.eq('base: 64-bit max → hex', val(w, 'hex'), 'FFFFFFFFFFFFFFFF');
    s.noErrors(errors);
  }

  /* ---------- Roman Numerals ---------- */
  {
    const { window: w, errors } = await boot('tools/roman-numeral-converter.html');

    const toRoman = async (n) => { set(w, 'number', String(n)); await wait(60); return val(w, 'roman'); };

    s.eq('roman: 1', await toRoman(1), 'I');
    s.eq('roman: 4 uses subtractive', await toRoman(4), 'IV');
    s.eq('roman: 9', await toRoman(9), 'IX');
    s.eq('roman: 40', await toRoman(40), 'XL');
    s.eq('roman: 49 is XLIX not IL', await toRoman(49), 'XLIX');
    s.eq('roman: 90', await toRoman(90), 'XC');
    s.eq('roman: 400', await toRoman(400), 'CD');
    s.eq('roman: 1994', await toRoman(1994), 'MCMXCIV');
    s.eq('roman: 2026', await toRoman(2026), 'MMXXVI');
    s.eq('roman: 3999 max', await toRoman(3999), 'MMMCMXCIX');

    const fromRoman = async (r) => { set(w, 'roman', r); await wait(60); return val(w, 'number'); };
    s.eq('roman: MCMXCIV → 1994', await fromRoman('MCMXCIV'), '1994');
    s.eq('roman: lowercase accepted', await fromRoman('mmxxvi'), '2026');

    // Malformed numerals must be rejected, not silently summed
    set(w, 'roman', 'IIII');
    await wait(60);
    s.match('roman: rejects IIII', text(w, 'status'), /not a valid/i);

    set(w, 'roman', 'IL');
    await wait(60);
    s.match('roman: rejects IL', text(w, 'status'), /not a valid/i);

    set(w, 'roman', 'VX');
    await wait(60);
    s.match('roman: rejects VX', text(w, 'status'), /not a valid/i);

    set(w, 'number', '4000');
    await wait(60);
    s.match('roman: rejects 4000', text(w, 'status'), /between 1 and 3999/i);

    set(w, 'number', '0');
    await wait(60);
    s.match('roman: rejects 0', text(w, 'status'), /between 1 and 3999/i);
    s.noErrors(errors);
  }

  /* ---------- Currency ---------- */
  {
    const { window: w, errors } = await boot('tools/currency-converter.html');

    set(w, 'amount', '100');
    set(w, 'rate', '0.85');
    await wait(80);
    s.includes('currency: 100 × 0.85 = 85', text(w, 'r-out'), '85.00');
    s.includes('currency: inverse rate shown', val(w, 'inverse'), '1.176471');

    // 2.5% fee
    s.includes('currency: fee applied', text(w, 'r-fee'), '82.88'); // 85 × 0.975 = 82.875, rounds to 82.88

    set(w, 'rate', '0');
    await wait(80);
    s.match('currency: zero rate rejected', text(w, 'status'), /greater than zero/i);

    set(w, 'rate', '2');
    await wait(80);
    click(w, 'swap');
    await wait(80);
    s.eq('currency: swap inverts rate', Number(val(w, 'rate')), 0.5);

    // JPY has zero decimal places
    set(w, 'to', 'JPY', 'change');
    set(w, 'amount', '100');
    set(w, 'rate', '150');
    await wait(80);
    s.match('currency: JPY has no decimals', text(w, 'r-out'), /¥15,000$/);
    s.noErrors(errors);
  }

  /* ---------- Time Zone ---------- */
  {
    const { window: w, errors } = await boot('tools/time-zone-converter.html');

    set(w, 'base-zone', 'UTC', 'change');
    set(w, 'when', '2025-01-15T12:00');
    await wait(120);

    const board = w.document.getElementById('board').textContent;
    s.includes('tz: board shows UTC', board, 'UTC');
    s.includes('tz: board shows New York', board, 'New York');
    s.includes('tz: board shows Tokyo', board, 'Tokyo');

    // 12:00 UTC in January is 07:00 in New York (EST, UTC-5)
    s.includes('tz: NY is 07:00 in January', board, '07:00');
    // and 21:00 in Tokyo (UTC+9)
    s.includes('tz: Tokyo is 21:00', board, '21:00');

    // July: New York is on daylight saving (EDT, UTC-4) → 08:00
    set(w, 'when', '2025-07-15T12:00');
    await wait(120);
    s.includes('tz: NY is 08:00 in July (DST)', w.document.getElementById('board').textContent, '08:00');

    s.check('tz: working-hours highlighting applied',
      w.document.querySelector('#board tbody tr[style*="success"]') !== null);
    s.noErrors(errors);
  }

  /* ---------- File Size ---------- */
  {
    const { window: w, errors } = await boot('tools/file-size-converter.html');

    set(w, 'value', '1');
    set(w, 'unit', 'TB', 'change');
    await wait(80);

    s.eq('filesize: 1 TB = 1e12 bytes', text(w, 'r-bytes'), '1,000,000,000,000');
    // The headline explanation: 1 TB decimal ≈ 931 GiB binary
    s.match('filesize: 1 TB ≈ 931 GiB', text(w, 'status'), /931\.32/);

    set(w, 'unit', 'GiB', 'change');
    set(w, 'value', '1');
    await wait(80);
    s.eq('filesize: 1 GiB = 1073741824 B', text(w, 'r-bytes'), '1,073,741,824');

    set(w, 'unit', 'MB', 'change');
    set(w, 'value', '100');
    set(w, 'speed', '100', 'change');
    await wait(80);
    // 100 MB over 100 Mbps at 90% efficiency ≈ 8.9 s
    s.match('filesize: transfer estimate', text(w, 'r-time'), /8\.\d seconds/);
    s.noErrors(errors);
  }

  /* ---------- Text to ASCII ---------- */
  {
    const { window: w, errors } = await boot('tools/text-to-ascii.html');

    set(w, 'input', 'Hi');
    set(w, 'format', 'dec', 'change');
    await wait(350);
    s.eq('ascii: Hi → 72 105', text(w, 'output'), '72 105');

    set(w, 'format', 'hex', 'change');
    await wait(350);
    s.eq('ascii: Hi → 48 69 hex', text(w, 'output'), '48 69');

    set(w, 'format', 'uni', 'change');
    await wait(350);
    s.eq('ascii: Hi → U+0048 U+0069', text(w, 'output'), 'U+0048 U+0069');

    set(w, 'format', 'html', 'change');
    await wait(350);
    s.eq('ascii: HTML entities', text(w, 'output'), '&#72; &#105;');

    // Astral-plane character: one code point, 4 UTF-8 bytes, 2 UTF-16 units
    set(w, 'input', '🌍');
    set(w, 'format', 'dec', 'change');
    await wait(350);
    s.eq('ascii: emoji single code point', text(w, 'output'), '127757');
    s.match('ascii: reports 4 UTF-8 bytes', text(w, 'status'), /4 UTF-8 byte/);
    s.match('ascii: reports 2 UTF-16 units', text(w, 'status'), /2 UTF-16 unit/);

    // Round trip
    set(w, 'direction', 'decode', 'change');
    set(w, 'input', '72 101 108 108 111');
    await wait(350);
    s.eq('ascii: decode decimal', text(w, 'output'), 'Hello');

    set(w, 'input', 'U+1F30D');
    await wait(350);
    s.eq('ascii: decode Unicode notation', text(w, 'output'), '🌍');

    set(w, 'input', '&#72;&#105;');
    await wait(350);
    s.eq('ascii: decode HTML entities', text(w, 'output'), 'Hi');

    set(w, 'input', 'not-a-codepoint');
    await wait(350);
    s.match('ascii: rejects junk', text(w, 'status'), /not a recognised code point/i);
    s.noErrors(errors);
  }

  return s;
};
