#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: tools_converter.py
# Purpose: The 10 Converters (ids 33-42).
# ============================================

from toolkit import (
 tool, ws, info, row, textarea, text_input, number_input, select, switch,
 output, status_line, buttons, readonly, STD_ACTIONS, HR, html_block,
)

PAGES = []

# ---------------------------------------------------------------
# 33. Unit Converter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="unit-converter", name="Unit Converter", icon="📏", cat="converter",
 title="Unit Converter: Length, Weight, Volume, Area, Speed and More",
 description="Convert length, weight, volume, area, speed, temperature, data and time between metric and imperial units with high precision.",
 tagline="Convert between metric and imperial units across eight measurement families.",
 workspace=ws(
 select("family", "What are you converting?", [
 ("length", "📏 Length"), ("mass", "⚖️ Weight / mass"), ("volume", "🧪 Volume"),
 ("area", "▦ Area"), ("speed", "🚀 Speed"), ("time", "⏱️ Time"),
 ("data", "💾 Digital storage"), ("pressure", "🌡️ Pressure"),
 ], selected="length"),
 row(
 html_block(""" <div class="field">
 <label class="field__label" for="from-value"><span>From</span></label>
 <input class="input" id="from-value" type="number" value="1" step="any" inputmode="decimal">
 <select class="select mt-2" id="from-unit" aria-label="Convert from unit"></select>
 </div>"""),
 html_block(""" <div class="field">
 <label class="field__label" for="to-value"><span>To</span></label>
 <input class="input" id="to-value" type="number" step="any" inputmode="decimal">
 <select class="select mt-2" id="to-unit" aria-label="Convert to unit"></select>
 </div>"""),
 ),
 buttons(("swap", "Swap units", "secondary"), ("copy", "Copy result", "primary"), ("share", "Share tool", "ghost")),
 status_line("status", "Enter a value to convert."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>All units</span><span class="field__hint">The same value in every unit</span></span>
 <div class="table-scroll"><div id="all-units"></div></div>
 </div>"""),
 label="Unit converter",
 ),
 info_block=info(
 features=[
 "Eight measurement families covering 60+ units",
 "Bidirectional, type into either box",
 "A full conversion table showing every unit at once",
 "Swap the two units with one click",
 "Precision preserved to 12 significant figures",
 ],
 howto=[
 "Choose what you are converting.",
 "Pick the source and target units.",
 "Type into either box, the other updates.",
 "Scroll down for the same value in every unit.",
 ],
 background_title="How the conversions are calculated",
 background_paragraphs=[
 "Every unit in a family is defined by its ratio to one base unit, metres for length, kilograms for mass, litres for volume. Converting from A to B means multiplying by A's ratio and dividing by B's. Chaining through a single base rather than storing every possible pair keeps the table small and, more importantly, keeps it consistent: there is no way for the metre-to-foot factor to disagree with the foot-to-metre one.",
 "The factors are exact where exact values exist. Since 1959 the international yard has been defined as precisely 0.9144 metres, which makes the inch exactly 25.4 millimetres and the mile exactly 1,609.344 metres. The pound is exactly 0.45359237 kilograms. These are definitional, not measured, so the only error is floating-point rounding.",
 "A few unit names are genuinely ambiguous and worth checking before you rely on a result. The US gallon (3.785 L) and imperial gallon (4.546 L) differ by 20%, and the same applies to pints and fluid ounces, this tool labels both explicitly. The ton is worse: a US short ton is 907 kg, a UK long ton is 1,016 kg, and a metric tonne is 1,000 kg. Digital storage carries its own ambiguity, covered in the file size converter.",
 ],
 ),
 script=r""" /**
 * Every unit expressed as a multiple of its family's base unit.
 * Base units: metre, kilogram, litre, square metre, metre/second,
 * second, byte, pascal.
 */
 const UNITS = {
 length: {
 base: 'm',
 units: {
 nm: ['Nanometre (nm)', 1e-9], um: ['Micrometre (µm)', 1e-6],
 mm: ['Millimetre (mm)', 0.001], cm: ['Centimetre (cm)', 0.01],
 m: ['Metre (m)', 1], km: ['Kilometre (km)', 1000],
 in: ['Inch (in)', 0.0254], ft: ['Foot (ft)', 0.3048],
 yd: ['Yard (yd)', 0.9144], mi: ['Mile (mi)', 1609.344],
 nmi: ['Nautical mile', 1852], ly: ['Light year', 9.4607304725808e15]
 }
 },
 mass: {
 base: 'kg',
 units: {
 mg: ['Milligram (mg)', 1e-6], g: ['Gram (g)', 0.001],
 kg: ['Kilogram (kg)', 1], t: ['Metric tonne (t)', 1000],
 oz: ['Ounce (oz)', 0.028349523125], lb: ['Pound (lb)', 0.45359237],
 st: ['Stone (st)', 6.35029318],
 ust: ['US short ton', 907.18474], ukt: ['UK long ton', 1016.0469088]
 }
 },
 volume: {
 base: 'L',
 units: {
 ml: ['Millilitre (ml)', 0.001], cl: ['Centilitre (cl)', 0.01],
 l: ['Litre (L)', 1], m3: ['Cubic metre (m³)', 1000],
 tsp: ['Teaspoon (US)', 0.00492892159375], tbsp: ['Tablespoon (US)', 0.01478676478125],
 floz: ['Fluid ounce (US)', 0.0295735295625], cup: ['Cup (US)', 0.2365882365],
 pt: ['Pint (US)', 0.473176473], qt: ['Quart (US)', 0.946352946],
 gal: ['Gallon (US)', 3.785411784], igal: ['Gallon (imperial)', 4.54609],
 ipt: ['Pint (imperial)', 0.56826125]
 }
 },
 area: {
 base: 'm²',
 units: {
 mm2: ['Square millimetre', 1e-6], cm2: ['Square centimetre', 1e-4],
 m2: ['Square metre (m²)', 1], ha: ['Hectare (ha)', 10000],
 km2: ['Square kilometre', 1e6], in2: ['Square inch', 0.00064516],
 ft2: ['Square foot', 0.09290304], yd2: ['Square yard', 0.83612736],
 ac: ['Acre', 4046.8564224], mi2: ['Square mile', 2589988.110336]
 }
 },
 speed: {
 base: 'm/s',
 units: {
 mps: ['Metres per second', 1], kph: ['Kilometres per hour', 1 / 3.6],
 mph: ['Miles per hour', 0.44704], fps: ['Feet per second', 0.3048],
 kn: ['Knot', 0.514444444444], mach: ['Mach (at sea level)', 340.29]
 }
 },
 time: {
 base: 's',
 units: {
 ms: ['Millisecond', 0.001], s: ['Second', 1], min: ['Minute', 60],
 h: ['Hour', 3600], d: ['Day', 86400], wk: ['Week', 604800],
 mo: ['Month (30 days)', 2592000], yr: ['Year (365 days)', 31536000]
 }
 },
 data: {
 base: 'B',
 units: {
 bit: ['Bit', 0.125], B: ['Byte', 1],
 KB: ['Kilobyte (1000 B)', 1e3], KiB: ['Kibibyte (1024 B)', 1024],
 MB: ['Megabyte (1000²)', 1e6], MiB: ['Mebibyte (1024²)', 1048576],
 GB: ['Gigabyte (1000³)', 1e9], GiB: ['Gibibyte (1024³)', 1073741824],
 TB: ['Terabyte (1000⁴)', 1e12], TiB: ['Tebibyte (1024⁴)', 1099511627776]
 }
 },
 pressure: {
 base: 'Pa',
 units: {
 Pa: ['Pascal (Pa)', 1], kPa: ['Kilopascal (kPa)', 1000],
 bar: ['Bar', 100000], atm: ['Atmosphere (atm)', 101325],
 psi: ['Pound per sq inch (psi)', 6894.757293168],
 mmHg: ['Millimetre of mercury', 133.322387415]
 }
 }
 };

 const DEFAULTS = {
 length: ['m', 'ft'], mass: ['kg', 'lb'], volume: ['l', 'gal'],
 area: ['m2', 'ft2'], speed: ['kph', 'mph'], time: ['h', 'min'],
 data: ['MB', 'MiB'], pressure: ['bar', 'psi']
 };

 /** Trim floating-point noise without losing genuine precision. */
 function tidy(n) {
 if (!isFinite(n)) return '';
 if (n === 0) return '0';
 const abs = Math.abs(n);
 if (abs < 1e-6 || abs >= 1e15) return n.toExponential(6);
 return String(Number(n.toPrecision(12)));
 }

 function populate() {
 const family = UNITS[T.$('family').value];
 const [defFrom, defTo] = DEFAULTS[T.$('family').value];

 ['from-unit', 'to-unit'].forEach((id, i) => {
 const sel = T.$(id);
 sel.innerHTML = '';
 for (const [key, [label]] of Object.entries(family.units)) {
 const opt = document.createElement('option');
 opt.value = key;
 opt.textContent = label;
 if (key === (i === 0 ? defFrom : defTo)) opt.selected = true;
 sel.append(opt);
 }
 });

 convert('from');
 }

 /**
 * Convert in the given direction.
 * @param {'from'|'to'} source - which box the user typed into
 */
 function convert(source) {
 const family = UNITS[T.$('family').value].units;
 const fromUnit = T.$('from-unit').value;
 const toUnit = T.$('to-unit').value;

 const srcId = source === 'from' ? 'from-value' : 'to-value';
 const dstId = source === 'from' ? 'to-value' : 'from-value';
 const srcUnit = source === 'from' ? fromUnit : toUnit;
 const dstUnit = source === 'from' ? toUnit : fromUnit;

 const value = T.num(T.$(srcId).value);

 if (isNaN(value)) {
 T.$(dstId).value = '';
 T.$('all-units').innerHTML = '';
 T.status('status', 'Enter a value to convert.', 'muted');
 return;
 }

 const inBase = value * family[srcUnit][1];
 const result = inBase / family[dstUnit][1];

 T.$(dstId).value = tidy(result);

 T.status('status',
 `${tidy(value)} ${family[srcUnit][0]} = ${tidy(result)} ${family[dstUnit][0]}`, 'ok');

 renderAll(inBase, family);
 }

 function renderAll(inBase, family) {
 const rows = Object.entries(family).map(([, [label, factor]]) =>
 [label, tidy(inBase / factor)]);
 const mount = T.$('all-units');
 mount.innerHTML = '';
 mount.append(T.table(['Unit', 'Value'], rows));
 }

 T.$('family').addEventListener('change', populate);
 T.$('from-value').addEventListener('input', () => convert('from'));
 T.$('to-value').addEventListener('input', () => convert('to'));
 T.on(['from-unit', 'to-unit'], () => convert('from'), 'change');

 T.$('swap').addEventListener('click', () => {
 const a = T.$('from-unit').value;
 T.$('from-unit').value = T.$('to-unit').value;
 T.$('to-unit').value = a;
 convert('from');
 });

 T.$('copy').addEventListener('click', () =>
 copyToClipboard(T.$('to-value').value, 'Result copied'));
 T.$('share').addEventListener('click', () => shareLink({ title: 'Unit Converter | 123MiniApps' }));

 populate();
 if (window.Analytics) Analytics.trackToolUse('unit-converter');""",
))

# ---------------------------------------------------------------
# 34. Temperature Converter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="temperature-converter", name="Temperature Converter", icon="🌡️", cat="converter",
 title="Temperature Converter: Celsius, Fahrenheit, Kelvin and Rankine",
 description="Convert between Celsius, Fahrenheit, Kelvin and Rankine instantly. All four scales update as you type, with reference points and absolute-zero validation.",
 tagline="Convert between Celsius, Fahrenheit, Kelvin and Rankine, all four update at once.",
 workspace=ws(
 row(
 number_input("celsius", "Celsius (°C)", "20", "20"),
 number_input("fahrenheit", "Fahrenheit (°F)", "68", "68"),
 ),
 row(
 number_input("kelvin", "Kelvin (K)", "293.15", "293.15"),
 number_input("rankine", "Rankine (°R)", "527.67", "527.67"),
 ),
 status_line("status", "Type into any box, the others follow."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Where this sits</span></span>
 <div id="context" class="output output--center">, </div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Reference points</span></span>
 <div class="table-scroll"><div id="reference"></div></div>
 </div>"""),
 buttons(("copy", "Copy all values", "primary"), ("share", "Share tool", "ghost")),
 label="Temperature converter",
 ),
 info_block=info(
 features=[
 "Four scales updating simultaneously",
 "Warns when you go below absolute zero",
 "Plain-English context for the temperature entered",
 "Reference table of familiar temperatures",
 "Handles negatives and decimals",
 ],
 howto=[
 "Type a temperature into any of the four boxes.",
 "The other three update immediately.",
 "Read the context line for a sense of scale.",
 "Copy all four values at once if you need them.",
 ],
 background_title="Where these scales come from",
 background_paragraphs=[
 "Celsius fixes 0 at the freezing point of water and 100 at its boiling point at standard atmospheric pressure, which makes it convenient for everyday use and for science. Fahrenheit's reference points are historical rather than natural: Daniel Fahrenheit set 0 at the freezing point of a brine solution and originally calibrated 96 to approximate human body temperature. The scales cross at −40, which is the same temperature in both.",
 "Kelvin starts at absolute zero, the point where classical thermal motion stops, and uses degrees the same size as Celsius, so K = °C + 273.15. It has no negative values by definition, which is why entering one here produces a warning. Rankine does the same for Fahrenheit-sized degrees, starting at absolute zero with °R = °F + 459.67. It survives mainly in some US engineering contexts.",
 "One notational detail: Kelvin takes no degree symbol and is written as 300 K rather than 300°K, because it measures absolute thermodynamic temperature rather than a position on a scale between two arbitrary reference points. Since 2019 the kelvin has been defined by fixing the Boltzmann constant, making it independent of any physical substance.",
 ],
 ),
 script=r""" let updating = false;

 const toC = {
 celsius: (v) => v,
 fahrenheit: (v) => (v - 32) * 5 / 9,
 kelvin: (v) => v - 273.15,
 rankine: (v) => (v - 491.67) * 5 / 9
 };

 const fromC = {
 celsius: (c) => c,
 fahrenheit: (c) => c * 9 / 5 + 32,
 kelvin: (c) => c + 273.15,
 rankine: (c) => (c + 273.15) * 9 / 5
 };

 const ABSOLUTE_ZERO_C = -273.15;

 const REFERENCES = [
 ['Absolute zero', -273.15],
 ['Nitrogen boils', -195.79],
 ['Dry ice sublimes', -78.5],
 ['Water freezes', 0],
 ['Refrigerator', 4],
 ['Room temperature', 20],
 ['Human body', 37],
 ['Hot bath', 40],
 ['Water boils', 100],
 ['Oven, moderate', 180],
 ['Paper ignites', 233]
 ];

 const tidy = (n) => Number(n.toFixed(4)).toString();

 /** Describe roughly what the temperature corresponds to. */
 function describe(c) {
 if (c < ABSOLUTE_ZERO_C) return 'Below absolute zero, physically impossible.';
 if (c < -100) return 'Cryogenic. Colder than anywhere on Earth’s surface.';
 if (c < -40) return 'Extreme polar cold. Exposed skin freezes in minutes.';
 if (c < 0) return 'Below freezing. Water turns to ice.';
 if (c < 10) return 'Cold. Winter coat weather.';
 if (c < 18) return 'Cool. A jumper would help.';
 if (c < 24) return 'Comfortable room temperature.';
 if (c < 30) return 'Warm. Pleasant summer day.';
 if (c < 40) return 'Hot. Above body temperature at the top of this range.';
 if (c < 100) return 'Very hot. Dangerous for sustained exposure.';
 if (c < 300) return 'Cooking temperatures.';
 return 'Industrial heat.';
 }

 function update(source) {
 if (updating) return;

 const raw = T.num(T.$(source).value);
 if (isNaN(raw)) {
 T.status('status', 'Type into any box, the others follow.', 'muted');
 return;
 }

 const celsius = toC[source](raw);

 updating = true;
 for (const id of ['celsius', 'fahrenheit', 'kelvin', 'rankine']) {
 if (id !== source) T.$(id).value = tidy(fromC[id](celsius));
 }
 updating = false;

 T.$('context').textContent = describe(celsius);

 if (celsius < ABSOLUTE_ZERO_C - 1e-9) {
 T.status('status', 'That is below absolute zero (−273.15 °C / 0 K).', 'error');
 T.$('context').style.color = 'var(--danger)';
 } else {
 T.status('status',
 `${tidy(celsius)} °C = ${tidy(fromC.fahrenheit(celsius))} °F = ${tidy(fromC.kelvin(celsius))} K`, 'ok');
 T.$('context').style.color = '';
 }

 renderReference(celsius);
 }

 function renderReference(current) {
 const mount = T.$('reference');
 mount.innerHTML = '';
 mount.append(T.table(
 ['Reference', '°C', '°F', 'Difference'],
 REFERENCES.map(([label, c]) => [
 label,
 tidy(c),
 tidy(fromC.fahrenheit(c)),
 (current > c ? '+' : '') + tidy(current - c) + ' °C'
 ])
 ));
 }

 ['celsius', 'fahrenheit', 'kelvin', 'rankine'].forEach((id) => {
 T.$(id).addEventListener('input', () => update(id));
 });

 T.$('copy').addEventListener('click', () => {
 const text = ['celsius', 'fahrenheit', 'kelvin', 'rankine']
 .map((id) => `${id[0].toUpperCase() + id.slice(1)}: ${T.$(id).value}`).join('\n');
 copyToClipboard(text, 'All values copied');
 });
 T.$('share').addEventListener('click', () => shareLink({ title: 'Temperature Converter | 123MiniApps' }));

 update('celsius');
 if (window.Analytics) Analytics.trackToolUse('temperature-converter');""",
))

