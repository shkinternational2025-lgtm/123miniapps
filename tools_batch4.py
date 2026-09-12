#!/usr/bin/env python3
# ============================================
# 123MiniApps.online, Phase 1 Batch 4
# File: tools_batch4.py
# Purpose: 5 utilities that round out Phase 1:
#   YAML to JSON Converter, HTML to Markdown Converter,
#   PX to REM Converter, Calorie Calculator,
#   Image to PDF Converter.
# Every tool is fully self-contained, no external
# libraries or CDNs, so the site stays privacy-first
# and needs no server or CSP changes.
# ============================================

from toolkit import (
    tool, ws, info, row, text_input, number_input, select, switch,
    textarea, status_line, buttons, HR, html_block, slider, dropzone, readonly,
)

PAGES = []

# ---------------------------------------------------------------
# YAML to JSON Converter
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="yaml-to-json-converter", name="YAML to JSON Converter", icon="🔄", cat="developer",
    title="YAML to JSON Converter",
    description="Convert YAML to JSON and JSON back to YAML in your browser, with live output, clear error messages and one-click copy. Nothing you paste is uploaded.",
    tagline="Convert YAML to JSON and back, right in your browser.",
    workspace=ws(
        row(
            select("mode", "Direction", [("y2j", "YAML to JSON"), ("j2y", "JSON to YAML")], "y2j"),
            select("indent", "Indent", [("2", "2 spaces"), ("4", "4 spaces")], "2"),
        ),
        textarea("input", "Input", "Paste YAML here...", rows=150,
                 value="name: 123MiniApps\ntools:\n  - YAML to JSON\n  - JSON to YAML\nprivate: true\ncount: 116"),
        status_line("status", "Output updates as you type."),
        HR,
        textarea("output", "Output", "", rows=150),
        buttons(("copy", "Copy output", "primary"), ("swap", "Swap direction"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
        label="YAML to JSON converter",
    ),
    info_block=info(
        features=[
            "Convert YAML to JSON and JSON to YAML both ways",
            "Live output that updates as you type",
            "Handles nested maps, lists, quoted strings and inline flow",
            "Clear error messages when the input does not parse",
            "Runs entirely in your browser, nothing is uploaded",
        ],
        howto=[
            "Pick the direction, YAML to JSON or JSON to YAML.",
            "Paste or type your input in the top box.",
            "Read the converted result in the output box below.",
            "Copy the output, or hit swap to convert it back.",
        ],
        background_title="How YAML and JSON relate",
        background_paragraphs=[
            "YAML and JSON describe the same kinds of data: scalars like numbers, strings and booleans, lists of items, and maps of key and value pairs. JSON does it with braces, brackets and quotes, which is compact and unambiguous but noisy to read and write by hand. YAML does it with indentation and dashes, which is far easier for a human to scan, which is why it is so common in configuration files. Because both express the same underlying structure, converting between them is mostly a matter of changing the punctuation.",
            "This converter parses your YAML into an in-memory structure and then serialises that structure as JSON, or the reverse. It understands the parts of YAML you meet every day: nested mappings by indentation, sequences with dashes, quoted and plain scalars, booleans and nulls, numbers, and inline flow collections written with brackets and braces. It infers types the way YAML does, so true becomes a boolean and 116 becomes a number rather than a string, which is usually what you want.",
            "A few advanced YAML features, anchors and aliases, complex multi-document streams, and unusual tag directives, are deliberately out of scope for a quick browser tool, so if a conversion looks wrong the culprit is almost always one of those. For everyday config files, API payloads and data snippets the round trip is reliable, and because it all happens in your browser you can safely paste YAML that contains real hostnames, tokens or internal values without any of it leaving your device.",
        ],
    ),
    faqs=[
        ("Is this YAML to JSON converter free?", "Yes, with no limits, no account and no sign-up. Convert as much as you like in either direction."),
        ("Does it convert JSON back to YAML?", "Yes. Switch the direction to JSON to YAML, or use the swap button to send the output back through the other way."),
        ("Which YAML features are supported?", "Nested maps, sequences, quoted and plain scalars, booleans, nulls, numbers and inline flow collections. Anchors, aliases and multi-document streams are not supported in this quick tool."),
        ("Is my data uploaded?", "No. The parsing and conversion run entirely in your browser, so anything you paste, including tokens or internal values, never leaves your device."),
    ],
    script=r""" function scalarize(s) {
      s = s.trim();
      if (s === '' || s === '~' || s === 'null' || s === 'Null' || s === 'NULL') return null;
      if (s === 'true' || s === 'True' || s === 'TRUE') return true;
      if (s === 'false' || s === 'False' || s === 'FALSE') return false;
      if (s[0] === '"' && s[s.length - 1] === '"') { try { return JSON.parse(s); } catch (e) { return s.slice(1, -1); } }
      if (s[0] === "'" && s[s.length - 1] === "'") return s.slice(1, -1).replace(/''/g, "'");
      if (s[0] === '[' || s[0] === '{') return parseFlow(s);
      if (/^[-+]?\d+$/.test(s)) return parseInt(s, 10);
      if (/^[-+]?(\d+\.\d*|\.\d+|\d+([eE][-+]?\d+))$/.test(s) && /[.eE]/.test(s)) return parseFloat(s);
      return s;
    }
    function parseFlow(str) {
      let i = 0;
      const ws = () => { while (i < str.length && /\s/.test(str[i])) i++; };
      function quoted() { const q = str[i++]; let s = ''; while (i < str.length && str[i] !== q) { if (str[i] === '\\' && q === '"') { s += str[i] + str[i + 1]; i += 2; } else s += str[i++]; } i++; return q === '"' ? JSON.parse('"' + s + '"') : s.replace(/''/g, "'"); }
      function value() {
        ws();
        if (str[i] === '[') return seq();
        if (str[i] === '{') return map();
        if (str[i] === '"' || str[i] === "'") return quoted();
        let s = '';
        while (i < str.length && ',]}'.indexOf(str[i]) === -1) s += str[i++];
        return scalarize(s.trim());
      }
      function seq() { const a = []; i++; ws(); if (str[i] === ']') { i++; return a; } while (i < str.length) { a.push(value()); ws(); if (str[i] === ',') { i++; continue; } if (str[i] === ']') { i++; break; } break; } return a; }
      function map() {
        const o = {}; i++; ws(); if (str[i] === '}') { i++; return o; }
        while (i < str.length) {
          ws(); let k;
          if (str[i] === '"' || str[i] === "'") k = quoted();
          else { k = ''; while (i < str.length && ':,}'.indexOf(str[i]) === -1) k += str[i++]; k = k.trim(); }
          ws(); if (str[i] === ':') i++;
          o[k] = value(); ws();
          if (str[i] === ',') { i++; continue; } if (str[i] === '}') { i++; break; } break;
        }
        return o;
      }
      return value();
    }
    function stripInline(line) {
      let inS = false, inD = false;
      for (let i = 0; i < line.length; i++) {
        const c = line[i];
        if (c === "'" && !inD) inS = !inS;
        else if (c === '"' && !inS) inD = !inD;
        else if (c === '#' && !inS && !inD && (i === 0 || /\s/.test(line[i - 1]))) return line.slice(0, i);
      }
      return line;
    }
    function splitKV(s) {
      let inS = false, inD = false;
      for (let i = 0; i < s.length; i++) {
        const c = s[i];
        if (c === "'" && !inD) inS = !inS;
        else if (c === '"' && !inS) inD = !inD;
        else if (c === ':' && !inS && !inD && (i + 1 >= s.length || s[i + 1] === ' ' || s[i + 1] === '\t')) return { key: s.slice(0, i), value: s.slice(i + 1) };
      }
      return { key: s, value: '' };
    }
    function keyScalar(s) { s = s.trim(); if ((s[0] === '"' && s[s.length - 1] === '"')) { try { return JSON.parse(s); } catch (e) { return s.slice(1, -1); } } if (s[0] === "'" && s[s.length - 1] === "'") return s.slice(1, -1).replace(/''/g, "'"); return s; }
    function parseYaml(text) {
      const lines = [];
      text.replace(/\r\n?/g, '\n').split('\n').forEach((ln) => {
        if (/^\s*#/.test(ln)) return;
        const s = stripInline(ln).replace(/\s+$/, '');
        const t = s.trim();
        if (t === '' || t === '---' || t === '...') return;
        lines.push(s);
      });
      let idx = 0;
      const indentOf = (s) => s.match(/^ */)[0].length;
      function block(min) {
        if (idx >= lines.length) return null;
        if (indentOf(lines[idx]) < min) return null;
        return /^\s*-(\s|$)/.test(lines[idx]) ? seq(indentOf(lines[idx])) : map(indentOf(lines[idx]));
      }
      function seq(ind) {
        const arr = [];
        while (idx < lines.length) {
          const line = lines[idx], cur = indentOf(line);
          if (cur !== ind || !/^\s*-(\s|$)/.test(line)) break;
          const rest = line.slice(cur + 1).replace(/^\s*/, '');
          if (rest === '') { idx++; arr.push(block(ind + 1)); }
          else if (splitKV(rest).value !== '' || /:\s*$/.test(rest)) {
            const ci = line.indexOf(rest); lines[idx] = ' '.repeat(ci) + rest; arr.push(map(ci));
          } else { idx++; arr.push(scalarize(rest)); }
        }
        return arr;
      }
      function map(ind) {
        const obj = {};
        while (idx < lines.length) {
          const line = lines[idx], cur = indentOf(line);
          if (cur !== ind || /^\s*-(\s|$)/.test(line)) break;
          const kv = splitKV(line.slice(cur));
          const key = keyScalar(kv.key), val = kv.value.trim();
          if (val === '' || /^[|>][+-]?$/.test(val)) {
            idx++;
            if (/^[|>]/.test(val)) obj[key] = blockScalar(ind, val);
            else obj[key] = (idx < lines.length && indentOf(lines[idx]) > ind) ? block(ind + 1) : null;
          } else { idx++; obj[key] = scalarize(val); }
        }
        return obj;
      }
      function blockScalar(ind, marker) {
        const folded = marker[0] === '>';
        const collected = [];
        let baseIndent = null;
        while (idx < lines.length) {
          const line = lines[idx];
          if (line.trim() !== '' && indentOf(line) <= ind) break;
          if (baseIndent === null && line.trim() !== '') baseIndent = indentOf(line);
          collected.push(line.slice(baseIndent || 0)); idx++;
        }
        let text = collected.join('\n').replace(/\n+$/, '');
        if (folded) text = text.replace(/\n(?!\n)/g, ' ');
        return marker.indexOf('-') !== -1 ? text : text + '\n';
      }
      const result = block(0);
      return result === null ? {} : result;
    }
    function needsQuote(s) {
      if (s === '') return true;
      if (/^[\s]|[\s]$/.test(s)) return true;
      if (/[:#\[\]{}&*!|>'"%@`,]/.test(s)) return true;
      if (/^(true|false|null|~|yes|no|on|off)$/i.test(s)) return true;
      if (/^[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$/.test(s)) return true;
      if (/^[-?]/.test(s)) return true;
      return false;
    }
    function yamlScalar(v) {
      if (v === null) return 'null';
      if (typeof v === 'boolean') return String(v);
      if (typeof v === 'number') return String(v);
      const s = String(v);
      return needsQuote(s) ? JSON.stringify(s) : s;
    }
    function toYaml(v, pad) {
      const step = parseInt(T.$('indent').value, 10) || 2;
      const sp = ' '.repeat(pad);
      if (Array.isArray(v)) {
        if (v.length === 0) return sp + '[]';
        return v.map((item) => {
          if (item !== null && typeof item === 'object') {
            const body = toYaml(item, pad + step);
            return sp + '- ' + body.slice(pad + step);
          }
          return sp + '- ' + yamlScalar(item);
        }).join('\n');
      }
      if (v !== null && typeof v === 'object') {
        const keys = Object.keys(v);
        if (keys.length === 0) return sp + '{}';
        return keys.map((k) => {
          const val = v[k];
          const key = needsQuote(k) ? JSON.stringify(k) : k;
          if (val !== null && typeof val === 'object' && (Array.isArray(val) ? val.length : Object.keys(val).length)) {
            return sp + key + ':\n' + toYaml(val, pad + step);
          }
          if (val !== null && typeof val === 'object') {
            return sp + key + ': ' + (Array.isArray(val) ? '[]' : '{}');
          }
          return sp + key + ': ' + yamlScalar(val);
        }).join('\n');
      }
      return sp + yamlScalar(v);
    }
    function convert() {
      const src = T.$('input').value;
      const step = parseInt(T.$('indent').value, 10) || 2;
      if (src.trim() === '') { T.$('output').value = ''; T.status('status', 'Waiting for input.', 'muted'); return; }
      try {
        if (T.$('mode').value === 'y2j') {
          const data = parseYaml(src);
          T.$('output').value = JSON.stringify(data, null, step);
          T.status('status', 'Converted YAML to JSON.', 'ok');
        } else {
          const data = JSON.parse(src);
          const out = toYaml(data, 0);
          T.$('output').value = (data !== null && typeof data === 'object') ? out : out.trim();
          T.status('status', 'Converted JSON to YAML.', 'ok');
        }
      } catch (err) {
        T.$('output').value = '';
        T.status('status', 'Could not parse input: ' + err.message, 'error');
      }
    }
    function applyPlaceholder() {
      T.$('input').placeholder = T.$('mode').value === 'y2j' ? 'Paste YAML here...' : 'Paste JSON here...';
    }
    ['input'].forEach((id) => T.$(id).addEventListener('input', convert));
    T.$('mode').addEventListener('change', () => { applyPlaceholder(); convert(); });
    T.$('indent').addEventListener('change', convert);
    T.$('swap').addEventListener('click', () => {
      const out = T.$('output').value;
      if (out.trim()) { T.$('input').value = out; T.$('mode').value = T.$('mode').value === 'y2j' ? 'j2y' : 'y2j'; applyPlaceholder(); convert(); }
    });
    T.$('copy').addEventListener('click', () => copyToClipboard(T.$('output').value, 'Output copied'));
    T.$('clear').addEventListener('click', () => { T.$('input').value = ''; convert(); });
    T.$('share').addEventListener('click', () => shareLink({ title: 'YAML to JSON Converter | 123MiniApps' }));
    applyPlaceholder(); convert();
    if (window.Analytics) Analytics.trackToolUse('yaml-to-json-converter');""",
))

