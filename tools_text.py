#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: tools_text.py
# Purpose: The 10 Text Tools (ids 1-10).
# ============================================

from toolkit import (
 tool, ws, info, row, textarea, text_input, select, switch, slider,
 output, status_line, buttons, STD_ACTIONS, HR, html_block,
)

PAGES = []

# ---------------------------------------------------------------
# 1. Word Counter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="word-counter", name="Word Counter", icon="🔢", cat="text",
 title="Word Counter: Live Word, Character and Reading Time Count",
 description="Count words, characters, sentences and paragraphs as you type, with reading time and keyword density. Runs entirely in your browser.",
 tagline="Live word, character and sentence counts, plus reading time and keyword density.",
 workspace=ws(
 textarea("input", "Your text", "Start typing or paste your text here…", rows=220),
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-words">0</span><span class="result__label">Words</span></div>
 <div class="result"><span class="result__value" id="r-chars">0</span><span class="result__label">Characters</span></div>
 <div class="result"><span class="result__value" id="r-nospace">0</span><span class="result__label">No spaces</span></div>
 <div class="result"><span class="result__value" id="r-sentences">0</span><span class="result__label">Sentences</span></div>
 <div class="result"><span class="result__value" id="r-paragraphs">0</span><span class="result__label">Paragraphs</span></div>
 <div class="result"><span class="result__value" id="r-read">0:00</span><span class="result__label">Reading time</span></div>
 </div>"""),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Most frequent words</span><span class="field__hint">Excluding common stop words</span></span>
 <div class="table-scroll"><div id="density"></div></div>
 </div>"""),
 buttons(("copy-stats", "Copy statistics", "primary"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
 label="Word counter",
 ),
 info_block=info(
 features=[
 "Live counts as you type, no button to press",
 "Words, characters, characters without spaces, sentences, paragraphs",
 "Reading and speaking time estimates",
 "Keyword density table with stop-word filtering",
 "Handles accented and non-Latin text correctly",
 ],
 howto=[
 "Paste or type your text into the box.",
 "Every statistic updates immediately.",
 "Scroll down for the keyword frequency table.",
 "Press Copy statistics to take the numbers with you.",
 ],
 background_title="How the counts are calculated",
 background_paragraphs=[
 "Word counting sounds trivial until you try to define a word. This tool matches runs of letters, digits, apostrophes and hyphens using Unicode-aware patterns, so <code>don't</code> counts as one word rather than two, and <code>well-known</code> stays a single hyphenated word. Accented Latin, Cyrillic and Greek text all count correctly, which naive whitespace-splitting gets wrong for languages that use different spacing conventions.",
 "Reading time uses 225 words per minute, which sits in the middle of the range most studies report for adults reading non-technical prose silently. Speaking time uses 150 words per minute, roughly the pace of clear presentation delivery. Both are estimates, dense technical material reads considerably slower, and your own pace may differ by 30% in either direction.",
 "The density table strips around 40 English stop words such as <em>the</em>, <em>and</em> and <em>of</em> before ranking, because otherwise those would occupy every top slot and tell you nothing. Density percentages are calculated against the total word count including stop words, which is the convention most SEO tools follow.",
 ],
 ),
 script=r""" const input = T.$('input');

 const STOP = new Set(('a an and are as at be but by for from has have he her his i in is it its of on or ' +
 'that the their they this to was were will with you your we our not can all if do so what which who').split(' '));

 function update() {
 const text = input.value;
 const words = T.words(text);
 const sentences = T.sentences(text);
 const paragraphs = text.split(/\n{2,}/).map((p) => p.trim()).filter(Boolean);

 T.$('r-words').textContent = words.length.toLocaleString();
 T.$('r-chars').textContent = text.length.toLocaleString();
 T.$('r-nospace').textContent = text.replace(/\s/g, '').length.toLocaleString();
 T.$('r-sentences').textContent = sentences.length.toLocaleString();
 T.$('r-paragraphs').textContent = paragraphs.length.toLocaleString();
 T.$('r-read').textContent = T.duration((words.length / 225) * 60);

 renderDensity(words);
 }

 function renderDensity(words) {
 const mount = T.$('density');
 mount.innerHTML = '';
 if (words.length < 5) return;

 const counts = new Map();
 for (const w of words) {
 const k = w.toLowerCase();
 if (STOP.has(k) || k.length < 3) continue;
 counts.set(k, (counts.get(k) || 0) + 1);
 }

 const top = [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 12);
 if (!top.length) return;

 mount.append(T.table(
 ['Word', 'Count', 'Density'],
 top.map(([w, n]) => [w, n, ((n / words.length) * 100).toFixed(2) + '%'])
 ));
 }

 function statsText() {
 const ids = [['Words','r-words'],['Characters','r-chars'],['Characters (no spaces)','r-nospace'],
 ['Sentences','r-sentences'],['Paragraphs','r-paragraphs'],['Reading time','r-read']];
 return ids.map(([label, id]) => `${label}: ${T.$(id).textContent}`).join('\n');
 }

 input.addEventListener('input', debounce(update, 120));
 T.$('copy-stats').addEventListener('click', () => copyToClipboard(statsText(), 'Statistics copied'));
 T.$('clear').addEventListener('click', () => { input.value = ''; update(); input.focus(); });
 T.$('share').addEventListener('click', () => shareLink({ title: 'Word Counter | 123MiniApps' }));

 update();""",
))