# ---------------------------------------------------------------
# 35. CSV to JSON
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="csv-to-json", name="CSV to JSON", icon="📊", cat="converter",
 title="CSV to JSON Converter: Both Directions, Quoted Fields Handled",
 description="Convert CSV data to structured JSON and back again. Handles quoted fields, embedded commas and custom delimiters. Runs entirely in your browser.",
 tagline="Convert CSV to JSON and back, with correct handling of quoted fields and embedded commas.",
 workspace=ws(
 select("direction", "Direction", [("csv2json", "CSV → JSON"), ("json2csv", "JSON → CSV")], selected="csv2json"),
 textarea("input", "Input", "name,age,city\nAda,36,London\nAlan,41,\"Wilmslow, Cheshire\"", "input-stats", rows=200),
 row(
 select("delimiter", "Delimiter", [(",", "Comma,"), (";", "Semicolon ;"), ("\\t", "Tab"), ("|", "Pipe |")], selected=","),
 switch("header", "First row contains column names", True),
 switch("typed", "Convert numbers and booleans automatically", True),
 ),
 status_line("status", "Paste CSV data to convert it."),
 HR,
 output("output", "Result", "output-stats"),
 buttons(("convert", "Convert", "primary"), ("sample", "Load sample"), ("copy", "Copy result"), ("download", "Download"), ("share", "Share tool", "ghost")),
 label="CSV to JSON converter",
 ),
 info_block=info(
 features=[
 "Both directions, CSV to JSON and JSON to CSV",
 "RFC 4180 quoted fields with embedded commas and newlines",
 "Four delimiter options including tab-separated",
 "Optional automatic type detection",
 "Headerless mode produces arrays instead of objects",
 ],
 howto=[
 "Pick a direction and paste your data.",
 "Confirm the delimiter and whether row one is a header.",
 "Press Convert.",
 "Copy the result or download it as a file.",
 ],
 background_title="Why CSV parsing is trickier than splitting on commas",
 background_paragraphs=[
 "The naive approach, splitting each line on commas, breaks on the first field that contains one. RFC 4180 allows any field to be wrapped in double quotes, and a quoted field may contain commas, line breaks and even quotes, provided each embedded quote is doubled. So <code>\"Wilmslow, Cheshire\"</code> is one field, and <code>\"She said \"\"hi\"\"\"</code> is the single value <code>She said \"hi\"</code>.",
 "That last rule means you cannot process CSV line by line either. A quoted field containing a newline spans multiple physical lines while remaining one logical record. This parser walks the input character by character tracking whether it is inside quotes, which handles all of these cases correctly.",
 "Type detection is convenient but occasionally destructive, which is why it is a toggle. Turning it on converts <code>42</code> to a number and <code>true</code> to a boolean, usually what you want. But it also converts a US zip code like <code>02134</code> to the number 2134, losing the leading zero, and can mangle long identifiers that exceed JavaScript's safe integer range. Turn it off when your columns contain codes rather than quantities.",
 ],
 ),
 script=r""" let lastResult = '';

 const SAMPLE_CSV = 'name,role,year,active\n' +
 'Ada Lovelace,Mathematician,1843,true\n' +
 'Alan Turing,Computer scientist,1936,true\n' +
 '"Hopper, Grace",Rear Admiral,1952,false';

 const SAMPLE_JSON = JSON.stringify([
 { name: 'Ada Lovelace', role: 'Mathematician', year: 1843 },
 { name: 'Alan Turing', role: 'Computer scientist', year: 1936 }
 ], null, 2);

 function delimiter() {
 const v = T.$('delimiter').value;
 return v === '\\t' ? '\t' : v;
 }

 /**
 * Parse CSV per RFC 4180, character by character, so quoted
 * fields containing delimiters and newlines survive intact.
 * @param {string} text
 * @param {string} sep
 * @returns {string[][]}
 */
 function parseCSV(text, sep) {
 const rows = [];
 let row = [];
 let field = '';
 let inQuotes = false;

 for (let i = 0; i < text.length; i++) {
 const ch = text[i];

 if (inQuotes) {
 if (ch === '"') {
 if (text[i + 1] === '"') { field += '"'; i++; } // escaped quote
 else inQuotes = false;
 } else {
 field += ch;
 }
 continue;
 }

 if (ch === '"') { inQuotes = true; }
 else if (ch === sep) { row.push(field); field = ''; }
 else if (ch === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
 else if (ch === '\r') { /* handled by the \n branch */ }
 else field += ch;
 }

 if (field !== '' || row.length) { row.push(field); rows.push(row); }
 return rows.filter((r) => r.length && !(r.length === 1 && r[0] === ''));
 }

 /** Quote a field only when it needs it. */
 function quote(value, sep) {
 const s = value == null ? '' : String(value);
 return /["\n\r]/.test(s) || s.includes(sep)
 ? '"' + s.replace(/"/g, '""') + '"'
 : s;
 }

 /** Best-effort type coercion for CSV cells. */
 function coerce(v) {
 if (!T.$('typed').checked) return v;
 const s = v.trim();
 if (s === '') return '';
 if (s === 'true') return true;
 if (s === 'false') return false;
 if (s === 'null') return null;
 // Only convert numbers that round-trip exactly, protects leading zeros
 if (/^-?\d+(\.\d+)?$/.test(s) && String(Number(s)) === s) return Number(s);
 return v;
 }

 function csvToJson() {
 const rows = parseCSV(T.$('input').value.trim(), delimiter());
 if (!rows.length) throw new Error('No rows found.');

 if (!T.$('header').checked) {
 return JSON.stringify(rows.map((r) => r.map(coerce)), null, 2);
 }

 const headers = rows[0].map((h) => h.trim());
 const out = rows.slice(1).map((row) => {
 const obj = {};
 headers.forEach((h, i) => { obj[h] = coerce(row[i] === undefined ? '' : row[i]); });
 return obj;
 });

 return JSON.stringify(out, null, 2);
 }

 function jsonToCsv() {
 const data = JSON.parse(T.$('input').value);
 const rows = Array.isArray(data) ? data : [data];
 if (!rows.length) throw new Error('The array is empty.');

 const sep = delimiter();

 // Arrays of arrays convert straight across
 if (Array.isArray(rows[0])) {
 return rows.map((r) => r.map((c) => quote(c, sep)).join(sep)).join('\n');
 }

 // Union of keys across all objects, so sparse records still line up
 const headers = [...new Set(rows.flatMap((r) => Object.keys(r)))];
 const lines = [headers.map((h) => quote(h, sep)).join(sep)];

 for (const row of rows) {
 lines.push(headers.map((h) => {
 const v = row[h];
 return quote(v !== null && typeof v === 'object' ? JSON.stringify(v) : v, sep);
 }).join(sep));
 }

 return lines.join('\n');
 }

 function convert() {
 const raw = T.$('input').value.trim();
 T.$('input-stats').textContent = raw ? raw.split(/\n/).length + ' lines' : '';

 if (!raw) {
 lastResult = '';
 T.setOutput('output', '');
 T.status('status', 'Paste data to convert it.', 'muted');
 return;
 }

 const toJson = T.$('direction').value === 'csv2json';

 try {
 lastResult = toJson ? csvToJson() : jsonToCsv();
 T.setOutput('output', lastResult);
 T.$('output-stats').textContent = lastResult.length.toLocaleString() + ' characters';

 const count = toJson
 ? (JSON.parse(lastResult).length)
 : lastResult.split('\n').length - (T.$('header').checked ? 1 : 0);
 T.status('status', `Converted ${count} record(s).`, 'ok');
 } catch (err) {
 lastResult = '';
 T.setOutput('output', '');
 T.status('status', 'Could not convert: ' + err.message, 'error');
 }
 }

 T.$('input').addEventListener('input', debounce(convert, 350));
 T.on(['direction', 'delimiter', 'header', 'typed'], convert, 'change');
 T.$('convert').addEventListener('click', convert);

 T.$('sample').addEventListener('click', () => {
 T.$('input').value = T.$('direction').value === 'csv2json' ? SAMPLE_CSV : SAMPLE_JSON;
 convert();
 });

 T.wireActions({
 slug: 'csv-to-json',
 getResult: () => lastResult,
 filename: 'converted.json'
 });

 convert();""",
))

