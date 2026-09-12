#!/usr/bin/env python3
# ============================================
# 123MiniApps.online, Phase 1 Batch 3
# File: tools_batch3.py
# Purpose: 5 text-style utilities, each with a distinct
#   primary job so they do not overlap with Fancy Text:
#   Bold Text Generator, Strikethrough Text Generator,
#   Small (Tiny) Text Generator, Bionic Reading Converter,
#   Word Repeater / Combiner.
# ============================================

from toolkit import (
    tool, ws, info, row, text_input, number_input, select, switch,
    textarea, status_line, buttons, HR, html_block, slider,
)

PAGES = []

# ---------------------------------------------------------------
# Bold Text Generator
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="bold-text-generator", name="Bold Text Generator", icon="🅱️", cat="text",
    title="Bold Text Generator",
    description="Turn plain text into bold Unicode letters you can paste into LinkedIn, Instagram and any box with no bold button. Several bold styles, click to copy.",
    tagline="Make bold text you can paste anywhere, even where there is no bold button.",
    workspace=ws(
        textarea("input", "Your text", "Type something to make bold...", rows=90, value="Bold text"),
        status_line("status", "Every bold style updates as you type. Click one to copy it."),
        html_block(""" <div id="styles"></div>"""),
        buttons(("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
        label="Bold text generator",
    ),
    info_block=info(
        features=[
            "Several genuine bold styles from one box of text",
            "Bold serif, bold sans, bold italic, bold script and bold fraktur",
            "Works where there is no formatting toolbar, like LinkedIn and Instagram",
            "Click any style to copy it instantly",
            "Runs entirely in your browser, nothing is uploaded",
        ],
        howto=[
            "Type or paste your text in the box.",
            "Pick the bold style you like from the list.",
            "Click it to copy the bold version to your clipboard.",
            "Paste it into your post, bio or headline.",
        ],
        background_title="Why there is no bold button, and how this works",
        background_paragraphs=[
            "Most social boxes, a LinkedIn post, an Instagram bio, a chat message, accept only plain text, with no way to mark a word as bold. That is because bold is normally a formatting instruction stored alongside the text, and a plain box throws that instruction away on paste. So the trick this tool uses is not formatting at all: it swaps your ordinary letters for entirely different Unicode characters that were designed to look bold.",
            "Those characters live in the Mathematical Alphanumeric Symbols block, which contains complete bold alphabets as real, distinct characters. When you paste a bold-looking headline into LinkedIn, you are sending genuine bold characters, not a bold command, which is exactly why the effect survives in a box that has no bold button.",
            "Because these are real characters and not styling, use them for emphasis in short places like a headline or a single standout word, and keep them out of long body text. Screen readers announce them by their Unicode names and search engines treat them as different characters, so a whole paragraph of bold Unicode is hard to read aloud and effectively invisible to search.",
        ],
    ),
    faqs=[
        ("Is this bold text generator free?", "Yes, with no limits, no account and no sign-up. Generate and copy as much bold text as you like."),
        ("Will the bold text work on LinkedIn and Instagram?", "Yes. Because the styles are real Unicode characters rather than formatting, they paste into most posts, bios and captions where there is no bold button. A few platforms block certain ranges, so if one style does not show, try another."),
        ("Why do some letters stay normal?", "Some bold Unicode ranges do not include every character, so any letter without a bold version falls back to plain. Bold serif and bold sans are the most complete."),
        ("Is my text sent anywhere?", "No. The conversion runs entirely in your browser, so nothing you type is uploaded."),
    ],
    script=r""" function mapRange(baseUpper, baseLower, baseDigit) {
      return (ch) => {
        const c = ch.codePointAt(0);
        if (c >= 65 && c <= 90 && baseUpper) return String.fromCodePoint(baseUpper + (c - 65));
        if (c >= 97 && c <= 122 && baseLower) return String.fromCodePoint(baseLower + (c - 97));
        if (c >= 48 && c <= 57 && baseDigit) return String.fromCodePoint(baseDigit + (c - 48));
        return ch;
      };
    }
    const STYLES = [
      ['Bold', mapRange(0x1D400, 0x1D41A, 0x1D7CE)],
      ['Bold Sans', mapRange(0x1D5D4, 0x1D5EE, 0x1D7EC)],
      ['Bold Italic', mapRange(0x1D468, 0x1D482, null)],
      ['Bold Sans Italic', mapRange(0x1D63C, 0x1D656, null)],
      ['Bold Script', mapRange(0x1D4D0, 0x1D4EA, null)],
      ['Bold Fraktur', mapRange(0x1D56C, 0x1D586, null)],
    ];
    function styleText(text, fn) { return Array.from(text).map(fn).join(''); }
    function render() {
      const text = T.$('input').value || '';
      const frag = document.createDocumentFragment();
      STYLES.forEach(([name, fn]) => {
        const out = styleText(text, fn);
        const card = document.createElement('button');
        card.type = 'button'; card.className = 'info-panel';
        card.style.cssText = 'display:block;width:100%;text-align:left;margin-bottom:var(--space-3);cursor:pointer';
        card.innerHTML = '<span class="text-sm text-muted">' + name + '</span><div style="font-size:var(--text-lg);word-break:break-word;margin-top:4px">' + (out || '&nbsp;') + '</div>';
        card.addEventListener('click', () => copyToClipboard(out, name + ' copied'));
        frag.appendChild(card);
      });
      T.$('styles').innerHTML = ''; T.$('styles').appendChild(frag);
    }
    T.$('input').addEventListener('input', render);
    T.$('clear').addEventListener('click', () => { T.$('input').value = ''; render(); });
    T.$('share').addEventListener('click', () => shareLink({ title: 'Bold Text Generator | 123MiniApps' }));
    render();
    if (window.Analytics) Analytics.trackToolUse('bold-text-generator');""",
))

