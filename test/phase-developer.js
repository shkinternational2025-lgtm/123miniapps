/* ============================================
   123MiniApps.online v2.0
   File: test/phase-developer.js
   Purpose: Behavioural tests for the 10 developer tools.
   ============================================ */

const { boot, Suite, set, click, text, val, wait } = require('./harness');

module.exports = async function run() {
  const s = new Suite('Developer tools');

  /* ---------- Regex Tester ---------- */
  {
    const { window: w, errors } = await boot('tools/regex-tester.html');

    set(w, 'pattern', '(\\w+)@(\\w+\\.\\w+)');
    set(w, 'flags', 'g');
    set(w, 'subject', 'Contact ada@example.com or alan@example.org today.');
    await wait(400);

    s.match('regex: finds 2 matches', text(w, 'status'), /2 match/);
    s.check('regex: highlights matches', w.document.querySelector('#highlight .hl') !== null);
    s.check('regex: capture group table renders', w.document.querySelector('#groups table') !== null);
    s.includes('regex: group 1 captured', w.document.getElementById('groups').textContent, 'ada');
    s.includes('regex: group 2 captured', w.document.getElementById('groups').textContent, 'example.com');

    // Replacement with backreferences
    set(w, 'replace', '$1 at $2');
    await wait(400);
    s.includes('regex: replacement uses groups', text(w, 'replaced'), 'ada at example.com');

    // Invalid pattern must be reported, not thrown
    set(w, 'pattern', '([unclosed');
    await wait(400);
    s.match('regex: invalid pattern reported', text(w, 'status'), /unterminated|invalid|incomplete/i);

    // Case-insensitive flag
    set(w, 'pattern', 'ADA');
    set(w, 'flags', 'gi');
    await wait(400);
    s.match('regex: case-insensitive matches', text(w, 'status'), /1 match/);

    set(w, 'flags', 'g');
    await wait(400);
    s.match('regex: case-sensitive finds none', text(w, 'status'), /no matches/i);

    // Zero-length match must not loop forever
    set(w, 'pattern', 'a*');
    set(w, 'flags', 'g');
    set(w, 'subject', 'bbb');
    await wait(500);
    s.check('regex: zero-length match terminates', text(w, 'status').length > 0);

    s.check('regex: pattern library renders',
      w.document.querySelectorAll('#library .chip').length === 12);
    s.check('regex: flag toggles render',
      w.document.querySelectorAll('#flag-toggles .chip').length === 6);
    s.noErrors(errors);
  }

  /* ---------- URL Encoder ---------- */
  {
    const { window: w, errors } = await boot('tools/url-encoder-decoder.html');

    set(w, 'mode', 'encode-component', 'change');
    set(w, 'input', 'hello world&foo=bar');
    await wait(350);
    s.eq('url: encodeURIComponent escapes & and =',
      text(w, 'output'), 'hello%20world%26foo%3Dbar');

    // encodeURI leaves structural characters alone
    set(w, 'mode', 'encode-uri', 'change');
    set(w, 'input', 'https://example.com/a b?q=1&r=2');
    await wait(350);
    s.eq('url: encodeURI preserves structure',
      text(w, 'output'), 'https://example.com/a%20b?q=1&r=2');

    set(w, 'mode', 'decode', 'change');
    set(w, 'input', 'hello%20world%26foo%3Dbar');
    await wait(350);
    s.eq('url: decodes', text(w, 'output'), 'hello world&foo=bar');

    // Form encoding uses + for space
    set(w, 'input', 'hello+world');
    await wait(350);
    s.eq('url: plus decodes to space', text(w, 'output'), 'hello world');

    // Malformed percent sequence
    set(w, 'input', '%ZZ');
    await wait(350);
    s.match('url: malformed percent reported', text(w, 'status'), /malformed percent/i);

    // URL breakdown
    set(w, 'mode', 'encode-component', 'change');
    set(w, 'input', 'https://user@example.com:8080/path/to/page?q=test&lang=en#section');
    await wait(350);
    const parts = w.document.getElementById('parts').textContent;
    s.includes('url: breakdown shows scheme', parts, 'https');
    s.includes('url: breakdown shows host', parts, 'example.com');
    s.includes('url: breakdown shows port', parts, '8080');
    s.includes('url: breakdown shows path', parts, '/path/to/page');
    s.includes('url: params table', w.document.getElementById('params').textContent, 'lang');
    s.noErrors(errors);
  }

  /* ---------- JWT Decoder ---------- */
  {
    const { window: w, errors } = await boot('tools/jwt-decoder.html');

    click(w, 'sample');
    await wait(350);

    s.includes('jwt: header decoded', text(w, 'header'), 'HS256');
    s.includes('jwt: payload decoded', text(w, 'payload'), 'Ada Lovelace');
    s.eq('jwt: algorithm shown', text(w, 'r-alg'), 'HS256');
    s.includes('jwt: claims table', w.document.getElementById('claims').textContent, 'Issuer');
    s.match('jwt: warns signature not verified', text(w, 'status'), /not been verified/i);

    // Wrong number of segments
    set(w, 'input', 'only.two');
    await wait(350);
    s.match('jwt: rejects 2-part token', text(w, 'status'), /three dot-separated parts/i);

    // Non-JSON payload
    set(w, 'input', 'aaa.bbb.ccc');
    await wait(350);
    s.match('jwt: rejects non-JSON', text(w, 'status'), /not valid Base64URL/i);

    // An expired token must be flagged
    const enc = (o) => Buffer.from(JSON.stringify(o)).toString('base64')
      .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
    const expired = `${enc({ alg: 'HS256', typ: 'JWT' })}.${enc({ sub: 'x', exp: 1000000000 })}.sig`;
    set(w, 'input', expired);
    await wait(350);
    s.eq('jwt: expired token flagged', text(w, 'r-status'), 'Expired');

    // alg: none must be called out prominently
    const none = `${enc({ alg: 'none', typ: 'JWT' })}.${enc({ sub: 'x' })}.`;
    set(w, 'input', none);
    await wait(350);
    s.match('jwt: alg none warning', text(w, 'status'), /alg is "none"/i);
    s.noErrors(errors);
  }

  /* ---------- HTML Formatter ---------- */
  {
    const { window: w, errors } = await boot('tools/html-formatter.html');

    set(w, 'input', '<div><p>Hello</p></div>');
    click(w, 'beautify');
    await wait(300);
    const pretty = text(w, 'output');
    s.includes('html: indents nested elements', pretty, '\n  <p>');
    s.check('html: produces multiple lines', pretty.split('\n').length >= 4);

    click(w, 'minify');
    await wait(300);
    s.check('html: minify removes newlines', !text(w, 'output').includes('\n'));

    // Void elements must not increase depth
    set(w, 'input', '<div><br><img src="x"><p>after</p></div>');
    click(w, 'beautify');
    await wait(300);
    const lines = text(w, 'output').split('\n');
    const pLine = lines.find((l) => l.includes('<p>'));
    s.eq('html: void elements do not nest', pLine.match(/^\s*/)[0].length, 2);

    // Comments are stripped on minify but banners survive
    set(w, 'input', '<!-- normal --><!--! keep --><p>x</p>');
    click(w, 'minify');
    await wait(300);
    s.check('html: strips normal comments', !text(w, 'output').includes('normal'));

    s.check('html: tag summary renders', w.document.querySelector('#tags table') !== null);
    s.noErrors(errors);
  }

  /* ---------- CSS Minifier ---------- */
  {
    const { window: w, errors } = await boot('tools/css-minifier.html');

    set(w, 'input', '/* comment */\n.a {\n  color: #ffffff;\n  padding: 0px;\n  margin: 0.5em;\n}');
    set(w, 'comments', true, 'change');
    set(w, 'zeros', true, 'change');
    set(w, 'lastsemi', true, 'change');
    click(w, 'minify');
    await wait(300);

    const min = text(w, 'output');
    s.check('css: comment removed', !min.includes('comment'));
    s.includes('css: hex shortened', min, '#fff');
    s.includes('css: zero unit dropped', min, 'padding:0');
    s.includes('css: leading zero dropped', min, 'margin:.5em');
    s.check('css: last semicolon removed', min.includes('.5em}'));
    s.check('css: whitespace collapsed', !min.includes('\n'));

    // url() contents must survive untouched
    set(w, 'input', '.b { background: url(a b/c.png); }');
    click(w, 'minify');
    await wait(300);
    s.includes('css: url() preserved verbatim', text(w, 'output'), 'url(a b/c.png)');

    // Strings must survive untouched
    set(w, 'input', '.c::after { content: "  spaced  "; }');
    click(w, 'minify');
    await wait(300);
    s.includes('css: string content preserved', text(w, 'output'), '"  spaced  "');

    click(w, 'beautify');
    await wait(300);
    s.check('css: beautify adds newlines', text(w, 'output').includes('\n'));
    s.noErrors(errors);
  }

  /* ---------- JavaScript Minifier ---------- */
  {
    const { window: w, errors } = await boot('tools/javascript-minifier.html');

    // The critical test: // inside a string must not be treated as a comment
    set(w, 'input', "const url = 'https://example.com'; // trailing comment\nconst x = 1;");
    click(w, 'minify');
    await wait(300);
    let out = text(w, 'output');
    s.includes('js: URL inside string survives', out, "'https://example.com'");
    s.check('js: trailing comment removed', !out.includes('trailing comment'));

    // Regex literal containing /* must not be read as a block comment
    set(w, 'input', 'const re = /a\\/*b/g;\nconst y = 2;');
    click(w, 'minify');
    await wait(300);
    out = text(w, 'output');
    s.includes('js: regex literal preserved', out, '/a\\/*b/g');
    s.includes('js: code after regex survives', out, 'const y=2');

    // Division must not be mistaken for a regex
    set(w, 'input', 'const z = a / b / c;');
    click(w, 'minify');
    await wait(300);
    s.includes('js: division handled', text(w, 'output'), 'a/b/c');

    // Template literal contents preserved exactly
    set(w, 'input', 'const t = `hello   ${name}   world`;');
    click(w, 'minify');
    await wait(300);
    s.includes('js: template literal spacing kept', text(w, 'output'), '`hello   ${name}   world`');

    // Identifier separation must be preserved
    set(w, 'input', 'const a = 1;\nlet b = 2;\nreturn a;');
    click(w, 'minify');
    await wait(300);
    s.includes('js: keyword separation kept', text(w, 'output'), 'const a=1');
    s.check('js: no keyword mangling', !text(w, 'output').includes('leta'));

    // Block comment removal
    set(w, 'input', '/* block */ const q = 1;');
    click(w, 'minify');
    await wait(300);
    s.check('js: block comment removed', !text(w, 'output').includes('block'));
    s.noErrors(errors);
  }

  /* ---------- SQL Formatter ---------- */
  {
    const { window: w, errors } = await boot('tools/sql-formatter.html');

    set(w, 'input', 'select id, name from users where active = 1 order by name');
    set(w, 'keywords', 'upper', 'change');
    click(w, 'format');
    await wait(300);

    const formatted = text(w, 'output');
    s.includes('sql: keywords uppercased', formatted, 'SELECT');
    s.includes('sql: FROM on its own line', formatted, '\nFROM');
    s.includes('sql: WHERE on its own line', formatted, '\nWHERE');
    s.includes('sql: ORDER BY handled as one keyword', formatted, 'ORDER BY');
    s.check('sql: identifiers not uppercased', formatted.includes('users'));

    set(w, 'keywords', 'lower', 'change');
    await wait(300);
    s.includes('sql: keywords lowercased', text(w, 'output'), 'select');

    click(w, 'compact');
    await wait(300);
    s.check('sql: compact is one line', !text(w, 'output').includes('\n'));

    // Missing WHERE on a DELETE should be flagged
    set(w, 'input', 'delete from users');
    click(w, 'format');
    await wait(300);
    s.includes('sql: warns about missing WHERE',
      w.document.getElementById('summary').textContent, 'No WHERE clause');

    set(w, 'input', 'select * from a join b on a.id = b.a_id join c on c.id = b.c_id');
    click(w, 'format');
    await wait(300);
    s.includes('sql: counts joins', w.document.getElementById('summary').textContent, 'Joins');
    s.noErrors(errors);
  }

  /* ---------- Markdown Preview ---------- */
  {
    const { window: w, errors } = await boot('tools/markdown-preview.html');

    set(w, 'input', '# Heading\n\nSome **bold** and *italic* text.');
    await wait(300);
    let html = text(w, 'html');
    s.includes('md: heading rendered', html, '<h1>Heading</h1>');
    s.includes('md: bold rendered', html, '<strong>bold</strong>');
    s.includes('md: italic rendered', html, '<em>italic</em>');

    set(w, 'input', '- one\n- two\n- three');
    await wait(300);
    html = text(w, 'html');
    s.includes('md: list rendered', html, '<ul>');
    s.eq('md: three list items', (html.match(/<li/g) || []).length, 3);

    set(w, 'input', '| A | B |\n| --- | --- |\n| 1 | 2 |');
    await wait(300);
    html = text(w, 'html');
    s.includes('md: table rendered', html, '<table>');
    s.includes('md: table header', html, '<th>A</th>');

    set(w, 'input', '```js\nconst x = 1;\n```');
    await wait(300);
    s.includes('md: fenced code rendered', text(w, 'html'), '<pre><code class="language-js">');

    set(w, 'input', '[link](https://example.com)');
    await wait(300);
    s.includes('md: link rendered', text(w, 'html'), 'href="https://example.com"');

    set(w, 'input', '- [x] done\n- [ ] todo');
    await wait(300);
    s.includes('md: task list rendered', text(w, 'html'), 'type="checkbox"');

    // The security assertion: raw HTML must be escaped, not executed
    set(w, 'input', '<script>alert(1)</script>\n\n<img src=x onerror=alert(1)>');
    await wait(300);
    html = text(w, 'html');
    s.check('md: script tag escaped', !html.includes('<script>'));
    s.includes('md: shows escaped markup', html, '&lt;script&gt;');
    s.check('md: no script element in preview',
      w.document.querySelector('#preview script') === null);
    s.noErrors(errors);
  }

  /* ---------- Cron Builder ---------- */
  {
    const { window: w, errors } = await boot('tools/cron-expression-builder.html');

    set(w, 'expression', '0 9 * * 1-5');
    await wait(350);
    s.match('cron: explains weekday schedule', text(w, 'explanation'), /09:00/);
    s.includes('cron: names the days', text(w, 'explanation'), 'Monday');
    s.check('cron: next runs table', w.document.querySelector('#runs table') !== null);
    s.eq('cron: five next runs', w.document.querySelectorAll('#runs tbody tr').length, 5);

    set(w, 'expression', '*/15 * * * *');
    await wait(350);
    s.match('cron: step explained', text(w, 'explanation'), /every 15 minutes/i);

    set(w, 'expression', '0 0 1 * *');
    await wait(350);
    s.includes('cron: day of month explained', text(w, 'explanation'), '1st');

    // Field count validation
    set(w, 'expression', '0 9 * *');
    await wait(350);
    s.match('cron: rejects 4 fields', text(w, 'status'), /five fields/i);

    // Out-of-range value
    set(w, 'expression', '99 9 * * *');
    await wait(350);
    s.match('cron: rejects minute 99', text(w, 'status'), /minute field/i);

    // The OR rule between day-of-month and day-of-week
    set(w, 'expression', '0 0 1 * 1');
    await wait(350);
    s.match('cron: explains the OR rule', text(w, 'explanation'), /OR/);

    s.check('cron: presets render', w.document.querySelectorAll('#presets .chip').length === 12);
    s.noErrors(errors);
  }

  /* ---------- HTTP Status Codes ---------- */
  {
    const { window: w, errors } = await boot('tools/http-status-codes.html');

    await wait(250);
    s.match('http: shows all codes initially', text(w, 'status'), /Showing \d+ of \d+/);

    set(w, 'search', '404');
    await wait(250);
    s.includes('http: finds 404', w.document.getElementById('results').textContent, 'Not Found');
    s.match('http: filters to few results', text(w, 'status'), /Showing [1-3] of/);

    set(w, 'search', 'teapot');
    await wait(250);
    s.includes('http: finds 418 by name', w.document.getElementById('results').textContent, '418');

    set(w, 'search', 'redirect');
    await wait(250);
    s.check('http: description search works',
      w.document.getElementById('results').textContent.includes('30'));

    set(w, 'search', 'zzzznothing');
    await wait(250);
    s.match('http: no matches state', text(w, 'status'), /no matches/i);

    set(w, 'search', '');
    await wait(250);
    // Class filter
    const chips = w.document.querySelectorAll('#classes .chip');
    s.eq('http: six class filters', chips.length, 6);
    chips[5].click();
    await wait(250);
    s.check('http: 5xx filter applied',
      !w.document.getElementById('results').textContent.includes('404'));
    s.includes('http: shows 500 under 5xx',
      w.document.getElementById('results').textContent, '500');
    s.noErrors(errors);
  }

  return s;
};
