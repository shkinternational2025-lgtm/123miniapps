#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: tools_content.py
# Purpose: The 6 Content Tools (ids 78-83).
# ============================================

from toolkit import (
 tool, ws, info, row, textarea, text_input, number_input, select, switch,
 slider, output, status_line, buttons, STD_ACTIONS, HR, html_block,
)

PAGES = []

# ---------------------------------------------------------------
# 78. Readability Checker
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="readability-checker", name="Readability Checker", icon="📖", cat="content",
 title="Readability Checker: Flesch Score and Grade Level",
 description="Score your writing with Flesch Reading Ease and four other formulas, and highlight long sentences and passive voice that hurt comprehension.",
 tagline="Score your writing for readability and find the sentences that need work.",
 workspace=ws(
 textarea("input", "Your text", "Paste the writing you want to check…", "input-stats", rows=220),
 row(
 select("audience", "Target audience", [
 ("general", "General public, grade 8"),
 ("simple", "Plain English, grade 6"),
 ("professional", "Professional, grade 12"),
 ("academic", "Academic, grade 16"),
 ], selected="general"),
 slider("long-sentence", "Flag sentences over", 15, 45, 25, 1, unit="words"),
 ),
 status_line("status", "Paste some text to analyse it."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-flesch">, </span><span class="result__label">Flesch Reading Ease</span></div>
 <div class="result"><span class="result__value" id="r-grade" style="font-size:var(--text-2xl)">, </span><span class="result__label">Grade level</span></div>
 <div class="result"><span class="result__value" id="r-verdict" style="font-size:var(--text-lg)">, </span><span class="result__label">Verdict</span></div>
 <div class="result"><span class="result__value" id="r-time" style="font-size:var(--text-2xl)">, </span><span class="result__label">Reading time</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>All formulas</span></span>
 <div class="table-scroll"><div id="formulas"></div></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Sentences to look at</span><span class="field__hint">Long sentences highlighted in place</span></span>
 <div class="output output--empty" id="highlight">Problem sentences will be highlighted here.</div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Suggestions</span></span>
 <div id="suggestions"></div>
 </div>"""),
 buttons(("copy", "Copy report", "primary"), ("sample", "Load a sample"), ("share", "Share tool", "ghost")),
 label="Readability checker",
 ),
 info_block=info(
 features=[
 "Flesch Reading Ease and Flesch-Kincaid Grade Level",
 "Gunning Fog, SMOG and Coleman-Liau for comparison",
 "Long-sentence highlighting at a threshold you choose",
 "Passive voice and adverb detection",
 "Target comparison against four audience levels",
 ],
 howto=[
 "Paste your writing into the box.",
 "Pick the audience you are writing for.",
 "Read the score and check the highlighted sentences.",
 "Work through the suggestions and re-check.",
 ],
 background_title="What these scores measure, and their limits",
 background_paragraphs=[
 "Flesch Reading Ease runs from 0 to 100, where higher is easier. It combines average sentence length and average syllables per word, that is genuinely all it looks at. Above 60 is considered plain English suitable for a general audience; below 30 is dense, academic prose. Flesch-Kincaid converts the same inputs into a US school grade level, which is why the two always move together.",
 "Because the formulas only count sentence and word length, they can be gamed and they can be wrong. Chopping a clear sentence into fragments improves the score while making the writing worse. Technical terms your audience knows perfectly well, <code>database</code>, <code>authentication</code>: get penalised for syllable count, while short but obscure words sail through. A high score does not mean the writing is good; it means the sentences are short and the words are simple.",
 "They remain useful as a signal rather than a verdict, and in some contexts they are mandatory: several US states require insurance policies to hit a specific Flesch score, and plain-language legislation often sets similar targets. The practical use is comparative, if a rewrite moves from grade 14 to grade 9, you have almost certainly made it more accessible. Use the highlighted sentences rather than the number as your editing guide.",
 ],
 ),
 script=r""" let report = '';

 const TARGETS = { general: 8, simple: 6, professional: 12, academic: 16 };

 // Common adverbs and passive-voice auxiliaries worth flagging
 const PASSIVE = /\b(?:am|is|are|was|were|be|been|being)\s+(\w+ed|born|done|made|given|taken|seen|known|found|used|held|shown|written|built|sent|kept|told)\b/gi;

 function syllablesIn(text) {
 return T.words(text).reduce((sum, word) => sum + T.syllables(word), 0);
 }

 function countComplexWords(words) {
 // Three or more syllables, excluding common suffix inflections
 return words.filter((word) => {
 if (T.syllables(word) < 3) return false;
 if (/(?:es|ed|ing)$/i.test(word) && T.syllables(word.replace(/(?:es|ed|ing)$/i, '')) < 3) {
 return false;
 }
 return true;
 }).length;
 }

 function analyse() {
 const text = T.$('input').value;
 T.$('input-stats').textContent = text
 ? `${T.words(text).length.toLocaleString()} words`
 : '';

 if (!text.trim() || T.words(text).length < 10) {
 ['r-flesch', 'r-grade', 'r-verdict', 'r-time'].forEach((id) => { T.$(id).textContent = ', '; });
 T.$('formulas').innerHTML = '';
 T.setOutput('highlight', '', 'Problem sentences will be highlighted here.');
 T.$('suggestions').innerHTML = '';
 T.status('status', 'Paste at least ten words to analyse.', 'muted');
 return;
 }

 const words = T.words(text);
 const sentences = T.sentences(text);
 const wordCount = words.length;
 const sentenceCount = Math.max(1, sentences.length);
 const syllableCount = syllablesIn(text);
 const complexWords = countComplexWords(words);
 const letters = text.replace(/[^a-zA-Z]/g, '').length;

 const wordsPerSentence = wordCount / sentenceCount;
 const syllablesPerWord = syllableCount / wordCount;

 // Flesch Reading Ease
 const flesch = 206.835 - 1.015 * wordsPerSentence - 84.6 * syllablesPerWord;

 // Flesch-Kincaid Grade Level
 const fkGrade = 0.39 * wordsPerSentence + 11.8 * syllablesPerWord - 15.59;

 // Gunning Fog
 const fog = 0.4 * (wordsPerSentence + 100 * (complexWords / wordCount));

 // SMOG, needs 30 sentences to be reliable, but approximates below that
 const smog = 1.0430 * Math.sqrt(complexWords * (30 / sentenceCount)) + 3.1291;

 // Coleman-Liau
 const L = (letters / wordCount) * 100;
 const S = (sentenceCount / wordCount) * 100;
 const coleman = 0.0588 * L - 0.296 * S - 15.8;

 const clampedFlesch = T.clamp(flesch, 0, 100);

 T.$('r-flesch').textContent = clampedFlesch.toFixed(1);
 T.$('r-grade').textContent = Math.max(1, Math.round(fkGrade));
 T.$('r-time').textContent = T.duration((wordCount / 225) * 60);

 // Verdict banding
 let verdict, colour;
 if (clampedFlesch >= 80) { verdict = 'Very easy'; colour = 'var(--success)'; }
 else if (clampedFlesch >= 60) { verdict = 'Plain English'; colour = 'var(--success)'; }
 else if (clampedFlesch >= 50) { verdict = 'Fairly difficult'; colour = 'var(--warning)'; }
 else if (clampedFlesch >= 30) { verdict = 'Difficult'; colour = 'var(--warning)'; }
 else { verdict = 'Very difficult'; colour = 'var(--danger)'; }

 T.$('r-verdict').textContent = verdict;
 T.$('r-verdict').style.color = colour;

 renderFormulas({ flesch: clampedFlesch, fkGrade, fog, smog, coleman,
 wordsPerSentence, syllablesPerWord, complexWords, wordCount, sentenceCount });

 highlightSentences(text, sentences);
 renderSuggestions({ wordsPerSentence, complexWords, wordCount, text, fkGrade });

 const target = TARGETS[T.$('audience').value];
 const delta = fkGrade - target;

 T.status('status',
 Math.abs(delta) <= 1.5
 ? `Grade ${Math.round(fkGrade)}, well matched to your target audience.`
 : delta > 0
 ? `Grade ${Math.round(fkGrade)} is about ${Math.round(delta)} level(s) above your target of ${target}.`
 : `Grade ${Math.round(fkGrade)} is below your target of ${target}, you may be over-simplifying.`,
 Math.abs(delta) <= 1.5 ? 'ok' : 'warn');

 report = [
 `Flesch Reading Ease: ${clampedFlesch.toFixed(1)} (${verdict})`,
 `Flesch-Kincaid Grade: ${fkGrade.toFixed(1)}`,
 `Gunning Fog: ${fog.toFixed(1)}`,
 `SMOG: ${smog.toFixed(1)}`,
 `Coleman-Liau: ${coleman.toFixed(1)}`,
 `Words: ${wordCount}, Sentences: ${sentenceCount}`,
 `Average sentence length: ${wordsPerSentence.toFixed(1)} words`
 ].join('\n');

 if (window.Analytics) Analytics.trackToolUse('readability-checker');
 }

 function renderFormulas(m) {
 const mount = T.$('formulas');
 mount.innerHTML = '';

 mount.append(T.table(['Measure', 'Score', 'Interpretation'], [
 ['Flesch Reading Ease', m.flesch.toFixed(1), m.flesch >= 60 ? 'Plain English' : 'Harder than plain English'],
 ['Flesch-Kincaid Grade', m.fkGrade.toFixed(1), `US grade ${Math.max(1, Math.round(m.fkGrade))}`],
 ['Gunning Fog', m.fog.toFixed(1), `${Math.round(m.fog)} years of education`],
 ['SMOG', m.smog.toFixed(1), m.sentenceCount < 30 ? 'Approximate, needs 30+ sentences' : `Grade ${Math.round(m.smog)}`],
 ['Coleman-Liau', m.coleman.toFixed(1), `Grade ${Math.max(1, Math.round(m.coleman))}`],
 ['Average sentence length', m.wordsPerSentence.toFixed(1) + ' words', m.wordsPerSentence > 25 ? 'Long' : 'Reasonable'],
 ['Average syllables per word', m.syllablesPerWord.toFixed(2), m.syllablesPerWord > 1.7 ? 'Complex vocabulary' : 'Straightforward'],
 ['Complex words', `${m.complexWords} (${((m.complexWords / m.wordCount) * 100).toFixed(1)}%)`,
 m.complexWords / m.wordCount > 0.15 ? 'Above typical' : 'Typical']
 ]));
 }

 function highlightSentences(text, sentences) {
 const threshold = Number(T.$('long-sentence').value);
 let html = T.esc(text);
 let flagged = 0;

 // Wrap sentences that exceed the threshold, longest first so that
 // replacing one does not disturb the others
 const long = sentences
 .filter((sentence) => T.words(sentence).length > threshold)
 .sort((a, b) => b.length - a.length);

 long.forEach((sentence) => {
 const escaped = T.esc(sentence);
 if (html.includes(escaped) && !html.includes(`class="hl">${escaped}`)) {
 html = html.replace(escaped, `<span class="hl">${escaped}</span>`);
 flagged++;
 }
 });

 T.setOutputHTML('highlight', html);
 void flagged;
 }

 function renderSuggestions({ wordsPerSentence, complexWords, wordCount, text, fkGrade }) {
 const mount = T.$('suggestions');
 mount.innerHTML = '';

 const tips = [];

 if (wordsPerSentence > 25) {
 tips.push(['Sentences are long', `Averaging ${wordsPerSentence.toFixed(0)} words. Splitting the highlighted sentences is the single fastest way to improve the score.`]);
 }

 if (complexWords / wordCount > 0.15) {
 tips.push(['High proportion of long words', `${((complexWords / wordCount) * 100).toFixed(0)}% of words have three or more syllables. Check whether shorter alternatives exist, but do not replace terms your readers already know.`]);
 }

 const passiveMatches = text.match(PASSIVE) || [];
 if (passiveMatches.length > 2) {
 tips.push(['Passive voice detected', `${passiveMatches.length} likely passive construction(s), such as “${passiveMatches[0]}”. Active voice is usually shorter and clearer.`]);
 }

 const adverbs = (text.match(/\b\w+ly\b/gi) || []).length;
 if (adverbs > wordCount * 0.04) {
 tips.push(['Many -ly adverbs', `${adverbs} found. Adverbs often signal a weak verb, “ran quickly” is usually better as “sprinted”.`]);
 }

 const target = TARGETS[T.$('audience').value];
 if (fkGrade > target + 2) {
 tips.push(['Above your target audience', `You are writing at grade ${Math.round(fkGrade)} for a grade ${target} audience.`]);
 }

 if (!tips.length) {
 mount.append(el('p', {
 className: 'text-sm',
 text: '✓ No obvious readability problems detected.',
 style: { color: 'var(--success)' }
 }));
 return;
 }

 const list = el('div', { className: 'stack' });
 tips.forEach(([heading, detail]) => {
 list.append(el('div', { className: 'info-panel' }, [
 el('strong', { className: 'text-sm', text: heading }),
 el('p', { className: 'text-sm text-muted mt-2', text: detail })
 ]));
 });
 mount.append(list);
 }

 const SAMPLE = 'The implementation of the aforementioned methodology necessitates a comprehensive ' +
 'understanding of the underlying architectural paradigms, which, when considered in conjunction ' +
 'with the operational constraints imposed by the existing infrastructure, presents a considerable ' +
 'challenge to practitioners. It is recommended that stakeholders be consulted. The system was ' +
 'designed by the team. Configuration is performed automatically.';

 T.$('input').addEventListener('input', debounce(analyse, 350));
 T.on(['audience'], analyse, 'change');
 T.$('long-sentence').addEventListener('input', () => {
 T.$('long-sentence-value').textContent = T.$('long-sentence').value;
 analyse();
 });

 T.$('sample').addEventListener('click', () => { T.$('input').value = SAMPLE; analyse(); });
 T.$('copy').addEventListener('click', () => copyToClipboard(report, 'Report copied'));
 T.$('share').addEventListener('click', () => shareLink({ title: 'Readability Checker | 123MiniApps' }));

 analyse();""",
))

# ---------------------------------------------------------------
# 79. Meta Tag Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="meta-tag-generator", name="Meta Tag Generator", icon="🏷️", cat="content",
 title="Meta Tag Generator: SEO, Open Graph and Twitter Cards",
 description="Produce complete SEO, Open Graph and Twitter Card meta tags with a live search-result preview and character-limit warnings.",
 tagline="Generate a complete meta tag block, with a live preview of how it will appear.",
 workspace=ws(
 row(
 text_input("title", "Page title", "Your page title", "123MiniApps, Free Browser Tools"),
 text_input("url", "Canonical URL", "https://example.com/page", "https://www.123miniapps.online/"),
 ),
 html_block(""" <div class="field">
 <label class="field__label" for="description">
 <span>Meta description</span>
 <span class="field__hint" id="desc-count"></span>
 </label>
 <textarea class="textarea" id="description" style="min-height:90px"
 placeholder="A concise summary of the page, around 155 characters.">95 free online tools for text, images, developers and designers. Everything runs in your browser, no uploads, no accounts, no tracking.</textarea>
 </div>"""),
 row(
 text_input("image", "Social image URL", "https://example.com/og.png"),
 text_input("site", "Site name", "123MiniApps"),
 text_input("author", "Author (optional)", "Your name"),
 ),
 row(
 select("type", "Open Graph type", [
 ("website", "website"), ("article", "article"), ("product", "product"), ("profile", "profile"),
 ], selected="website"),
 select("card", "Twitter card type", [
 ("summary_large_image", "Large image"), ("summary", "Summary"),
 ], selected="summary_large_image"),
 text_input("twitter", "Twitter handle", "@yourhandle"),
 ),
 row(
 switch("robots", "Allow indexing", True),
 switch("include-og", "Include Open Graph tags", True),
 switch("include-twitter", "Include Twitter Card tags", True),
 ),
 status_line("status", "Fill in the fields to generate your tags."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Search result preview</span></span>
 <div style="padding:var(--space-5);background:#fff;border-radius:var(--radius-sm);font-family:arial,sans-serif">
 <div id="serp-url" style="color:#202124;font-size:12px;margin-bottom:2px"></div>
 <div id="serp-title" style="color:#1a0dab;font-size:20px;line-height:1.3;margin-bottom:3px"></div>
 <div id="serp-desc" style="color:#4d5156;font-size:14px;line-height:1.58"></div>
 </div>
 </div>"""),
 output("output", "Meta tags", "output-stats"),
 STD_ACTIONS,
 label="Meta tag generator",
 ),
 info_block=info(
 features=[
 "SEO, Open Graph and Twitter Card tags together",
 "Live Google search result preview",
 "Character-limit warnings for title and description",
 "Canonical URL and robots directives",
 "Copy the whole block ready to paste into <head>",
 ],
 howto=[
 "Enter your title, description and URL.",
 "Add a social image, 1200×630 works everywhere.",
 "Check the preview and the character counts.",
 "Copy the block into your page's <head>.",
 ],
 background_title="What actually affects how your page appears",
 background_paragraphs=[
 "Google truncates titles at around 580 pixels of rendered width, not a fixed character count, roughly 55 to 60 characters, but a title full of wide letters gets cut sooner. More importantly, Google rewrites titles it considers unhelpful in a substantial share of cases, so the title tag is a strong suggestion rather than a guarantee. Descriptions are truncated around 155 to 160 characters and are also frequently replaced with text pulled from the page body when that better matches the query.",
 "The meta description has no direct effect on ranking, Google confirmed this years ago. It affects click-through rate, which is worth optimising for on its own terms. The meta keywords tag has been entirely ignored by every major search engine since 2009 and is not generated here.",
 "Open Graph tags matter more than people expect, because they control how a link looks everywhere it is shared: Facebook, LinkedIn, Slack, Discord, WhatsApp and iMessage all read them. Twitter falls back to Open Graph when Twitter-specific tags are absent, so the twitter: tags are largely optional. Use an absolute URL for <code>og:image</code>: relative paths silently fail, and size it 1200×630, which is the aspect ratio every major platform crops toward.",
 ],
 ),
 script=r""" let lastResult = '';

 const LIMITS = { title: 60, description: 158 };

 function esc(s) { return T.esc(s); }

 function generate() {
 const title = T.$('title').value.trim();
 const description = T.$('description').value.trim();
 const url = T.$('url').value.trim();
 const image = T.$('image').value.trim();
 const site = T.$('site').value.trim();
 const author = T.$('author').value.trim();
 const twitter = T.$('twitter').value.trim();

 T.$('desc-count').textContent = `${description.length} / ${LIMITS.description} characters`;
 T.$('desc-count').style.color = description.length > LIMITS.description
 ? 'var(--danger)' : description.length < 70 ? 'var(--warning)' : 'var(--text-muted)';

 updatePreview(title, description, url);

 const lines = ['<!-- Primary meta tags -->'];

 if (title) lines.push(`<title>${esc(title)}</title>`);
 if (title) lines.push(`<meta name="title" content="${esc(title)}">`);
 if (description) lines.push(`<meta name="description" content="${esc(description)}">`);
 if (author) lines.push(`<meta name="author" content="${esc(author)}">`);

 lines.push(`<meta name="robots" content="${T.$('robots').checked
 ? 'index, follow, max-image-preview:large' : 'noindex, nofollow'}">`);

 if (url) lines.push(`<link rel="canonical" href="${esc(url)}">`);

 if (T.$('include-og').checked) {
 lines.push('', '<!-- Open Graph, Facebook, LinkedIn, Slack, Discord, WhatsApp -->');
 lines.push(`<meta property="og:type" content="${esc(T.$('type').value)}">`);
 if (site) lines.push(`<meta property="og:site_name" content="${esc(site)}">`);
 if (title) lines.push(`<meta property="og:title" content="${esc(title)}">`);
 if (description) lines.push(`<meta property="og:description" content="${esc(description)}">`);
 if (url) lines.push(`<meta property="og:url" content="${esc(url)}">`);
 if (image) {
 lines.push(`<meta property="og:image" content="${esc(image)}">`);
 lines.push('<meta property="og:image:width" content="1200">');
 lines.push('<meta property="og:image:height" content="630">');
 lines.push(`<meta property="og:image:alt" content="${esc(title)}">`);
 }
 lines.push('<meta property="og:locale" content="en_US">');
 }

 if (T.$('include-twitter').checked) {
 lines.push('', '<!-- Twitter Card -->');
 lines.push(`<meta name="twitter:card" content="${esc(T.$('card').value)}">`);
 if (twitter) {
 lines.push(`<meta name="twitter:site" content="${esc(twitter)}">`);
 lines.push(`<meta name="twitter:creator" content="${esc(twitter)}">`);
 }
 if (title) lines.push(`<meta name="twitter:title" content="${esc(title)}">`);
 if (description) lines.push(`<meta name="twitter:description" content="${esc(description)}">`);
 if (image) lines.push(`<meta name="twitter:image" content="${esc(image)}">`);
 }

 lines.push('', '<!-- Viewport and charset, required on every page -->');
 lines.push('<meta charset="utf-8">');
 lines.push('<meta name="viewport" content="width=device-width, initial-scale=1">');

 lastResult = lines.join('\n');
 T.setOutput('output', lastResult);
 T.$('output-stats').textContent = `${lines.filter((l) => l.startsWith('<')).length} tags`;

 reportWarnings(title, description, image, url);
 }

 function updatePreview(title, description, url) {
 const truncate = (text, limit) =>
 text.length > limit ? text.slice(0, limit - 1).trimEnd() + '…' : text;

 let display = url || 'https://example.com';
 try {
 const parsed = new URL(url);
 display = parsed.hostname + (parsed.pathname === '/' ? '' : parsed.pathname.replace(/\//g, ' › '));
 } catch { /* leave the raw value */ }

 T.$('serp-url').textContent = display;
 T.$('serp-title').textContent = truncate(title || 'Untitled page', LIMITS.title);
 T.$('serp-desc').textContent = truncate(
 description || 'No description provided. Google will generate one from the page content.',
 LIMITS.description);
 }

 function reportWarnings(title, description, image, url) {
 const issues = [];

 if (!title) issues.push('no title');
 else if (title.length > LIMITS.title) issues.push(`title is ${title.length} characters and will be truncated`);
 else if (title.length < 20) issues.push('title is very short');

 if (!description) issues.push('no description');
 else if (description.length > LIMITS.description) issues.push(`description is ${description.length} characters and will be truncated`);
 else if (description.length < 70) issues.push('description is short, aim for 120 to 155');

 if (!image) issues.push('no social image, so shared links will show no preview');
 else if (!/^https?:\/\//i.test(image)) issues.push('the social image must be an absolute URL');

 if (!url) issues.push('no canonical URL');

 if (!T.$('robots').checked) issues.push('indexing is disabled, search engines will skip this page');

 T.status('status',
 issues.length ? 'Check: ' + issues.join('; ') + '.' : 'All the essentials are present.',
 issues.length ? 'warn' : 'ok');

 if (window.Analytics) Analytics.trackToolUse('meta-tag-generator');
 }

 T.on(['title', 'description', 'url', 'image', 'site', 'author', 'twitter'],
 debounce(generate, 250));
 T.on(['type', 'card', 'robots', 'include-og', 'include-twitter'], generate, 'change');

 T.wireActions({
 slug: 'meta-tag-generator',
 getResult: () => lastResult,
 filename: 'meta-tags.html',
 mime: 'text/html'
 });

 generate();""",
))