# ---------------------------------------------------------------
# HTML to Markdown Converter
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="html-to-markdown-converter", name="HTML to Markdown Converter", icon="📝", cat="developer",
    title="HTML to Markdown Converter",
    description="Convert HTML to clean Markdown, or Markdown back to HTML, in your browser. Handles headings, links, lists, tables and code, with instant one-click copy.",
    tagline="Turn HTML into clean Markdown, or Markdown into HTML.",
    workspace=ws(
        select("mode", "Direction", [("h2m", "HTML to Markdown"), ("m2h", "Markdown to HTML")], "h2m"),
        textarea("input", "Input", "Paste HTML here...", rows=150,
                 value="<h1>Hello</h1>\n<p>This is <strong>bold</strong> and <a href=\"https://123miniapps.online\">a link</a>.</p>\n<ul><li>One</li><li>Two</li></ul>"),
        status_line("status", "Output updates as you type."),
        HR,
        textarea("output", "Output", "", rows=150),
        buttons(("copy", "Copy output", "primary"), ("swap", "Swap direction"), ("clear", "Clear", "ghost"), ("share", "Share tool", "ghost")),
        label="HTML to Markdown converter",
    ),
    info_block=info(
        features=[
            "Convert HTML to Markdown and Markdown to HTML both ways",
            "Handles headings, bold, italic, links and images",
            "Converts lists, blockquotes, code blocks and simple tables",
            "Live output that updates as you type",
            "Runs entirely in your browser, nothing is uploaded",
        ],
        howto=[
            "Choose the direction you want to convert.",
            "Paste your HTML or Markdown into the top box.",
            "Read the converted result in the output box.",
            "Copy the output, or swap to convert it back.",
        ],
        background_title="Why convert between HTML and Markdown",
        background_paragraphs=[
            "Markdown and HTML both describe formatted text, but they are aimed at different readers. HTML is what browsers actually render, precise and verbose, with an opening and closing tag around everything. Markdown is a lightweight shorthand meant to be readable as plain text, where a hash means a heading and asterisks mean emphasis. Writers, note-takers and documentation systems love Markdown because it stays legible even before it is rendered, while the web ultimately needs HTML.",
            "Converting between the two comes up constantly. You might paste rich content from a web page and want clean Markdown for your notes or a README, or you might write in Markdown and need the HTML to drop into a template, an email or a content field that does not understand Markdown. This tool walks the structure of your input and rewrites it in the other syntax, mapping headings to headings, links to links, and lists to lists rather than doing a blind find and replace.",
            "A converter like this focuses on the common, well-behaved elements, headings, paragraphs, bold and italic, links and images, lists, blockquotes, code and simple tables, which covers the vast majority of real content. Deeply nested markup, inline styles and unusual custom tags do not always have a Markdown equivalent, so they are simplified or passed through. For everyday writing and documentation the result is clean and ready to use, and because it runs in your browser you can convert private drafts without uploading them anywhere.",
        ],
    ),
    faqs=[
        ("Is this HTML to Markdown converter free?", "Yes, with no limits, no account and no sign-up, in both directions."),
        ("Can it convert Markdown to HTML too?", "Yes. Switch the direction to Markdown to HTML, or use the swap button to send the output back through the other way."),
        ("What formatting does it support?", "Headings, bold and italic, links and images, ordered and unordered lists, blockquotes, inline code and code blocks, horizontal rules and simple tables."),
        ("Is my content uploaded?", "No. Both conversions run entirely in your browser, so private drafts never leave your device."),
    ],
    script=r""" /* ---------- HTML to Markdown ---------- */
    function esc(t) { return t.replace(/([\\`*_{}\[\]()#+\-.!>])/g, '\\$1'); }
    function inline(node) {
      let out = '';
      node.childNodes.forEach((c) => { out += render(c, true); });
      return out;
    }
    function render(node, inl) {
      if (node.nodeType === 3) return node.textContent.replace(/\s+/g, ' ');
      if (node.nodeType !== 1) return '';
      const tag = node.tagName.toLowerCase();
      const kids = () => inline(node);
      switch (tag) {
        case 'h1': case 'h2': case 'h3': case 'h4': case 'h5': case 'h6':
          return '\n\n' + '#'.repeat(+tag[1]) + ' ' + kids().trim() + '\n\n';
        case 'p': return '\n\n' + kids().trim() + '\n\n';
        case 'br': return '  \n';
        case 'hr': return '\n\n---\n\n';
        case 'strong': case 'b': return '**' + kids().trim() + '**';
        case 'em': case 'i': return '*' + kids().trim() + '*';
        case 'del': case 's': return '~~' + kids().trim() + '~~';
        case 'code':
          if (node.parentNode && node.parentNode.tagName && node.parentNode.tagName.toLowerCase() === 'pre') return node.textContent;
          return '`' + node.textContent + '`';
        case 'pre': {
          const code = node.textContent.replace(/\n$/, '');
          return '\n\n```\n' + code + '\n```\n\n';
        }
        case 'a': {
          const href = node.getAttribute('href') || '';
          return '[' + kids().trim() + '](' + href + ')';
        }
        case 'img': {
          const src = node.getAttribute('src') || '';
          const alt = node.getAttribute('alt') || '';
          return '![' + alt + '](' + src + ')';
        }
        case 'blockquote':
          return '\n\n' + kids().trim().split('\n').map((l) => '> ' + l).join('\n') + '\n\n';
        case 'ul': case 'ol': {
          let i = 1, out = '\n';
          node.childNodes.forEach((li) => {
            if (li.nodeType === 1 && li.tagName.toLowerCase() === 'li') {
              const marker = tag === 'ol' ? (i++ + '. ') : '- ';
              const body = inline(li).trim().replace(/\n/g, '\n  ');
              out += marker + body + '\n';
            }
          });
          return out + '\n';
        }
        case 'table': return '\n\n' + renderTable(node) + '\n\n';
        default: return kids();
      }
    }
    function renderTable(table) {
      const rows = Array.from(table.querySelectorAll('tr'));
      if (!rows.length) return '';
      const cells = (tr) => Array.from(tr.children).map((td) => inline(td).trim().replace(/\|/g, '\\|'));
      const head = cells(rows[0]);
      let out = '| ' + head.join(' | ') + ' |\n';
      out += '| ' + head.map(() => '---').join(' | ') + ' |\n';
      rows.slice(1).forEach((tr) => { out += '| ' + cells(tr).join(' | ') + ' |\n'; });
      return out.trim();
    }
    function htmlToMd(html) {
      const doc = new DOMParser().parseFromString(html, 'text/html');
      let out = '';
      doc.body.childNodes.forEach((c) => { out += render(c, false); });
      return out.replace(/\n{3,}/g, '\n\n').replace(/[ \t]+\n/g, '\n').trim();
    }
    /* ---------- Markdown to HTML ---------- */
    function mdInline(s) {
      s = s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      s = s.replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, '<img src="$2" alt="$1">');
      s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2">$1</a>');
      s = s.replace(/`([^`]+)`/g, (m, c) => '<code>' + c + '</code>');
      s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
      s = s.replace(/(^|[^*])\*([^*]+)\*/g, '$1<em>$2</em>');
      s = s.replace(/~~([^~]+)~~/g, '<del>$1</del>');
      return s;
    }
    function mdToHtml(md) {
      const lines = md.replace(/\r\n?/g, '\n').split('\n');
      const out = [];
      let i = 0, para = [], listType = null, listItems = [];
      const flushPara = () => { if (para.length) { out.push('<p>' + mdInline(para.join(' ')) + '</p>'); para = []; } };
      const flushList = () => { if (listType) { out.push('<' + listType + '>' + listItems.map((x) => '<li>' + mdInline(x) + '</li>').join('') + '</' + listType + '>'); listType = null; listItems = []; } };
      while (i < lines.length) {
        const line = lines[i];
        if (/^```/.test(line)) {
          flushPara(); flushList(); i++;
          const code = [];
          while (i < lines.length && !/^```/.test(lines[i])) { code.push(lines[i]); i++; }
          i++;
          out.push('<pre><code>' + code.join('\n').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</code></pre>');
          continue;
        }
        const h = line.match(/^(#{1,6})\s+(.*)$/);
        if (h) { flushPara(); flushList(); out.push('<h' + h[1].length + '>' + mdInline(h[2].trim()) + '</h' + h[1].length + '>'); i++; continue; }
        if (/^\s*([-*_])(\s*\1){2,}\s*$/.test(line)) { flushPara(); flushList(); out.push('<hr>'); i++; continue; }
        if (/^\s*>\s?/.test(line)) {
          flushPara(); flushList();
          const q = [];
          while (i < lines.length && /^\s*>\s?/.test(lines[i])) { q.push(lines[i].replace(/^\s*>\s?/, '')); i++; }
          out.push('<blockquote><p>' + mdInline(q.join(' ')) + '</p></blockquote>');
          continue;
        }
        const ul = line.match(/^\s*[-*+]\s+(.*)$/);
        const ol = line.match(/^\s*\d+\.\s+(.*)$/);
        if (ul || ol) {
          flushPara();
          const t = ul ? 'ul' : 'ol';
          if (listType && listType !== t) flushList();
          listType = t; listItems.push((ul ? ul[1] : ol[1]).trim()); i++; continue;
        }
        if (line.trim() === '') { flushPara(); flushList(); i++; continue; }
        para.push(line.trim()); i++;
      }
      flushPara(); flushList();
      return out.join('\n');
    }
    function convert() {
      const src = T.$('input').value;
      if (src.trim() === '') { T.$('output').value = ''; T.status('status', 'Waiting for input.', 'muted'); return; }
      try {
        if (T.$('mode').value === 'h2m') { T.$('output').value = htmlToMd(src); T.status('status', 'Converted HTML to Markdown.', 'ok'); }
        else { T.$('output').value = mdToHtml(src); T.status('status', 'Converted Markdown to HTML.', 'ok'); }
      } catch (err) { T.$('output').value = ''; T.status('status', 'Could not convert: ' + err.message, 'error'); }
    }
    function applyPlaceholder() { T.$('input').placeholder = T.$('mode').value === 'h2m' ? 'Paste HTML here...' : 'Paste Markdown here...'; }
    T.$('input').addEventListener('input', convert);
    T.$('mode').addEventListener('change', () => { applyPlaceholder(); convert(); });
    T.$('swap').addEventListener('click', () => { const out = T.$('output').value; if (out.trim()) { T.$('input').value = out; T.$('mode').value = T.$('mode').value === 'h2m' ? 'm2h' : 'h2m'; applyPlaceholder(); convert(); } });
    T.$('copy').addEventListener('click', () => copyToClipboard(T.$('output').value, 'Output copied'));
    T.$('clear').addEventListener('click', () => { T.$('input').value = ''; convert(); });
    T.$('share').addEventListener('click', () => shareLink({ title: 'HTML to Markdown Converter | 123MiniApps' }));
    applyPlaceholder(); convert();
    if (window.Analytics) Analytics.trackToolUse('html-to-markdown-converter');""",
))