# ---------------------------------------------------------------
# 2. Case Converter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="case-converter", name="Case Converter", icon="🔠", cat="text",
 title="Case Converter: Upper, Lower, Title, camelCase and snake_case",
 description="Convert text between uppercase, lowercase, title, sentence, camel, snake, kebab and constant case. Nine styles, instant preview, one-click copy.",
 tagline="Switch text between nine case styles, including camelCase, snake_case and kebab-case.",
 workspace=ws(
 textarea("input", "Your text", "The quick brown fox jumps over the lazy dog", rows=140),
 select("style", "Convert to", [
 ("upper", "UPPERCASE"), ("lower", "lowercase"),
 ("title", "Title Case"), ("sentence", "Sentence case"),
 ("camel", "camelCase"), ("pascal", "PascalCase"),
 ("snake", "snake_case"), ("kebab", "kebab-case"),
 ("constant", "CONSTANT_CASE"), ("alternate", "aLtErNaTiNg"),
 ], selected="title"),
 status_line("status", "Output updates as you type."),
 HR,
 output("output", "Result", "output-stats"),
 buttons(("copy", "Copy result", "primary"), ("swap", "Use result as input"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
 label="Case converter",
 ),
 info_block=info(
 features=[
 "Nine case styles covering prose and code conventions",
 "Preserves punctuation and spacing where appropriate",
 "Handles existing camelCase and snake_case input correctly",
 "Feed the result back in with one click",
 ],
 howto=[
 "Paste your text into the input box.",
 "Choose the case style you want.",
 "The result appears immediately below.",
 "Press Copy result, or Use result as input to chain conversions.",
 ],
 background_title="Which case style to use where",
 background_paragraphs=[
 "Prose styles and code styles solve different problems. <strong>Sentence case</strong> capitalises only the first word and proper nouns, it is the house style for most UK publications and increasingly for UI labels, because it reads faster than title case. <strong>Title case</strong> capitalises principal words and is standard for headlines in US publications. This tool uses a simple every-word rule for title case; strict style guides also lowercase short prepositions and articles, so check the output against your guide.",
 "Code conventions are largely arbitrary but strongly enforced by ecosystem. JavaScript and Java use <code>camelCase</code> for variables and <code>PascalCase</code> for classes. Python and Ruby prefer <code>snake_case</code>. CSS classes and URL slugs use <code>kebab-case</code>, since underscores were historically unreliable in URLs. <code>CONSTANT_CASE</code> marks compile-time constants and environment variables almost universally.",
 "The tricky part is splitting the input into words before rejoining it. This tool detects existing boundaries from spaces, hyphens, underscores and lowercase-to-uppercase transitions, so converting <code>myVariableName</code> straight to <code>my-variable-name</code> works without a manual pass first.",
 ],
 ),
 script=r""" const input = T.$('input');
 let lastResult = '';

 /**
 * Split any input convention into a list of lowercase words.
 * Handles spaces, hyphens, underscores and camelCase humps.
 * @param {string} s
 * @returns {string[]}
 */
 function splitWords(s) {
 return String(s)
 .replace(/([a-z0-9])([A-Z])/g, '$1 $2')
 .replace(/([A-Z]+)([A-Z][a-z])/g, '$1 $2')
 .split(/[\s_\-]+/)
 .filter(Boolean)
 .map((w) => w.toLowerCase());
 }

 const CONVERTERS = {
 upper: (s) => s.toUpperCase(),
 lower: (s) => s.toLowerCase(),
 title: (s) => T.titleCase(s),
 sentence: (s) =>
 s.toLowerCase().replace(/(^\s*\w|[.!?]\s+\w)/g, (m) => m.toUpperCase()),
 camel: (s) => splitWords(s).map((w, i) => (i ? w[0].toUpperCase() + w.slice(1) : w)).join(''),
 pascal: (s) => splitWords(s).map((w) => w[0].toUpperCase() + w.slice(1)).join(''),
 snake: (s) => splitWords(s).join('_'),
 kebab: (s) => splitWords(s).join('-'),
 constant: (s) => splitWords(s).join('_').toUpperCase(),
 alternate: (s) => {
 let i = 0;
 return s.replace(/[a-z]/gi, (c) => (i++ % 2 ? c.toUpperCase() : c.toLowerCase()));
 }
 };

 function run() {
 const text = input.value;

 if (!text.trim()) {
 lastResult = '';
 T.setOutput('output', '');
 T.$('output-stats').textContent = '';
 T.status('status', 'Output updates as you type.', 'muted');
 return;
 }

 lastResult = CONVERTERS[T.$('style').value](text);
 T.setOutput('output', lastResult);
 T.$('output-stats').textContent = lastResult.length.toLocaleString() + ' characters';
 T.status('status', 'Converted to ' + T.$('style').selectedOptions[0].textContent + '.', 'ok');
 }

 input.addEventListener('input', debounce(run, 150));
 T.$('style').addEventListener('change', run);

 T.$('swap').addEventListener('click', () => {
 if (!lastResult) return;
 input.value = lastResult;
 run();
 });

 T.$('clear').addEventListener('click', () => { input.value = ''; run(); input.focus(); });

 T.wireActions({ slug: 'case-converter', getResult: () => lastResult, filename: 'converted.txt' });
 run();""",
))

