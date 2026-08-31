/* ============================================
   123MiniApps.online v2.0
   File: test/phase-text.js
   Purpose: Behavioural tests for the 10 text tools.
   ============================================ */

const { boot, Suite, set, click, text, val, wait } = require('./harness');

module.exports = async function run() {
  const s = new Suite('Text tools');

  /* ---------- Word Counter ---------- */
  {
    const { window: w, errors } = await boot('tools/word-counter.html');
    set(w, 'input', 'The quick brown fox jumps over the lazy dog. It was well-known and fast!\n\nSecond paragraph here.');
    await wait(200);

    s.eq('word-counter: word count', text(w, 'r-words'), '17');
    s.eq('word-counter: sentence count', text(w, 'r-sentences'), '3');
    s.eq('word-counter: paragraph count', text(w, 'r-paragraphs'), '2');
    s.match('word-counter: reading time', text(w, 'r-read'), /^\d+:\d{2}$/);

    // "well-known" must count as one word, not two
    set(w, 'input', 'well-known');
    await wait(200);
    s.eq('word-counter: hyphenated = 1 word', text(w, 'r-words'), '1');

    // apostrophes stay inside the word
    set(w, 'input', "don't stop");
    await wait(200);
    s.eq('word-counter: apostrophe = 2 words', text(w, 'r-words'), '2');

    // accented text
    set(w, 'input', 'café naïve résumé');
    await wait(200);
    s.eq('word-counter: accented = 3 words', text(w, 'r-words'), '3');

    set(w, 'input', 'alpha beta alpha gamma alpha beta delta epsilon zeta');
    await wait(200);
    s.includes('word-counter: density table renders', w.document.getElementById('density').textContent, 'alpha');

    click(w, 'clear');
    s.eq('word-counter: clear resets', text(w, 'r-words'), '0');
    s.noErrors(errors);
  }

  /* ---------- Case Converter ---------- */
  {
    const { window: w, errors } = await boot('tools/case-converter.html');
    const conv = async (style, input) => {
      set(w, 'input', input);
      set(w, 'style', style, 'change');
      await wait(200);
      return text(w, 'output');
    };

    s.eq('case: UPPER', await conv('upper', 'hello world'), 'HELLO WORLD');
    s.eq('case: lower', await conv('lower', 'HELLO WORLD'), 'hello world');
    s.eq('case: Title', await conv('title', 'hello world'), 'Hello World');
    s.eq('case: Sentence', await conv('sentence', 'hello world. goodbye now'), 'Hello world. Goodbye now');
    s.eq('case: camelCase', await conv('camel', 'hello world again'), 'helloWorldAgain');
    s.eq('case: PascalCase', await conv('pascal', 'hello world'), 'HelloWorld');
    s.eq('case: snake_case', await conv('snake', 'hello world'), 'hello_world');
    s.eq('case: kebab-case', await conv('kebab', 'hello world'), 'hello-world');
    s.eq('case: CONSTANT_CASE', await conv('constant', 'hello world'), 'HELLO_WORLD');

    // Splitting an existing camelCase input is the hard case
    s.eq('case: camelCase → kebab', await conv('kebab', 'myVariableName'), 'my-variable-name');
    s.eq('case: snake_case → camel', await conv('camel', 'my_variable_name'), 'myVariableName');
    s.eq('case: CONSTANT → kebab', await conv('kebab', 'MY_CONST_VALUE'), 'my-const-value');

    set(w, 'input', 'abc');
    set(w, 'style', 'upper', 'change');
    await wait(200);
    click(w, 'swap');
    await wait(200);
    s.eq('case: swap feeds result back', val(w, 'input'), 'ABC');
    s.noErrors(errors);
  }

  /* ---------- Text Diff ---------- */
  {
    const { window: w, errors } = await boot('tools/text-diff-checker.html');

    set(w, 'left', 'the quick brown fox');
    set(w, 'right', 'the quick red fox');
    await wait(450);

    s.eq('diff: 1 addition', text(w, 'r-added'), '1');
    s.eq('diff: 1 deletion', text(w, 'r-removed'), '1');
    s.check('diff: marks addition', w.document.querySelector('.diff-add') !== null);
    s.check('diff: marks deletion', w.document.querySelector('.diff-del') !== null);

    set(w, 'left', 'identical text here');
    set(w, 'right', 'identical text here');
    await wait(450);
    s.eq('diff: identical → 0 added', text(w, 'r-added'), '0');
    s.eq('diff: identical → 100%', text(w, 'r-similarity'), '100%');
    s.match('diff: identical status', text(w, 'status'), /identical/i);

    // case insensitivity
    set(w, 'left', 'Hello World');
    set(w, 'right', 'hello world');
    set(w, 'ignore-case', true, 'change');
    await wait(450);
    s.eq('diff: ignore-case → 0 changes', text(w, 'r-removed'), '0');

    set(w, 'ignore-case', false, 'change');
    await wait(450);
    s.check('diff: case-sensitive finds changes', Number(text(w, 'r-removed')) > 0);

    // line mode
    set(w, 'mode', 'line', 'change');
    set(w, 'left', 'a\nb\nc');
    set(w, 'right', 'a\nX\nc');
    await wait(450);
    s.eq('diff: line mode 1 removed', text(w, 'r-removed'), '1');

    click(w, 'swap');
    await wait(450);
    s.eq('diff: swap exchanges sides', val(w, 'left'), 'a\nX\nc');
    s.noErrors(errors);
  }

  /* ---------- Lorem Ipsum ---------- */
  {
    const { window: w, errors } = await boot('tools/lorem-ipsum-generator.html');

    set(w, 'unit', 'paragraphs', 'change');
    set(w, 'count', '3');
    await wait(150);
    let out = text(w, 'output');
    s.eq('lorem: 3 paragraphs', out.split(/\n\n/).length, 3);
    s.match('lorem: starts with Lorem ipsum', out, /^Lorem ipsum dolor sit amet/);

    set(w, 'unit', 'words', 'change');
    set(w, 'count', '12');
    await wait(150);
    out = text(w, 'output');
    s.eq('lorem: 12 words', out.trim().split(/\s+/).length, 12);

    set(w, 'unit', 'sentences', 'change');
    set(w, 'count', '5');
    await wait(150);
    s.check('lorem: 5 sentences', (text(w, 'output').match(/\./g) || []).length >= 5);

    set(w, 'unit', 'paragraphs', 'change');
    set(w, 'count', '2');
    set(w, 'wrap-html', true, 'change');
    await wait(150);
    s.match('lorem: HTML wrapping', text(w, 'output'), /^<p>[\s\S]*<\/p>$/);

    set(w, 'wrap-html', false, 'change');
    set(w, 'flavour', 'modern', 'change');
    await wait(150);
    s.check('lorem: modern flavour differs', !text(w, 'output').includes('consectetur'));

    // two generations should not be identical
    const a = text(w, 'output');
    click(w, 'generate');
    await wait(100);
    s.check('lorem: regenerates differently', text(w, 'output') !== a);
    s.noErrors(errors);
  }

  /* ---------- Text Reverser ---------- */
  {
    const { window: w, errors } = await boot('tools/text-reverser.html');
    const rev = async (mode, input) => {
      set(w, 'input', input);
      set(w, 'mode', mode, 'change');
      await wait(200);
      return text(w, 'output');
    };

    s.eq('reverse: characters', await rev('chars', 'hello'), 'olleh');
    s.eq('reverse: words', await rev('words', 'one two three'), 'three two one');
    s.eq('reverse: lines', await rev('lines', 'a\nb\nc'), 'c\nb\na');
    s.eq('reverse: each word', await rev('words-inner', 'one two'), 'eno owt');

    // The emoji test — naive split('') would corrupt this
    const emoji = await rev('chars', 'ab🎉cd');
    s.eq('reverse: emoji survives', emoji, 'dc🎉ba');

    set(w, 'input', 'A man a plan a canal Panama');
    set(w, 'mode', 'chars', 'change');
    await wait(200);
    s.match('reverse: detects palindrome', text(w, 'palindrome'), /palindrome/i);

    set(w, 'input', 'not a palindrome at all');
    await wait(200);
    s.eq('reverse: no false palindrome', text(w, 'palindrome'), '');
    s.noErrors(errors);
  }

  /* ---------- Remove Duplicate Lines ---------- */
  {
    const { window: w, errors } = await boot('tools/remove-duplicate-lines.html');

    set(w, 'input', 'apple\nbanana\napple\ncherry\nbanana');
    await wait(350);
    s.eq('dedupe: keeps 3 unique', text(w, 'r-out'), '3');
    s.eq('dedupe: removed 2', text(w, 'r-removed'), '2');
    s.eq('dedupe: preserves order', text(w, 'output'), 'apple\nbanana\ncherry');

    // trailing whitespace should be caught by trim
    set(w, 'input', 'apple\napple  \n apple');
    await wait(350);
    s.eq('dedupe: trim catches whitespace variants', text(w, 'r-out'), '1');

    set(w, 'trim', false, 'change');
    await wait(350);
    s.check('dedupe: without trim they differ', Number(text(w, 'r-out')) > 1);
    set(w, 'trim', true, 'change');

    set(w, 'input', 'Apple\napple\nAPPLE');
    set(w, 'ignore-case', true, 'change');
    await wait(350);
    s.eq('dedupe: case-insensitive', text(w, 'r-out'), '1');
    set(w, 'ignore-case', false, 'change');
    await wait(350);
    s.eq('dedupe: case-sensitive keeps 3', text(w, 'r-out'), '3');

    // "unique only" drops every line that ever repeated
    set(w, 'input', 'a\nb\na\nc');
    set(w, 'keep', 'unique', 'change');
    await wait(350);
    s.eq('dedupe: unique-only keeps b and c', text(w, 'output'), 'b\nc');

    set(w, 'keep', 'first', 'change');
    set(w, 'sort', 'asc', 'change');
    set(w, 'input', 'cherry\napple\nbanana');
    await wait(350);
    s.eq('dedupe: sorts A-Z', text(w, 'output'), 'apple\nbanana\ncherry');
    s.noErrors(errors);
  }

  /* ---------- Find and Replace ---------- */
  {
    const { window: w, errors } = await boot('tools/find-and-replace.html');

    set(w, 'input', 'the cat sat on the mat');
    set(w, 'find', 'cat');
    set(w, 'replace', 'dog');
    await wait(350);
    s.match('replace: preview counts 1 match', text(w, 'status'), /1 match/);

    click(w, 'apply');
    await wait(350);
    s.eq('replace: applied', text(w, 'output'), 'the dog sat on the mat');

    click(w, 'undo');
    await wait(350);
    s.eq('replace: undo restores', val(w, 'input'), 'the cat sat on the mat');

    // literal mode must not treat . as a wildcard
    set(w, 'input', 'a.b axb');
    set(w, 'find', 'a.b');
    set(w, 'replace', 'Z');
    set(w, 'regex', false, 'change');
    await wait(350);
    click(w, 'apply');
    await wait(350);
    s.eq('replace: literal dot is literal', text(w, 'output'), 'Z axb');

    // regex mode with capture groups
    set(w, 'input', 'Smith, John');
    set(w, 'find', '(\\w+), (\\w+)');
    set(w, 'replace', '$2 $1');
    set(w, 'regex', true, 'change');
    await wait(350);
    click(w, 'apply');
    await wait(350);
    s.eq('replace: capture groups swap', text(w, 'output'), 'John Smith');

    // invalid regex is reported, not thrown
    set(w, 'find', '([unclosed');
    await wait(350);
    s.match('replace: invalid regex reported', text(w, 'status'), /invalid regular expression/i);

    // whole-word mode
    set(w, 'regex', false, 'change');
    set(w, 'input', 'cat catalogue cat');
    set(w, 'find', 'cat');
    set(w, 'replace', 'X');
    set(w, 'whole', true, 'change');
    await wait(350);
    click(w, 'apply');
    await wait(350);
    s.eq('replace: whole-word spares catalogue', text(w, 'output'), 'X catalogue X');
    s.noErrors(errors);
  }

  /* ---------- Text to Speech ---------- */
  {
    const { window: w, errors } = await boot('tools/text-to-speech.html');
    set(w, 'input', 'Hello there.');
    await wait(300);
    s.match('tts: counts words', text(w, 'input-stats'), /2 words/);
    click(w, 'speak');
    s.match('tts: reports speaking', text(w, 'status'), /speaking/i);
    click(w, 'stop');
    s.match('tts: reports stopped', text(w, 'status'), /stopped/i);

    set(w, 'input', '');
    click(w, 'speak');
    s.match('tts: empty input rejected', text(w, 'status'), /enter some text/i);
    s.noErrors(errors);
  }

  /* ---------- Character Counter ---------- */
  {
    const { window: w, errors } = await boot('tools/character-counter.html');

    set(w, 'input', 'a'.repeat(100));
    await wait(120);
    s.eq('chars: used', text(w, 'r-used'), '100');
    s.eq('chars: remaining on 280 limit', text(w, 'r-left'), '180');
    s.eq('chars: 100 GSM chars = 1 segment', text(w, 'r-sms'), '1');

    set(w, 'input', 'a'.repeat(300));
    await wait(120);
    s.eq('chars: over limit goes negative', text(w, 'r-left'), '-20');
    s.match('chars: over-limit warning', text(w, 'status'), /over the limit/i);
    s.eq('chars: 300 GSM chars = 2 segments', text(w, 'r-sms'), '2');

    // a single emoji forces UCS-2 and shrinks the segment size
    set(w, 'input', '🎉' + 'a'.repeat(69));
    await wait(120);
    s.match('chars: emoji switches to UCS-2', text(w, 'status'), /UCS-2/);
    s.check('chars: UCS-2 needs 2 segments at 71 units', Number(text(w, 'r-sms')) >= 2);

    set(w, 'platform', '60', 'change');
    await wait(120);
    s.eq('chars: preset changes limit', text(w, 'r-left'), String(60 - w.document.getElementById('input').value.length));

    set(w, 'input', 'a b c');
    set(w, 'count-spaces', false, 'change');
    await wait(120);
    s.eq('chars: excluding spaces', text(w, 'r-used'), '3');
    s.noErrors(errors);
  }

  /* ---------- Text Formatter ---------- */
  {
    const { window: w, errors } = await boot('tools/text-formatter.html');

    set(w, 'input', 'too    many     spaces');
    await wait(350);
    s.eq('format: collapses spaces', text(w, 'output'), 'too many spaces');

    set(w, 'input', 'line one   \n   line two');
    await wait(350);
    s.eq('format: trims lines', text(w, 'output'), 'line one\nline two');

    set(w, 'input', 'a\n\n\n\n\nb');
    await wait(350);
    s.eq('format: collapses blank lines', text(w, 'output'), 'a\n\nb');

    set(w, 'input', '<p>Hello <b>world</b></p>');
    set(w, 'strip-html', true, 'change');
    await wait(350);
    s.eq('format: strips HTML', text(w, 'output'), 'Hello world');
    set(w, 'strip-html', false, 'change');

    // invisible characters
    set(w, 'input', 'a​b c');
    await wait(350);
    s.eq('format: removes invisibles', text(w, 'output'), 'ab c');

    set(w, 'input', '“smart” ‘quotes’');
    set(w, 'straight-quotes', true, 'change');
    await wait(350);
    s.eq('format: straightens quotes', text(w, 'output'), '"smart" \'quotes\'');

    // the two quote options must be mutually exclusive
    set(w, 'smart-quotes', true, 'change');
    await wait(350);
    s.check('format: quote options exclusive', w.document.getElementById('straight-quotes').checked === false);

    set(w, 'smart-quotes', false, 'change');
    set(w, 'input', 'This is a sentence\nthat was hard wrapped\nby a PDF.\n\nNew paragraph.');
    set(w, 'unwrap', true, 'change');
    await wait(350);
    s.includes('format: unwraps hard-wrapped lines', text(w, 'output'), 'This is a sentence that was hard wrapped by a PDF.');
    s.includes('format: keeps paragraph break', text(w, 'output'), '\n\nNew paragraph.');

    set(w, 'unwrap', false, 'change');
    set(w, 'fix-dashes', true, 'change');
    set(w, 'input', 'a--b and c...d');
    await wait(350);
    s.eq('format: normalises dashes', text(w, 'output'), 'a–b and c…d');
    s.noErrors(errors);
  }

  return s;
};