# ---------------------------------------------------------------
# 36. Timestamp Converter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="timestamp-converter", name="Timestamp Converter", icon="🕐", cat="converter",
 title="Unix Timestamp Converter: Epoch to Date and Back",
 description="Convert Unix timestamps to readable dates and back. Seconds or milliseconds, any timezone, ISO 8601 output and a live current timestamp.",
 tagline="Convert Unix timestamps to dates and back, seconds, milliseconds, any timezone.",
 workspace=ws(
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="now-s" style="font-size:var(--text-2xl)">, </span><span class="result__label">Current timestamp (s)</span></div>
 <div class="result"><span class="result__value" id="now-ms" style="font-size:var(--text-2xl)">, </span><span class="result__label">Current timestamp (ms)</span></div>
 </div>"""),
 HR,
 row(
 text_input("timestamp", "Unix timestamp", "1735689600"),
 select("unit", "Units", [("auto", "Detect automatically"), ("s", "Seconds"), ("ms", "Milliseconds")], selected="auto"),
 ),
 row(
 text_input("datetime", "Date and time", "2025-01-01T00:00", "", "datetime-local"),
 select("timezone", "Timezone", [("local", "Your local timezone"), ("UTC", "UTC")], selected="local"),
 ),
 status_line("status", "Enter a timestamp or pick a date."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>All formats</span></span>
 <div class="table-scroll"><div id="formats"></div></div>
 </div>"""),
 buttons(("use-now", "Use current time", "primary"), ("copy", "Copy all formats"), ("share", "Share tool", "ghost")),
 label="Timestamp converter",
 ),
 info_block=info(
 features=[
 "Live current timestamp in seconds and milliseconds",
 "Automatic detection of seconds versus milliseconds",
 "Local timezone or UTC",
 "ISO 8601, RFC 2822 and relative-time output",
 "Relative description such as “3 days ago”",
 ],
 howto=[
 "Paste a Unix timestamp into the first box.",
 "Or pick a date and time to get its timestamp.",
 "Switch between your timezone and UTC.",
 "Copy every format at once from the button below.",
 ],
 background_title="Understanding Unix time",
 background_paragraphs=[
 "A Unix timestamp counts the seconds since 1 January 1970 at 00:00:00 UTC, a moment called the epoch. Because it is a single integer anchored to UTC, it sidesteps timezones, daylight saving and calendar formatting entirely, which is exactly why it remains the default way to store an instant in databases, log files and APIs.",
 "The main confusion is seconds versus milliseconds. Unix tooling, most databases and JSON APIs use seconds; JavaScript's <code>Date.now()</code> returns milliseconds. A millisecond value interpreted as seconds lands roughly 50,000 years in the future, which is a common and very visible bug. This tool detects the difference by magnitude: values above about 100 billion are almost certainly milliseconds.",
 "Two edge cases are worth knowing. Unix time deliberately ignores leap seconds, so it is not a true count of elapsed SI seconds since the epoch, a leap second repeats the same timestamp value. And systems storing timestamps in a signed 32-bit integer overflow on 19 January 2038, the Year 2038 problem. Most modern systems have moved to 64-bit, but embedded and legacy code has not always followed.",
 ],
 ),
 script=r""" let clockTimer = null;

 function tickClock() {
 const now = Date.now();
 T.$('now-s').textContent = Math.floor(now / 1000).toLocaleString('en-US', { useGrouping: false });
 T.$('now-ms').textContent = String(now);
 }

 /** Interpret the entered timestamp, honouring the units setting. */
 function parseTimestamp(raw) {
 const n = Number(String(raw).trim());
 if (!isFinite(n)) return null;

 const unit = T.$('unit').value;
 if (unit === 's') return n * 1000;
 if (unit === 'ms') return n;

 // Auto: anything past ~5138 AD in seconds is really milliseconds
 return Math.abs(n) > 1e11 ? n : n * 1000;
 }

 /** Human-readable "3 days ago" / "in 2 hours". */
 function relative(ms) {
 const diff = ms - Date.now();
 const abs = Math.abs(diff);
 const units = [
 ['year', 31536000000], ['month', 2592000000], ['day', 86400000],
 ['hour', 3600000], ['minute', 60000], ['second', 1000]
 ];

 for (const [name, size] of units) {
 if (abs >= size || name === 'second') {
 const n = Math.round(abs / size);
 const plural = n === 1 ? '' : 's';
 return diff < 0 ? `${n} ${name}${plural} ago` : `in ${n} ${name}${plural}`;
 }
 }
 return 'now';
 }

 function render(ms, source) {
 if (!isFinite(ms)) {
 T.status('status', 'That is not a valid timestamp.', 'error');
 return;
 }

 const date = new Date(ms);
 if (isNaN(date.getTime())) {
 T.status('status', 'That timestamp is out of range.', 'error');
 return;
 }

 const utc = T.$('timezone').value === 'UTC';
 const opts = utc ? { timeZone: 'UTC' } : {};

 // Sync whichever field the user did not edit
 if (source !== 'timestamp') {
 T.$('timestamp').value = String(Math.floor(ms / 1000));
 }
 if (source !== 'datetime') {
 const iso = new Date(ms - (utc ? 0 : date.getTimezoneOffset() * 60000)).toISOString();
 T.$('datetime').value = iso.slice(0, 16);
 }

 const rows = [
 ['Unix seconds', String(Math.floor(ms / 1000))],
 ['Unix milliseconds', String(ms)],
 ['ISO 8601 (UTC)', date.toISOString()],
 ['RFC 2822', date.toUTCString()],
 ['Local string', date.toLocaleString(undefined, opts)],
 ['Date only', date.toLocaleDateString(undefined, opts)],
 ['Time only', date.toLocaleTimeString(undefined, opts)],
 ['Day of week', date.toLocaleDateString(undefined, { ...opts, weekday: 'long' })],
 ['Relative', relative(ms)]
 ];

 const mount = T.$('formats');
 mount.innerHTML = '';
 mount.append(T.table(['Format', 'Value'], rows));

 T.status('status', `${date.toISOString()}, ${relative(ms)}`, 'ok');
 }

 T.$('timestamp').addEventListener('input', () => {
 const ms = parseTimestamp(T.$('timestamp').value);
 if (ms !== null) render(ms, 'timestamp');
 });

 T.$('datetime').addEventListener('input', () => {
 const v = T.$('datetime').value;
 if (!v) return;
 const ms = T.$('timezone').value === 'UTC'
 ? Date.parse(v + ':00Z')
 : new Date(v).getTime();
 if (isFinite(ms)) render(ms, 'datetime');
 });

 T.on(['unit', 'timezone'], () => {
 const ms = parseTimestamp(T.$('timestamp').value);
 if (ms !== null) render(ms, 'timestamp');
 }, 'change');

 T.$('use-now').addEventListener('click', () => {
 T.$('timestamp').value = String(Math.floor(Date.now() / 1000));
 render(Date.now(), 'timestamp');
 });

 T.$('copy').addEventListener('click', () => {
 const rows = T.$$('#formats tbody tr').map((tr) =>
 [...tr.children].map((td) => td.textContent).join(': '));
 copyToClipboard(rows.join('\n'), 'All formats copied');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Timestamp Converter | 123MiniApps' }));

 tickClock();
 clockTimer = setInterval(tickClock, 1000);
 window.addEventListener('beforeunload', () => clearInterval(clockTimer));

 render(Date.now(), null);
 if (window.Analytics) Analytics.trackToolUse('timestamp-converter');""",
))

