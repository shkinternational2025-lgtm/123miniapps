# 123MiniApps — Launch Playbook

Two parts: (1) a step-by-step Google Search Console setup so Google finds and
indexes the site, and (2) ready-to-post launch copy for sharing the blog
articles, written to earn the external links that build domain authority.

Everything here happens **after** the files are uploaded and the domain is live.

---

## Part 1 — Google Search Console checklist

Do these once, in order. Budget ~30 minutes plus a few days of waiting for Google.

### A. Verify the site
1. Go to https://search.google.com/search-console and sign in.
2. Add a **Domain** property (not URL-prefix) — enter `123miniapps.online`.
   Domain covers `www`, non-`www`, `http` and `https` in one property.
3. Google gives you a **TXT record**. Add it in your domain registrar's DNS
   settings (the same place you set the nameservers). Save, then click Verify.
   DNS can take 15 min–24 hr to propagate; if it fails, wait and retry.

### B. Submit the sitemap
4. In Search Console → **Sitemaps** (left menu).
5. Enter `sitemap.xml` and Submit. Status should read "Success" within a day.
   Your sitemap already lists all 95 tools, the homepage, static pages, the
   blog index and all 8 articles (109 URLs total), and `robots.txt` already
   points to it — so this is the only submission you need.

### C. Confirm indexing
6. Use the **URL Inspection** bar (top). Paste your homepage URL → "Request
   indexing". Do the same for the blog index and 2–3 top articles.
7. Over the next 1–2 weeks, check **Pages** → "Indexed". New sites index
   slowly; don't panic if it's gradual. If a page shows "Discovered – not
   indexed", that's normal early on.

### D. Watch the right reports
8. **Performance** — after ~1 week you'll see impressions and the actual
   search queries bringing people in. This tells you which long-tail terms are
   landing, so you know what to write next.
9. **Enhancements / Rich results** — confirm the FAQ and HowTo structured data
   is picked up with no errors. You can also spot-check any page at
   https://search.google.com/test/rich-results before launch.

### E. One-time extras
10. Also add the site to **Bing Webmaster Tools**
    (https://www.bing.com/webmasters) — same sitemap, ~10 minutes, and it feeds
    Bing + DuckDuckGo + ChatGPT search.
11. Set up **Google Analytics 4** (or a privacy-friendly alternative like
    Plausible) only if you want traffic numbers — Search Console alone covers
    search performance.

---

## Part 2 — Launch posts (earning the external links)

The goal is not "promote my site." It's to **be genuinely useful in a place
where the article answers a question people are already asking.** That's what
earns links and upvotes instead of removals. Rules of thumb:

- Lead with the *answer or tool*, not the brand. Mention the site once.
- Post the specific article that fits the specific community — never the same
  post everywhere.
- The privacy angle (everything runs in the browser, nothing is uploaded) is
  your strongest differentiator against the ad-heavy incumbents. Use it.
- Space posts out over days. Reply to comments — engagement is what makes a
  post rank and stick.

### Reddit / forum posts

**r/webdev, r/programming — pair with "Why is my JSON invalid when it looks fine?"**
> Wrote up the JSON-validity mistakes that trip me up most — trailing commas,
> smart quotes pasted from Docs, unescaped newlines inside strings — and *why*
> each one is invalid rather than just "it's broken." There's a formatter
> attached that runs entirely client-side (nothing gets uploaded), which
> matters when you're pasting config you shouldn't be sending to a random
> server. Feedback on the explanations welcome. [link]

**r/sysadmin, r/devops — pair with "The cron day-of-week trap"**
> PSA that has bitten me more than once: in cron, `0` and `7` both mean Sunday,
> and if you set *both* day-of-month and day-of-week they're OR'd, not AND'd —
> so `0 0 13 * 5` runs on the 13th *and* every Friday, not "Friday the 13th."
> Wrote up the gotchas with examples. [link]

**r/DataHoarder, r/buildapc — pair with "Why a 1TB drive shows 931GB"**
> The "missing" space isn't missing and the drive isn't lying — it's the
> 1000-vs-1024 (GB vs GiB) unit mismatch. Short explainer with the actual math,
> plus a converter to check any capacity. [link]

**r/photography, r/web_design — pair with "WebP, JPEG or PNG"**
> Quick decision guide for which image format to actually use — WebP vs JPEG vs
> PNG — with the "when does each one win" cases rather than a spec table. [link]

**r/DnD, r/rpg — pair with "What does 4d6kh3 mean? Dice notation explained"**
> Explainer on dice notation (the `kh3` / `kl1` / `4d6kh3` stuff) for anyone who's
> seen it in a character-gen guide and wasn't sure. Roller included. [link]

**r/personalfinance, r/Frugal — pair with "Why stacked discounts never add up"**
> "20% off then an extra 10%" is not 30% off — it's 28%, because the second cut
> applies to the already-reduced price. Wrote up why, with the math. [link]

### Hacker News

Post the **most technical, least promotional** article — the cron trap or the
checksum one — as a "Show HN" only if you're comfortable with blunt feedback.
Format:
> **Title:** The cron day-of-week trap (0 and 7 both mean Sunday)
> **URL:** [article link, not the homepage]
> First comment (from you): one paragraph on why you wrote it and that the
> whole site is static/client-side with no tracking. HN rewards substance and
> punishes marketing — let the article carry it.

### Stack Overflow (slow burn, high authority)

Find existing questions like "why does my JSON say unexpected token" or "cron
runs on wrong day" and write a genuinely complete answer. *Then*, if the tool
directly helps, link it as a supporting resource at the end. A link inside a
top-voted SO answer is one of the highest-quality backlinks you can get — but
only if the answer stands on its own first.

### Dev communities

Share the relevant article (not the homepage) in dev-focused Discords/Slack
communities you're already part of, in the appropriate channel, phrased as
"wrote this up, might save someone a headache" — never a cold drop.

### What to do next (content compounding)

After ~2 weeks, open Search Console → Performance, sort by impressions, and
find queries where you're ranking on page 2. Those are the articles to expand
and the topics to write the *next* article about. Ten more long-tail articles
built from real query data will do more than any single launch push.

---

### The one-line truth about domain authority

You can't set it, buy it cheaply-and-safely, or code it. It rises as real sites
link to yours because your content was worth linking to. This playbook is the
mechanism: useful articles + posting them where the question is being asked +
answering comments. Everything on-page (schema, internal links, speed, the
privacy angle) is already done — it's what makes each earned link count for more.