# ---------------------------------------------------------------
# Strikethrough Text Generator
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="strikethrough-text-generator", name="Strikethrough Text Generator", icon="🚫", cat="text",
    title="Strikethrough Text Generator",
    description="Cross out text with real strikethrough characters that paste anywhere: long stroke, short stroke and slash-through styles. Everything runs in your browser.",
    tagline="Cross out text with strikethrough characters you can paste anywhere.",
    workspace=ws(
        textarea("input", "Your text", "Type something to cross out...", rows=90, value="Strikethrough"),
        status_line("status", "Each strikethrough style updates as you type. Click one to copy it."),
        html_block(""" <div id="styles"></div>"""),
        buttons(("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
        label="Strikethrough text generator",
    ),
    info_block=info(
        features=[
            "Real strikethrough that survives copy and paste",
            "Long stroke, short bar and slash-through styles",
            "Works in chat, bios, posts and documents",
            "Click a style to copy it instantly",
            "Runs entirely in your browser, nothing is uploaded",
        ],
        howto=[
            "Type or paste your text in the box.",
            "Choose the strikethrough style you want.",
            "Click it to copy the crossed-out text.",
            "Paste it into your message, list or post.",
        ],
        background_title="How strikethrough survives a plain text box",
        background_paragraphs=[
            "Crossing out text normally needs a formatting toolbar, which most chat boxes, bios and comment fields do not have. This tool gets the same look without any formatting by using combining characters: invisible marks in Unicode that attach to the character just before them and draw a line through it. Each letter carries its own strike, so the effect travels with the text wherever it is pasted.",
            "There are a few combining marks that produce slightly different results. A long stroke overlay draws a continuous line through the whole word, a short bar strikes each letter individually, and a solidus overlay puts a diagonal slash through the text. They are all real characters, so a plain box that would discard bold or italic formatting keeps the strikethrough intact.",
            "Strikethrough is perfect for showing an old price next to a new one, marking a completed item, or a bit of dry humour, and it works in places a formatting button never reaches. Because it relies on combining characters, a few older apps render it imperfectly, and screen readers do not announce the line, so keep it decorative rather than load-bearing for meaning.",
        ],
    ),
    faqs=[
        ("Is this strikethrough generator free?", "Yes, with no limits, no account and no sign-up."),
        ("Will strikethrough work in chat apps and social media?", "Yes in most of them, because the effect uses real combining characters rather than formatting. A few apps render certain marks imperfectly, so if one style looks off, try another."),
        ("What is the difference between the styles?", "The long stroke draws one continuous line through the text, the short bar strikes each letter, and the slash puts a diagonal line through it. Pick whichever reads best where you are pasting."),
        ("Is my text uploaded?", "No. The conversion runs entirely in your browser."),
    ],
    script=r""" function combine(mark) { return (ch) => (ch === ' ' || ch === '\n') ? ch : ch + mark; }
    const STYLES = [
      ['Strikethrough', combine('̶')],
      ['Short strike', combine('̵')],
      ['Slash through', combine('̸')],
      ['Short slash', combine('̷')],
    ];
    function styleText(text, fn) { return Array.from(text).map(fn).join(''); }
    function render() {
      const text = T.$('input').value || '';
      const frag = document.createDocumentFragment();
      STYLES.forEach(([name, fn]) => {
        const out = styleText(text, fn);
        const card = document.createElement('button');
        card.type = 'button'; card.className = 'info-panel';
        card.style.cssText = 'display:block;width:100%;text-align:left;margin-bottom:var(--space-3);cursor:pointer';
        card.innerHTML = '<span class="text-sm text-muted">' + name + '</span><div style="font-size:var(--text-lg);word-break:break-word;margin-top:4px">' + (out || '&nbsp;') + '</div>';
        card.addEventListener('click', () => copyToClipboard(out, name + ' copied'));
        frag.appendChild(card);
      });
      T.$('styles').innerHTML = ''; T.$('styles').appendChild(frag);
    }
    T.$('input').addEventListener('input', render);
    T.$('clear').addEventListener('click', () => { T.$('input').value = ''; render(); });
    T.$('share').addEventListener('click', () => shareLink({ title: 'Strikethrough Text Generator | 123MiniApps' }));
    render();
    if (window.Analytics) Analytics.trackToolUse('strikethrough-text-generator');""",
))