# ---------------------------------------------------------------
# 37. Number Base Converter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="number-base-converter", name="Number Base Converter", icon="🔢", cat="converter",
 title="Number Base Converter: Binary, Octal, Decimal and Hexadecimal",
 description="Convert numbers between binary, octal, decimal, hexadecimal and any base from 2 to 36. All fields update together, with bit-length display.",
 tagline="Convert between binary, octal, decimal, hex and any base from 2 to 36.",
 workspace=ws(
 row(
 text_input("dec", "Decimal (base 10)", "255", "255"),
 text_input("hex", "Hexadecimal (base 16)", "FF", "FF"),
 ),
 row(
 text_input("oct", "Octal (base 8)", "377", "377"),
 text_input("bin", "Binary (base 2)", "11111111", "11111111"),
 ),
 HR,
 row(
 text_input("custom", "Custom base value", "e.g. z1"),
 html_block(""" <div class="field">
 <label class="field__label" for="custom-base">
 <span>Custom base</span>
 <span class="field__hint"><strong id="custom-base-value">36</strong></span>
 </label>
 <input class="range" id="custom-base" type="range" min="2" max="36" value="36" step="1">
 </div>"""),
 ),
 status_line("status", "Type into any field, the rest follow."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-bits" style="font-size:var(--text-2xl)">8</span><span class="result__label">Bits needed</span></div>
 <div class="result"><span class="result__value" id="r-bytes" style="font-size:var(--text-2xl)">1</span><span class="result__label">Bytes</span></div>
 <div class="result"><span class="result__value" id="r-fits" style="font-size:var(--text-lg)">uint8</span><span class="result__label">Smallest type</span></div>
 </div>"""),
 buttons(("copy", "Copy all bases", "primary"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
 label="Number base converter",
 ),
 info_block=info(
 features=[
 "Binary, octal, decimal and hexadecimal at once",
 "Any custom base from 2 to 36",
 "Bit and byte width calculation",
 "Smallest fitting integer type",
 "Rejects digits that are invalid for the base",
 ],
 howto=[
 "Type a number into whichever base you have.",
 "Every other field updates immediately.",
 "Use the slider for an unusual base.",
 "Copy all representations at once.",
 ],
 background_title="Why these particular bases",
 background_paragraphs=[
 "Binary is how hardware actually works, since a transistor is either conducting or not. It becomes unreadable quickly though, a single 32-bit value is 32 characters of ones and zeros with no visual structure, and miscounting a run of them is easy.",
 "Hexadecimal solves that by being a compact, lossless view of binary. Because 16 is 2⁴, exactly one hex digit maps to exactly four bits, so you can convert between the two by inspection with no arithmetic. One byte is always two hex digits. That direct correspondence is why memory addresses, colour codes, hashes and byte dumps are all written in hex.",
 "Octal has the same property with three bits per digit, and survives mainly in Unix file permissions, where the read, write and execute bits form natural groups of three, <code>chmod 755</code> is really <code>111 101 101</code>. Bases beyond 16 borrow letters and appear in URL shorteners and identifier encodings, where base 36 packs a number into the shortest string using only digits and letters.",
 ],
 ),
 script=r""" const FIELDS = { bin: 2, oct: 8, dec: 10, hex: 16 };
 let updating = false;
 let current = 255n;

 const DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz';

 /**
 * Parse a string in an arbitrary base into a BigInt.
 * BigInt keeps very large values exact, which Number would not.
 * @returns {bigint|null} null if any digit is invalid for the base
 */
 function parseBase(str, base) {
 const s = String(str).trim().toLowerCase().replace(/^[+]/, '');
 if (!s) return null;

 const negative = s.startsWith('-');
 const body = negative ? s.slice(1) : s;
 if (!body) return null;

 let value = 0n;
 const b = BigInt(base);

 for (const ch of body) {
 const digit = DIGITS.indexOf(ch);
 if (digit < 0 || digit >= base) return null;
 value = value * b + BigInt(digit);
 }

 return negative ? -value : value;
 }

 /** Render a BigInt in an arbitrary base. */
 function toBase(value, base) {
 if (value === 0n) return '0';
 const negative = value < 0n;
 let v = negative ? -value : value;
 const b = BigInt(base);
 let out = '';

 while (v > 0n) {
 out = DIGITS[Number(v % b)] + out;
 v /= b;
 }

 return (negative ? '-' : '') + out;
 }

 function smallestType(bits, negative) {
 const widths = [8, 16, 32, 64];
 for (const w of widths) {
 if (negative ? bits < w : bits <= w) return (negative ? 'int' : 'uint') + w;
 }
 return 'bigint';
 }

 function sync(source) {
 if (updating) return;

 const base = source === 'custom' ? Number(T.$('custom-base').value) : FIELDS[source];
 const value = parseBase(T.$(source).value, base);

 if (value === null) {
 T.status('status', `That is not a valid base-${base} number.`, 'error');
 T.$(source).classList.add('is-invalid');
 return;
 }

 T.$(source).classList.remove('is-invalid');
 current = value;

 updating = true;
 for (const [id, b] of Object.entries(FIELDS)) {
 if (id !== source) T.$(id).value = toBase(value, b).toUpperCase();
 }
 if (source !== 'custom') {
 T.$('custom').value = toBase(value, Number(T.$('custom-base').value));
 }
 updating = false;

 const magnitude = value < 0n ? -value : value;
 const bits = magnitude === 0n ? 1 : toBase(magnitude, 2).length;

 T.$('r-bits').textContent = String(bits);
 T.$('r-bytes').textContent = String(Math.ceil(bits / 8));
 T.$('r-fits').textContent = smallestType(bits, value < 0n);

 T.status('status', `Decimal ${toBase(value, 10)} · ${bits} bit(s).`, 'ok');
 }

 Object.keys(FIELDS).forEach((id) => {
 T.$(id).addEventListener('input', () => sync(id));
 });

 T.$('custom').addEventListener('input', () => sync('custom'));

 T.$('custom-base').addEventListener('input', () => {
 T.$('custom-base-value').textContent = T.$('custom-base').value;
 updating = true;
 T.$('custom').value = toBase(current, Number(T.$('custom-base').value));
 updating = false;
 });

 T.$('copy').addEventListener('click', () => {
 const base = Number(T.$('custom-base').value);
 copyToClipboard(
 `Decimal: ${T.$('dec').value}\nHex: ${T.$('hex').value}\n` +
 `Octal: ${T.$('oct').value}\nBinary: ${T.$('bin').value}\n` +
 `Base ${base}: ${T.$('custom').value}`,
 'All bases copied'
 );
 });

 T.$('clear').addEventListener('click', () => {
 updating = true;
 ['bin', 'oct', 'dec', 'hex', 'custom'].forEach((id) => {
 T.$(id).value = '';
 T.$(id).classList.remove('is-invalid');
 });
 updating = false;
 T.status('status', 'Type into any field, the rest follow.', 'muted');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Number Base Converter | 123MiniApps' }));

 sync('dec');
 if (window.Analytics) Analytics.trackToolUse('number-base-converter');""",
))

# ---------------------------------------------------------------
# 38. Roman Numeral Converter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="roman-numeral-converter", name="Roman Numeral Converter", icon="🏛️", cat="converter",
 title="Roman Numeral Converter: Numbers to Roman Numerals and Back",
 description="Convert numbers to Roman numerals and Roman numerals back to numbers, with strict validation that rejects malformed forms like IIII and VX.",
 tagline="Convert numbers to Roman numerals and back, with strict validation of the result.",
 workspace=ws(
 row(
 text_input("number", "Number", "2026", "2026", "number", attrs='min="1" max="3999"'),
 text_input("roman", "Roman numeral", "MMXXVI", "MMXXVI"),
 ),
 status_line("status", "Type into either box."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>How it breaks down</span></span>
 <div class="table-scroll"><div id="breakdown"></div></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>The symbols</span></span>
 <div class="chip-grid" id="symbols"></div>
 </div>"""),
 buttons(("copy", "Copy numeral", "primary"), ("year", "This year"), ("share", "Share tool", "ghost")),
 label="Roman numeral converter",
 ),
 info_block=info(
 features=[
 "Both directions with live updating",
 "Strict validation rejecting malformed numerals",
 "Symbol-by-symbol breakdown of the conversion",
 "Covers 1 to 3,999 in standard notation",
 "One-click conversion of the current year",
 ],
 howto=[
 "Type a number from 1 to 3999 on the left.",
 "Or type a Roman numeral on the right.",
 "The other box updates immediately.",
 "The table below shows how the value decomposes.",
 ],
 background_title="The rules of Roman numerals",
 background_paragraphs=[
 "Seven symbols carry all the values: I is 1, V is 5, X is 10, L is 50, C is 100, D is 500 and M is 1,000. Numerals are written largest to smallest and added together, so MMXXVI is 1000 + 1000 + 10 + 10 + 5 + 1 = 2026.",
 "Subtractive notation is the complication. Placing a smaller symbol before a larger one subtracts it, so IV is 4 rather than IIII. But only six subtractive pairs are valid, IV, IX, XL, XC, CD and CM, and only powers of ten may be subtracted, from the next two values up. That rules out IL for 49, which must be written XLIX. This converter enforces those rules, so pasting in a malformed numeral produces an error rather than a silently wrong number.",
 "Standard notation stops at 3,999, because expressing 4,000 would need four Ms. Larger values historically used a vinculum, an overbar multiplying a numeral by 1,000, but that convention was never fully standardised and does not render reliably in plain text, so this tool caps at MMMCMXCIX. There is also no zero: the concept simply had no symbol in the system, which is one reason Roman numerals are hopeless for arithmetic.",
 ],
 ),
 script=r""" const VALUES = [
 [1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'],
 [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'],
 [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I']
 ];

 const SYMBOLS = [['I', 1], ['V', 5], ['X', 10], ['L', 50], ['C', 100], ['D', 500], ['M', 1000]];

 // Canonical form, this is what makes IIII and IL invalid
 const VALID = /^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$/;

 let updating = false;

 /**
 * @param {number} n 1-3999
 * @returns {{numeral: string, parts: [number, string][]}}
 */
 function toRoman(n) {
 let remaining = Math.floor(n);
 let numeral = '';
 const parts = [];

 for (const [value, symbol] of VALUES) {
 while (remaining >= value) {
 numeral += symbol;
 parts.push([value, symbol]);
 remaining -= value;
 }
 }

 return { numeral, parts };
 }

 /**
 * @param {string} s
 * @returns {number|null} null when the numeral is malformed
 */
 function fromRoman(s) {
 const str = String(s).trim().toUpperCase();
 if (!str) return null;
 if (!VALID.test(str)) return null;

 const map = Object.fromEntries(SYMBOLS);
 let total = 0;

 for (let i = 0; i < str.length; i++) {
 const value = map[str[i]];
 const next = map[str[i + 1]];
 // A smaller symbol before a larger one subtracts
 total += next && value < next ? -value : value;
 }

 return total;
 }

 function renderBreakdown(parts, total) {
 const mount = T.$('breakdown');
 mount.innerHTML = '';
 if (!parts.length) return;

 let running = 0;
 mount.append(T.table(
 ['Symbol', 'Value', 'Running total'],
 parts.map(([value, symbol]) => {
 running += value;
 return [symbol, value.toLocaleString(), running.toLocaleString()];
 })
 ));
 void total;
 }

 function fromNumber() {
 if (updating) return;

 const n = T.num(T.$('number').value);

 if (isNaN(n) || n < 1 || n > 3999 || n !== Math.floor(n)) {
 T.status('status', 'Enter a whole number between 1 and 3999.', 'error');
 T.$('breakdown').innerHTML = '';
 return;
 }

 const { numeral, parts } = toRoman(n);

 updating = true;
 T.$('roman').value = numeral;
 updating = false;

 T.$('roman').classList.remove('is-invalid');
 renderBreakdown(parts, n);
 T.status('status', `${n.toLocaleString()} = ${numeral}`, 'ok');
 }

 function fromNumeral() {
 if (updating) return;

 const raw = T.$('roman').value;
 const n = fromRoman(raw);

 if (n === null) {
 T.$('roman').classList.add('is-invalid');
 T.status('status',
 raw.trim() ? `“${raw.toUpperCase()}” is not a valid Roman numeral.` : 'Type into either box.',
 raw.trim() ? 'error' : 'muted');
 T.$('breakdown').innerHTML = '';
 return;
 }

 T.$('roman').classList.remove('is-invalid');

 updating = true;
 T.$('number').value = String(n);
 updating = false;

 renderBreakdown(toRoman(n).parts, n);
 T.status('status', `${raw.toUpperCase()} = ${n.toLocaleString()}`, 'ok');
 }

 T.$('number').addEventListener('input', fromNumber);
 T.$('roman').addEventListener('input', fromNumeral);

 T.$('year').addEventListener('click', () => {
 T.$('number').value = String(new Date().getFullYear());
 fromNumber();
 });

 T.$('copy').addEventListener('click', () => copyToClipboard(T.$('roman').value, 'Numeral copied'));
 T.$('share').addEventListener('click', () => shareLink({ title: 'Roman Numeral Converter | 123MiniApps' }));

 // Symbol reference chips
 const chips = T.$('symbols');
 SYMBOLS.forEach(([sym, val]) => {
 chips.append(el('span', { className: 'chip', text: `${sym} = ${val.toLocaleString()}` }));
 });

 fromNumber();
 if (window.Analytics) Analytics.trackToolUse('roman-numeral-converter');""",
))

