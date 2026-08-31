#!/usr/bin/env python3
# ============================================
# 123MiniApps.online v2.0
# File: toolkit.py
# Purpose: Markup builders so each tool definition
#          describes *what* its controls are, not
#          how the HTML is spelled.
#
# Every helper returns an HTML string. Compose them
# with ws() to build a workspace section.
# ============================================

from html import escape as _esc


def esc(s):
    return _esc(str(s), quote=True)


# ---------------------------------------------------------------
# Form controls
# ---------------------------------------------------------------

def textarea(id, label, placeholder="", hint_id=None, rows=None, value=""):
    """A labelled multi-line input."""
    hint = f'\n        <span class="field__hint" id="{hint_id}"></span>' if hint_id else ""
    style = f' style="min-height:{rows}px"' if rows else ""
    return f"""    <div class="field">
      <label class="field__label" for="{id}">
        <span>{esc(label)}</span>{hint}
      </label>
      <textarea class="textarea" id="{id}"{style} spellcheck="false" placeholder="{esc(placeholder)}">{esc(value)}</textarea>
    </div>"""


def text_input(id, label, placeholder="", value="", type="text", hint="", attrs=""):
    """A labelled single-line input."""
    hint_html = f'\n      <span class="field__hint">{esc(hint)}</span>' if hint else ""
    return f"""    <div class="field">
      <label class="field__label" for="{id}"><span>{esc(label)}</span></label>
      <input class="input" id="{id}" type="{type}" value="{esc(value)}" placeholder="{esc(placeholder)}" {attrs}>{hint_html}
    </div>"""


def number_input(id, label, value="", placeholder="", step="any", min=None, max=None, hint=""):
    attrs = f'step="{step}"'
    if min is not None:
        attrs += f' min="{min}"'
    if max is not None:
        attrs += f' max="{max}"'
    attrs += ' inputmode="decimal"'
    return text_input(id, label, placeholder, value, "number", hint, attrs)


def select(id, label, options, selected=None):
    """options: list of (value, label) tuples or plain strings."""
    opts = []
    for o in options:
        val, lab = (o, o) if isinstance(o, str) else o
        sel = ' selected' if (selected is not None and val == selected) else ""
        opts.append(f'        <option value="{esc(val)}"{sel}>{esc(lab)}</option>')
    body = "\n".join(opts)
    return f"""    <div class="field">
      <label class="field__label" for="{id}"><span>{esc(label)}</span></label>
      <select class="select" id="{id}">
{body}
      </select>
    </div>"""


def switch(id, label, checked=False):
    """A toggle. The input sits inside the label, so it is implicitly labelled."""
    chk = " checked" if checked else ""
    return f"""    <label class="switch">
      <input class="switch__input" type="checkbox" id="{id}"{chk}>
      <span class="switch__track"><span class="switch__thumb"></span></span>
      <span>{label}</span>
    </label>"""


def slider(id, label, min, max, value, step=1, value_id=None, unit=""):
    vid = value_id or f"{id}-value"
    return f"""    <div class="field">
      <label class="field__label" for="{id}">
        <span>{esc(label)}</span>
        <span class="field__hint"><strong id="{vid}">{value}</strong>{(' ' + esc(unit)) if unit else ''}</span>
      </label>
      <input class="range" id="{id}" type="range" min="{min}" max="{max}" value="{value}" step="{step}">
    </div>"""


def color_input(id, label, value="#00D4FF"):
    return f"""    <div class="field">
      <label class="field__label" for="{id}"><span>{esc(label)}</span></label>
      <input class="input" id="{id}" type="color" value="{value}" style="height:52px;padding:6px;cursor:pointer">
    </div>"""


def readonly(id, label, value=""):
    return f"""    <div class="field">
      <label class="field__label" for="{id}"><span>{esc(label)}</span></label>
      <input class="input font-mono" id="{id}" type="text" value="{esc(value)}" readonly>
    </div>"""


# ---------------------------------------------------------------
# Layout and output
# ---------------------------------------------------------------