# ---------------------------------------------------------------
# PX to REM Converter
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="px-to-rem-converter", name="PX to REM Converter", icon="📐", cat="design",
    title="PX to REM Converter",
    description="Convert px to rem and em, or rem and em back to px, using any root font size. Live two-way conversion plus a handy reference table, all in your browser.",
    tagline="Convert px to rem and em with any root font size.",
    workspace=ws(
        row(
            number_input("root", "Root font size (px)", value="16", step="1", min=1, max=100),
            number_input("pxval", "Pixels (px)", value="24", step="0.5"),
        ),
        row(
            readonly("remval", "rem"),
            readonly("emval", "em"),
        ),
        status_line("status", "Change any value and the others update instantly."),
        HR,
        html_block(""" <div class="field"><label class="field__label"><span>Convert from rem or em back to px</span></label></div>"""),
        row(
            number_input("reminput", "rem", value="1.5", step="0.1"),
            readonly("pxfromrem", "px"),
        ),
        HR,
        html_block(""" <div class="field"><label class="field__label"><span>Common conversions at your root size</span></label>
      <div class="output" id="table" style="overflow-x:auto"></div></div>"""),
        buttons(("copy", "Copy rem value", "primary"), ("share", "Share tool", "ghost")),
        label="PX to REM converter",
    ),
    info_block=info(
        features=[
            "Two-way conversion between px, rem and em",
            "Set any root font size, not just the default 16px",
            "Convert rem or em back to pixels",
            "A reference table of common pixel values",
            "Runs entirely in your browser, nothing is uploaded",
        ],
        howto=[
            "Set your root font size, usually 16px unless you have changed it.",
            "Type a pixel value to see it in rem and em.",
            "Or type a rem value to convert it back to pixels.",
            "Use the table for the values you reach for most often.",
        ],
        background_title="px, rem and em, and why the unit matters",
        background_paragraphs=[
            "A pixel is a fixed, absolute unit: 24px is always 24px regardless of anything else on the page. rem and em are relative units. One rem equals the root font size of the document, which is the font size set on the html element and defaults to 16px in every browser. One em equals the font size of the current element, so it depends on its context rather than the root. This is why 1.5rem is 24px when the root is 16px, but becomes 30px if a user or a stylesheet sets the root to 20px.",
            "Relative units matter most for accessibility. When someone increases their browser's default font size, everything sized in rem scales up with it, so your layout grows to remain readable. Anything hard-coded in pixels ignores that preference and stays put, which can leave text uncomfortably small for the people who most need it larger. Sizing typography and spacing in rem is the simplest way to respect the reader's own settings, which is why it is now the common recommendation.",
            "em is the right choice when you want a value to scale with its own element rather than the page root, for example padding inside a button that should grow with the button's text. The catch is that em compounds through nested elements, so an em inside an em inside an em can drift in ways that are hard to predict. A practical rule many designers follow is rem for global sizing where you want predictability, and em for local sizing that should track a specific element's font size.",
        ],
    ),
    faqs=[
        ("Is this px to rem converter free?", "Yes, with no limits, no account and no sign-up. Convert as many values as you like."),
        ("What root font size should I use?", "Browsers default to 16px, so use 16 unless you have deliberately changed the font size on your html element. The converter lets you set any root value."),
        ("What is the difference between rem and em?", "One rem is always the document root font size, while one em is the font size of the current element, so em depends on its context and can compound through nesting. rem is more predictable for global sizing."),
        ("Is anything uploaded?", "No. The conversion is pure arithmetic that runs entirely in your browser."),
    ],
    script=r""" function root() { return parseFloat(T.$('root').value) || 16; }
    function fmt(n) { return (Math.round(n * 100000) / 100000).toString(); }
    function fromPx() {
      const px = parseFloat(T.$('pxval').value);
      if (isNaN(px)) { T.$('remval').value = ''; T.$('emval').value = ''; return; }
      const r = px / root();
      T.$('remval').value = fmt(r) + 'rem';
      T.$('emval').value = fmt(r) + 'em';
      T.status('status', px + 'px is ' + fmt(r) + 'rem at a ' + root() + 'px root.', 'ok');
    }
    function fromRem() {
      const rem = parseFloat(T.$('reminput').value);
      if (isNaN(rem)) { T.$('pxfromrem').value = ''; return; }
      T.$('pxfromrem').value = fmt(rem * root()) + 'px';
    }
    function buildTable() {
      const vals = [8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 40, 48, 64];
      const r = root();
      let html = '<table class="data-table"><thead><tr><th>px</th><th>rem</th><th>em</th></tr></thead><tbody>';
      vals.forEach((v) => { html += '<tr><td>' + v + 'px</td><td>' + fmt(v / r) + 'rem</td><td>' + fmt(v / r) + 'em</td></tr>'; });
      html += '</tbody></table>';
      T.$('table').innerHTML = html;
      T.$('table').classList.remove('output--empty');
    }
    function all() { fromPx(); fromRem(); buildTable(); }
    ['root', 'pxval'].forEach((id) => T.$(id).addEventListener('input', all));
    T.$('reminput').addEventListener('input', fromRem);
    T.$('copy').addEventListener('click', () => copyToClipboard(T.$('remval').value, 'rem value copied'));
    T.$('share').addEventListener('click', () => shareLink({ title: 'PX to REM Converter | 123MiniApps' }));
    all();
    if (window.Analytics) Analytics.trackToolUse('px-to-rem-converter');""",
))