# ---------------------------------------------------------------
# 39. Currency Converter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="currency-converter", name="Currency Converter", icon="💱", cat="converter",
 title="Currency Converter: Offline, With Rates You Control",
 description="Convert between currencies using rates you enter yourself. No live feed and no tracking, useful when you need a repeatable rate rather than today's.",
 tagline="Convert currencies using rates you set, repeatable, offline and private.",
 workspace=ws(
 html_block(""" <p class="field__hint" style="color:var(--warning)">
 This tool does <strong>not</strong> fetch live exchange rates. Doing so would mean calling an external
 service on every keystroke, which would break the promise that nothing leaves your device.
 Instead you enter the rate yourself, from your bank, your accounting system, or the rate agreed
 for a contract. That also makes results reproducible, which live rates are not.
 </p>"""),
 HR,
 row(
 number_input("amount", "Amount", "100", "100"),
 select("from", "From", [], selected=None),
 select("to", "To", [], selected=None),
 ),
 row(
 number_input("rate", "Rate, 1 unit of “From” equals", "0.85", "0.85"),
 html_block(""" <div class="field">
 <span class="field__label"><span>Inverse rate</span></span>
 <input class="input font-mono" id="inverse" type="text" readonly
 aria-label="Inverse exchange rate">
 </div>"""),
 ),
 status_line("status", "Enter an amount and a rate."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-out">, </span><span class="result__label">Converted amount</span></div>
 <div class="result"><span class="result__value" id="r-fee" style="font-size:var(--text-2xl)">, </span><span class="result__label">After a 2.5% fee</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Saved rates</span><span class="field__hint">Stored on this device only</span></span>
 <div class="chip-grid" id="saved"></div>
 </div>"""),
 buttons(("save", "Save this rate", "primary"), ("swap", "Swap currencies"), ("copy", "Copy result"), ("share", "Share tool", "ghost")),
 label="Currency converter",
 ),
 info_block=info(
 features=[
 "35 major currencies with correct symbols and decimal places",
 "You control the rate, results are reproducible",
 "Automatic inverse rate calculation",
 "Shows the effect of a typical 2.5% conversion fee",
 "Save frequently used rates on your device",
 ],
 howto=[
 "Pick the two currencies and enter an amount.",
 "Enter the rate from your bank or accounting system.",
 "Read the converted amount below.",
 "Save the rate if you will use it again.",
 ],
 background_title="Why the headline rate is not what you get",
 background_paragraphs=[
 "The rate quoted on financial news sites is the interbank mid-market rate, the midpoint between what buyers bid and sellers ask in the wholesale market. Almost nobody transacting retail amounts receives it. Banks and card networks apply a spread on top, then sometimes a separate fee, so the effective rate is typically 1% to 4% worse than the mid-market figure.",
 "Dynamic currency conversion is the version worth actively refusing. When a foreign card terminal offers to charge you in your home currency, it is applying its own rate with a markup often exceeding 5%. Choosing the local currency and letting your own bank convert is nearly always cheaper.",
 "For accounting purposes the date matters as much as the rate. Most jurisdictions require you to record a transaction at the rate on the transaction date, not the date you noticed it, and many tax authorities publish official monthly or annual rates that must be used instead of market ones. Entering the rate manually, rather than pulling whatever is live right now, is what makes this tool usable for that.",
 ],
 ),
 script=r""" const CURRENCIES = [
 ['USD', 'US Dollar', '$', 2], ['EUR', 'Euro', '€', 2], ['GBP', 'British Pound', '£', 2],
 ['JPY', 'Japanese Yen', '¥', 0], ['CNY', 'Chinese Yuan', '¥', 2], ['INR', 'Indian Rupee', '₹', 2],
 ['AUD', 'Australian Dollar', 'A$', 2], ['CAD', 'Canadian Dollar', 'C$', 2],
 ['CHF', 'Swiss Franc', 'CHF', 2], ['HKD', 'Hong Kong Dollar', 'HK$', 2],
 ['SGD', 'Singapore Dollar', 'S$', 2], ['SEK', 'Swedish Krona', 'kr', 2],
 ['NOK', 'Norwegian Krone', 'kr', 2], ['DKK', 'Danish Krone', 'kr', 2],
 ['NZD', 'New Zealand Dollar', 'NZ$', 2], ['KRW', 'South Korean Won', '₩', 0],
 ['MXN', 'Mexican Peso', '$', 2], ['BRL', 'Brazilian Real', 'R$', 2],
 ['ZAR', 'South African Rand', 'R', 2], ['RUB', 'Russian Ruble', '₽', 2],
 ['TRY', 'Turkish Lira', '₺', 2], ['PLN', 'Polish Zloty', 'zł', 2],
 ['THB', 'Thai Baht', '฿', 2], ['IDR', 'Indonesian Rupiah', 'Rp', 0],
 ['MYR', 'Malaysian Ringgit', 'RM', 2], ['PHP', 'Philippine Peso', '₱', 2],
 ['AED', 'UAE Dirham', 'د.إ', 2], ['SAR', 'Saudi Riyal', '﷼', 2],
 ['PKR', 'Pakistani Rupee', '₨', 2], ['BDT', 'Bangladeshi Taka', '৳', 2],
 ['EGP', 'Egyptian Pound', 'E£', 2], ['NGN', 'Nigerian Naira', '₦', 2],
 ['VND', 'Vietnamese Dong', '₫', 0], ['ILS', 'Israeli Shekel', '₪', 2],
 ['CZK', 'Czech Koruna', 'Kč', 2]
 ];

 const byCode = Object.fromEntries(CURRENCIES.map((c) => [c[0], c]));

 function populate() {
 ['from', 'to'].forEach((id, i) => {
 const sel = T.$(id);
 sel.innerHTML = '';
 CURRENCIES.forEach(([code, name, symbol]) => {
 const opt = document.createElement('option');
 opt.value = code;
 opt.textContent = `${code}, ${name} (${symbol})`;
 if (code === (i === 0 ? 'USD' : 'EUR')) opt.selected = true;
 sel.append(opt);
 });
 });
 }

 /** Format with the target currency's conventional decimal places. */
 function format(value, code) {
 const [,, symbol, places] = byCode[code] || ['', '', '', 2];
 return symbol + value.toLocaleString(undefined, {
 minimumFractionDigits: places,
 maximumFractionDigits: places
 });
 }

 function convert() {
 const amount = T.num(T.$('amount').value);
 const rate = T.num(T.$('rate').value);
 const from = T.$('from').value;
 const to = T.$('to').value;

 T.$('inverse').value = isNaN(rate) || rate === 0
 ? ''
 : `1 ${to} = ${(1 / rate).toFixed(6)} ${from}`;

 if (isNaN(amount) || isNaN(rate)) {
 T.$('r-out').textContent = ', ';
 T.$('r-fee').textContent = ', ';
 T.status('status', 'Enter an amount and a rate.', 'muted');
 return;
 }

 if (rate <= 0) {
 T.status('status', 'The rate must be greater than zero.', 'error');
 return;
 }

 const converted = amount * rate;
 const afterFee = converted * 0.975;

 T.$('r-out').textContent = format(converted, to);
 T.$('r-fee').textContent = format(afterFee, to);

 T.status('status',
 `${format(amount, from)} × ${rate} = ${format(converted, to)}`, 'ok');
 }

 /* ---- Saved rates ---- */
 function renderSaved() {
 const saved = T.store.get('currency-rates', {});
 const mount = T.$('saved');
 mount.innerHTML = '';

 const entries = Object.entries(saved);
 if (!entries.length) {
 mount.append(el('span', { className: 'text-xs text-muted', text: 'No saved rates yet.' }));
 return;
 }

 entries.forEach(([pair, rate]) => {
 const chip = el('button', {
 className: 'chip',
 attrs: { type: 'button', title: 'Click to use, shift-click to delete' },
 text: `${pair} @ ${rate}`
 });

 chip.addEventListener('click', (e) => {
 if (e.shiftKey) {
 const next = T.store.get('currency-rates', {});
 delete next[pair];
 T.store.set('currency-rates', next);
 renderSaved();
 return;
 }
 const [from, to] = pair.split('/');
 T.$('from').value = from;
 T.$('to').value = to;
 T.$('rate').value = rate;
 convert();
 });

 mount.append(chip);
 });
 }

 T.on(['amount', 'rate'], convert);
 T.on(['from', 'to'], convert, 'change');

 T.$('swap').addEventListener('click', () => {
 const from = T.$('from').value;
 T.$('from').value = T.$('to').value;
 T.$('to').value = from;

 const rate = T.num(T.$('rate').value);
 if (rate > 0) T.$('rate').value = String(Number((1 / rate).toFixed(6)));

 convert();
 });

 T.$('save').addEventListener('click', () => {
 const rate = T.num(T.$('rate').value);
 if (isNaN(rate) || rate <= 0) {
 toast({ type: 'error', title: 'Enter a valid rate first' });
 return;
 }
 const pair = `${T.$('from').value}/${T.$('to').value}`;
 const saved = T.store.get('currency-rates', {});
 saved[pair] = rate;
 T.store.set('currency-rates', saved);
 renderSaved();
 toast({ type: 'success', title: 'Rate saved', message: pair + ', on this device only.' });
 });

 T.$('copy').addEventListener('click', () =>
 copyToClipboard(T.$('r-out').textContent, 'Result copied'));
 T.$('share').addEventListener('click', () => shareLink({ title: 'Currency Converter | 123MiniApps' }));

 populate();
 renderSaved();
 convert();
 if (window.Analytics) Analytics.trackToolUse('currency-converter');""",
))

# ---------------------------------------------------------------
# 40. Time Zone Converter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="time-zone-converter", name="Time Zone Converter", icon="🌍", cat="converter",
 title="Time Zone Converter: Compare a Moment Across Cities",
 description="See one moment in time across several time zones at once. Daylight saving aware, with a meeting-time finder that highlights working hours.",
 tagline="See one moment across several time zones at once, daylight saving handled correctly.",
 workspace=ws(
 row(
 text_input("when", "Date and time", "", "", "datetime-local"),
 select("base-zone", "In this zone", [], selected=None),
 ),
 row(
 select("add-zone", "Add a zone", [], selected=None),
 html_block(""" <div class="field">
 <span class="field__label"><span>&nbsp;</span></span>
 <button class="btn btn--secondary" id="add" type="button">Add to board</button>
 </div>"""),
 ),
 status_line("status", "Pick a time to compare across zones."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Your board</span><span class="field__hint">Green rows are inside 9am-6pm working hours</span></span>
 <div class="table-scroll"><div id="board"></div></div>
 </div>"""),
 buttons(("now", "Use current time", "primary"), ("copy", "Copy board"), ("reset", "Reset board", "ghost"), ("share", "Share tool", "ghost")),
 label="Time zone converter",
 ),
 info_block=info(
 features=[
 "Compare unlimited zones side by side",
 "Daylight saving handled automatically by the browser",
 "Working-hours highlighting for meeting planning",
 "Shows UTC offset and day difference for each zone",
 "Board persists on your device between visits",
 ],
 howto=[
 "Set the date and time, and the zone it is in.",
 "Add the other zones you care about.",
 "Green rows are within 9am to 6pm locally.",
 "Copy the board to paste into a meeting invite.",
 ],
 background_title="Why timezone maths goes wrong",
 background_paragraphs=[
 "Offsets are not fixed properties of a place. New York is UTC−5 in winter and UTC−4 in summer, so storing “−5” alongside a timestamp gives the wrong answer for half the year. The correct approach is to store the instant in UTC and the location as an IANA zone identifier such as <code>America/New_York</code>, then convert at display time. That is what this tool does through the browser's own <code>Intl</code> implementation, which carries the full IANA database.",
 "Daylight saving transitions do not happen simultaneously worldwide. Europe and North America change on different weekends, producing a two-week window each spring and autumn when the usual offset between London and New York is one hour different from normal. Recurring meetings scheduled across that boundary silently shift for one party, which is a common and irritating source of missed calls.",
 "The southern hemisphere inverts everything, Australia's daylight saving runs during the northern winter, and a large part of the world, including most of Asia and Africa, does not observe it at all. India is offset by 5 hours 30 minutes, Nepal by 5 hours 45, and the Chatham Islands by 12 hours 45, which is why any code assuming whole-hour offsets eventually breaks.",
 ],
 ),
 script=r""" const ZONES = [
 ['UTC', 'UTC'],
 ['America/Los_Angeles', 'Los Angeles'], ['America/Denver', 'Denver'],
 ['America/Chicago', 'Chicago'], ['America/New_York', 'New York'],
 ['America/Sao_Paulo', 'São Paulo'], ['Europe/London', 'London'],
 ['Europe/Dublin', 'Dublin'], ['Europe/Paris', 'Paris'],
 ['Europe/Berlin', 'Berlin'], ['Europe/Madrid', 'Madrid'],
 ['Europe/Moscow', 'Moscow'], ['Africa/Lagos', 'Lagos'],
 ['Africa/Cairo', 'Cairo'], ['Africa/Johannesburg', 'Johannesburg'],
 ['Asia/Dubai', 'Dubai'], ['Asia/Karachi', 'Karachi'],
 ['Asia/Kolkata', 'Mumbai / Delhi'], ['Asia/Dhaka', 'Dhaka'],
 ['Asia/Bangkok', 'Bangkok'], ['Asia/Singapore', 'Singapore'],
 ['Asia/Shanghai', 'Shanghai'], ['Asia/Tokyo', 'Tokyo'],
 ['Asia/Seoul', 'Seoul'], ['Australia/Perth', 'Perth'],
 ['Australia/Sydney', 'Sydney'], ['Pacific/Auckland', 'Auckland']
 ];

 const localZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
 let board = T.store.get('tz-board', ['UTC', 'America/New_York', 'Europe/London', 'Asia/Tokyo']);

 function populate() {
 ['base-zone', 'add-zone'].forEach((id) => {
 const sel = T.$(id);
 sel.innerHTML = '';
 ZONES.forEach(([zone, label]) => {
 const opt = document.createElement('option');
 opt.value = zone;
 opt.textContent = label + (zone === localZone ? ' (your zone)' : '');
 sel.append(opt);
 });
 if (ZONES.some(([z]) => z === localZone)) sel.value = localZone;
 });
 }

 /** Parts of an instant as rendered in a given zone. */
 function partsIn(date, zone) {
 const fmt = new Intl.DateTimeFormat('en-GB', {
 timeZone: zone, weekday: 'short', day: '2-digit', month: 'short',
 hour: '2-digit', minute: '2-digit', hour12: false
 });
 const parts = Object.fromEntries(fmt.formatToParts(date).map((p) => [p.type, p.value]));
 return parts;
 }

 /** UTC offset of a zone at a given instant, in minutes. */
 function offsetMinutes(date, zone) {
 const fmt = new Intl.DateTimeFormat('en-US', {
 timeZone: zone, hour12: false,
 year: 'numeric', month: '2-digit', day: '2-digit',
 hour: '2-digit', minute: '2-digit', second: '2-digit'
 });
 const p = Object.fromEntries(fmt.formatToParts(date).map((x) => [x.type, x.value]));
 const asUTC = Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour % 24, +p.minute, +p.second);
 return Math.round((asUTC - date.getTime()) / 60000);
 }

 function formatOffset(mins) {
 const sign = mins < 0 ? '-' : '+';
 const abs = Math.abs(mins);
 return `UTC${sign}${T.pad2(Math.floor(abs / 60))}:${T.pad2(abs % 60)}`;
 }

 /** The instant currently selected, or null. */
 function selectedInstant() {
 const raw = T.$('when').value;
 if (!raw) return null;

 const zone = T.$('base-zone').value;
 // Interpret the wall-clock value as being in the chosen zone:
 // parse as UTC, then correct by that zone's offset at that moment.
 const naive = new Date(raw + ':00Z');
 if (isNaN(naive)) return null;

 const guess = new Date(naive.getTime() - offsetMinutes(naive, zone) * 60000);
 // One refinement pass handles instants near a DST boundary
 return new Date(naive.getTime() - offsetMinutes(guess, zone) * 60000);
 }

 function render() {
 const instant = selectedInstant();
 const mount = T.$('board');
 mount.innerHTML = '';

 if (!instant) {
 T.status('status', 'Pick a time to compare across zones.', 'muted');
 return;
 }

 const baseDay = partsIn(instant, T.$('base-zone').value).day;

 const rows = board.map((zone) => {
 const p = partsIn(instant, zone);
 const label = (ZONES.find(([z]) => z === zone) || [zone, zone])[1];
 const hour = Number(p.hour);
 const working = hour >= 9 && hour < 18;
 const dayDiff = Number(p.day) - Number(baseDay);
 const dayNote = dayDiff === 0 ? '' : dayDiff > 0 || dayDiff < -20 ? ' (+1 day)' : ' (−1 day)';

 return {
 cells: [
 label,
 `${p.hour}:${p.minute}${dayNote}`,
 `${p.weekday} ${p.day} ${p.month}`,
 formatOffset(offsetMinutes(instant, zone)),
 working ? '✓ working hours' : ', '
 ],
 working
 };
 });

 const table = T.table(
 ['Location', 'Local time', 'Date', 'Offset', 'Availability'],
 rows.map((r) => r.cells)
 );

 // Tint the rows that fall inside working hours
 [...table.querySelectorAll('tbody tr')].forEach((tr, i) => {
 if (rows[i].working) {
 tr.style.background = 'color-mix(in srgb, var(--success) 12%, transparent)';
 }
 });

 mount.append(table);

 const allWorking = rows.every((r) => r.working);
 T.status('status',
 allWorking
 ? 'This time is inside working hours for every zone on the board.'
 : `Working hours for ${rows.filter((r) => r.working).length} of ${rows.length} zones.`,
 allWorking ? 'ok' : 'warn');
 }

 function setNow() {
 const now = new Date();
 const zone = T.$('base-zone').value;
 const p = new Intl.DateTimeFormat('sv-SE', {
 timeZone: zone, year: 'numeric', month: '2-digit', day: '2-digit',
 hour: '2-digit', minute: '2-digit', hour12: false
 }).format(now).replace(' ', 'T');
 T.$('when').value = p.slice(0, 16);
 render();
 }

 T.on(['when'], render);
 T.on(['base-zone'], render, 'change');

 T.$('add').addEventListener('click', () => {
 const zone = T.$('add-zone').value;
 if (board.includes(zone)) {
 toast({ type: 'warning', title: 'Already on the board' });
 return;
 }
 board.push(zone);
 T.store.set('tz-board', board);
 render();
 });

 T.$('reset').addEventListener('click', () => {
 board = ['UTC', 'America/New_York', 'Europe/London', 'Asia/Tokyo'];
 T.store.set('tz-board', board);
 render();
 });

 T.$('now').addEventListener('click', setNow);

 T.$('copy').addEventListener('click', () => {
 const lines = T.$$('#board tbody tr').map((tr) =>
 [...tr.children].map((td) => td.textContent).join(' · '));
 copyToClipboard(lines.join('\n'), 'Board copied');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Time Zone Converter | 123MiniApps' }));

 populate();
 setNow();
 if (window.Analytics) Analytics.trackToolUse('time-zone-converter');""",
))