def row(*fields):
    """Lay fields out in a responsive grid."""
    return '    <div class="workspace__row">\n' + "\n".join(fields) + "\n    </div>"


def output(id="output", label="Result", stats_id=None, placeholder="Result will appear here.", center=False):
    stats = f'\n        <span class="field__hint" id="{stats_id}"></span>' if stats_id else ""
    cls = "output output--empty" + (" output--center" if center else "")
    return f"""    <div class="field">
      <label class="field__label" for="{id}">
        <span>{esc(label)}</span>{stats}
      </label>
      <div class="{cls}" id="{id}">{esc(placeholder)}</div>
    </div>"""


def status_line(id="status", text="Ready."):
    return f'    <p id="{id}" class="field__hint" role="status" aria-live="polite">{esc(text)}</p>'


def buttons(*specs):
    """specs: (id, label, variant) tuples. variant defaults to secondary."""
    out = []
    for spec in specs:
        bid, label = spec[0], spec[1]
        variant = spec[2] if len(spec) > 2 else "secondary"
        out.append(f'      <button class="btn btn--{variant}" id="{bid}" type="button">{esc(label)}</button>')
    return '    <div class="actions">\n' + "\n".join(out) + "\n    </div>"


# Standard trio wired automatically by T.wireActions()
STD_ACTIONS = buttons(
    ("copy", "Copy result"),
    ("download", "Download"),
    ("share", "Share tool", "ghost"),
)

HR = '    <hr class="hr">'


def dropzone(id="dropzone", label="Drop an image here, or click to browse",
             hint="Processed on your device, never uploaded."):
    return f"""    <div class="dropzone" id="{id}" role="button" tabindex="0"
         aria-label="{esc(label)}">
      <span class="dropzone__icon" aria-hidden="true">📁</span>
      <span class="dropzone__label">{esc(label)}</span>
      <span class="dropzone__hint">{esc(hint)}</span>
    </div>"""


def canvas(id="canvas", label="Preview"):
    return f"""    <div class="field">
      <span class="field__label"><span>{esc(label)}</span><span class="field__hint" id="{id}-meta"></span></span>
      <div class="output output--center" style="padding:var(--space-6)">
        <canvas id="{id}" role="img" aria-label="{esc(label)}"></canvas>
      </div>
    </div>"""


def html_block(markup):
    """Escape hatch for tool-specific markup."""
    return markup


def ws(*parts, label=""):
    """Assemble a workspace <section> from its parts."""
    body = "\n\n".join(p for p in parts if p)
    return f"""    <section class="workspace" aria-label="{esc(label)}">
{body}
    </section>"""


# ---------------------------------------------------------------
# Info panels
# ---------------------------------------------------------------

class InfoBlock(str):
    """
    The rendered info-panel HTML, carrying its source data as
    attributes so tool() can emit HowTo and FAQPage schema that
    matches the visible content exactly.

    Google requires structured data to reflect what a user actually
    sees. Generating both from one source makes drift impossible.
    """
    features = ()
    howto = ()
    background_title = ""
    background_paragraphs = ()


def info(features, howto, background_title, background_paragraphs):
    """
    Build the three-panel info block beneath the workspace.
    background_paragraphs: list of strings, aim for 150+ words total,
    since this is what carries the page's search relevance.
    """
    feat = "\n".join(f"        <li>{f}</li>" for f in features)
    steps = "\n".join(f"        <li>{s}</li>" for s in howto)
    paras = "\n".join(
        f'      <p class="text-sm text-muted{" mt-3" if i else ""}">{p}</p>'
        for i, p in enumerate(background_paragraphs)
    )
    block = InfoBlock(f"""    <div class="info-grid">
      <section class="info-panel">
        <h2>Features</h2>
        <ul>
{feat}
        </ul>
      </section>

      <section class="info-panel">
        <h2>How to use it</h2>
        <ol>
{steps}
        </ol>
      </section>

      <section class="info-panel">
        <h2>{esc(background_title)}</h2>
{paras}
      </section>
    </div>""")

    block.features = tuple(features)
    block.howto = tuple(howto)
    block.background_title = background_title
    block.background_paragraphs = tuple(background_paragraphs)
    return block