# ---------------------------------------------------------------
# Small (Tiny) Text Generator
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="small-text-generator", name="Small Text Generator", icon="🔡", cat="text",
    title="Small Text Generator",
    description="Turn text into tiny Unicode letters: superscript, small caps and subscript. Copy the small text into bios, usernames and posts, all in your browser.",
    tagline="Turn text into tiny superscript, small-caps and subscript letters.",
    workspace=ws(
        textarea("input", "Your text", "Type something to shrink...", rows=90, value="small text"),
        status_line("status", "Each small style updates as you type. Click one to copy it."),
        html_block(""" <div id="styles"></div>"""),
        buttons(("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
        label="Small text generator",
    ),
    info_block=info(
        features=[
            "Three tiny styles: superscript, small caps and subscript",
            "Real Unicode characters that paste into most boxes",
            "Great for bios, usernames and a subtle aesthetic",
            "Click a style to copy it instantly",
            "Runs entirely in your browser, nothing is uploaded",
        ],
        howto=[
            "Type or paste your text in the box.",
            "Pick superscript, small caps or subscript.",
            "Click the style to copy the tiny text.",
            "Paste it into your bio, username or post.",
        ],
        background_title="How tiny text works, and its limits",
        background_paragraphs=[
            "Small text is not a smaller font size, which a plain box could not keep anyway. It is a set of separate Unicode characters that happen to be drawn small: superscript letters like the ones used in footnotes, small capitals used in phonetics, and subscript characters used in chemistry. Swapping your ordinary letters for these makes text look shrunk while remaining plain, pasteable characters.",
            "Because these ranges were created for specific purposes rather than as a full alphabet, they are incomplete. Superscript is fairly complete for lowercase letters and digits, small caps covers the alphabet well, but subscript only exists for a handful of letters and all the digits. Any character without a small version falls back to normal, which is why some words come out partly shrunk.",
            "Tiny text is a nice decorative touch for a username, a bio line or a subtle label, but it is genuinely hard to read at length and is announced awkwardly by screen readers. Treat it as a visual flourish for short snippets rather than something to write real sentences in, and prefer the more complete superscript or small-caps styles when you want every letter to shrink.",
        ],
    ),
    faqs=[
        ("Is this small text generator free?", "Yes, with no limits, no account and no sign-up."),
        ("Will small text work in my bio or username?", "Usually yes, because the styles are real Unicode characters. A few platforms block certain ranges, so if one style does not appear, try another, and prefer superscript or small caps for the most complete coverage."),
        ("Why are some letters not shrunk?", "The subscript range in particular only covers a few letters, so any character without a small version stays normal. Superscript and small caps are much more complete."),
        ("Is my text uploaded?", "No. The conversion runs entirely in your browser."),
    ],
    script=r""" const SUP = { a:'ᵃ',b:'ᵇ',c:'ᶜ',d:'ᵈ',e:'ᵉ',f:'ᶠ',g:'ᵍ',h:'ʰ',i:'ⁱ',j:'ʲ',k:'ᵏ',l:'ˡ',m:'ᵐ',n:'ⁿ',o:'ᵒ',p:'ᵖ',q:'q',r:'ʳ',s:'ˢ',t:'ᵗ',u:'ᵘ',v:'ᵛ',w:'ʷ',x:'ˣ',y:'ʸ',z:'ᶻ','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹' };
    const SUB = { a:'ₐ',e:'ₑ',h:'ₕ',i:'ᵢ',j:'ⱼ',k:'ₖ',l:'ₗ',m:'ₘ',n:'ₙ',o:'ₒ',p:'ₚ',r:'ᵣ',s:'ₛ',t:'ₜ',u:'ᵤ',v:'ᵥ',x:'ₓ','0':'₀','1':'₁','2':'₂','3':'₃','4':'₄','5':'₅','6':'₆','7':'₇','8':'₈','9':'₉' };
    const SMALL = { a:'ᴀ',b:'ʙ',c:'ᴄ',d:'ᴅ',e:'ᴇ',f:'ꜰ',g:'ɢ',h:'ʜ',i:'ɪ',j:'ᴊ',k:'ᴋ',l:'ʟ',m:'ᴍ',n:'ɴ',o:'ᴏ',p:'ᴘ',q:'q',r:'ʀ',s:'s',t:'ᴛ',u:'ᴜ',v:'ᴠ',w:'ᴡ',x:'x',y:'ʏ',z:'ᴢ' };
    function lookup(map) { return (ch) => { const l = ch.toLowerCase(); return map[l] !== undefined ? map[l] : ch; }; }
    const STYLES = [ ['Superscript', lookup(SUP)], ['Small caps', lookup(SMALL)], ['Subscript', lookup(SUB)] ];
    function styleText(text, fn) { return Array.from(text).map(fn).join(''); }
    function render() {
      const text = T.$('input').value || '';
      const frag = document.createDocumentFragment();
      STYLES.forEach(([name, fn]) => {
        const out = styleText(text, fn);
        const card = document.createElement('button');
        card.type = 'button'; card.className = 'info-panel';
        card.style.cssText = 'display:block;width:100%;text-align:left;margin-bottom:var(--space-3);cursor:pointer';
        card.innerHTML = '<span class="text-sm text-muted">' + name + '</span><div style="font-size:var(--text-lg);word-break:break-word;margin-top:4px">' + (out || '&nbsp;') + '</div>';
        card.addEventListener('click', () => copyToClipboard(out, name + ' copied'));
        frag.appendChild(card);
      });
      T.$('styles').innerHTML = ''; T.$('styles').appendChild(frag);
    }
    T.$('input').addEventListener('input', render);
    T.$('clear').addEventListener('click', () => { T.$('input').value = ''; render(); });
    T.$('share').addEventListener('click', () => shareLink({ title: 'Small Text Generator | 123MiniApps' }));
    render();
    if (window.Analytics) Analytics.trackToolUse('small-text-generator');""",
))

