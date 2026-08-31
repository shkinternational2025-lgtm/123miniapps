/* ============================================
   123MiniApps.online v2.0
   File: test/phase-content.js
   Purpose: Behavioural tests for the 6 content tools.
   ============================================ */

const { boot, Suite, set, click, text, val, wait } = require('./harness');

const num = (s) => Number(String(s).replace(/[^0-9.-]/g, ''));

module.exports = async function run() {
  const s = new Suite('Content tools');

  /* ---------- Readability ---------- */
  {
    const { window: w, errors } = await boot('tools/readability-checker.html');

    // Short, simple sentences should score as very easy
    set(w, 'input', 'The cat sat on the mat. The dog ran fast. Birds fly high. ' +
      'Fish swim well. The sun is hot. Rain falls down. Wind blows hard. ' +
      'Snow is cold. Trees grow tall. Grass is green.');
    await wait(450);
    s.check('readability: simple text scores high', num(text(w, 'r-flesch')) > 80,
      text(w, 'r-flesch'));
    s.match('readability: verdict easy', text(w, 'r-verdict'), /easy|plain/i);

    // Dense academic prose should score low
    click(w, 'sample');
    await wait(450);
    s.check('readability: dense text scores low', num(text(w, 'r-flesch')) < 40,
      text(w, 'r-flesch'));
    s.check('readability: grade level high', num(text(w, 'r-grade')) > 12);

    s.check('readability: formula table renders',
      w.document.querySelector('#formulas table') !== null);
    s.eq('readability: eight formula rows',
      w.document.querySelectorAll('#formulas tbody tr').length, 8);

    // The sample contains passive voice and should be flagged
    const suggestions = w.document.getElementById('suggestions').textContent;
    s.check('readability: gives suggestions on dense text', suggestions.length > 20);

    // Long-sentence highlighting
    set(w, 'long-sentence', '15');
    set(w, 'input', 'This is a deliberately very long sentence that goes on and on well beyond ' +
      'any reasonable threshold for readability purposes indeed. Short one here.');
    await wait(450);
    s.check('readability: highlights long sentences',
      w.document.querySelector('#highlight .hl') !== null);

    set(w, 'input', 'Too short.');
    await wait(450);
    s.match('readability: rejects very short input', text(w, 'status'), /at least ten words/i);
    s.noErrors(errors);
  }

  /* ---------- Meta Tags ---------- */
  {
    const { window: w, errors } = await boot('tools/meta-tag-generator.html');

    set(w, 'title', 'My Page Title');
    set(w, 'description', 'A description of the page that is long enough to be useful for search engines and social sharing previews.');
    set(w, 'url', 'https://example.com/page');
    set(w, 'image', 'https://example.com/og.png');
    await wait(400);

    const out = text(w, 'output');
    s.includes('meta: title tag', out, '<title>My Page Title</title>');
    s.includes('meta: description tag', out, 'name="description"');
    s.includes('meta: canonical link', out, 'rel="canonical"');
    s.includes('meta: og:title', out, 'property="og:title"');
    s.includes('meta: og:image with absolute URL', out, 'content="https://example.com/og.png"');
    s.includes('meta: og:image dimensions', out, 'og:image:width');
    s.includes('meta: twitter card', out, 'name="twitter:card"');
    s.includes('meta: robots index', out, 'index, follow');

    // SERP preview
    s.eq('meta: preview title', text(w, 'serp-title'), 'My Page Title');
    s.includes('meta: preview URL formatted', text(w, 'serp-url'), 'example.com');

    // Over-length description warning
    set(w, 'description', 'x'.repeat(200));
    await wait(400);
    s.match('meta: warns on long description', text(w, 'status'), /will be truncated/i);
    s.check('meta: preview truncates', text(w, 'serp-desc').endsWith('…'));

    // Relative image URL must be flagged
    set(w, 'description', 'A reasonable description of about the right length for a search result snippet here.');
    set(w, 'image', '/relative.png');
    await wait(400);
    s.match('meta: flags relative image URL', text(w, 'status'), /absolute URL/i);

    // Noindex
    set(w, 'image', 'https://example.com/og.png');
    set(w, 'robots', false, 'change');
    await wait(400);
    s.includes('meta: noindex applied', text(w, 'output'), 'noindex, nofollow');
    s.match('meta: warns about noindex', text(w, 'status'), /indexing is disabled/i);

    // Toggling sections off
    set(w, 'robots', true, 'change');
    set(w, 'include-og', false, 'change');
    await wait(400);
    s.check('meta: OG tags removed', !text(w, 'output').includes('og:title'));
    s.noErrors(errors);
  }

  /* ---------- Keyword Density ---------- */
  {
    const { window: w, errors } = await boot('tools/keyword-density-checker.html');

    set(w, 'ngram', '1', 'change');
    set(w, 'stopwords', true, 'change');
    set(w, 'min-count', '2');
    set(w, 'input', 'coffee beans are great. coffee is the best drink. coffee beans roast well. ' +
      'the beans come from farms and the coffee tastes rich and full of flavour today.');
    await wait(450);

    const table = w.document.getElementById('table').textContent;
    s.includes('density: finds top word', table, 'coffee');
    s.check('density: word counts shown', /coffee/.test(table) && /4/.test(table));
    s.check('density: stop words filtered', !/\bthe\b/.test(table.split('\n')[1] || ''));

    // Phrase mode
    set(w, 'ngram', '2', 'change');
    await wait(450);
    s.includes('density: finds two-word phrase',
      w.document.getElementById('table').textContent, 'coffee beans');

    // Focus keyword
    set(w, 'ngram', '1', 'change');
    set(w, 'focus', 'coffee');
    await wait(450);
    s.match('density: focus keyword counted', text(w, 'r-focus'), /4×/);

    set(w, 'focus', 'nonexistent');
    await wait(450);
    s.eq('density: missing focus keyword', text(w, 'r-focus'), 'Not found');

    // Stuffing detection
    set(w, 'focus', '');
    set(w, 'input', ('seo ').repeat(40) + 'and some other words here to pad it out a little bit more.');
    await wait(450);
    s.includes('density: flags stuffing',
      w.document.getElementById('assessment').textContent, 'stuffing');

    s.match('density: lexical variety shown', text(w, 'r-variety'), /%$/);
    s.noErrors(errors);
  }

  /* ---------- Citation ---------- */
  {
    const { window: w, errors } = await boot('tools/citation-generator.html');

    set(w, 'style', 'apa', 'change');
    set(w, 'type', 'journal', 'change');
    set(w, 'authors', 'Lovelace, Ada');
    set(w, 'year', '1843');
    set(w, 'title', 'Notes on the Analytical Engine');
    set(w, 'container', 'Scientific Memoirs');
    set(w, 'volume', '3');
    set(w, 'pages', '666-731');
    await wait(400);

    let out = text(w, 'output');
    s.includes('citation: APA author with initial', out, 'Lovelace, A.');
    s.includes('citation: APA year in brackets', out, '(1843)');
    s.includes('citation: APA journal', out, 'Scientific Memoirs');
    s.includes('citation: APA in-text', text(w, 'intext'), '(Lovelace, 1843)');

    // MLA formats the same source differently
    set(w, 'style', 'mla', 'change');
    await wait(400);
    out = text(w, 'output');
    s.includes('citation: MLA spells out first name', out, 'Lovelace, Ada');
    s.includes('citation: MLA quotes the title', out, '"Notes on the Analytical Engine."');
    s.includes('citation: MLA vol prefix', out, 'vol. 3');

    set(w, 'style', 'harvard', 'change');
    await wait(400);
    s.includes('citation: Harvard single quotes', text(w, 'output'), "'Notes on the Analytical Engine',");

    // Multiple authors
    set(w, 'style', 'apa', 'change');
    set(w, 'authors', 'Lovelace, Ada; Babbage, Charles');
    await wait(400);
    s.includes('citation: APA ampersand for two authors', text(w, 'output'), '& Babbage, C.');

    // Bibliography
    click(w, 'add');
    await wait(300);
    s.includes('citation: added to bibliography',
      w.document.getElementById('bibliography').textContent, 'Lovelace');
    s.match('citation: bibliography count', text(w, 'bib-count'), /1 entry/);

    click(w, 'add');
    await wait(300);
    s.match('citation: duplicate not added twice', text(w, 'bib-count'), /1 entry/);

    click(w, 'clear-bib');
    await wait(300);
    s.eq('citation: bibliography cleared', text(w, 'bib-count'), '');

    // Missing fields are reported
    click(w, 'clear-form');
    await wait(400);
    s.match('citation: empty form handled', text(w, 'status'), /at least a title/i);
    s.noErrors(errors);
  }

  /* ---------- Blog Titles ---------- */
  {
    const { window: w, errors } = await boot('tools/blog-title-generator.html');

    set(w, 'topic', 'remote work');
    set(w, 'count', '20');
    set(w, 'tone', 'all', 'change');
    await wait(500);

    const rows = w.document.querySelectorAll('#results .info-panel');
    s.eq('titles: 20 headlines generated', rows.length, 20);
    s.check('titles: all mention the topic',
      [...rows].every((r) => /Remote Work/i.test(r.textContent)));
    s.check('titles: all unique',
      new Set([...rows].map((r) => r.textContent)).size === 20);
    s.check('titles: length badges shown',
      w.document.querySelectorAll('#results .badge').length === 20);

    // Tone filtering changes the formulas used
    set(w, 'tone', 'question', 'change');
    await wait(500);
    const questions = [...w.document.querySelectorAll('#results .info-panel')]
      .map((r) => r.textContent);
    s.check('titles: question tone produces questions',
      questions.filter((q) => q.includes('?')).length > questions.length / 2);

    set(w, 'tone', 'list', 'change');
    await wait(500);
    const lists = [...w.document.querySelectorAll('#results .info-panel')].map((r) => r.textContent);
    s.check('titles: list tone includes numbers',
      lists.filter((l) => /\d+/.test(l)).length > lists.length / 2);

    s.check('titles: power words rendered',
      w.document.querySelectorAll('#power .chip').length === 18);
    s.noErrors(errors);
  }

  /* ---------- Summarizer ---------- */
  {
    const { window: w, errors } = await boot('tools/text-summarizer.html');

    const article =
      'Renewable energy adoption accelerated sharply over the past decade. ' +
      'Solar panel costs fell by roughly ninety percent between 2010 and 2020. ' +
      'This decline made solar competitive with fossil fuels in most markets worldwide. ' +
      'Wind power followed a similar trajectory, though the cost reductions were less dramatic. ' +
      'Grid operators initially resisted these changes because of concerns about intermittency. ' +
      'Battery storage has since addressed many of those intermittency concerns effectively. ' +
      'Several countries now generate more than half their electricity from renewable sources. ' +
      'The transition still faces meaningful obstacles in heavy industry and aviation. ' +
      'Policy support remains uneven across different regions and political systems. ' +
      'Nevertheless the direction of travel is now widely considered irreversible by analysts.';

    set(w, 'input', article);
    set(w, 'length', '30');
    set(w, 'method', 'hybrid', 'change');
    set(w, 'order', true, 'change');
    await wait(550);

    const summary = text(w, 'output');
    s.check('summarizer: produced a summary', summary.length > 30);
    s.check('summarizer: summary is shorter than source', summary.length < article.length);
    s.match('summarizer: reduction reported', text(w, 'r-reduction'), /\d+%/);
    s.match('summarizer: kept count shown', text(w, 'r-kept'), /\d+ \/ \d+/);

    // Every sentence in the summary must appear verbatim in the source —
    // this is the guarantee extractive summarisation provides
    const summarySentences = summary.split(/(?<=[.!?])\s+/).filter((x) => x.trim().length > 10);
    s.check('summarizer: every sentence is verbatim from the source',
      summarySentences.every((sent) => article.includes(sent.trim())),
      summarySentences.find((sent) => !article.includes(sent.trim())) || '');

    s.check('summarizer: keywords extracted',
      w.document.querySelectorAll('#keywords .chip').length > 0);

    // Longer setting keeps more
    set(w, 'length', '60');
    await wait(550);
    s.check('summarizer: longer setting keeps more text',
      text(w, 'output').length > summary.length);

    // Order preservation
    set(w, 'length', '30');
    set(w, 'order', true, 'change');
    await wait(550);
    const ordered = text(w, 'output');
    const firstIndex = article.indexOf(ordered.split(/(?<=[.!?])\s+/)[0].trim());
    const lastPart = ordered.split(/(?<=[.!?])\s+/).slice(-1)[0].trim();
    s.check('summarizer: preserves original order',
      firstIndex <= article.indexOf(lastPart));

    // Abbreviation handling — periods must survive
    set(w, 'input', 'Dr. Smith led the study across twelve separate research institutions. ' +
      'Mrs. Jones coordinated the funding and the reporting throughout the whole period. ' +
      'The results were published in a major journal and widely discussed afterwards. ' +
      'Critics noted several methodological limitations in the sampling approach used. ' +
      'The authors responded with a detailed rebuttal addressing each point raised.');
    set(w, 'length', '60');
    await wait(550);
    const withAbbr = text(w, 'output');
    s.check('summarizer: abbreviation periods preserved',
      !withAbbr.includes('Dr ') && !withAbbr.includes('Mrs '),
      withAbbr.slice(0, 60));

    set(w, 'input', 'Too short to summarise.');
    await wait(550);
    s.match('summarizer: rejects short input', text(w, 'status'), /at least 60 words/i);
    s.noErrors(errors);
  }

  return s;
};