# ---------------------------------------------------------------
# 80. Keyword Density Checker
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="keyword-density-checker", name="Keyword Density Checker", icon="📊", cat="content",
 title="Keyword Density Checker: Word and Phrase Frequency",
 description="Find your most-used words and phrases with density percentages, stop-word filtering and an over-optimisation warning for keyword stuffing.",
 tagline="See which words and phrases dominate your text, and whether you have overdone it.",
 workspace=ws(
 textarea("input", "Your text", "Paste your content here…", "input-stats", rows=220),
 row(
 select("ngram", "Phrase length", [
 ("1", "Single words"), ("2", "Two-word phrases"),
 ("3", "Three-word phrases"), ("all", "All lengths"),
 ], selected="1"),
 number_input("min-count", "Minimum occurrences", "2", "2", step="1", min=1),
 switch("stopwords", "Ignore common stop words", True),
 ),
 row(
 text_input("focus", "Focus keyword (optional)", "Check density for one specific term"),
 switch("case", "Case sensitive", False),
 ),
 status_line("status", "Paste text to analyse it."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result"><span class="result__value" id="r-words" style="font-size:var(--text-2xl)">, </span><span class="result__label">Total words</span></div>
 <div class="result"><span class="result__value" id="r-unique" style="font-size:var(--text-2xl)">, </span><span class="result__label">Unique words</span></div>
 <div class="result"><span class="result__value" id="r-variety" style="font-size:var(--text-2xl)">, </span><span class="result__label">Lexical variety</span></div>
 <div class="result result--primary"><span class="result__value" id="r-focus" style="font-size:var(--text-2xl)">, </span><span class="result__label">Focus keyword</span></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Frequency table</span><span class="field__hint">Sorted by count</span></span>
 <div class="table-scroll"><div id="table"></div></div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>Assessment</span></span>
 <div id="assessment"></div>
 </div>"""),
 buttons(("copy", "Copy table", "primary"), ("download", "Download CSV"), ("share", "Share tool", "ghost")),
 label="Keyword density checker",
 ),
 info_block=info(
 features=[
 "Single words, two-word and three-word phrases",
 "Stop-word filtering",
 "Density percentages against total word count",
 "Focus keyword tracking",
 "Over-optimisation warning",
 ],
 howto=[
 "Paste your content into the box.",
 "Choose whether to look at words or phrases.",
 "Enter a focus keyword to track it specifically.",
 "Check the assessment for stuffing warnings.",
 ],
 background_title="Keyword density is a diagnostic, not a target",
 background_paragraphs=[
 "There is no optimal keyword density, and there has not been one for well over a decade. Google's algorithms moved to semantic understanding with Hummingbird in 2013 and BERT in 2019, which means they interpret what a page is about from context rather than counting term repetitions. Any guide quoting a magic figure like 2.5% is repeating advice that stopped being true a long time ago.",
 "Where density remains useful is as a diagnostic. If your target term appears zero times, the page probably is not clearly about it. If it appears 40 times in 500 words, the writing is almost certainly unnatural, and that is a real risk, Google's spam policies explicitly name keyword stuffing, and the penalty is applied to pages that read as written for a crawler rather than a person.",
 "The more useful signal in this table is the phrase list rather than the single-word one. Two and three-word phrases show what your content actually covers, and they often reveal that a page is unfocused, if the top phrases have nothing to do with each other, the page is trying to be about too many things. Modern SEO rewards covering a topic thoroughly with natural language, including related terms and synonyms, over hitting any repetition count.",
 ],
 ),
 script=r""" const STOP_WORDS = new Set(('a about above after again against all am an and any are as at be because been ' +
 'before being below between both but by can cannot could did do does doing down during each few for ' +
 'from further had has have having he her here hers herself him himself his how i if in into is it its ' +
 'itself me more most my myself no nor not of off on once only or other ought our ours ourselves out ' +
 'over own same she should so some such than that the their theirs them themselves then there these ' +
 'they this those through to too under until up very was we were what when where which while who whom ' +
 'why with would you your yours yourself yourselves will just also').split(' '));

 let rows = [];

 function tokenise(text) {
 const caseSensitive = T.$('case').checked;
 const words = T.words(text).map((word) => (caseSensitive ? word : word.toLowerCase()));
 return words;
 }

 function buildNgrams(words, n) {
 const counts = new Map();

 for (let i = 0; i <= words.length - n; i++) {
 const gram = words.slice(i, i + n);

 // For single words, drop stop words. For phrases, drop only
 // those made entirely of stop words, "state of the art" is
 // a real phrase even though three of its words are stop words.
 if (T.$('stopwords').checked) {
 const lowered = gram.map((g) => g.toLowerCase());
 if (n === 1 && STOP_WORDS.has(lowered[0])) continue;
 if (n > 1 && lowered.every((g) => STOP_WORDS.has(g))) continue;
 }

 if (n === 1 && gram[0].length < 2) continue;

 const key = gram.join(' ');
 counts.set(key, (counts.get(key) || 0) + 1);
 }

 return counts;
 }

 function analyse() {
 const text = T.$('input').value;
 const words = tokenise(text);

 T.$('input-stats').textContent = words.length
 ? `${words.length.toLocaleString()} words`
 : '';

 if (words.length < 10) {
 ['r-words', 'r-unique', 'r-variety', 'r-focus'].forEach((id) => { T.$(id).textContent = ', '; });
 T.$('table').innerHTML = '';
 T.$('assessment').innerHTML = '';
 T.status('status', 'Paste at least ten words to analyse.', 'muted');
 return;
 }

 const minCount = Math.max(1, Math.floor(T.num(T.$('min-count').value) || 1));
 const selection = T.$('ngram').value;
 const lengths = selection === 'all' ? [1, 2, 3] : [Number(selection)];

 const collected = [];
 lengths.forEach((n) => {
 buildNgrams(words, n).forEach((count, phrase) => {
 if (count < minCount) return;
 collected.push({
 phrase,
 length: n,
 count,
 density: (count / words.length) * 100
 });
 });
 });

 collected.sort((a, b) => b.count - a.count || a.phrase.localeCompare(b.phrase));
 rows = collected.slice(0, 40);

 const unique = new Set(words.map((word) => word.toLowerCase())).size;

 T.$('r-words').textContent = words.length.toLocaleString();
 T.$('r-unique').textContent = unique.toLocaleString();
 T.$('r-variety').textContent = ((unique / words.length) * 100).toFixed(1) + '%';

 // Focus keyword
 const focus = T.$('focus').value.trim().toLowerCase();
 if (focus) {
 const focusWords = focus.split(/\s+/).length;
 const focusCount = buildFocusCount(words, focus, focusWords);
 const density = (focusCount / words.length) * 100;
 T.$('r-focus').textContent = focusCount
 ? `${focusCount}× (${density.toFixed(1)}%)`
 : 'Not found';
 T.$('r-focus').style.color = !focusCount ? 'var(--danger)'
 : density > 4 ? 'var(--danger)' : 'var(--success)';
 } else {
 T.$('r-focus').textContent = ', ';
 T.$('r-focus').style.color = '';
 }

 renderTable();
 renderAssessment(words, rows, focus);

 T.status('status', `${rows.length} term(s) appearing at least ${minCount} time(s).`, 'ok');

 if (window.Analytics) Analytics.trackToolUse('keyword-density-checker');
 }

 function buildFocusCount(words, focus, focusWords) {
 const joined = words.map((word) => word.toLowerCase()).join(' ');
 // Count non-overlapping occurrences of the phrase
 let count = 0;
 let index = 0;
 while ((index = joined.indexOf(focus, index)) !== -1) {
 count++;
 index += focus.length;
 }
 void focusWords;
 return count;
 }

 function renderTable() {
 const mount = T.$('table');
 mount.innerHTML = '';
 if (!rows.length) return;

 const table = T.table(
 ['Term', 'Words', 'Count', 'Density'],
 rows.map((r) => [r.phrase, r.length, r.count, r.density.toFixed(2) + '%'])
 );

 // Flag anything above 4%, which reads as stuffing
 [...table.querySelectorAll('tbody tr')].forEach((tr, i) => {
 if (rows[i].density > 4 && rows[i].length === 1) {
 tr.style.background = 'color-mix(in srgb, var(--danger) 12%, transparent)';
 }
 });

 mount.append(table);
 }

 function renderAssessment(words, list, focus) {
 const mount = T.$('assessment');
 mount.innerHTML = '';

 const notes = [];
 const topSingle = list.filter((r) => r.length === 1)[0];

 if (topSingle && topSingle.density > 5) {
 notes.push(['Possible keyword stuffing',
 `“${topSingle.phrase}” makes up ${topSingle.density.toFixed(1)}% of the text. Above about 4% usually reads as unnatural to a human, which is the real test.`,
 'var(--danger)']);
 }

 if (words.length < 300) {
 notes.push(['Short content',
 `${words.length} words. Density figures are unstable on short text, a single extra mention moves the percentage substantially.`,
 'var(--warning)']);
 }

 const unique = new Set(words.map((w) => w.toLowerCase())).size;
 const variety = (unique / words.length) * 100;
 if (variety < 30 && words.length > 200) {
 notes.push(['Low lexical variety',
 `Only ${variety.toFixed(0)}% of words are distinct. Repetitive phrasing is harder to read and offers search engines less context.`,
 'var(--warning)']);
 }

 if (focus) {
 const found = list.find((r) => r.phrase.toLowerCase() === focus);
 if (!found) {
 notes.push(['Focus keyword not prominent',
 `“${focus}” does not appear often enough to reach the frequency table. If the page is about this topic, it should probably appear in the title, first paragraph and at least one heading.`,
 'var(--warning)']);
 }
 }

 if (!notes.length) {
 mount.append(el('p', {
 className: 'text-sm',
 text: '✓ Nothing concerning, the distribution looks natural.',
 style: { color: 'var(--success)' }
 }));
 return;
 }

 const container = el('div', { className: 'stack' });
 notes.forEach(([heading, detail, colour]) => {
 container.append(el('div', { className: 'info-panel' }, [
 el('strong', { className: 'text-sm', text: heading, style: { color: colour } }),
 el('p', { className: 'text-sm text-muted mt-2', text: detail })
 ]));
 });
 mount.append(container);
 }

 T.$('input').addEventListener('input', debounce(analyse, 350));
 T.on(['focus', 'min-count'], debounce(analyse, 300));
 T.on(['ngram', 'stopwords', 'case'], analyse, 'change');

 T.$('copy').addEventListener('click', () => {
 copyToClipboard(
 rows.map((r) => `${r.phrase}\t${r.count}\t${r.density.toFixed(2)}%`).join('\n'),
 'Table copied');
 });

 T.$('download').addEventListener('click', () => {
 if (!rows.length) { toast({ type: 'warning', title: 'Nothing to download' }); return; }
 const csv = ['Term,Words,Count,Density']
 .concat(rows.map((r) => `"${r.phrase.replace(/"/g, '""')}",${r.length},${r.count},${r.density.toFixed(2)}`))
 .join('\n');
 downloadFile(csv, 'keyword-density.csv', 'text/csv');
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Keyword Density Checker | 123MiniApps' }));

 analyse();""",
))

# ---------------------------------------------------------------
# 81. Citation Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="citation-generator", name="Citation Generator", icon="📚", cat="content",
 title="Citation Generator: APA, MLA, Chicago and Harvard",
 description="Format references in APA 7, MLA 9, Chicago and Harvard styles for books, journal articles, websites and more, with a bibliography builder.",
 tagline="Format references in four citation styles, and build a bibliography as you go.",
 workspace=ws(
 row(
 select("style", "Citation style", [
 ("apa", "APA 7th edition"), ("mla", "MLA 9th edition"),
 ("chicago", "Chicago 17th (notes-bibliography)"), ("harvard", "Harvard"),
 ], selected="apa"),
 select("type", "Source type", [
 ("book", "Book"), ("journal", "Journal article"),
 ("website", "Website"), ("chapter", "Book chapter"), ("news", "Newspaper article"),
 ], selected="journal"),
 ),
 row(
 text_input("authors", "Author(s)", "Surname, First M.; Second, A.", "Lovelace, Ada"),
 text_input("year", "Year", "2026", "2026"),
 ),
 text_input("title", "Title", "Title of the work", "Notes on the Analytical Engine"),
 row(
 text_input("container", "Journal / book / site name", "Where it was published", "Scientific Memoirs"),
 text_input("publisher", "Publisher", "Publisher name"),
 ),
 row(
 text_input("volume", "Volume", "3"),
 text_input("issue", "Issue", "1"),
 text_input("pages", "Pages", "666-731"),
 ),
 row(
 text_input("url", "URL", "https://example.com/article"),
 text_input("doi", "DOI", "10.1000/example"),
 text_input("accessed", "Date accessed", "", "", "date"),
 ),
 status_line("status", "Fill in what you have, blank fields are omitted."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Reference list entry</span></span>
 <div class="output" id="output" style="font-family:var(--font-body)">, </div>
 </div>"""),
 html_block(""" <div class="field">
 <span class="field__label"><span>In-text citation</span></span>
 <div class="output" id="intext" style="font-family:var(--font-body);min-height:52px">, </div>
 </div>"""),
 buttons(("add", "Add to bibliography", "primary"), ("copy", "Copy reference"), ("clear-form", "Clear form", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Bibliography</span><span class="field__hint" id="bib-count"></span></span>
 <div class="output output--empty" id="bibliography" style="font-family:var(--font-body)">Entries you add will appear here, sorted alphabetically.</div>
 </div>"""),
 buttons(("copy-bib", "Copy bibliography", "primary"), ("download", "Download"), ("clear-bib", "Clear bibliography", "ghost"), ("share", "Share tool", "ghost")),
 label="Citation generator",
 ),
 info_block=info(
 features=[
 "Four major citation styles",
 "Five source types including chapters and news",
 "Reference list entry and in-text citation",
 "Bibliography builder with alphabetical sorting",
 "Saved on your device between visits",
 ],
 howto=[
 "Choose a style and source type.",
 "Fill in the fields you have, blanks are omitted.",
 "Copy the reference, or add it to the bibliography.",
 "Download the finished bibliography when done.",
 ],
 background_title="Which style, and why they differ",
 background_paragraphs=[
 "The styles encode different disciplinary priorities. APA puts the year immediately after the author because in the sciences the recency of a finding matters enormously. MLA omits the year from the in-text citation and gives a page number instead, because literary scholarship cares about locating a passage rather than dating a claim. Chicago's notes-bibliography system uses footnotes, which suits history where a citation often carries commentary as well as a source.",
 "Author formatting is where most errors creep in. APA uses initials only and an ampersand before the final author; MLA spells out first names and uses “and”; both invert only the first author's name. APA switched at the 7th edition to listing up to 20 authors before using an ellipsis, where the 6th edition stopped at seven, a change that still catches people using older templates.",
 "Two practical points. Always prefer a DOI to a URL when one exists: DOIs are permanent identifiers that survive a journal moving its site, which URLs frequently do not. And treat any generated citation as a first draft, automated tools including this one cannot verify that the metadata you entered is correct, cannot know whether a source has been retracted, and handle unusual source types imperfectly. Check the output against your institution's style guide before submitting anything that is being marked.",
 ],
 ),
 script=r""" let bibliography = T.store.get('bibliography', []);

 function fields() {
 const get = (id) => T.$(id).value.trim();
 return {
 authors: get('authors'), year: get('year'), title: get('title'),
 container: get('container'), publisher: get('publisher'),
 volume: get('volume'), issue: get('issue'), pages: get('pages'),
 url: get('url'), doi: get('doi'), accessed: get('accessed'),
 type: T.$('type').value
 };
 }

 /**
 * Split the author field into structured names.
 * Accepts "Surname, First M.; Second, A." or "Surname, First".
 */
 function parseAuthors(raw) {
 if (!raw) return [];
 return raw.split(/;|\band\b|&/)
 .map((entry) => entry.trim())
 .filter(Boolean)
 .map((entry) => {
 const [surname, given] = entry.split(',').map((part) => part.trim());
 return { surname: surname || entry, given: given || '' };
 });
 }

 const initials = (given) =>
 given.split(/\s+/).filter(Boolean)
 .map((part) => part[0].toUpperCase() + '.').join(' ');

 /* ---------- Style formatters ---------- */

 function apaAuthors(list) {
 if (!list.length) return '';
 const formatted = list.map((a) => a.given ? `${a.surname}, ${initials(a.given)}` : a.surname);
 if (formatted.length === 1) return formatted[0];
 if (formatted.length === 2) return `${formatted[0]}, & ${formatted[1]}`;
 return formatted.slice(0, -1).join(', ') + ', & ' + formatted[formatted.length - 1];
 }

 function mlaAuthors(list) {
 if (!list.length) return '';
 const first = list[0].given ? `${list[0].surname}, ${list[0].given}` : list[0].surname;
 if (list.length === 1) return first;
 if (list.length === 2) {
 const second = list[1].given ? `${list[1].given} ${list[1].surname}` : list[1].surname;
 return `${first}, and ${second}`;
 }
 return `${first}, et al.`;
 }

 function harvardAuthors(list) {
 if (!list.length) return '';
 const formatted = list.map((a) => a.given ? `${a.surname}, ${initials(a.given)}` : a.surname);
 if (formatted.length === 1) return formatted[0];
 return formatted.slice(0, -1).join(', ') + ' and ' + formatted[formatted.length - 1];
 }

 const join = (parts, sep = ' ') => parts.filter(Boolean).join(sep);

 function formatAPA(f, authors) {
 const who = apaAuthors(authors) || '[No author]';
 const when = f.year ? `(${f.year}).` : '(n.d.).';
 const link = f.doi ? `https://doi.org/${f.doi}` : f.url;

 if (f.type === 'journal') {
 const vol = f.volume ? `${f.volume}${f.issue ? `(${f.issue})` : ''}` : '';
 return join([who, when, `${f.title}.`,
 f.container ? `${f.container}${vol ? ',' : '.'}` : '',
 vol ? `${vol}${f.pages ? ',' : '.'}` : '',
 f.pages ? `${f.pages}.` : '', link]);
 }

 if (f.type === 'website') {
 return join([who, when, `${f.title}.`,
 f.container ? `${f.container}.` : '', link]);
 }

 if (f.type === 'chapter') {
 return join([who, when, `${f.title}.`,
 f.container ? `In ${f.container}` : '',
 f.pages ? `(pp. ${f.pages}).` : '',
 f.publisher ? `${f.publisher}.` : '', link]);
 }

 return join([who, when, `${f.title}.`, f.publisher ? `${f.publisher}.` : '', link]);
 }

 function formatMLA(f, authors) {
 const who = mlaAuthors(authors) || '';
 const link = f.url || (f.doi ? `https://doi.org/${f.doi}` : '');
 const accessed = f.accessed
 ? `Accessed ${new Date(f.accessed).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })}.`
 : '';

 if (f.type === 'journal') {
 return join([who ? `${who}.` : '', `"${f.title}."`,
 f.container ? `${f.container},` : '',
 f.volume ? `vol. ${f.volume},` : '',
 f.issue ? `no. ${f.issue},` : '',
 f.year ? `${f.year},` : '',
 f.pages ? `pp. ${f.pages}.` : '', link]);
 }

 if (f.type === 'website') {
 return join([who ? `${who}.` : '', `"${f.title}."`,
 f.container ? `${f.container},` : '',
 f.year ? `${f.year},` : '', link ? `${link}.` : '', accessed]);
 }

 return join([who ? `${who}.` : '', `${f.title}.`,
 f.publisher ? `${f.publisher},` : '', f.year ? `${f.year}.` : '']);
 }

 function formatChicago(f, authors) {
 const who = authors.length
 ? authors.map((a, i) => i === 0
 ? (a.given ? `${a.surname}, ${a.given}` : a.surname)
 : (a.given ? `${a.given} ${a.surname}` : a.surname)).join(', and ')
 : '';
 const link = f.doi ? `https://doi.org/${f.doi}` : f.url;

 if (f.type === 'journal') {
 return join([who ? `${who}.` : '', `"${f.title}."`,
 f.container ? `${f.container}` : '',
 f.volume ? `${f.volume},` : '',
 f.issue ? `no. ${f.issue}` : '',
 f.year ? `(${f.year}):` : '',
 f.pages ? `${f.pages}.` : '', link]);
 }

 return join([who ? `${who}.` : '', `${f.title}.`,
 f.publisher ? `${f.publisher},` : '', f.year ? `${f.year}.` : '', link]);
 }

 function formatHarvard(f, authors) {
 const who = harvardAuthors(authors) || '[No author]';
 const link = f.url || (f.doi ? `https://doi.org/${f.doi}` : '');
 const accessed = f.accessed
 ? `[Accessed ${new Date(f.accessed).toLocaleDateString('en-GB')}]`
 : '';

 if (f.type === 'journal') {
 return join([`${who}`, f.year ? `(${f.year})` : '(n.d.)',
 `'${f.title}',`, f.container ? `${f.container},` : '',
 f.volume ? `${f.volume}${f.issue ? `(${f.issue})` : ''},` : '',
 f.pages ? `pp. ${f.pages}.` : '', link]);
 }

 return join([`${who}`, f.year ? `(${f.year})` : '(n.d.)',
 `${f.title}.`, f.publisher ? `${f.publisher}.` : '', link, accessed]);
 }

 function inTextCitation(f, authors) {
 const style = T.$('style').value;
 const surname = authors.length ? authors[0].surname : 'Author';
 const etal = authors.length > 2 ? ' et al.' : authors.length === 2
 ? ` ${style === 'apa' ? '&' : 'and'} ${authors[1].surname}` : '';

 if (style === 'apa') return `(${surname}${etal}, ${f.year || 'n.d.'})`;
 if (style === 'harvard') return `(${surname}${etal}, ${f.year || 'n.d.'})`;
 if (style === 'mla') return `(${surname}${authors.length > 2 ? ' et al.' : ''} ${f.pages ? f.pages.split('-')[0] : ''})`.trim() + ')';
 return `${surname}${etal}, "${f.title}," ${f.year || 'n.d.'}.`;
 }

 function generate() {
 const f = fields();
 const authors = parseAuthors(f.authors);

 if (!f.title) {
 T.setOutput('output', '', ', ');
 T.setOutput('intext', '', ', ');
 T.status('status', 'Enter at least a title.', 'muted');
 return '';
 }

 const style = T.$('style').value;
 const formatter = { apa: formatAPA, mla: formatMLA, chicago: formatChicago, harvard: formatHarvard }[style];
 const reference = formatter(f, authors).replace(/\s+/g, ' ').replace(/\s([.])/g, '$1').trim();

 T.setOutput('output', reference);
 T.setOutput('intext', inTextCitation(f, authors));

 const missing = [];
 if (!authors.length) missing.push('author');
 if (!f.year) missing.push('year');
 if (f.type === 'journal' && !f.container) missing.push('journal name');
 if (f.type === 'website' && !f.url) missing.push('URL');

 T.status('status',
 missing.length
 ? `Generated, but missing: ${missing.join(', ')}. Check against your style guide.`
 : 'Generated. Verify against your institution’s guide before submitting.',
 missing.length ? 'warn' : 'ok');

 if (window.Analytics) Analytics.trackToolUse('citation-generator');
 return reference;
 }

 function renderBibliography() {
 const mount = T.$('bibliography');
 mount.innerHTML = '';

 if (!bibliography.length) {
 mount.textContent = 'Entries you add will appear here, sorted alphabetically.';
 mount.classList.add('output--empty');
 T.$('bib-count').textContent = '';
 return;
 }

 mount.classList.remove('output--empty');
 const sorted = [...bibliography].sort((a, b) => a.localeCompare(b));

 sorted.forEach((entry) => {
 mount.append(el('p', {
 text: entry,
 style: {
 marginBottom: 'var(--space-3)',
 paddingLeft: '2em',
 textIndent: '-2em' // hanging indent, as every style requires
 }
 }));
 });

 T.$('bib-count').textContent = `${bibliography.length} entr${bibliography.length === 1 ? 'y' : 'ies'}`;
 }

 T.on(['authors', 'year', 'title', 'container', 'publisher', 'volume',
 'issue', 'pages', 'url', 'doi', 'accessed'], debounce(generate, 250));
 T.on(['style', 'type'], generate, 'change');

 T.$('add').addEventListener('click', () => {
 const reference = generate();
 if (!reference) {
 toast({ type: 'warning', title: 'Nothing to add', message: 'Enter at least a title.' });
 return;
 }
 if (bibliography.includes(reference)) {
 toast({ type: 'warning', title: 'Already in the bibliography' });
 return;
 }
 bibliography.push(reference);
 T.store.set('bibliography', bibliography);
 renderBibliography();
 toast({ type: 'success', title: 'Added', message: 'Stored on this device only.' });
 });

 T.$('copy').addEventListener('click', () => copyToClipboard(T.$('output').textContent, 'Reference copied'));

 T.$('copy-bib').addEventListener('click', () =>
 copyToClipboard([...bibliography].sort().join('\n\n'), 'Bibliography copied'));

 T.$('download').addEventListener('click', () => {
 if (!bibliography.length) { toast({ type: 'warning', title: 'Bibliography is empty' }); return; }
 downloadFile([...bibliography].sort().join('\n\n'), 'bibliography.txt');
 });

 T.$('clear-form').addEventListener('click', () => {
 ['authors', 'year', 'title', 'container', 'publisher', 'volume',
 'issue', 'pages', 'url', 'doi', 'accessed'].forEach((id) => { T.$(id).value = ''; });
 generate();
 });

 T.$('clear-bib').addEventListener('click', () => {
 bibliography = [];
 T.store.set('bibliography', bibliography);
 renderBibliography();
 });

 T.$('share').addEventListener('click', () => shareLink({ title: 'Citation Generator | 123MiniApps' }));

 renderBibliography();
 generate();""",
))

# ---------------------------------------------------------------
# 82. Blog Title Generator
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="blog-title-generator", name="Blog Title Generator", icon="✏️", cat="content",
 title="Blog Title Generator: Headline Variations from a Topic",
 description="Turn a topic into dozens of headline variations across proven formats, with length scoring for search results and power-word suggestions.",
 tagline="Spin a topic into headline variations, scored for length and clarity.",
 workspace=ws(
 row(
 text_input("topic", "Your topic", "e.g. remote work productivity", "remote work productivity"),
 text_input("audience", "Audience (optional)", "e.g. freelancers"),
 ),
 row(
 select("tone", "Tone", [
 ("all", "Every format"), ("howto", "How-to and guides"),
 ("list", "Listicles"), ("question", "Questions"),
 ("contrarian", "Contrarian and opinion"), ("beginner", "Beginner-friendly"),
 ], selected="all"),
 number_input("count", "How many", "20", "20", step="1", min=5, max=60),
 ),
 status_line("status", "Enter a topic and press Generate."),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Headlines</span><span class="field__hint">Green length is ideal for search results · click to copy</span></span>
 <div id="results"></div>
 </div>"""),
 buttons(("generate", "Generate", "primary"), ("copy", "Copy all"), ("download", "Download"), ("share", "Share tool", "ghost")),
 HR,
 html_block(""" <div class="field">
 <span class="field__label"><span>Power words to consider</span></span>
 <div class="chip-grid" id="power"></div>
 </div>"""),
 label="Blog title generator",
 ),
 info_block=info(
 features=[
 "Ten headline formulas across five tones",
 "Length scoring against the search-result limit",
 "Audience insertion for targeted headlines",
 "Power-word suggestions",
 "Up to 60 variations at once",
 ],
 howto=[
 "Type your topic as a plain noun phrase.",
 "Optionally name the audience you are writing for.",
 "Pick a tone, or leave it on every format.",
 "Click any headline to copy it.",
 ],
 background_title="What makes a headline work",
 background_paragraphs=[
 "Around 50 to 60 characters is the practical sweet spot, because that is roughly where Google truncates a title in search results. Longer headlines are not wrong, they just get cut, so front-load the words that matter. This tool colour-codes length for that reason rather than because shorter is inherently better.",
 "Numbers work, and the research on why is fairly consistent: they promise a bounded, scannable structure. A reader knows what they are committing to with “7 ways” in a way they do not with “ways”. Odd numbers slightly outperform even ones in most tests, though the effect is small enough that it should not override a genuine count.",
 "The line worth not crossing is between curiosity and deception. Curiosity gaps, withholding just enough to make someone want the answer, are legitimate and effective. Clickbait promises something the article does not deliver, and while it may win the click, it loses the reader, damages return visits, and increasingly gets punished by platforms measuring dwell time. The reliable test is whether the headline would still feel honest to someone who has finished reading.",
 ],
 ),
 script=r""" const FORMULAS = {
 howto: [
 'How to {topic} (Without {pain})',
 'How to {topic} in {n} Simple Steps',
 'The Complete Guide to {topic}',
 'How I {verbed} {topic} in {timeframe}',
 '{topic}: A Practical Guide for {audience}'
 ],
 list: [
 '{n} {adj} Ways to {topic}',
 '{n} {topic} Mistakes Almost Everyone Makes',
 '{n} Tools That Make {topic} Easier',
 '{n} Things Nobody Tells You About {topic}',
 'The {n} {adj} Rules of {topic}'
 ],
 question: [
 'Is {topic} Actually Worth It?',
 'Why Does {topic} Feel So Hard?',
 'What Nobody Tells You About {topic}',
 'Should You {topic}? Here Is the Honest Answer',
 'Can You Really {topic} Without {pain}?'
 ],
 contrarian: [
 'Why Everything You Know About {topic} Is Wrong',
 'Stop {topic}. Do This Instead.',
 'The Uncomfortable Truth About {topic}',
 '{topic} Is Overrated. Here Is Why.',
 'I Was Wrong About {topic}'
 ],
 beginner: [
 '{topic} for Beginners: Where to Actually Start',
 'A Beginner’s Guide to {topic}',
 '{topic}, Explained Simply',
 'The Absolute Basics of {topic}',
 'New to {topic}? Read This First'
 ]
 };

 const ADJECTIVES = ['Practical', 'Surprising', 'Proven', 'Underrated', 'Essential',
 'Simple', 'Effective', 'Overlooked', 'Honest', 'Counterintuitive'];

 const PAINS = ['Burning Out', 'Wasting Time', 'Losing Your Mind', 'Spending a Fortune',
 'Starting Over', 'Overthinking It', 'the Usual Advice'];

 const TIMEFRAMES = ['a Week', '30 Days', 'Three Months', 'a Single Afternoon', 'Under an Hour'];

 const VERBS = ['Fixed', 'Rethought', 'Rebuilt', 'Simplified', 'Doubled'];

 const POWER_WORDS = ['proven', 'essential', 'surprising', 'effortless', 'honest', 'practical',
 'complete', 'ultimate', 'simple', 'underrated', 'quietly', 'actually', 'finally',
 'without', 'nobody', 'stop', 'truth', 'mistake'];

 let headlines = [];

 const titleCase = (s) => s.replace(/\b\w/g, (c) => c.toUpperCase());

 function generate() {
 const topicRaw = T.$('topic').value.trim();
 const audience = T.$('audience').value.trim() || 'Anyone';
 const count = T.clamp(Math.floor(T.num(T.$('count').value) || 20), 5, 60);
 const tone = T.$('tone').value;

 if (!topicRaw) {
 T.$('results').innerHTML = '';
 T.status('status', 'Enter a topic to generate headlines.', 'muted');
 return;
 }

 const topic = titleCase(topicRaw);
 const templates = tone === 'all'
 ? Object.values(FORMULAS).flat()
 : FORMULAS[tone];

 const produced = new Set();
 let guard = 0;

 while (produced.size < count && guard < count * 20) {
 guard++;

 const template = T.pick(templates);
 const headline = template
 .replace(/\{topic\}/g, topic)
 .replace(/\{n\}/g, String(T.pick([5, 7, 9, 11, 13])))
 .replace(/\{adj\}/g, T.pick(ADJECTIVES))
 .replace(/\{pain\}/g, T.pick(PAINS))
 .replace(/\{timeframe\}/g, T.pick(TIMEFRAMES))
 .replace(/\{verbed\}/g, T.pick(VERBS))
 .replace(/\{audience\}/g, titleCase(audience));

 produced.add(headline);
 }

 headlines = [...produced];
 render();

 T.status('status', `Generated ${headlines.length} headline(s).`, 'ok');
 if (window.Analytics) Analytics.trackToolUse('blog-title-generator');
 }

 function render() {
 const mount = T.$('results');
 mount.innerHTML = '';

 headlines.forEach((headline) => {
 const length = headline.length;

 // Colour by how it will fare in a search result
 const colour = length <= 60 ? 'var(--success)'
 : length <= 70 ? 'var(--warning)' : 'var(--danger)';
 const note = length <= 60 ? 'ideal'
 : length <= 70 ? 'may be trimmed' : 'will be truncated';

 const row = el('button', {
 className: 'info-panel mb-2',
 attrs: { type: 'button', 'aria-label': `Copy: ${headline}` },
 style: {
 display: 'flex', alignItems: 'center', justifyContent: 'space-between',
 gap: 'var(--space-4)', width: '100%', textAlign: 'left', cursor: 'pointer'
 }
 }, [
 el('span', { text: headline, style: { flex: '1' } }),
 el('span', {
 className: 'badge',
 text: `${length} · ${note}`,
 style: { color: colour, borderColor: colour, flexShrink: '0' }
 })
 ]);

 row.addEventListener('click', () => copyToClipboard(headline, 'Headline copied'));
 mount.append(row);
 });
 }

 function renderPowerWords() {
 const mount = T.$('power');
 mount.innerHTML = '';
 POWER_WORDS.forEach((word) => {
 const chip = el('button', { className: 'chip', attrs: { type: 'button' }, text: word });
 chip.addEventListener('click', () => copyToClipboard(word, `“${word}” copied`));
 mount.append(chip);
 });
 }

 T.$('generate').addEventListener('click', generate);
 T.on(['topic', 'audience', 'count'], debounce(generate, 400));
 T.on(['tone'], generate, 'change');

 T.$('copy').addEventListener('click', () => copyToClipboard(headlines.join('\n'), 'All headlines copied'));
 T.$('download').addEventListener('click', () => {
 if (!headlines.length) { toast({ type: 'warning', title: 'Nothing to download' }); return; }
 downloadFile(headlines.join('\n'), 'headlines.txt');
 });
 T.$('share').addEventListener('click', () => shareLink({ title: 'Blog Title Generator | 123MiniApps' }));

 renderPowerWords();
 generate();""",
))

# ---------------------------------------------------------------
# 83. Text Summarizer
# ---------------------------------------------------------------
PAGES.append(tool(
 slug="text-summarizer", name="Text Summarizer", icon="📄", cat="content",
 title="Text Summarizer: Extract the Key Sentences",
 description="Condense long text to its most important sentences using extractive scoring. Adjustable length, keyword extraction, and runs entirely offline.",
 tagline="Condense long text to its key sentences, extractive, offline, and transparent.",
 workspace=ws(
 textarea("input", "Text to summarise", "Paste an article, report or document…", "input-stats", rows=240),
 row(
 slider("length", "Summary length", 10, 60, 25, 5, unit="%"),
 select("method", "Method", [
 ("hybrid", "Hybrid, position and word frequency"),
 ("frequency", "Word frequency only"),
 ("position", "Position only, lead sentences"),
 ], selected="hybrid"),
 switch("order", "Keep original sentence order", True),
 ),
 status_line("status", "Paste at least a few paragraphs."),
 HR,
 html_block(""" <div class="result-grid">
 <div class="result result--primary"><span class="result__value" id="r-reduction" style="font-size:var(--text-2xl)">, </span><span class="result__label">Reduction</span></div>
 <div class="result"><span class="result__value" id="r-kept" style="font-size:var(--text-2xl)">, </span><span class="result__label">Sentences kept</span></div>
 <div class="result"><span class="result__value" id="r-time" style="font-size:var(--text-2xl)">, </span><span class="result__label">Reading time saved</span></div>
 </div>"""),
 output("output", "Summary", "output-stats"),
 html_block(""" <div class="field">
 <span class="field__label"><span>Key terms</span><span class="field__hint">The words that drove the selection</span></span>
 <div class="chip-grid" id="keywords"></div>
 </div>"""),
 STD_ACTIONS,
 label="Text summarizer",
 ),
 info_block=info(
 features=[
 "Adjustable summary length from 10% to 60%",
 "Three scoring methods",
 "Keyword extraction showing what drove the selection",
 "Preserves original sentence order by default",
 "Runs entirely offline, no model, no API",
 ],
 howto=[
 "Paste the text you want condensed.",
 "Set how much of the original to keep.",
 "Read the summary and the key terms.",
 "Copy or download the result.",
 ],
 background_title="Extractive summarisation, and why it is honest",
 background_paragraphs=[
 "This is extractive summarisation: it selects existing sentences rather than writing new ones. Each sentence is scored on the frequency of its significant words, after stop words are removed, plus a positional bonus, since the opening sentences of a document and of each paragraph disproportionately carry the main claims. The highest-scoring sentences are kept.",
 "The advantage over the abstractive approach used by large language models is that nothing can be fabricated. Every sentence in the summary appeared verbatim in the source, so the summary cannot invent a statistic, misattribute a quotation or assert something the document never said. For legal, medical or technical material, that guarantee is often worth more than fluency.",
 "The limitation is equally clear. Extracted sentences can read disjointedly, and pronouns lose their referents, a kept sentence beginning “This meant that…” may no longer have an antecedent. The method also works best on structured expository writing such as news, reports and documentation, and poorly on narrative, dialogue or anything where meaning is distributed rather than concentrated. Keeping original order, which is the default here, helps coherence considerably.",
 ],
 ),
 script=r""" const STOP_WORDS = new Set(('a about above after again against all am an and any are as at be because been ' +
 'before being below between both but by can cannot could did do does doing down during each few for ' +
 'from further had has have having he her here hers him his how i if in into is it its me more most my ' +
 'no nor not of off on once only or other ought our out over own same she should so some such than that ' +
 'the their them then there these they this those through to too under until up very was we were what ' +
 'when where which while who whom why with would you your also just will').split(' '));

 let lastResult = '';

 /**
 * Score every sentence, then keep the top-scoring share.
 */
 function summarise(text) {
 const sentences = splitSentences(text);
 if (sentences.length < 3) return null;

 const method = T.$('method').value;

 // Word frequencies across the whole document
 const frequencies = new Map();
 T.words(text).forEach((word) => {
 const key = word.toLowerCase();
 if (STOP_WORDS.has(key) || key.length < 3) return;
 frequencies.set(key, (frequencies.get(key) || 0) + 1);
 });

 const maxFrequency = Math.max(1, ...frequencies.values());

 const scored = sentences.map((sentence, index) => {
 const words = T.words(sentence).map((w) => w.toLowerCase());
 const significant = words.filter((w) => !STOP_WORDS.has(w) && w.length >= 3);

 // Normalised frequency score, averaged so long sentences are not
 // automatically favoured
 const frequencyScore = significant.length
 ? significant.reduce((sum, w) => sum + (frequencies.get(w) || 0) / maxFrequency, 0) / significant.length
 : 0;

 // Position score: openings matter most, endings somewhat
 const relative = index / sentences.length;
 const positionScore = relative < 0.15 ? 1
 : relative < 0.3 ? 0.7
 : relative > 0.9 ? 0.5
 : 0.3;

 // Very short sentences rarely carry the main point
 const lengthPenalty = words.length < 6 ? 0.4 : 1;

 let score;
 if (method === 'frequency') score = frequencyScore;
 else if (method === 'position') score = positionScore;
 else score = (frequencyScore * 0.7 + positionScore * 0.3);

 return { sentence, index, score: score * lengthPenalty, words: words.length };
 });

 const share = Number(T.$('length').value) / 100;
 const keep = Math.max(1, Math.round(sentences.length * share));

 const selected = [...scored]
 .sort((a, b) => b.score - a.score)
 .slice(0, keep);

 if (T.$('order').checked) selected.sort((a, b) => a.index - b.index);

 const topKeywords = [...frequencies.entries()]
 .sort((a, b) => b[1] - a[1])
 .slice(0, 12);

 return {
 summary: selected.map((s) => s.sentence.trim()).join(' '),
 keptCount: selected.length,
 totalCount: sentences.length,
 keywords: topKeywords
 };
 }

 /**
 * Split into sentences, keeping the terminal punctuation and
 * avoiding splits on common abbreviations.
 */
 function splitSentences(text) {
 const protectedText = text
 // Swap the period after a known abbreviation for a sentinel so the
 // splitter does not treat it as a sentence boundary. An explicit
 // \u0001 escape keeps this file plain text rather than embedding
 // a raw control byte in the source.
 .replace(/\b(Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|vs|etc|e\.g|i\.e|Inc|Ltd|Co)\./gi, '$1\u0001');

 return protectedText
 .split(/(?<=[.!?])\s+(?=[A-Z"'“])/)
 .map((s) => s.split('\u0001').join('.').trim())
 .filter((s) => s.length > 15);
 }

 function run() {
 const text = T.$('input').value;
 const wordCount = T.words(text).length;

 T.$('input-stats').textContent = wordCount
 ? `${wordCount.toLocaleString()} words`
 : '';

 if (wordCount < 60) {
 lastResult = '';
 T.setOutput('output', '');
 T.$('keywords').innerHTML = '';
 ['r-reduction', 'r-kept', 'r-time'].forEach((id) => { T.$(id).textContent = ', '; });
 T.status('status', 'Paste at least 60 words, summarisation needs something to work with.', 'muted');
 return;
 }

 const result = summarise(text);

 if (!result) {
 T.status('status', 'Could not find enough distinct sentences to summarise.', 'warn');
 return;
 }

 lastResult = result.summary;
 T.setOutput('output', lastResult);

 const summaryWords = T.words(lastResult).length;
 const reduction = ((1 - summaryWords / wordCount) * 100);

 T.$('r-reduction').textContent = reduction.toFixed(0) + '%';
 T.$('r-kept').textContent = `${result.keptCount} / ${result.totalCount}`;
 T.$('r-time').textContent = T.duration(((wordCount - summaryWords) / 225) * 60);
 T.$('output-stats').textContent = `${summaryWords.toLocaleString()} words`;

 renderKeywords(result.keywords);

 T.status('status',
 `Kept ${result.keptCount} of ${result.totalCount} sentences, ${reduction.toFixed(0)}% shorter.`, 'ok');

 if (window.Analytics) Analytics.trackToolUse('text-summarizer');
 }

 function renderKeywords(keywords) {
 const mount = T.$('keywords');
 mount.innerHTML = '';

 keywords.forEach(([word, count]) => {
 mount.append(el('span', { className: 'chip', text: `${word} · ${count}` }));
 });
 }

 T.$('input').addEventListener('input', debounce(run, 400));
 T.on(['method', 'order'], run, 'change');
 T.$('length').addEventListener('input', () => {
 T.$('length-value').textContent = T.$('length').value;
 run();
 });

 T.wireActions({ slug: 'text-summarizer', getResult: () => lastResult, filename: 'summary.txt' });

 run();""",
))