# ---------------------------------------------------------------
# Bionic Reading Converter
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="bionic-reading-converter", name="Bionic Reading Converter", icon="⚡", cat="text",
    title="Bionic Reading Converter",
    description="Convert text to a bionic-reading format that bolds the first part of each word to guide your eyes and help you read faster. Adjustable, runs in your browser.",
    tagline="Bold the start of each word to guide your eyes and read faster.",
    workspace=ws(
        textarea("input", "Your text", "Paste a paragraph to convert to bionic reading...", rows=120,
                 value="Reading is faster when your eyes have a fixed point to jump to. Bolding the first part of each word gives your brain just enough of a cue to fill in the rest."),
        slider("fixation", "Fixation (how much of each word to bold)", 20, 70, 45, step=5, unit="%"),
        status_line("status", "Adjust the fixation, then copy the bolded text to paste elsewhere."),
        HR,
        html_block(""" <div class="field"><label class="field__label"><span>Preview</span></label>
      <div id="preview" class="output" style="line-height:1.9;font-size:var(--text-lg)"></div></div>"""),
        buttons(("copy", "Copy bold text", "primary"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
        label="Bionic reading converter",
    ),
    info_block=info(
        features=[
            "Bolds the first part of every word as a reading guide",
            "Adjustable fixation, from a light cue to a strong one",
            "Live preview as you type or drag the slider",
            "Copies real bold Unicode so it pastes into other apps",
            "Runs entirely in your browser, nothing is uploaded",
        ],
        howto=[
            "Paste the text you want to read into the box.",
            "Drag the fixation slider to set how much of each word is bolded.",
            "Read the preview, or copy the bold version to paste elsewhere.",
            "Use a lighter fixation for easy text and a stronger one for dense text.",
        ],
        background_title="What bionic reading is, and what the evidence says",
        background_paragraphs=[
            "Bionic reading is a formatting idea that bolds the first few letters of each word and leaves the rest light. The claim is that these bold openings act as fixation points your eyes jump between, so your brain recognises each word from its first letters and fills in the remainder without reading every character. Many people find it makes long or dense text feel quicker and easier to move through.",
            "This tool builds the effect by bolding a share of each word that you control with the fixation slider, using real bold Unicode characters so the result can be copied into other apps rather than living only on this page. A lighter fixation bolds just the first letter or two for a subtle guide, while a stronger one bolds up to the first two thirds of each word for a more forceful lead.",
            "It is worth being honest about the evidence: controlled studies so far have not found a reliable increase in reading speed or comprehension across readers, and results vary a lot from person to person. Plenty of people still prefer it and read more comfortably with it, so treat it as a personal aid worth trying rather than a proven speed boost, and pick the fixation that feels best to you.",
        ],
    ),
    faqs=[
        ("Is this bionic reading converter free?", "Yes, with no limits, no account and no sign-up."),
        ("Can I paste the result into other apps?", "Yes. The tool bolds the word openings with real bold Unicode characters, so the bolded text copies and pastes into most apps, not just this page."),
        ("Does bionic reading actually make you read faster?", "It helps some people and not others. Controlled studies have not found a consistent speed or comprehension gain, but many readers find it more comfortable, so it is worth trying at a fixation that suits you."),
        ("Is my text uploaded?", "No. The conversion runs entirely in your browser, so your text never leaves your device."),
    ],
    script=r""" function boldChar(ch) {
      const c = ch.codePointAt(0);
      if (c >= 65 && c <= 90) return String.fromCodePoint(0x1D400 + (c - 65));
      if (c >= 97 && c <= 122) return String.fromCodePoint(0x1D41A + (c - 97));
      if (c >= 48 && c <= 57) return String.fromCodePoint(0x1D7CE + (c - 48));
      return ch;
    }
    function headLen(word) {
      const frac = (parseInt(T.$('fixation').value, 10) || 45) / 100;
      const letters = word.replace(/[^A-Za-z0-9]/g, '').length;
      return Math.max(1, Math.ceil(letters * frac));
    }
    function convert() {
      const text = T.$('input').value || '';
      let bold = '';
      const prev = document.createElement('div');
      const parts = text.split(/(\s+)/);
      parts.forEach((tok) => {
        if (/^\s+$/.test(tok) || tok === '') { bold += tok; prev.appendChild(document.createTextNode(tok)); return; }
        let need = headLen(tok), taken = 0, head = '', tail = '';
        for (const ch of tok) {
          if (taken < need && /[A-Za-z0-9]/.test(ch)) { head += ch; taken++; }
          else if (taken < need) { head += ch; }
          else { tail += ch; }
        }
        bold += Array.from(head).map(boldChar).join('') + tail;
        const b = document.createElement('b'); b.textContent = head;
        prev.appendChild(b); prev.appendChild(document.createTextNode(tail));
      });
      T.$('preview').innerHTML = prev.innerHTML || '<span class="text-muted">Nothing to convert yet.</span>';
      T.$('preview').dataset.bold = bold;
      T.status('status', 'Converted. Copy the bold text to paste it elsewhere.', 'ok');
    }
    T.$('input').addEventListener('input', convert);
    T.$('fixation').addEventListener('input', convert);
    T.$('copy').addEventListener('click', () => copyToClipboard(T.$('preview').dataset.bold || '', 'Bold text copied'));
    T.$('clear').addEventListener('click', () => { T.$('input').value = ''; convert(); });
    T.$('share').addEventListener('click', () => shareLink({ title: 'Bionic Reading Converter | 123MiniApps' }));
    convert();
    if (window.Analytics) Analytics.trackToolUse('bionic-reading-converter');""",
))