# ---------------------------------------------------------------
# 3. Text Diff Checker
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="text-diff-checker", name="Text Diff Checker", icon="🔍", cat="text",
 title="Text Diff Checker: Compare Two Texts and Highlight Changes",
 description="Compare two blocks of text side by side and highlight every addition and deletion. Word or line granularity, with an optional whitespace-insensitive mode.",
 tagline="Compare two texts and see exactly what was added, removed and kept.",
 workspace=ws(
 row(
 textarea("left", "Original", "Paste the original text…", rows=200),
 textarea("right", "Changed", "Paste the changed text…", rows=200),
 ),
 row(
 select("mode", "Compare by", [("word", "Words"), ("line", "Lines")], selected="word"),
 switch("ignore-ws", "Ignore whitespace differences", True),
 switch("ignore-case", "Ignore capitalisation", False),
 ),
 status_line("status", "Paste text into both boxes to compare."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-added" style="color:var(--success)">0</span><span class="result__label">Added</span></div>
 <div class="result"><span class="result__value" id="r-removed" style="color:var(--danger)">0</span><span class="result__label">Removed</span></div>
 <div class="result"><span class="result__value" id="r-same">0</span><span class="result__label">Unchanged</span></div>
 <div class="result result--primary"><span class="result__value" id="r-similarity">100%</span><span class="result__label">Similarity</span></div>
 </div>"""),
 output("output", "Differences", None, "The comparison will appear here."),
 buttons(("copy", "Copy result", "primary"), ("swap", "Swap sides"), ("clear", "Clear both", "ghost"), ("share", "Share tool", "ghost")),
 label="Text diff checker",
 ),
 info_block=info(
 features=[
 "Word-level or line-level comparison",
 "Additions and deletions colour-coded inline",
 "Optional whitespace and case insensitivity",
 "Similarity percentage and change counts",
 "Copy a plain-text unified summary",
 ],
 howto=[
 "Paste the original version on the left.",
 "Paste the changed version on the right.",
 "Choose word or line granularity.",
 "Green marks additions, struck-through red marks deletions.",
 ],
 background_title="How the comparison works",
 background_paragraphs=[
 "This uses a longest common subsequence algorithm, the same foundation as <code>diff</code> and Git. It finds the longest sequence of tokens appearing in both texts in the same order, then treats everything else as either an insertion or a deletion. That produces a minimal, readable set of changes rather than simply reporting that everything after the first difference changed.",
 "Word granularity is best for prose, where a single edited word inside a long paragraph should not mark the whole paragraph as changed. Line granularity matches how code review tools work and is better for source files, configuration and any text where line boundaries carry meaning.",
 "The similarity percentage is the proportion of tokens unchanged relative to the longer of the two texts. It is a rough guide rather than a precise measure of semantic similarity, reordering two paragraphs produces a low score even though nothing was truly added or removed. For large inputs the algorithm is capped at 4,000 tokens per side, since LCS cost grows with the product of both lengths.",
 ],
 ),
 script=r""" const MAX_TOKENS = 4000;
 let lastResult = '';

 /** Tokenise according to the current mode and normalisation options. */
 function tokenise(text) {
 const byLine = T.$('mode').value === 'line';
 let tokens = byLine ? text.split(/\r?\n/) : text.split(/(\s+)/).filter((t) => t !== '');
 return tokens.slice(0, MAX_TOKENS);
 }

 /** The comparison key, what "equal" means given the toggles. */
 function key(token) {
 let k = token;
 if (T.$('ignore-ws').checked) k = k.replace(/\s+/g, ' ').trim();
 if (T.$('ignore-case').checked) k = k.toLowerCase();
 return k;
 }

 /**
 * Longest common subsequence, returned as an edit script.
 * @returns {{type: 'same'|'add'|'del', value: string}[]}
 */
 function diff(a, b) {
 const n = a.length, m = b.length;

 // DP table of LCS lengths, Uint32Array keeps a 4000x4000 grid manageable
 const rows = n + 1, cols = m + 1;
 const dp = new Uint32Array(rows * cols);

 for (let i = n - 1; i >= 0; i--) {
 for (let j = m - 1; j >= 0; j--) {
 dp[i * cols + j] = key(a[i]) === key(b[j])
 ? dp[(i + 1) * cols + (j + 1)] + 1
 : Math.max(dp[(i + 1) * cols + j], dp[i * cols + (j + 1)]);
 }
 }

 const out = [];
 let i = 0, j = 0;
 while (i < n && j < m) {
 if (key(a[i]) === key(b[j])) {
 out.push({ type: 'same', value: a[i] }); i++; j++;
 } else if (dp[(i + 1) * cols + j] >= dp[i * cols + (j + 1)]) {
 out.push({ type: 'del', value: a[i] }); i++;
 } else {
 out.push({ type: 'add', value: b[j] }); j++;
 }
 }
 while (i < n) out.push({ type: 'del', value: a[i++] });
 while (j < m) out.push({ type: 'add', value: b[j++] });

 return out;
 }

 function run() {
 const leftText = T.$('left').value;
 const rightText = T.$('right').value;

 if (!leftText.trim() && !rightText.trim()) {
 T.setOutput('output', '', 'The comparison will appear here.');
 T.status('status', 'Paste text into both boxes to compare.', 'muted');
 return;
 }

 const a = tokenise(leftText);
 const b = tokenise(rightText);

 if (a.length >= MAX_TOKENS || b.length >= MAX_TOKENS) {
 T.status('status', `Input truncated to ${MAX_TOKENS.toLocaleString()} tokens per side.`, 'warn');
 }

 const script = diff(a, b);
 const byLine = T.$('mode').value === 'line';

 let added = 0, removed = 0, same = 0;
 const html = [];
 const plain = [];

 for (const part of script) {
 const safe = T.esc(part.value) + (byLine ? '\n' : '');
 if (part.type === 'add') {
 added++;
 html.push(`<span class="diff-add">${safe}</span>`);
 plain.push('+ ' + part.value);
 } else if (part.type === 'del') {
 removed++;
 html.push(`<span class="diff-del">${safe}</span>`);
 plain.push('- ' + part.value);
 } else {
 same++;
 html.push(safe);
 if (byLine) plain.push(' ' + part.value);
 }
 }

 T.setOutputHTML('output', html.join(''));
 lastResult = plain.join(byLine ? '\n' : ' ');

 T.$('r-added').textContent = added.toLocaleString();
 T.$('r-removed').textContent = removed.toLocaleString();
 T.$('r-same').textContent = same.toLocaleString();

 const total = Math.max(a.length, b.length, 1);
 T.$('r-similarity').textContent = Math.round((same / total) * 100) + '%';

 if (!added && !removed) T.status('status', 'The two texts are identical.', 'ok');
 else T.status('status', `${added} addition(s), ${removed} deletion(s).`, 'ok');
 }

 T.on(['left', 'right'], debounce(run, 300));
 T.on(['mode', 'ignore-ws', 'ignore-case'], run, 'change');

 T.$('swap').addEventListener('click', () => {
 const tmp = T.$('left').value;
 T.$('left').value = T.$('right').value;
 T.$('right').value = tmp;
 run();
 });

 T.$('clear').addEventListener('click', () => {
 T.$('left').value = '';
 T.$('right').value = '';
 run();
 });

 T.wireActions({ slug: 'text-diff-checker', getResult: () => lastResult, filename: 'diff.txt' });
 run();""",
))

# ---------------------------------------------------------------
# 4. Lorem Ipsum Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="lorem-ipsum-generator", name="Lorem Ipsum Generator", icon="📄", cat="text",
 title="Lorem Ipsum Generator: Placeholder Text for Mockups",
 description="Generate placeholder paragraphs, sentences or words for design mockups. Classic Latin or modern variants, with optional HTML tag wrapping.",
 tagline="Generate placeholder copy for mockups, classic Latin, or plain-English filler.",
 workspace=ws(
 row(
 select("unit", "Generate", [("paragraphs", "Paragraphs"), ("sentences", "Sentences"), ("words", "Words")], selected="paragraphs"),
 slider("count", "How many", 1, 50, 4, 1, unit="items"),
 select("flavour", "Flavour", [("classic", "Classic Latin"), ("modern", "Plain English"), ("hipster", "Tech jargon")], selected="classic"),
 ),
 row(
 switch("start-lorem", "Start with “Lorem ipsum dolor sit amet”", True),
 switch("wrap-html", "Wrap in HTML tags", False),
 ),
 status_line("status", "Press Generate for fresh placeholder text."),
 HR,
 output("output", "Placeholder text", "output-stats", "Your placeholder text will appear here."),
 buttons(("generate", "Generate", "primary"), ("copy", "Copy result"), ("download", "Download"), ("share", "Share tool", "ghost")),
 label="Lorem ipsum generator",
 ),
 info_block=info(
 features=[
 "Paragraphs, sentences or individual words",
 "Three flavours: classic Latin, plain English, tech jargon",
 "Optional <p> tag wrapping for direct paste into HTML",
 "Realistic sentence-length variation",
 "Up to 50 units per generation",
 ],
 howto=[
 "Choose paragraphs, sentences or words.",
 "Set how many you need with the slider.",
 "Pick a flavour and press Generate.",
 "Copy the result or download it as a text file.",
 ],
 background_title="Why placeholder text exists",
 background_paragraphs=[
 "Lorem ipsum has been the printing industry's dummy text since the 1500s, when a typesetter scrambled a passage from Cicero's <em>De finibus bonorum et malorum</em> to make a type specimen book. The scrambling is the point: the text is recognisably language-shaped but carries no meaning, so nobody reads it instead of evaluating the layout.",
 "That is the argument for Latin filler generally. When you put real copy into an unfinished design, reviewers read the copy and comment on the wording rather than the typography, hierarchy and spacing you actually wanted feedback on. Meaningless text keeps attention on the visual system.",
 "There is a counter-argument worth knowing. Real content has properties that Lorem ipsum lacks, actual heading lengths, awkward product names, and the wildly varying string lengths that break layouts in production. Many designers now prototype with realistic sample content for exactly that reason. Use Latin filler for early-stage layout exploration, and switch to representative real copy before you sign off on anything.",
 ],
 ),
 script=r""" const CLASSIC = ('lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut ' +
 'labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea ' +
 'commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum eu fugiat nulla pariatur excepteur ' +
 'sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum at vero eos ' +
 'accusamus iusto odio dignissimos ducimus blanditiis praesentium voluptatum deleniti atque corrupti quos').split(' ');

 const MODERN = ('the quick design system needs a clear structure before any colour is chosen layout comes first ' +
 'then typography then contrast a page should read well before it looks good spacing carries more weight than most ' +
 'people expect and a consistent scale removes a hundred small decisions from every screen you build after that ' +
 'the work becomes assembling parts rather than inventing them each time which is the entire point of the exercise ' +
 'good defaults beat clever options and restraint tends to age better than novelty in almost every case').split(' ');

 const HIPSTER = ('scalable microservice architecture leverages containerised deployment pipelines to orchestrate ' +
 'distributed workloads across ephemeral compute nodes observability tooling surfaces latency percentiles while ' +
 'circuit breakers isolate cascading failures declarative infrastructure encodes environment parity and idempotent ' +
 'migrations keep schema drift bounded event sourcing preserves an immutable audit trail whereas eventual ' +
 'consistency trades strict ordering for partition tolerance under load at the edge of the service mesh').split(' ');

 const VOCAB = { classic: CLASSIC, modern: MODERN, hipster: HIPSTER };
 const OPENER = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit';
 let lastResult = '';

 /** One sentence of 6-16 words, capitalised and punctuated. */
 function sentence(vocab) {
 const n = T.randomInt(6, 16);
 const parts = Array.from({ length: n }, () => T.pick(vocab));

 let s = parts.join(' ');
 // Insert a comma somewhere in the middle of longer sentences
 if (n > 9) {
 const at = T.randomInt(3, n - 3);
 parts[at] = parts[at] + ',';
 s = parts.join(' ');
 }

 return s[0].toUpperCase() + s.slice(1) + '.';
 }

 function paragraph(vocab) {
 return Array.from({ length: T.randomInt(3, 6) }, () => sentence(vocab)).join(' ');
 }

 function generate() {
 const vocab = VOCAB[T.$('flavour').value];
 const unit = T.$('unit').value;
 const count = Number(T.$('count').value);
 const wrap = T.$('wrap-html').checked;

 let parts;

 if (unit === 'words') {
 parts = [Array.from({ length: count }, () => T.pick(vocab)).join(' ')];
 } else if (unit === 'sentences') {
 parts = Array.from({ length: count }, () => sentence(vocab));
 } else {
 parts = Array.from({ length: count }, () => paragraph(vocab));
 }

 if (T.$('start-lorem').checked && T.$('flavour').value === 'classic' && unit !== 'words') {
 parts[0] = OPENER + ', ' + parts[0][0].toLowerCase() + parts[0].slice(1);
 }

 lastResult = wrap
 ? parts.map((p) => '<p>' + p + '</p>').join('\n')
 : parts.join(unit === 'paragraphs' ? '\n\n' : ' ');

 T.setOutput('output', lastResult);

 const words = T.words(lastResult).length;
 T.$('output-stats').textContent = `${words.toLocaleString()} words · ${lastResult.length.toLocaleString()} characters`;
 T.status('status', `Generated ${count} ${unit}.`, 'ok');
 }

 T.$('count').addEventListener('input', () => {
 T.$('count-value').textContent = T.$('count').value;
 generate();
 });

 T.on(['unit', 'flavour', 'start-lorem', 'wrap-html'], generate, 'change');
 T.$('generate').addEventListener('click', generate);

 T.wireActions({ slug: 'lorem-ipsum-generator', getResult: () => lastResult, filename: 'lorem-ipsum.txt' });
 generate();""",
))

# ---------------------------------------------------------------
# 5. Text Reverser
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="text-reverser", name="Text Reverser", icon="↔️", cat="text",
 title="Text Reverser: Reverse Characters, Words or Lines",
 description="Reverse text by characters, words or lines, with correct handling of emoji and accented characters. Includes a palindrome check.",
 tagline="Reverse text by character, word or line, with correct emoji handling.",
 workspace=ws(
 textarea("input", "Your text", "Type something to reverse…", rows=140),
 select("mode", "Reverse by", [
 ("chars", "Characters, “hello” → “olleh”"),
 ("words", "Words, “one two” → “two one”"),
 ("lines", "Lines, first line becomes last"),
 ("words-inner", "Each word individually, “one two” → “eno owt”"),
 ], selected="chars"),
 status_line("status", "Output updates as you type."),
 HR,
 output("output", "Reversed", "output-stats"),
 html_block(' <p id="palindrome" class="field__hint"></p>'),
 buttons(("copy", "Copy result", "primary"), ("swap", "Use result as input"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
 label="Text reverser",
 ),
 info_block=info(
 features=[
 "Four reversal modes",
 "Grapheme-aware, emoji and combining accents stay intact",
 "Automatic palindrome detection",
 "Feed the result back in with one click",
 ],
 howto=[
 "Type or paste your text.",
 "Choose what to reverse: characters, words or lines.",
 "The result updates immediately.",
 "Copy it, or press Use result as input to reverse again.",
 ],
 background_title="Why reversing a string is harder than it looks",
 background_paragraphs=[
 "The obvious approach, <code>str.split('').reverse().join('')</code>: is subtly broken. JavaScript strings are sequences of UTF-16 code units, and any character outside the Basic Multilingual Plane occupies two of them. Splitting on code units tears those pairs apart, so reversing a string containing an emoji produces replacement characters instead of the emoji.",
 "Combining marks cause a second problem. The letter é can be a single code point, or it can be a plain <code>e</code> followed by a combining acute accent. Reverse the second form naively and the accent detaches, landing on whatever character now precedes it. Flag emoji, skin-tone modifiers and family sequences are made of several code points joined by zero-width joiners and break the same way.",
 "This tool uses <code>Intl.Segmenter</code> where the browser supports it, which splits text into grapheme clusters, what a reader would call a character, rather than code units. Where it is unavailable, it falls back to a code-point split, which at least keeps surrogate pairs together. That handles emoji correctly even if some exotic combining sequences still shift.",
 ],
 ),
 script=r""" const input = T.$('input');
 let lastResult = '';

 /**
 * Split into user-perceived characters (grapheme clusters).
 * Falls back to code points where Intl.Segmenter is unavailable.
 * @param {string} s
 * @returns {string[]}
 */
 function graphemes(s) {
 if (typeof Intl !== 'undefined' && Intl.Segmenter) {
 const seg = new Intl.Segmenter(undefined, { granularity: 'grapheme' });
 return Array.from(seg.segment(s), (part) => part.segment);
 }
 return Array.from(s); // spread iterates code points, keeping surrogate pairs whole
 }

 const MODES = {
 chars: (s) => graphemes(s).reverse().join(''),
 words: (s) => s.split(/(\s+)/).reverse().join(''),
 lines: (s) => s.split(/\r?\n/).reverse().join('\n'),
 'words-inner': (s) => s.replace(/\S+/g, (w) => graphemes(w).reverse().join(''))
 };

 function run() {
 const text = input.value;

 if (!text) {
 lastResult = '';
 T.setOutput('output', '');
 T.$('output-stats').textContent = '';
 T.$('palindrome').textContent = '';
 T.status('status', 'Output updates as you type.', 'muted');
 return;
 }

 lastResult = MODES[T.$('mode').value](text);
 T.setOutput('output', lastResult);
 T.$('output-stats').textContent = lastResult.length.toLocaleString() + ' characters';
 T.status('status', 'Reversed.', 'ok');

 // Palindrome check ignores case, spacing and punctuation
 const normalised = text.toLowerCase().replace(/[^a-z0-9]/g, '');
 const node = T.$('palindrome');

 if (normalised.length >= 3) {
 const isPalindrome = normalised === graphemes(normalised).reverse().join('');
 node.textContent = isPalindrome
 ? '✓ This is a palindrome, it reads the same in both directions.'
 : '';
 node.style.color = 'var(--success)';
 } else {
 node.textContent = '';
 }
 }

 input.addEventListener('input', debounce(run, 120));
 T.$('mode').addEventListener('change', run);

 T.$('swap').addEventListener('click', () => {
 if (!lastResult) return;
 input.value = lastResult;
 run();
 });

 T.$('clear').addEventListener('click', () => { input.value = ''; run(); input.focus(); });

 T.wireActions({ slug: 'text-reverser', getResult: () => lastResult, filename: 'reversed.txt' });
 run();""",
))

# ---------------------------------------------------------------
# 6. Remove Duplicate Lines
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="remove-duplicate-lines", name="Remove Duplicate Lines", icon="🧹", cat="text",
 title="Remove Duplicate Lines: Deduplicate Any List Instantly",
 description="Strip repeated lines from any list while keeping the original order. Case-insensitive and whitespace-trimming options, plus a duplicate count report.",
 tagline="Strip repeated lines from a list, keeping the first occurrence of each.",
 workspace=ws(
 textarea("input", "Your list", "One item per line…", "input-stats", rows=200),
 row(
 switch("trim", "Trim surrounding whitespace", True),
 switch("ignore-case", "Case-insensitive matching", False),
 switch("drop-empty", "Remove blank lines", True),
 ),
 row(
 select("sort", "Sort output", [("none", "Keep original order"), ("asc", "A → Z"), ("desc", "Z → A"), ("length", "Shortest first")], selected="none"),
 select("keep", "When duplicated", [("first", "Keep the first occurrence"), ("last", "Keep the last occurrence"), ("unique", "Remove all duplicated lines entirely")], selected="first"),
 ),
 status_line("status", "Paste a list to deduplicate it."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-in">0</span><span class="result__label">Lines in</span></div>
 <div class="result result--primary"><span class="result__value" id="r-out">0</span><span class="result__label">Lines out</span></div>
 <div class="result"><span class="result__value" id="r-removed">0</span><span class="result__label">Removed</span></div>
 </div>"""),
 output("output", "Deduplicated list"),
 STD_ACTIONS,
 label="Remove duplicate lines",
 ),
 info_block=info(
 features=[
 "Preserves original order by default",
 "Case-insensitive and whitespace-trimming modes",
 "Keep the first or last occurrence, or drop duplicates entirely",
 "Optional alphabetical or length sorting",
 "Reports exactly how many lines were removed",
 ],
 howto=[
 "Paste your list, one item per line.",
 "Choose how strictly lines should be matched.",
 "Decide which occurrence to keep.",
 "Copy the deduplicated list or download it.",
 ],
 background_title="Choosing the right matching rules",
 background_paragraphs=[
 "Exact matching is the safest default but often misses what you meant. Trailing spaces are invisible and extremely common in lists pasted from spreadsheets or terminal output, so <code>apple</code> and <code>apple&nbsp;</code> look identical while comparing as different strings. Leaving the trim option on catches those.",
 "Case sensitivity depends entirely on your data. Email addresses are case-insensitive in the domain part and effectively so in practice, meaning <code>User@Example.com</code> and <code>user@example.com</code> reach the same inbox. Passwords, file paths on Linux, and most identifiers are case-sensitive, so folding case there would destroy meaning.",
 "The third option deserves explanation. <em>Keep the first occurrence</em> and <em>keep the last</em> both leave you with one copy of every line. <em>Remove all duplicated lines entirely</em> does something different: it keeps only lines that appeared exactly once, discarding every line that was ever repeated. That is what you want when you are looking for the items unique to a list rather than a tidy version of it.",
 ],
 ),
 script=r""" const input = T.$('input');
 let lastResult = '';

 function run() {
 const raw = input.value;
 T.$('input-stats').textContent = raw ? raw.split(/\r?\n/).length.toLocaleString() + ' lines' : '';

 if (!raw.trim()) {
 lastResult = '';
 T.setOutput('output', '');
 ['r-in', 'r-out', 'r-removed'].forEach((id) => { T.$(id).textContent = '0'; });
 T.status('status', 'Paste a list to deduplicate it.', 'muted');
 return;
 }

 let lines = raw.split(/\r?\n/);
 const totalIn = lines.length;

 if (T.$('trim').checked) lines = lines.map((l) => l.trim());
 if (T.$('drop-empty').checked) lines = lines.filter((l) => l.trim() !== '');

 const norm = (l) => (T.$('ignore-case').checked ? l.toLowerCase() : l);

 // Count occurrences first, needed for the "unique only" mode
 const counts = new Map();
 lines.forEach((l) => counts.set(norm(l), (counts.get(norm(l)) || 0) + 1));

 const mode = T.$('keep').value;
 let out;

 if (mode === 'unique') {
 out = lines.filter((l) => counts.get(norm(l)) === 1);
 } else {
 const seen = new Set();
 const source = mode === 'last' ? [...lines].reverse() : lines;
 out = source.filter((l) => {
 const k = norm(l);
 if (seen.has(k)) return false;
 seen.add(k);
 return true;
 });
 if (mode === 'last') out.reverse();
 }

 const sort = T.$('sort').value;
 if (sort === 'asc') out.sort((a, b) => a.localeCompare(b));
 else if (sort === 'desc') out.sort((a, b) => b.localeCompare(a));
 else if (sort === 'length') out.sort((a, b) => a.length - b.length || a.localeCompare(b));

 lastResult = out.join('\n');
 T.setOutput('output', lastResult);

 T.$('r-in').textContent = totalIn.toLocaleString();
 T.$('r-out').textContent = out.length.toLocaleString();
 T.$('r-removed').textContent = (totalIn - out.length).toLocaleString();

 const removed = totalIn - out.length;
 T.status('status', removed
 ? `Removed ${removed.toLocaleString()} line(s).`
 : 'No duplicates found, every line is unique.', 'ok');
 }

 input.addEventListener('input', debounce(run, 250));
 T.on(['trim', 'ignore-case', 'drop-empty', 'sort', 'keep'], run, 'change');

 T.wireActions({ slug: 'remove-duplicate-lines', getResult: () => lastResult, filename: 'deduplicated.txt' });
 run();""",
))