# ---------------------------------------------------------------
# 41. File Size Converter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="file-size-converter", name="File Size Converter", icon="💾", cat="converter",
 title="File Size Converter: Bytes, KB, MB, GB with Binary and Decimal",
 description="Convert between bytes, kilobytes, megabytes, gigabytes and terabytes in both binary and decimal conventions, with transfer time estimates.",
 tagline="Convert data sizes across both conventions, and see why your drive looks smaller than advertised.",
 workspace=ws(
 row(
 number_input("value", "Size", "1", "1"),
 select("unit", "Unit", [
 ("B", "Bytes"), ("KB", "Kilobytes (KB, ×1000)"), ("KiB", "Kibibytes (KiB, ×1024)"),
 ("MB", "Megabytes (MB)"), ("MiB", "Mebibytes (MiB)"),
 ("GB", "Gigabytes (GB)"), ("GiB", "Gibibytes (GiB)"),
 ("TB", "Terabytes (TB)"), ("TiB", "Tebibytes (TiB)"),
 ], selected="GB"),
 ),
 status_line("status", "Enter a size to convert."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Decimal (SI, ×1000)</span><span class="field__hint">What drive manufacturers advertise</span></span>
 <div class="table-scroll"><div id="decimal"></div></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Binary (IEC, ×1024)</span><span class="field__hint">What your operating system reports</span></span>
 <div class="table-scroll"><div id="binary"></div></div>
 </div>"""),
 HR,
 select("speed", "Estimate transfer time at", [
 ("1", "1 Mbps, slow mobile"), ("10", "10 Mbps, basic broadband"),
 ("50", "50 Mbps, average broadband"), ("100", "100 Mbps, fast broadband"),
 ("300", "300 Mbps, fibre"), ("1000", "1 Gbps, gigabit"),
 ], selected="100"),
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-time" style="font-size:var(--text-2xl)">, </span><span class="result__label">Transfer time</span></div>
 <div class="result"><span class="result__value" id="r-bytes" style="font-size:var(--text-2xl)">, </span><span class="result__label">Exact bytes</span></div>
 </div>"""),
 buttons(("copy", "Copy all sizes", "primary"), ("share", "Share tool", "ghost")),
 label="File size converter",
 ),
 info_block=info(
 features=[
 "Both decimal (SI) and binary (IEC) conventions side by side",
 "Every unit from bytes to tebibytes",
 "Exact byte count with no rounding",
 "Transfer time estimates at six connection speeds",
 "Explains the drive-capacity discrepancy",
 ],
 howto=[
 "Enter a size and pick its unit.",
 "Read the decimal and binary tables.",
 "Choose a connection speed for a transfer estimate.",
 "Copy every representation at once.",
 ],
 background_title="Why your 1 TB drive shows as 931 GB",
 background_paragraphs=[
 "There are two competing definitions of a kilobyte and both are in active use. The decimal convention follows SI prefixes: a kilobyte is 1,000 bytes, a megabyte 1,000,000. The binary convention treats a kilobyte as 1,024 bytes, because computers address memory in powers of two and 2¹⁰ is conveniently close to 1,000.",
 "Storage manufacturers use the decimal definition, so a drive sold as 1 TB contains 1,000,000,000,000 bytes. Windows reports capacity using the binary definition but labels it with decimal-looking units, dividing by 1024 three times and calling the result GB. That gives 931, which is why the drive appears to be missing 7% of its capacity. Nothing is actually missing, the two systems are just counting differently. macOS switched to decimal reporting in 2009, so the same drive shows as 1 TB there.",
 "The IEC introduced unambiguous binary prefixes in 1998, kibibyte, mebibyte, gibibyte, written KiB, MiB and GiB. They are precise and largely ignored outside Linux tooling and technical documentation. Networking adds one more trap: transfer speeds are quoted in bits per second, not bytes, so a 100 Mbps connection moves at best 12.5 MB per second, and less after protocol overhead. The estimate above assumes about 90% efficiency.",
 ],
 ),
 script=r""" const UNITS = {
 B: 1,
 KB: 1e3, MB: 1e6, GB: 1e9, TB: 1e12, PB: 1e15,
 KiB: 1024, MiB: 1048576, GiB: 1073741824, TiB: 1099511627776, PiB: 1125899906842624
 };

 const DECIMAL = ['B', 'KB', 'MB', 'GB', 'TB', 'PB'];
 const BINARY = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB'];

 function tidy(n) {
 if (n === 0) return '0';
 if (n < 0.001) return n.toExponential(4);
 if (n >= 1e15) return n.toExponential(4);
 return Number(n.toPrecision(10)).toLocaleString(undefined, { maximumFractionDigits: 6 });
 }

 function humanTime(seconds) {
 if (!isFinite(seconds) || seconds <= 0) return ', ';
 if (seconds < 1) return Math.round(seconds * 1000) + ' ms';
 if (seconds < 60) return seconds.toFixed(1) + ' seconds';
 if (seconds < 3600) return (seconds / 60).toFixed(1) + ' minutes';
 if (seconds < 86400) return (seconds / 3600).toFixed(1) + ' hours';
 return (seconds / 86400).toFixed(1) + ' days';
 }

 function convert() {
 const value = T.num(T.$('value').value);
 const unit = T.$('unit').value;

 if (isNaN(value) || value < 0) {
 T.status('status', 'Enter a size to convert.', 'muted');
 T.$('decimal').innerHTML = '';
 T.$('binary').innerHTML = '';
 T.$('r-time').textContent = ', ';
 T.$('r-bytes').textContent = ', ';
 return;
 }

 const bytes = value * UNITS[unit];

 const decMount = T.$('decimal');
 decMount.innerHTML = '';
 decMount.append(T.table(['Unit', 'Value'],
 DECIMAL.map((u) => [u, tidy(bytes / UNITS[u])])));

 const binMount = T.$('binary');
 binMount.innerHTML = '';
 binMount.append(T.table(['Unit', 'Value'],
 BINARY.map((u) => [u, tidy(bytes / UNITS[u])])));

 T.$('r-bytes').textContent = Math.round(bytes).toLocaleString();

 // Mbps → bytes per second, allowing ~90% for protocol overhead
 const mbps = Number(T.$('speed').value);
 const bytesPerSecond = (mbps * 1e6 / 8) * 0.9;
 T.$('r-time').textContent = humanTime(bytes / bytesPerSecond);

 // The headline comparison: decimal vs binary for the same byte count
 const asDecGB = bytes / UNITS.GB;
 const asBinGB = bytes / UNITS.GiB;
 T.status('status',
 `${tidy(bytes)} bytes = ${tidy(asDecGB)} GB (decimal) = ${tidy(asBinGB)} GiB (binary).`, 'ok');
 }

 T.on(['value'], convert);
 T.on(['unit', 'speed'], convert, 'change');

 T.$('copy').addEventListener('click', () => {
 const rows = [...T.$$('#decimal tbody tr'), ...T.$$('#binary tbody tr')]
 .map((tr) => [...tr.children].map((td) => td.textContent).join(': '));
 copyToClipboard(rows.join('\n'), 'All sizes copied');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'File Size Converter | 123MiniApps' }));

 convert();
 if (window.Analytics) Analytics.trackToolUse('file-size-converter');""",
))