# ---------------------------------------------------------------
# Word Repeater / Combiner
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="word-repeater", name="Word Repeater", icon="🔁", cat="text",
    title="Word Repeater",
    description="Repeat a word or phrase any number of times with your chosen separator, optionally numbered, then copy the result. A fast text repeater in your browser.",
    tagline="Repeat a word or phrase as many times as you need, your way.",
    workspace=ws(
        textarea("input", "Text to repeat", "Type a word or phrase...", rows=70, value="hello"),
        row(
            number_input("times", "Repeat how many times", value="10", step="1", min=1, max=10000),
            select("sep", "Separator between copies", [("space", "Space"), ("newline", "New line"), ("comma", "Comma"), ("none", "Nothing"), ("custom", "Custom")], "newline"),
        ),
        row(
            text_input("customsep", "Custom separator", placeholder="e.g. , or | "),
            switch("number", "Number each copy (1, 2, 3...)"),
        ),
        status_line("status", "Set the count and separator, then copy the result."),
        HR,
        textarea("output", "Result", "", rows=120),
        buttons(("copy", "Copy result", "primary"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
        label="Word repeater",
    ),
    info_block=info(
        features=[
            "Repeat any word, phrase or line a set number of times",
            "Separate copies with a space, new line, comma or your own separator",
            "Optionally number each copy",
            "Live character and line count on the result",
            "Runs entirely in your browser, nothing is uploaded",
        ],
        howto=[
            "Type the word or phrase you want to repeat.",
            "Set how many times and pick a separator.",
            "Turn on numbering if you want each copy labelled.",
            "Copy the result and paste it wherever you need it.",
        ],
        background_title="When repeating text is actually useful",
        background_paragraphs=[
            "Repeating a piece of text by hand is tedious and error prone once you pass a handful of copies, and it is surprisingly common: filling a column of test data, building a quick numbered list, padding a document to a length, generating placeholder lines, or making a block of a repeated phrase for a template. A repeater does the counting for you and gets the separators exactly right every time.",
            "The separator is the part people most often get wrong by hand. A space keeps everything on one line, a new line stacks the copies vertically, a comma builds a simple list, and a custom separator lets you produce things like pipe-delimited or bracketed output. Choosing the right one turns a wall of repeated words into something you can paste straight into a spreadsheet, a config file or a message.",
            "Numbering each copy turns the repeater into a fast way to scaffold an ordered list: ten numbered blanks to fill in, a set of labelled placeholders, or a countdown of identical steps. Because everything happens in your browser, even a very large repeat is instant and private, and nothing you type is uploaded, which matters if the text you are repeating is a draft or something sensitive.",
        ],
    ),
    faqs=[
        ("Is this word repeater free?", "Yes, with no limits, no account and no sign-up."),
        ("How many times can I repeat text?", "Up to ten thousand copies at once, which is more than almost anyone needs. Very large counts still run instantly because everything happens in your browser."),
        ("Can I put each copy on its own line?", "Yes. Choose the new line separator to stack the copies vertically, or pick a comma, a space, nothing, or your own custom separator."),
        ("Is my text uploaded?", "No. The tool runs entirely in your browser, so nothing you type is sent anywhere."),
    ],
    script=r""" function sepValue() {
      switch (T.$('sep').value) {
        case 'space': return ' ';
        case 'newline': return '\n';
        case 'comma': return ', ';
        case 'none': return '';
        case 'custom': return T.$('customsep').value;
        default: return '\n';
      }
    }
    function build() {
      const text = T.$('input').value;
      let n = parseInt(T.$('times').value, 10) || 0;
      if (n < 1) { T.$('output').value = ''; T.status('status', 'Enter how many times to repeat.', 'muted'); return; }
      if (n > 10000) { n = 10000; T.$('times').value = 10000; }
      const sep = sepValue();
      const numbered = T.$('number').checked;
      const parts = [];
      for (let i = 1; i <= n; i++) parts.push(numbered ? (i + '. ' + text) : text);
      const out = parts.join(sep);
      T.$('output').value = out;
      T.status('status', n + ' copies, ' + out.length + ' characters.', 'ok');
    }
    ['input', 'times', 'customsep'].forEach((id) => T.$(id).addEventListener('input', build));
    T.$('sep').addEventListener('change', build);
    T.$('number').addEventListener('change', build);
    T.$('copy').addEventListener('click', () => copyToClipboard(T.$('output').value, 'Result copied'));
    T.$('clear').addEventListener('click', () => { T.$('input').value = ''; build(); });
    T.$('share').addEventListener('click', () => shareLink({ title: 'Word Repeater | 123MiniApps' }));
    build();
    if (window.Analytics) Analytics.trackToolUse('word-repeater');""",
))