# ---------------------------------------------------------------
# 7. Find and Replace
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="find-and-replace", name="Find and Replace", icon="🔁", cat="text",
 title="Find and Replace: Bulk Text Replacement with Regex Support",
 description="Bulk find-and-replace across large text with optional regular expressions, capture groups, case sensitivity and live match highlighting.",
 tagline="Bulk find-and-replace with optional regex, capture groups and live match highlighting.",
 workspace=ws(
 textarea("input", "Your text", "Paste the text you want to edit…", "input-stats", rows=200),
 row(
 text_input("find", "Find", "Text or pattern to search for"),
 text_input("replace", "Replace with", "Leave blank to delete matches"),
 ),
 row(
 switch("regex", "Treat “Find” as a regular expression", False),
 switch("case", "Case sensitive", False),
 switch("whole", "Whole words only", False),
 ),
 status_line("status", "Enter something to find."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Preview</span><span class="field__hint">Matches highlighted in place</span></span>
 <div class="output output--empty" id="preview">Matches will be highlighted here.</div>
 </div>"""),
 output("output", "Result", "output-stats"),
 buttons(("apply", "Replace all", "primary"), ("copy", "Copy result"), ("download", "Download"), ("undo", "Undo"), ("share", "Share tool", "ghost")),
 label="Find and replace",
 ),
 info_block=info(
 features=[
 "Plain-text or regular-expression matching",
 "Capture group references such as $1 in the replacement",
 "Case-sensitive and whole-word modes",
 "Live preview highlighting every match before you commit",
 "Undo the last replacement",
 ],
 howto=[
 "Paste your text into the top box.",
 "Type what to find and what to replace it with.",
 "Check the preview, matches are highlighted.",
 "Press Replace all, then copy the result.",
 ],
 background_title="Using regular expressions safely",
 background_paragraphs=[
 "With regex mode off, your search text is escaped and matched literally, so characters like <code>.</code> and <code>*</code> mean exactly themselves. That is almost always what you want for ordinary editing, and it prevents the surprise of a full stop matching every character in the document.",
 "Turn regex mode on and the pattern gains real power. <code>\\d+</code> matches runs of digits, <code>\\s+</code> matches whitespace, and parentheses create capture groups you can reference in the replacement as <code>$1</code>, <code>$2</code> and so on. Swapping <code>(\\w+), (\\w+)</code> for <code>$2 $1</code> reverses comma-separated pairs across an entire file in one pass.",
 "Two cautions. First, always read the preview before replacing, a pattern that matches more than you expected is the single most common way to damage a document, and the highlighting exists precisely to catch that. Second, certain nested-quantifier patterns such as <code>(a+)+b</code> can take exponential time on non-matching input, freezing the tab. If the preview stops updating after you type a complex pattern, simplify it.",
 ],
 ),
 script=r""" const input = T.$('input');
 let lastResult = '';
 let history = null;

 const escapeRegex = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

 /**
 * Build the search RegExp from the current options.
 * @returns {RegExp|null} null if the pattern is invalid or empty
 */
 function buildPattern() {
 const find = T.$('find').value;
 if (!find) return null;

 let source = T.$('regex').checked ? find : escapeRegex(find);
 if (T.$('whole').checked) source = '\\b(?:' + source + ')\\b';

 const flags = 'g' + (T.$('case').checked ? '' : 'i');

 try {
 return new RegExp(source, flags);
 } catch (err) {
 T.status('status', 'Invalid regular expression: ' + err.message, 'error');
 return false; // distinguishes "invalid" from "empty"
 }
 }

 function preview() {
 const text = input.value;
 T.$('input-stats').textContent = text.length.toLocaleString() + ' characters';

 const pattern = buildPattern();

 if (pattern === null) {
 T.setOutput('preview', '', 'Matches will be highlighted here.');
 T.status('status', 'Enter something to find.', 'muted');
 return;
 }
 if (pattern === false) return; // error already reported

 let count = 0;
 const html = T.esc(text).replace(
 new RegExp(pattern.source, pattern.flags),
 (m) => { count++; return `<span class="hl">${m}</span>`; }
 );

 T.setOutputHTML('preview', html || '');
 T.status('status',
 count ? `${count.toLocaleString()} match(es) found.` : 'No matches.',
 count ? 'ok' : 'warn');
 }

 function apply() {
 const pattern = buildPattern();
 if (!pattern) return;

 history = input.value;

 try {
 const replaced = input.value.replace(pattern, T.$('replace').value);
 input.value = replaced;
 lastResult = replaced;

 T.setOutput('output', replaced);
 T.$('output-stats').textContent = replaced.length.toLocaleString() + ' characters';

 preview();
 toast({ type: 'success', title: 'Replaced', message: 'Press Undo to revert.' });
 } catch (err) {
 T.status('status', 'Replacement failed: ' + err.message, 'error');
 }
 }

 input.addEventListener('input', debounce(preview, 250));
 T.on(['find', 'replace'], debounce(preview, 250));
 T.on(['regex', 'case', 'whole'], preview, 'change');

 T.$('apply').addEventListener('click', apply);

 T.$('undo').addEventListener('click', () => {
 if (history === null) {
 toast({ type: 'warning', title: 'Nothing to undo' });
 return;
 }
 input.value = history;
 history = null;
 lastResult = '';
 T.setOutput('output', '');
 preview();
 toast({ type: 'success', title: 'Reverted' });
 });

 T.wireActions({ slug: 'find-and-replace', getResult: () => lastResult, filename: 'replaced.txt' });
 preview();""",
))

# ---------------------------------------------------------------
# 8. Text to Speech
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="text-to-speech", name="Text to Speech", icon="🔊", cat="text",
 title="Text to Speech: Read Text Aloud with Your Device Voices",
 description="Read any text aloud using the voices already installed on your device. Adjust rate, pitch and volume. No audio is recorded or transmitted anywhere.",
 tagline="Read text aloud using your device's own voices, nothing is recorded or uploaded.",
 workspace=ws(
 textarea("input", "Text to read", "Type or paste what you would like read aloud…", "input-stats", rows=180),
 row(
 select("voice", "Voice", [("", "Loading voices…")]),
 slider("rate", "Speed", 0.5, 2, 1, 0.1, unit="×"),
 ),
 row(
 slider("pitch", "Pitch", 0, 2, 1, 0.1, unit=""),
 slider("volume", "Volume", 0, 1, 1, 0.05, unit=""),
 ),
 status_line("status", "Press Speak to begin."),
 buttons(("speak", "Speak", "primary"), ("pause", "Pause"), ("resume", "Resume"), ("stop", "Stop", "ghost"), ("share", "Share tool", "ghost")),
 html_block(""" <p class="field__hint">
 Speech is produced by your operating system's built-in synthesiser through the Web Speech API.
 Your text is passed to the local speech engine and is not sent to this site or any third party.
 Note that some browsers route certain premium voices through a cloud service, if that matters
 for your content, pick a voice marked “local” in the list.
 </p>"""),
 label="Text to speech",
 ),
 info_block=info(
 features=[
 "Uses every voice installed on your device",
 "Adjustable rate, pitch and volume",
 "Pause and resume mid-sentence",
 "Highlights nothing and stores nothing",
 "Works offline with locally installed voices",
 ],
 howto=[
 "Paste the text you want read aloud.",
 "Choose a voice and adjust the speed.",
 "Press Speak.",
 "Use Pause and Resume to control playback.",
 ],
 background_title="About the Web Speech API",
 background_paragraphs=[
 "Speech synthesis in the browser is handled by <code>speechSynthesis</code>, which hands your text to the voice engine already installed on your operating system. That means the available voices differ by platform: macOS and iOS ship a large set, Windows includes several, and Linux depends on whether a package like espeak or Festival is present. If the voice list is empty, no synthesiser is installed.",
 "Voice quality varies enormously. Older concatenative voices sound robotic; recent neural voices on macOS, Windows 11 and Android are close to natural. Some browsers list cloud-backed voices alongside local ones, those send text to a remote service to be rendered. The list here marks which voices report themselves as local, and choosing one of those keeps everything on your device.",
 "Two quirks are worth knowing. Chrome silently truncates utterances longer than roughly 32,000 characters, so this tool splits long text into sentence-sized chunks and queues them. And most browsers require a user gesture before the first utterance will play, which is why nothing happens until you press Speak.",
 ],
 ),
 script=r""" const input = T.$('input');
 const synth = window.speechSynthesis;
 let voices = [];

 if (!synth) {
 T.status('status', 'This browser does not support speech synthesis.', 'error');
 ['speak', 'pause', 'resume', 'stop'].forEach((id) => { T.$(id).disabled = true; });
 }

 /** Populate the voice dropdown, marking local voices. */
 function loadVoices() {
 voices = synth.getVoices();
 const select = T.$('voice');

 if (!voices.length) {
 select.innerHTML = '<option value="">No voices installed on this device</option>';
 return;
 }

 select.innerHTML = '';
 voices.forEach((v, i) => {
 const opt = document.createElement('option');
 opt.value = String(i);
 opt.textContent = `${v.name} (${v.lang})${v.localService ? ', local' : ', cloud'}`;
 if (v.default) opt.selected = true;
 select.append(opt);
 });
 }

 if (synth) {
 loadVoices();
 // Voices load asynchronously in Chrome; this fires once they arrive
 synth.addEventListener('voiceschanged', loadVoices);
 }

 /** Split into chunks small enough to survive Chrome's utterance limit. */
 function chunk(text, size = 200) {
 const parts = text.match(/[^.!?]+[.!?]*\s*/g) || [text];
 const out = [];
 let buf = '';

 for (const part of parts) {
 if ((buf + part).length > size && buf) {
 out.push(buf);
 buf = part;
 } else {
 buf += part;
 }
 }
 if (buf) out.push(buf);
 return out;
 }

 function speak() {
 const text = input.value.trim();

 if (!text) {
 T.status('status', 'Enter some text first.', 'error');
 return;
 }

 synth.cancel();

 const voice = voices[Number(T.$('voice').value)] || null;
 const chunks = chunk(text);
 let spoken = 0;

 chunks.forEach((part, i) => {
 const utter = new SpeechSynthesisUtterance(part);
 if (voice) utter.voice = voice;
 utter.rate = Number(T.$('rate').value);
 utter.pitch = Number(T.$('pitch').value);
 utter.volume = Number(T.$('volume').value);

 utter.addEventListener('end', () => {
 spoken++;
 if (spoken === chunks.length) T.status('status', 'Finished.', 'ok');
 else T.status('status', `Speaking, part ${spoken + 1} of ${chunks.length}.`, 'ok');
 });

 utter.addEventListener('error', (e) => {
 if (e.error !== 'interrupted') T.status('status', 'Playback error: ' + e.error, 'error');
 });

 synth.speak(utter);
 });

 T.status('status', `Speaking ${T.words(text).length} words in ${chunks.length} part(s).`, 'ok');
 if (window.Analytics) Analytics.trackToolUse('text-to-speech');
 }

 input.addEventListener('input', debounce(() => {
 T.$('input-stats').textContent = T.words(input.value).length.toLocaleString() + ' words';
 }, 250));

 ['rate', 'pitch', 'volume'].forEach((id) => {
 T.$(id).addEventListener('input', () => {
 T.$(id + '-value').textContent = T.$(id).value;
 });
 });

 T.$('speak').addEventListener('click', speak);
 T.$('pause').addEventListener('click', () => { synth.pause(); T.status('status', 'Paused.', 'warn'); });
 T.$('resume').addEventListener('click', () => { synth.resume(); T.status('status', 'Resumed.', 'ok'); });
 T.$('stop').addEventListener('click', () => { synth.cancel(); T.status('status', 'Stopped.', 'muted'); });
 T.$('share').addEventListener('click', () => shareLink({ title: 'Text to Speech | 123MiniApps' }));

 // Stop speaking if the user navigates away mid-utterance
 window.addEventListener('beforeunload', () => synth && synth.cancel());""",
))

# ---------------------------------------------------------------
# 9. Character Counter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="character-counter", name="Character Counter", icon="🔤", cat="text",
 title="Character Counter: Track Limits for Tweets, Meta Tags and SMS",
 description="Count characters against platform limits for social posts, meta descriptions, SMS and more. Live remaining count with an over-limit warning.",
 tagline="Count characters against the limit that actually matters for where you're posting.",
 workspace=ws(
 textarea("input", "Your text", "Start typing…", rows=180),
 row(
 select("platform", "Limit preset", [
 ("280", "X / Twitter post, 280"),
 ("160", "SMS single message, 160"),
 ("155", "Meta description, 155"),
 ("60", "SEO page title, 60"),
 ("2200", "Instagram caption, 2,200"),
 ("3000", "LinkedIn post, 3,000"),
 ("5000", "Facebook post, 5,000"),
 ("100", "YouTube title, 100"),
 ("custom", "Custom limit…"),
 ], selected="280"),
 text_input("custom-limit", "Custom limit", "e.g. 500", "", "number", attrs='min="1"'),
 ),
 switch("count-spaces", "Include spaces in the count", True),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-used">0</span><span class="result__label">Characters used</span></div>
 <div class="result"><span class="result__value" id="r-left">280</span><span class="result__label">Remaining</span></div>
 <div class="result"><span class="result__value" id="r-words">0</span><span class="result__label">Words</span></div>
 <div class="result"><span class="result__value" id="r-sms">1</span><span class="result__label">SMS segments</span></div>
 </div>"""),
 html_block(""" <div class="meter" id="meter" role="img" aria-label="Usage against the limit">
 <span class="meter__seg"></span><span class="meter__seg"></span>
 <span class="meter__seg"></span><span class="meter__seg"></span>
 </div>"""),
 status_line("status", "Choose a platform and start typing."),
 buttons(("copy", "Copy text", "primary"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
 label="Character counter",
 ),
 info_block=info(
 features=[
 "Nine platform presets plus a custom limit",
 "Live remaining count that goes negative when over",
 "Optional exclusion of spaces",
 "SMS segment calculation including Unicode handling",
 "Visual usage meter",
 ],
 howto=[
 "Pick the platform you are writing for.",
 "Type or paste your text.",
 "Watch the remaining count as you write.",
 "Copy the text once it fits.",
 ],
 background_title="Why character limits are not all the same",
 background_paragraphs=[
 "Different platforms count differently, and the differences matter. X counts most characters as one but treats CJK characters as two, and any URL as a fixed 23 characters regardless of its real length. Meta descriptions have no hard limit at all, Google truncates around 155 to 160 characters of rendered width, so a description full of wide characters gets cut sooner than the count suggests.",
 "SMS is the strangest case. A message using only the GSM 7-bit alphabet fits 160 characters in one segment. Include a single character outside that set, a curly apostrophe, an em dash or any emoji, and the whole message switches to UCS-2 encoding, dropping the limit to 70 characters per segment. That is why pasting text from a word processor can unexpectedly triple your messaging cost: the smart quotes did it.",
 "Multi-part messages shrink further, to 153 characters per segment for GSM and 67 for UCS-2, because each part carries a header telling the receiving phone how to reassemble them. The segment counter here accounts for all of that, so it will sometimes show two segments where a naive character count suggests one.",
 ],
 ),
 script=r""" const input = T.$('input');

 // GSM 03.38 basic set, anything outside it forces UCS-2 encoding
 const GSM = new Set(
 ("@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?" +
 "¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà").split('')
 );
 const GSM_EXT = new Set(['\f', '^', '{', '}', '\\', '[', '~', ']', '|', '€']);

 /**
 * Work out how many SMS segments a message needs.
 * @param {string} text
 * @returns {{segments: number, encoding: string, chars: number}}
 */
 function smsSegments(text) {
 const isGsm = [...text].every((c) => GSM.has(c) || GSM_EXT.has(c));

 if (isGsm) {
 // Extended characters occupy two septets
 const septets = [...text].reduce((n, c) => n + (GSM_EXT.has(c) ? 2 : 1), 0);
 const segments = septets <= 160 ? 1 : Math.ceil(septets / 153);
 return { segments: septets === 0 ? 0 : segments, encoding: 'GSM-7', chars: septets };
 }

 const units = text.length; // UTF-16 code units, which is what UCS-2 counts
 const segments = units <= 70 ? 1 : Math.ceil(units / 67);
 return { segments: units === 0 ? 0 : segments, encoding: 'UCS-2', chars: units };
 }

 function currentLimit() {
 const preset = T.$('platform').value;
 if (preset === 'custom') return Math.max(1, Number(T.$('custom-limit').value) || 1);
 return Number(preset);
 }

 function update() {
 const raw = input.value;
 const counted = T.$('count-spaces').checked ? raw : raw.replace(/\s/g, '');
 const used = counted.length;
 const limit = currentLimit();
 const left = limit - used;

 T.$('r-used').textContent = used.toLocaleString();
 T.$('r-left').textContent = left.toLocaleString();
 T.$('r-left').style.color = left < 0 ? 'var(--danger)' : left < limit * 0.1 ? 'var(--warning)' : '';
 T.$('r-words').textContent = T.words(raw).length.toLocaleString();

 const sms = smsSegments(raw);
 T.$('r-sms').textContent = sms.segments.toLocaleString();

 // Meter fills in quarters
 const ratio = T.clamp(used / limit, 0, 1);
 const lit = Math.ceil(ratio * 4);
 const key = left < 0 ? 'weak' : ratio > 0.9 ? 'fair' : ratio > 0.6 ? 'good' : 'strong';
 T.$$('#meter .meter__seg').forEach((seg, i) => {
 seg.className = 'meter__seg' + (i < lit ? ` is-on-${key}` : '');
 });

 if (left < 0) {
 T.status('status', `Over the limit by ${Math.abs(left).toLocaleString()} character(s).`, 'error');
 } else if (used === 0) {
 T.status('status', 'Choose a platform and start typing.', 'muted');
 } else {
 T.status('status',
 `${left.toLocaleString()} character(s) remaining · ${sms.segments} SMS segment(s) using ${sms.encoding}.`,
 'ok');
 }
 }

 function syncCustom() {
 const isCustom = T.$('platform').value === 'custom';
 T.$('custom-limit').closest('.field').style.display = isCustom ? '' : 'none';
 update();
 }

 input.addEventListener('input', update);
 T.on(['platform'], syncCustom, 'change');
 T.on(['count-spaces'], update, 'change');
 T.$('custom-limit').addEventListener('input', update);

 T.$('copy').addEventListener('click', () => copyToClipboard(input.value, 'Text copied'));
 T.$('clear').addEventListener('click', () => { input.value = ''; update(); input.focus(); });
 T.$('share').addEventListener('click', () => shareLink({ title: 'Character Counter | 123MiniApps' }));

 syncCustom();""",
))