# ---------------------------------------------------------------
# Calorie Calculator
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="calorie-calculator", name="Calorie Calculator", icon="🍎", cat="calculator",
    title="Calorie Calculator",
    description="Estimate your daily calories from BMR and activity, with targets to lose, maintain or gain weight and a macro split. Metric or imperial, runs in your browser.",
    tagline="Estimate your daily calorie needs and targets.",
    workspace=ws(
        row(
            select("units", "Units", [("metric", "Metric (kg, cm)"), ("imperial", "Imperial (lb, ft/in)")], "metric"),
            select("sex", "Sex", [("male", "Male"), ("female", "Female")], "male"),
        ),
        row(
            number_input("age", "Age (years)", value="30", step="1", min=14, max=100),
            number_input("weight", "Weight (kg)", value="70", step="0.1", min=1),
        ),
        html_block(""" <div id="metric-height"></div>"""),
        row(
            number_input("heightcm", "Height (cm)", value="175", step="0.1", min=1),
            select("activity", "Activity level", [
                ("1.2", "Sedentary (little or no exercise)"),
                ("1.375", "Light (1 to 3 days a week)"),
                ("1.55", "Moderate (3 to 5 days a week)"),
                ("1.725", "Active (6 to 7 days a week)"),
                ("1.9", "Very active (hard exercise or physical job)"),
            ], "1.55"),
        ),
        html_block(""" <div id="imperial-height" style="display:none"><div class="workspace__row">
      <div class="field"><label class="field__label" for="heightft"><span>Height (ft)</span></label><input class="input" id="heightft" type="number" value="5" step="1" min="1" inputmode="decimal"></div>
      <div class="field"><label class="field__label" for="heightin"><span>Height (in)</span></label><input class="input" id="heightin" type="number" value="9" step="0.1" min="0" inputmode="decimal"></div>
      </div></div>"""),
        status_line("status", "Fill in your details to estimate your daily calories."),
        HR,
        html_block(""" <div class="result-grid">
      <div class="result"><span class="result__value" id="r-bmr" style="font-size:var(--text-2xl)">-</span><span class="result__label">BMR (at rest)</span></div>
      <div class="result result--primary"><span class="result__value" id="r-tdee" style="font-size:var(--text-2xl)">-</span><span class="result__label">Maintenance (TDEE)</span></div>
      <div class="result"><span class="result__value" id="r-target" style="font-size:var(--text-2xl)">-</span><span class="result__label">Your target</span></div>
    </div>"""),
        select("goal", "Goal", [
            ("-500", "Lose weight (about 0.5 kg / 1 lb a week)"),
            ("-250", "Lose slowly (about 0.25 kg a week)"),
            ("0", "Maintain weight"),
            ("250", "Gain slowly (about 0.25 kg a week)"),
            ("500", "Gain weight (about 0.5 kg / 1 lb a week)"),
        ], "0"),
        html_block(""" <div class="field"><label class="field__label"><span>Suggested daily macros at your target</span></label>
      <div class="output" id="macros" style="overflow-x:auto"></div></div>"""),
        buttons(("copy", "Copy results", "primary"), ("share", "Share tool", "ghost")),
        label="Calorie calculator",
    ),
    info_block=info(
        features=[
            "Estimates BMR with the Mifflin-St Jeor equation",
            "Applies your activity level for maintenance calories",
            "Targets for losing, maintaining or gaining weight",
            "A suggested protein, carb and fat split in grams",
            "Metric or imperial, runs entirely in your browser",
        ],
        howto=[
            "Choose your units and enter your age, sex, height and weight.",
            "Pick the activity level that matches a typical week.",
            "Read your BMR and maintenance calories.",
            "Choose a goal to see your daily target and macro split.",
        ],
        background_title="How calorie needs are estimated, and the caveats",
        background_paragraphs=[
            "Your body burns energy even at complete rest to keep your heart, brain and other organs running. That baseline is your basal metabolic rate, or BMR. This calculator estimates it with the Mifflin-St Jeor equation, which is one of the most accurate general formulas and uses your weight, height, age and sex. Your total daily energy expenditure, or TDEE, is then your BMR multiplied by an activity factor, because moving around, exercising and even digesting food all burn additional energy on top of the resting baseline.",
            "To change weight, you adjust intake relative to that maintenance number. Eating fewer calories than you burn creates a deficit and you tend to lose weight; eating more creates a surplus and you tend to gain. A commonly used guide is that a deficit or surplus of about 500 calories a day corresponds to roughly half a kilogram, or about a pound, a week, though the real figure varies from person to person. The macro split shown here is one balanced suggestion, splitting your target calories across protein, carbohydrate and fat, with protein and carbs at four calories a gram and fat at nine.",
            "Treat every number here as an estimate, not a prescription. Formulas like Mifflin-St Jeor describe an average person and cannot account for your individual metabolism, body composition, medical conditions or medications, and activity multipliers are broad brush by nature. Use the results as a sensible starting point, watch how your body actually responds over a few weeks, and adjust from there. If you have a health condition, are pregnant, or are planning a significant change to how you eat or train, talk to a doctor or a registered dietitian rather than relying on a calculator.",
        ],
    ),
    faqs=[
        ("Is this calorie calculator free?", "Yes, with no limits, no account and no sign-up. Everything runs in your browser."),
        ("Which formula does it use?", "It estimates your BMR with the Mifflin-St Jeor equation, then multiplies by an activity factor to get your maintenance calories, or TDEE."),
        ("Is this medical or dietary advice?", "No. The results are general estimates for information only, not medical or nutritional advice. If you have a health condition or are planning a major change, speak to a doctor or a registered dietitian."),
        ("Is my information uploaded?", "No. The calculation happens entirely in your browser, so the details you enter never leave your device."),
    ],
    script=r""" function toggleUnits() {
      const metric = T.$('units').value === 'metric';
      T.$('metric-height').style.display = metric ? '' : 'none';
      document.getElementById('imperial-height').style.display = metric ? 'none' : '';
      T.$('weight').previousElementSibling.querySelector('span').textContent = metric ? 'Weight (kg)' : 'Weight (lb)';
      calc();
    }
    function metrics() {
      const metric = T.$('units').value === 'metric';
      let kg, cm;
      if (metric) {
        kg = parseFloat(T.$('weight').value);
        cm = parseFloat(T.$('heightcm').value);
      } else {
        kg = parseFloat(T.$('weight').value) * 0.45359237;
        const ft = parseFloat(T.$('heightft').value) || 0;
        const inch = parseFloat(T.$('heightin').value) || 0;
        cm = (ft * 12 + inch) * 2.54;
      }
      return { kg, cm };
    }
    function calc() {
      const { kg, cm } = metrics();
      const age = parseFloat(T.$('age').value);
      if (isNaN(kg) || isNaN(cm) || isNaN(age) || kg <= 0 || cm <= 0 || age <= 0) {
        T.$('r-bmr').textContent = '-'; T.$('r-tdee').textContent = '-'; T.$('r-target').textContent = '-';
        T.$('macros').innerHTML = ''; T.$('macros').classList.add('output--empty');
        T.status('status', 'Enter your age, height and weight.', 'muted'); return;
      }
      const s = T.$('sex').value === 'male' ? 5 : -161;
      const bmr = 10 * kg + 6.25 * cm - 5 * age + s;
      const tdee = bmr * (parseFloat(T.$('activity').value) || 1.2);
      const target = tdee + (parseFloat(T.$('goal').value) || 0);
      T.$('r-bmr').textContent = Math.round(bmr).toLocaleString() + ' kcal';
      T.$('r-tdee').textContent = Math.round(tdee).toLocaleString() + ' kcal';
      T.$('r-target').textContent = Math.round(target).toLocaleString() + ' kcal';
      const p = Math.round(target * 0.30 / 4);
      const c = Math.round(target * 0.40 / 4);
      const f = Math.round(target * 0.30 / 9);
      T.$('macros').innerHTML = '<table class="data-table"><thead><tr><th>Macro</th><th>Share</th><th>Per day</th></tr></thead><tbody>'
        + '<tr><td>Protein</td><td>30%</td><td>' + p + ' g</td></tr>'
        + '<tr><td>Carbohydrate</td><td>40%</td><td>' + c + ' g</td></tr>'
        + '<tr><td>Fat</td><td>30%</td><td>' + f + ' g</td></tr>'
        + '</tbody></table>';
      T.$('macros').classList.remove('output--empty');
      T.status('status', 'Estimate ready. These are general figures, not medical advice.', 'ok');
    }
    function copyResults() {
      const txt = 'BMR: ' + T.$('r-bmr').textContent + '\nMaintenance (TDEE): ' + T.$('r-tdee').textContent + '\nTarget: ' + T.$('r-target').textContent;
      copyToClipboard(txt, 'Results copied');
    }
    T.$('units').addEventListener('change', toggleUnits);
    ['age', 'weight', 'heightcm', 'heightft', 'heightin'].forEach((id) => { const el = T.$(id); if (el) el.addEventListener('input', calc); });
    ['sex', 'activity', 'goal'].forEach((id) => T.$(id).addEventListener('change', calc));
    T.$('copy').addEventListener('click', copyResults);
    T.$('share').addEventListener('click', () => shareLink({ title: 'Calorie Calculator | 123MiniApps' }));
    toggleUnits(); calc();
    if (window.Analytics) Analytics.trackToolUse('calorie-calculator');""",
))