# ---------------------------------------------------------------
# FAQ generation
#
# Google requires FAQPage structured data to reflect questions and
# answers that are VISIBLE on the page. So these are rendered as a
# real accordion, and the schema is built from the same source.
#
# Answers are derived from each tool's own attributes, its category,
# its actual features, its background copy, so no two tools produce
# the same FAQ. Pass `faqs=[...]` to tool() to override entirely.
# ---------------------------------------------------------------

# How each category handles data, used to answer the privacy question
# accurately rather than with one boilerplate sentence.
_DATA_HANDLING = {
    "image": (
        "Your image is decoded and processed by your own browser using the File and Canvas APIs. "
        "It is never uploaded, there is no server to receive it. You can verify this by opening "
        "your browser's developer tools, switching to the Network tab, and watching while you use "
        "the tool: you will see no request carrying your file."
    ),
    "security": (
        "Nothing you type is transmitted. All processing happens locally through the browser's "
        "built-in Web Crypto API, which is the same audited implementation your browser uses for "
        "HTTPS. Because there is no backend, there is no log, no database and no copy of your input "
        "anywhere but this tab. Close the tab and it is gone."
    ),
    "developer": (
        "Everything is processed in your browser. Code, tokens and payloads you paste in never "
        "leave your device, which matters when you are debugging something that contains real "
        "credentials or customer data. Check the Network tab if you want to confirm it."
    ),
    "productivity": (
        "Your data is stored in your browser's localStorage, which lives on your device and is "
        "readable only by this site in this browser. Nothing syncs and nothing is uploaded. The "
        "trade-off is that clearing your browser data will erase it, so export anything important."
    ),
}

_DEFAULT_HANDLING = (
    "Everything happens inside your browser. The text you enter is processed by JavaScript running "
    "on your own device and is never sent to a server, there is no backend to send it to. You can "
    "confirm this in your browser's Network tab while you use the tool."
)


def _default_faqs(name, cat, features, background_paragraphs, tagline):
    """
    Build four questions that are genuinely specific to this tool.

    Q1 and Q4 are universal concerns phrased for this tool.
    Q2 draws on the tool's real feature list.
    Q3 draws on the tool's own background copy, so it differs
    meaningfully from every other page on the site.
    """
    handling = _DATA_HANDLING.get(cat, _DEFAULT_HANDLING)

    # Q2: built from the tool's actual capabilities
    feature_list = ", ".join(f[0].lower() + f[1:] for f in features[:3])
    q2_answer = (
        f"{name} covers {feature_list}"
        + (", among other things. " if len(features) > 3 else ". ")
        + "Everything is available immediately with no account, no sign-up and no usage limit."
    )

    # Q3: the first background paragraph, which is unique per tool.
    # Strip any inline markup so the schema answer is clean text.
    import re as _re
    context = _re.sub(r"<[^>]+>", "", background_paragraphs[0]) if background_paragraphs else tagline
    context = _re.sub(r"\s+", " ", context).strip()
    if len(context) > 620:
        cut = context.rfind(". ", 0, 620)
        context = context[: cut + 1] if cut > 300 else context[:620].rsplit(" ", 1)[0] + "…"

    return [
        (
            f"Is {name} free to use?",
            f"Yes, completely. {name} is free with no usage limits, no account and no sign-up. "
            "There is no paid tier and no trial that expires. Tools marked Premium on this site "
            "carry that label to indicate a deeper feature set, not a price.",
        ),
        (
            f"What can {name} do?",
            q2_answer,
        ),
        (
            f"How does {name} work?",
            context,
        ),
        (
            f"Is my data private, and does {name} work offline?",
            handling
            + " Because nothing depends on a server, the tool also keeps working offline once the "
            "page has loaded, the site registers a service worker that caches it after your first visit.",
        ),
    ]