# ---------------------------------------------------------------
# 10. Text Formatter
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="text-formatter", name="Text Formatter", icon="✨", cat="text",
 title="Text Formatter: Clean Up Messy Spacing, Quotes and Line Breaks",
 description="Tidy messy text: collapse extra spaces, normalise line endings, fix smart quotes, remove trailing whitespace and rewrap paragraphs.",
 tagline="Clean up text pasted from PDFs and documents, spacing, quotes and line breaks.",
 workspace=ws(
 textarea("input", "Messy text", "Paste text that needs tidying…", "input-stats", rows=200),
 row(
 switch("collapse-spaces", "Collapse repeated spaces", True),
 switch("trim-lines", "Trim each line", True),
 switch("collapse-blanks", "Collapse repeated blank lines", True),
 ),
 row(
 switch("straight-quotes", "Convert smart quotes to straight", False),
 switch("smart-quotes", "Convert straight quotes to smart", False),
 switch("fix-dashes", "Normalise dashes and ellipses", False),
 ),
 row(
 switch("unwrap", "Join hard-wrapped lines into paragraphs", False),
 switch("strip-html", "Strip HTML tags", False),
 switch("strip-nonprint", "Remove invisible characters", True),
 ),
 status_line("status", "Output updates as you type."),
 HR,
 output("output", "Cleaned text", "output-stats"),
 STD_ACTIONS,
 label="Text formatter",
 ),
 info_block=info(
 features=[
 "Collapse repeated spaces and blank lines",
 "Convert between straight and typographic quotes",
 "Rejoin hard-wrapped lines into flowing paragraphs",
 "Strip HTML tags and invisible control characters",
 "Every transformation is individually toggleable",
 ],
 howto=[
 "Paste the messy text into the top box.",
 "Turn on the cleanups you want.",
 "Check the result below.",
 "Copy or download the cleaned text.",
 ],
 background_title="What actually breaks when you copy text",
 background_paragraphs=[
 "Text copied from a PDF is the worst offender. PDFs store glyph positions rather than flowing text, so extraction inserts a line break at the end of every visual line. Paste that into a document and each line becomes its own paragraph, ignoring the window width entirely. The unwrap option fixes this by joining lines that end mid-sentence while preserving genuine paragraph breaks, blank lines and lines ending in terminal punctuation.",
 "Invisible characters are the ones that cause mysterious bugs. Non-breaking spaces (U+00A0) look identical to normal spaces but do not match <code>\\s</code> in some contexts and break word wrapping. Zero-width spaces, soft hyphens and byte-order marks are completely invisible yet corrupt string comparisons, break CSV parsing and cause a search for a word to fail against text that visibly contains it. The invisible-character option strips them.",
 "Smart quotes are a genuine trade-off rather than a mistake. Typographic quotes and apostrophes look better in prose and are correct for published writing. They break code, CSV files, JSON and command-line input, where only straight quotes parse. Convert to straight quotes when the text is headed anywhere a machine will read it, and to smart quotes when it is headed for a reader.",
 ],
 ),
 script=r""" const input = T.$('input');
 let lastResult = '';

 function run() {
 let text = input.value;
 T.$('input-stats').textContent = text.length.toLocaleString() + ' characters';

 if (!text) {
 lastResult = '';
 T.setOutput('output', '');
 T.$('output-stats').textContent = '';
 T.status('status', 'Output updates as you type.', 'muted');
 return;
 }

 const applied = [];

 // Always normalise line endings first so later rules see one form
 text = text.replace(/\r\n?/g, '\n');

 if (T.$('strip-html').checked) {
 text = text.replace(/<[^>]*>/g, '');
 // Decode the handful of entities that survive tag stripping
 text = text.replace(/&(nbsp|amp|lt|gt|quot|#39);/g, (m, e) =>
 ({ nbsp: ' ', amp: '&', lt: '<', gt: '>', quot: '"', '#39': "'" }[e]));
 applied.push('stripped HTML');
 }

 if (T.$('strip-nonprint').checked) {
 // Zero-width, BOM, soft hyphen, and other invisible formatting marks
 text = text.replace(/[​-‍﻿­⁠]/g, '');
 text = text.replace(/ /g, ' '); // non-breaking → normal space
 applied.push('removed invisible characters');
 }

 if (T.$('unwrap').checked) {
 // Join a line to the next unless it ends a paragraph or looks like a list item
 text = text.replace(/([^\n.!?:;])\n(?!\n)(?![-*•\d]\s)/g, '$1 ');
 applied.push('rejoined wrapped lines');
 }

 if (T.$('collapse-spaces').checked) {
 text = text.replace(/[^\S\n]{2,}/g, ' ');
 applied.push('collapsed spaces');
 }

 if (T.$('trim-lines').checked) {
 text = text.split('\n').map((l) => l.replace(/^[^\S\n]+|[^\S\n]+$/g, '')).join('\n');
 applied.push('trimmed lines');
 }

 if (T.$('collapse-blanks').checked) {
 text = text.replace(/\n{3,}/g, '\n\n');
 applied.push('collapsed blank lines');
 }

 if (T.$('fix-dashes').checked) {
 text = text.replace(/---/g, ', ').replace(/--/g, '–').replace(/\.\.\./g, '…');
 applied.push('normalised dashes');
 }

 if (T.$('straight-quotes').checked) {
 text = text.replace(/[‘’‚‛]/g, "'").replace(/[“”„‟]/g, '"');
 applied.push('straightened quotes');
 } else if (T.$('smart-quotes').checked) {
 // Opening quote after start-of-line or whitespace; closing quote otherwise
 text = text
 .replace(/(^|[\s([{])"/g, '$1“').replace(/"/g, '”')
 .replace(/(^|[\s([{])'/g, '$1‘').replace(/'/g, '’');
 applied.push('applied smart quotes');
 }

 lastResult = text.trim();
 T.setOutput('output', lastResult);

 const saved = input.value.length - lastResult.length;
 T.$('output-stats').textContent =
 lastResult.length.toLocaleString() + ' characters' +
 (saved > 0 ? ` · ${saved.toLocaleString()} removed` : '');

 T.status('status', applied.length ? 'Applied: ' + applied.join(', ') + '.' : 'No cleanups selected.', 'ok');
 }

 // The two quote options are mutually exclusive
 T.$('straight-quotes').addEventListener('change', () => {
 if (T.$('straight-quotes').checked) T.$('smart-quotes').checked = false;
 run();
 });
 T.$('smart-quotes').addEventListener('change', () => {
 if (T.$('smart-quotes').checked) T.$('straight-quotes').checked = false;
 run();
 });

 input.addEventListener('input', debounce(run, 250));
 T.on(['collapse-spaces', 'trim-lines', 'collapse-blanks', 'fix-dashes',
 'unwrap', 'strip-html', 'strip-nonprint'], run, 'change');

 T.wireActions({ slug: 'text-formatter', getResult: () => lastResult, filename: 'cleaned.txt' });
 run();""",
))