# ---------------------------------------------------------------
# 42. Text to ASCII
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="text-to-ascii", name="Text to ASCII", icon="🔡", cat="converter",
 title="Text to ASCII Converter: Code Points, Hex and Binary",
 description="Convert text to ASCII and Unicode code points in decimal, hex, binary or escape notation, and decode them back. Per-character inspection table.",
 tagline="Convert text to code points in any notation, and decode them back again.",
 workspace=ws(
 select("direction", "Direction", [("encode", "Text → code points"), ("decode", "Code points → text")], selected="encode"),
 textarea("input", "Input", "Hello 🌍", "input-stats", rows=130),
 row(
 select("format", "Notation", [
 ("dec", "Decimal, 72 101 108"),
 ("hex", "Hexadecimal, 48 65 6C"),
 ("bin", "Binary, 01001000"),
 ("uni", "Unicode, U+0048"),
 ("esc", "JS escape, \\u0048"),
 ("html", "HTML entity, &#72;"),
 ], selected="dec"),
 text_input("separator", "Separator", "space", " "),
 ),
 status_line("status", "Output updates as you type."),
 HR,
 output("output", "Result", "output-stats"),
 buttons(("copy", "Copy result", "primary"), ("download", "Download"), ("swap", "Swap direction"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Character breakdown</span><span class="field__hint">First 60 characters</span></span>
 <div class="table-scroll"><div id="breakdown"></div></div>
 </div>"""),
 label="Text to ASCII converter",
 ),
 info_block=info(
 features=[
 "Six output notations including JS and HTML escapes",
 "Decodes every notation back to text",
 "Per-character table with code point, hex and UTF-8 length",
 "Correct handling of emoji and astral-plane characters",
 "Custom separator between values",
 ],
 howto=[
 "Choose whether you are encoding or decoding.",
 "Type or paste your input.",
 "Pick the notation you need.",
 "Copy the result or study the breakdown table.",
 ],
 background_title="ASCII, Unicode and the difference between them",
 background_paragraphs=[
 "ASCII defines 128 characters numbered 0 to 127, the English alphabet, digits, common punctuation and a set of control codes. It was designed for teleprinters in the early 1960s, which is why it contains oddities like the bell character and why carriage return and line feed are separate. Everything in that range still has the same number today, which is why ASCII text is valid in essentially every encoding in use.",
 "Unicode extends that to over 150,000 characters covering every living script, historical alphabets, mathematical symbols and emoji. A Unicode code point is written <code>U+</code> followed by hex, so <code>U+0041</code> is the letter A and <code>U+1F30D</code> is the Earth globe emoji. Code points above U+FFFF are the astral planes, and they are where naive string handling falls over.",
 "The distinction that causes most bugs is between code points and encoded bytes. UTF-8 stores a code point in one to four bytes, ASCII characters take one, most European accented letters two, most CJK characters three, and emoji four. JavaScript strings, meanwhile, are UTF-16, storing astral characters as two 16-bit surrogates. So a single emoji has one code point, four UTF-8 bytes, and a JavaScript <code>.length</code> of 2. The table below shows all three so the discrepancy is visible.",
 ],
 ),
 script=r""" let lastResult = '';

 function separator() {
 const raw = T.$('separator').value;
 if (raw === 'space' || raw === '') return ' ';
 if (raw === '\\n') return '\n';
 return raw;
 }

 const ENCODERS = {
 dec: (cp) => String(cp),
 hex: (cp) => cp.toString(16).toUpperCase().padStart(2, '0'),
 bin: (cp) => cp.toString(2).padStart(8, '0'),
 uni: (cp) => 'U+' + cp.toString(16).toUpperCase().padStart(4, '0'),
 esc: (cp) => cp > 0xffff
 ? '\\u{' + cp.toString(16).toUpperCase() + '}'
 : '\\u' + cp.toString(16).toUpperCase().padStart(4, '0'),
 html: (cp) => '&#' + cp + ';'
 };

 /**
 * Self-delimiting notations, HTML entities and JS escapes carry
 * their own start and end markers, so they are often written with
 * no separator at all ("&#72;&#105;"). Splitting those on
 * whitespace or semicolons would tear them apart, so match them
 * directly first and only fall back to separator-splitting when
 * the input is a plain list of numbers.
 */
 const STRUCTURED = /&#x[0-9a-f]+;|&#\d+;|\\u\{[0-9a-f]+\}|\\u[0-9a-f]{4}|U\+[0-9a-f]+/gi;

 /** Decode any of the supported notations back to text. */
 function decode(input) {
 const structured = input.match(STRUCTURED);

 // Use structured tokens only if they account for the whole input,
 // ignoring whitespace and separators between them.
 const remainder = input.replace(STRUCTURED, '').replace(/[\s;]+/g, '');
 const tokens = structured && remainder === ''
 ? structured
 : input.trim().split(/[\s;]+/).filter(Boolean);

 const chars = [];

 for (const raw of tokens) {
 let cp = NaN;
 const t = raw.trim();

 if (/^U\+[0-9a-f]+$/i.test(t)) cp = parseInt(t.slice(2), 16);
 else if (/^\\u\{[0-9a-f]+\}$/i.test(t)) cp = parseInt(t.slice(3, -1), 16);
 else if (/^\\u[0-9a-f]{4}$/i.test(t)) cp = parseInt(t.slice(2), 16);
 else if (/^&#x[0-9a-f]+;$/i.test(t)) cp = parseInt(t.slice(3, -1), 16);
 else if (/^&#\d+;$/.test(t)) cp = parseInt(t.slice(2, -1), 10);
 else if (/^0x[0-9a-f]+$/i.test(t)) cp = parseInt(t.slice(2), 16);
 else if (/^[01]{8,}$/.test(t)) cp = parseInt(t, 2);
 else if (/^\d+$/.test(t)) cp = parseInt(t, 10);
 else if (/^[0-9a-f]+$/i.test(t)) cp = parseInt(t, 16);

 if (isNaN(cp) || cp < 0 || cp > 0x10ffff) {
 throw new Error(`“${t}” is not a recognised code point.`);
 }
 chars.push(String.fromCodePoint(cp));
 }

 return chars.join('');
 }

 /** UTF-8 byte length of a single code point. */
 function utf8Length(cp) {
 if (cp < 0x80) return 1;
 if (cp < 0x800) return 2;
 if (cp < 0x10000) return 3;
 return 4;
 }

 function run() {
 const input = T.$('input').value;
 T.$('input-stats').textContent = input.length.toLocaleString() + ' UTF-16 units';

 if (!input) {
 lastResult = '';
 T.setOutput('output', '');
 T.$('output-stats').textContent = '';
 T.$('breakdown').innerHTML = '';
 T.status('status', 'Output updates as you type.', 'muted');
 return;
 }

 const encoding = T.$('direction').value === 'encode';

 try {
 if (encoding) {
 const encoder = ENCODERS[T.$('format').value];
 const points = [...input].map((ch) => ch.codePointAt(0));
 lastResult = points.map(encoder).join(separator());

 const bytes = points.reduce((n, cp) => n + utf8Length(cp), 0);
 T.status('status',
 `${points.length} code point(s) · ${bytes} UTF-8 byte(s) · ${input.length} UTF-16 unit(s).`, 'ok');

 renderBreakdown([...input]);
 } else {
 lastResult = decode(input);
 T.status('status', `Decoded to ${[...lastResult].length} character(s).`, 'ok');
 renderBreakdown([...lastResult]);
 }

 T.setOutput('output', lastResult);
 T.$('output-stats').textContent = lastResult.length.toLocaleString() + ' characters';
 } catch (err) {
 lastResult = '';
 T.setOutput('output', '');
 T.$('breakdown').innerHTML = '';
 T.status('status', err.message, 'error');
 }
 }

 function renderBreakdown(chars) {
 const mount = T.$('breakdown');
 mount.innerHTML = '';
 if (!chars.length) return;

 const rows = chars.slice(0, 60).map((ch) => {
 const cp = ch.codePointAt(0);
 const printable = cp < 32 ? '(control)' : ch;
 return [
 printable,
 String(cp),
 'U+' + cp.toString(16).toUpperCase().padStart(4, '0'),
 cp.toString(2).padStart(8, '0'),
 utf8Length(cp) + ' byte' + (utf8Length(cp) === 1 ? '' : 's'),
 ch.length + ' unit' + (ch.length === 1 ? '' : 's')
 ];
 });

 mount.append(T.table(
 ['Char', 'Decimal', 'Unicode', 'Binary', 'UTF-8', 'UTF-16'],
 rows
 ));
 }

 T.$('input').addEventListener('input', debounce(run, 250));
 T.on(['direction', 'format'], run, 'change');
 T.$('separator').addEventListener('input', debounce(run, 250));

 T.$('swap').addEventListener('click', () => {
 if (!lastResult) return;
 T.$('input').value = lastResult;
 T.$('direction').value = T.$('direction').value === 'encode' ? 'decode' : 'encode';
 run();
 });

 T.wireActions({ slug: 'text-to-ascii', getResult: () => lastResult, filename: 'codepoints.txt' });
 run();""",
))