def faq_section(faqs):
    """Render the visible FAQ accordion that the schema mirrors."""
    items = []
    for i, (question, answer) in enumerate(faqs):
        items.append(f"""      <div class="accordion__item">
        <button class="accordion__trigger" type="button" aria-expanded="false" aria-controls="faq-panel-{i}" id="faq-trigger-{i}">
          <span>{esc(question)}</span>
          <span class="accordion__icon" aria-hidden="true">+</span>
        </button>
        <div class="accordion__panel" id="faq-panel-{i}" role="region" aria-labelledby="faq-trigger-{i}">
          <div class="accordion__panel-inner">
            <div class="accordion__content">{esc(answer)}</div>
          </div>
        </div>
      </div>""")

    body = "\n".join(items)
    return f"""    <section class="section" aria-labelledby="faq-heading">
      <h2 class="text-2xl mb-4" id="faq-heading">Frequently asked questions</h2>
      <div class="accordion" id="tool-faq">
{body}
      </div>
    </section>"""


# ---------------------------------------------------------------
# Tool record
# ---------------------------------------------------------------

CATEGORY_NAMES = {
    "text": ("Text Tools", "UtilitiesApplication"),
    "image": ("Image Tools", "MultimediaApplication"),
    "developer": ("Developer Tools", "DeveloperApplication"),
    "converter": ("Converters", "UtilitiesApplication"),
    "generator": ("Generators", "UtilitiesApplication"),
    "calculator": ("Calculators", "UtilitiesApplication"),
    "security": ("Security Tools", "SecurityApplication"),
    "design": ("Design Tools", "DesignApplication"),
    "content": ("Content Tools", "UtilitiesApplication"),
    "productivity": ("Productivity Tools", "BusinessApplication"),
    "fun": ("Fun Tools", "GameApplication"),
}


def tool(slug, name, icon, cat, title, description, tagline,
         workspace, info_block, script, extra_scripts="", faqs=None):
    """
    Assemble a page record for build-tool-page.py.

    `description` must be 100-175 characters, the Phase 13 audit
    fails the build otherwise.

    HowTo and FAQPage schema are generated here from the same data
    that renders the visible content, so the two can never drift
    apart. Google penalises structured data that describes content
    the user cannot see.
    """
    import json

    cat_name, schema_cat = CATEGORY_NAMES[cat]
    n = len(description)
    assert 100 <= n <= 175, f"{slug}: description is {n} chars, want 100-175"

    url = f"https://www.123miniapps.online/tools/{slug}.html"

    # ---- FAQ: visible section + matching schema ----
    if faqs is None:
        faqs = _default_faqs(
            name, cat,
            getattr(info_block, "features", ()),
            getattr(info_block, "background_paragraphs", ()),
            tagline,
        )

    faq_html = faq_section(faqs)

    faq_schema = {
        "@type": "FAQPage",
        "@id": url + "#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
            for question, answer in faqs
        ],
    }

    # ---- HowTo: built from the visible "How to use it" steps ----
    howto_steps = getattr(info_block, "howto", ())
    extra = [faq_schema]

    if howto_steps:
        extra.append({
            "@type": "HowTo",
            "@id": url + "#howto",
            "name": f"How to use {name}",
            "description": tagline,
            "totalTime": "PT1M",
            "tool": [{"@type": "HowToTool", "name": "A web browser"}],
            "step": [
                {
                    "@type": "HowToStep",
                    "position": i + 1,
                    "name": step.rstrip("."),
                    "text": step,
                    "url": f"{url}#step{i + 1}",
                }
                for i, step in enumerate(howto_steps)
            ],
        })

    # Rendered as additional entries in the page's @graph
    extra_schema = ",\n    " + ",\n    ".join(
        json.dumps(entry, ensure_ascii=False, indent=6)[1:-1].strip().join("{}")
        for entry in extra
    )

    return {
        "slug": slug,
        "tool_name": name,
        "icon": icon,
        "category_id": cat,
        "category_name": cat_name,
        "schema_category": schema_cat,
        "purpose": tagline,
        "title": title,
        "og_title": f"{name} | 123MiniApps",
        "description": description,
        "tagline": tagline,
        "workspace": workspace,
        "info": str(info_block) + "\n\n" + faq_html,
        "script": script,
        "extra_scripts": extra_scripts,
        "extra_schema": extra_schema,
    }