# ---------------------------------------------------------------
# Image to PDF Converter (self-contained PDF writer, no libraries)
# ---------------------------------------------------------------
PAGES.append(tool(
    slug="image-to-pdf-converter", name="Image to PDF Converter", icon="🖼️", cat="image",
    title="Image to PDF Converter",
    description="Combine JPG and PNG images into a single PDF in your browser. Reorder pages, choose A4, Letter or fit-to-image, and download. Nothing is ever uploaded.",
    tagline="Combine your images into one PDF, privately.",
    workspace=ws(
        dropzone("dropzone", "Drop images here, or click to add",
                 "JPG, PNG and WebP. Built into a PDF on your device, never uploaded."),
        html_block(""" <div class="field"><label class="field__label"><span>Pages</span><span class="field__hint" id="count-hint"></span></label>
      <div id="list"></div></div>"""),
        row(
            select("pagesize", "Page size", [("fit", "Fit to each image"), ("a4", "A4"), ("letter", "Letter")], "fit"),
            select("orient", "Orientation", [("portrait", "Portrait"), ("landscape", "Landscape")], "portrait"),
        ),
        row(
            slider("margin", "Margin", 0, 72, 24, step=4, unit="pt"),
            slider("quality", "JPEG quality", 50, 100, 85, step=5, unit="%"),
        ),
        status_line("status", "Add some images to get started."),
        buttons(("build", "Build PDF", "primary"), ("clear", "Clear all", "ghost"), ("share", "Share tool", "ghost")),
        label="Image to PDF converter",
    ),
    info_block=info(
        features=[
            "Combine many JPG, PNG or WebP images into one PDF",
            "Reorder and remove pages before building",
            "A4, Letter or a page that fits each image exactly",
            "Adjustable margin and JPEG quality",
            "Built entirely in your browser, nothing is uploaded",
        ],
        howto=[
            "Drop in the images you want, or click to browse.",
            "Reorder them into the page order you want, and remove any you do not.",
            "Choose the page size, orientation, margin and quality.",
            "Click Build PDF to download the finished file.",
        ],
        background_title="How images become a PDF, entirely on your device",
        background_paragraphs=[
            "A PDF is a container format that can hold text, vector graphics and images together with instructions for how to lay them out on each page. When you turn a set of photos into a PDF, each image becomes an embedded object placed on its own page. This tool does exactly that: it reads each image with your browser, re-encodes it as a JPEG, and assembles a valid PDF file byte by byte, with one page per image, then hands you the finished file to download.",
            "The key point is that all of this happens locally. Many online image-to-PDF services upload your files to a server, convert them there, and send the result back, which means your images, which are often scans of documents, receipts or personal photos, pass through someone else's computer. Here there is no server involved at all. The PDF is generated by JavaScript running in your own browser, so your images never leave your device, and you can confirm that by watching your browser's Network tab while you build a PDF.",
            "The options let you match the output to its purpose. Fit to each image makes every page exactly the size of its photo, which is ideal for a gallery or a set of screenshots. A4 or Letter with a margin produces tidy, printable document pages with the image centred, which suits scanned paperwork. Higher JPEG quality keeps more detail at the cost of a larger file, while a lower setting produces a smaller PDF that is easier to email. Because everything runs on your device, even a large batch of images stays completely private.",
        ],
    ),
    faqs=[
        ("Is this image to PDF converter free?", "Yes, with no limits, no account, no sign-up and no watermark on the output."),
        ("Are my images uploaded to a server?", "No. The PDF is built entirely by your browser on your own device, so your images are never uploaded. You can verify this in your browser's Network tab while you build a PDF."),
        ("Can I combine several images into one PDF?", "Yes. Add as many images as you like, reorder them into the page order you want, and they are combined into a single PDF, one image per page."),
        ("Which image formats work?", "Any format your browser can display, including JPG, PNG and WebP. Transparent areas in PNGs are flattened onto a white background in the PDF."),
    ],
    script=r""" const items = [];
    const PT = 72 / 96;
    const SIZES = { a4: [595.28, 841.89], letter: [612, 792] };
    function latin1(s) { const a = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) a[i] = s.charCodeAt(i) & 0xff; return a; }
    function b64ToBytes(b64) { const bin = atob(b64); const a = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) a[i] = bin.charCodeAt(i); return a; }
    function f(n) { return (Math.round(n * 100) / 100).toString(); }

    async function addFiles(fileList) {
      const files = Array.from(fileList).filter((f) => f.type.startsWith('image/'));
      if (!files.length) return;
      T.status('status', 'Reading images...', 'muted');
      for (const file of files) {
        try {
          const url = await T.readAsDataURL(file);
          const img = await T.loadImage(url);
          items.push({ name: file.name, url, w: img.naturalWidth, h: img.naturalHeight });
        } catch (e) { /* skip unreadable file */ }
      }
      render();
      T.status('status', items.length + ' image' + (items.length === 1 ? '' : 's') + ' ready. Build your PDF when you are set.', 'ok');
    }
    function render() {
      const list = T.$('list');
      T.$('count-hint').textContent = items.length ? items.length + ' page' + (items.length === 1 ? '' : 's') : '';
      if (!items.length) { list.innerHTML = '<p class="text-sm text-muted">No images added yet.</p>'; return; }
      list.innerHTML = '';
      items.forEach((it, i) => {
        const rowEl = document.createElement('div');
        rowEl.className = 'info-panel';
        rowEl.style.cssText = 'display:flex;align-items:center;gap:var(--space-3);margin-bottom:var(--space-2)';
        rowEl.innerHTML =
          '<img src="' + it.url + '" alt="" style="width:48px;height:48px;object-fit:cover;border-radius:var(--radius-sm);flex:none">' +
          '<span style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" class="text-sm">' + (i + 1) + '. ' + T.esc(it.name) + ' <span class="text-muted">(' + it.w + '×' + it.h + ')</span></span>';
        const mk = (label, aria, fn, disabled) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'btn btn--icon btn--sm'; b.textContent = label; b.setAttribute('aria-label', aria); if (disabled) b.disabled = true; b.addEventListener('click', fn); return b; };
        rowEl.appendChild(mk('↑', 'Move up', () => { [items[i - 1], items[i]] = [items[i], items[i - 1]]; render(); }, i === 0));
        rowEl.appendChild(mk('↓', 'Move down', () => { [items[i + 1], items[i]] = [items[i], items[i + 1]]; render(); }, i === items.length - 1));
        rowEl.appendChild(mk('✕', 'Remove', () => { items.splice(i, 1); render(); }));
        list.appendChild(rowEl);
      });
    }
    function jpegFor(it, quality) {
      const canvas = document.createElement('canvas');
      canvas.width = it.w; canvas.height = it.h;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, it.w, it.h);
      const img = new Image(); img.src = it.url;
      ctx.drawImage(img, 0, 0);
      const durl = canvas.toDataURL('image/jpeg', quality);
      return b64ToBytes(durl.split(',')[1]);
    }
    function layout(it) {
      const mode = T.$('pagesize').value;
      if (mode === 'fit') { const pw = it.w * PT, ph = it.h * PT; return { pw, ph, dx: 0, dy: 0, dw: pw, dh: ph }; }
      let [pw, ph] = SIZES[mode];
      if (T.$('orient').value === 'landscape') { const t = pw; pw = ph; ph = t; }
      const m = parseFloat(T.$('margin').value) || 0;
      const availW = pw - 2 * m, availH = ph - 2 * m;
      const scale = Math.min(availW / it.w, availH / it.h);
      const dw = it.w * scale, dh = it.h * scale;
      return { pw, ph, dx: (pw - dw) / 2, dy: (ph - dh) / 2, dw, dh };
    }
    function buildPdf() {
      const quality = (parseFloat(T.$('quality').value) || 85) / 100;
      const parts = []; let len = 0;
      const put = (d) => { const b = (typeof d === 'string') ? latin1(d) : d; parts.push(b); len += b.length; };
      const N = items.length;
      const totalObjs = 2 + N * 3;
      const off = new Array(totalObjs + 1).fill(0);
      put('%PDF-1.3\n%\xE2\xE3\xCF\xD3\n');
      off[1] = len; put('1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n');
      const kids = []; for (let i = 0; i < N; i++) kids.push((3 + i * 3) + ' 0 R');
      off[2] = len; put('2 0 obj\n<< /Type /Pages /Kids [' + kids.join(' ') + '] /Count ' + N + ' >>\nendobj\n');
      for (let i = 0; i < N; i++) {
        const it = items[i];
        const L = layout(it);
        const bytes = jpegFor(it, quality);
        const pageId = 3 + i * 3, contId = 4 + i * 3, imgId = 5 + i * 3;
        const content = 'q\n' + f(L.dw) + ' 0 0 ' + f(L.dh) + ' ' + f(L.dx) + ' ' + f(L.dy) + ' cm\n/Im0 Do\nQ\n';
        off[pageId] = len;
        put(pageId + ' 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ' + f(L.pw) + ' ' + f(L.ph) + '] /Resources << /XObject << /Im0 ' + imgId + ' 0 R >> >> /Contents ' + contId + ' 0 R >>\nendobj\n');
        off[contId] = len;
        put(contId + ' 0 obj\n<< /Length ' + content.length + ' >>\nstream\n' + content + 'endstream\nendobj\n');
        off[imgId] = len;
        put(imgId + ' 0 obj\n<< /Type /XObject /Subtype /Image /Width ' + it.w + ' /Height ' + it.h + ' /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ' + bytes.length + ' >>\nstream\n');
        put(bytes);
        put('\nendstream\nendobj\n');
      }
      const xrefStart = len;
      let xref = 'xref\n0 ' + (totalObjs + 1) + '\n0000000000 65535 f \n';
      for (let n = 1; n <= totalObjs; n++) xref += String(off[n]).padStart(10, '0') + ' 00000 n \n';
      put(xref);
      put('trailer\n<< /Size ' + (totalObjs + 1) + ' /Root 1 0 R >>\nstartxref\n' + xrefStart + '\n%%EOF');
      const out = new Uint8Array(len); let o = 0; for (const p of parts) { out.set(p, o); o += p.length; }
      return out;
    }
    // wire dropzone (multi-file)
    const zone = T.$('dropzone');
    function pick() { const inp = document.createElement('input'); inp.type = 'file'; inp.accept = 'image/*'; inp.multiple = true; inp.addEventListener('change', () => addFiles(inp.files), { once: true }); inp.click(); }
    zone.addEventListener('click', pick);
    zone.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(); } });
    ['dragenter', 'dragover'].forEach((ev) => zone.addEventListener(ev, (e) => { e.preventDefault(); zone.classList.add('is-dragover'); }));
    ['dragleave', 'drop'].forEach((ev) => zone.addEventListener(ev, (e) => { e.preventDefault(); zone.classList.remove('is-dragover'); }));
    zone.addEventListener('drop', (e) => { if (e.dataTransfer && e.dataTransfer.files) addFiles(e.dataTransfer.files); });
    T.$('build').addEventListener('click', () => {
      if (!items.length) { T.status('status', 'Add at least one image first.', 'warn'); return; }
      T.status('status', 'Building PDF...', 'muted');
      try {
        const bytes = buildPdf();
        downloadFile(new Blob([bytes], { type: 'application/pdf' }), 'images.pdf', 'application/pdf');
        T.status('status', 'PDF built from ' + items.length + ' image' + (items.length === 1 ? '' : 's') + '.', 'ok');
      } catch (err) { T.status('status', 'Could not build the PDF: ' + err.message, 'error'); }
    });
    T.$('clear').addEventListener('click', () => { items.length = 0; render(); T.status('status', 'Cleared. Add some images to start again.', 'muted'); });
    T.$('share').addEventListener('click', () => shareLink({ title: 'Image to PDF Converter | 123MiniApps' }));
    render();
    if (window.Analytics) Analytics.trackToolUse('image-to-pdf-converter');""",
))
