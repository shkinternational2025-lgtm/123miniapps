# 123MiniApps - My Ranking Checklist (SEO + GEO + AEO)

This is **your** to-do list. Claude already did the on-site technical work
(schema, sitemap, robots.txt, llms.txt, IndexNow, fast/mobile/clean pages).
These are the steps only you can do because they need your logins and your
real-world actions. Do them **in order**, tick each box, and don't rush -
one item at a time is fine.

Legend: ⏱️ = how long it takes · 🔁 = repeat regularly

---

## PHASE 0 - Deploy the latest changes (do this first)

Everything below assumes the newest code is live. Push and pull once.

- [ ] **0.1** On your PC, open the repo folder in a terminal and run these three, one at a time:
  ```
  git add -A
  git commit -m "SEO/GEO setup: robots, llms.txt, IndexNow, equal category cards"
  git push
  ```
- [ ] **0.2** On the VPS (your `mubasher` SSH session) run:
  ```
  cd /opt/123miniapps && git pull
  ```
- [ ] **0.3** In a browser, open each of these and confirm they load (not a 404):
  - https://www.123miniapps.online/robots.txt
  - https://www.123miniapps.online/sitemap.xml
  - https://www.123miniapps.online/llms.txt
  - https://www.123miniapps.online/76cd4323f3b048f7e5c46419eb98a9ea.txt

✅ When all four open, you're ready.

---

## PHASE 1 - Google Search Console (the single most important step) ⏱️ ~30 min

This is how Google discovers and indexes your pages, and how you see what
you rank for. Google does **not** use IndexNow, so this step is mandatory.

- [ ] **1.1** Go to https://search.google.com/search-console and sign in with your Google account.
- [ ] **1.2** Click **Add property** → choose the **Domain** option (left box) → type `123miniapps.online` (no https, no www) → click **Continue**.
- [ ] **1.3** Google shows a **TXT record** to add to your DNS. Copy it (it looks like `google-site-verification=xxxxxxxx`).
- [ ] **1.4** In a new tab, log in to **Hostinger** → go to the **DNS / Nameservers** area for `123miniapps.online` (Domains → Manage → DNS Zone).
- [ ] **1.5** Add a new record:
  - Type: **TXT**
  - Name / Host: **@**
  - Value / Content: paste the `google-site-verification=...` string
  - TTL: leave default
  - Save.
- [ ] **1.6** Wait 10–30 minutes (DNS needs to propagate), then back in Search Console click **Verify**. If it fails, wait longer and try again - it's normal.
- [ ] **1.7** Once verified, in the left menu click **Sitemaps** → in the "Add a new sitemap" box type `sitemap.xml` → **Submit**. It should say **Success** and later show ~200 discovered URLs.
- [ ] **1.8** In the top search bar (URL Inspection), paste your homepage `https://www.123miniapps.online/` → press Enter → click **Request Indexing**.
- [ ] **1.9** Repeat 1.8 for your 6 best tool pages, one at a time:
  - https://www.123miniapps.online/tools/password-generator.html
  - https://www.123miniapps.online/tools/json-formatter.html
  - https://www.123miniapps.online/tools/qr-code-generator.html
  - https://www.123miniapps.online/tools/base64-encoder-decoder.html
  - https://www.123miniapps.online/tools/color-picker.html
  - https://www.123miniapps.online/tools/image-compressor.html

✅ Done when the sitemap shows "Success" and you've requested indexing on the homepage + 6 tools.

> Note: indexing is not instant. Pages appear in Google over **days to a few weeks**. Be patient; don't resubmit the same URL repeatedly.

---

## PHASE 2 - Bing Webmaster Tools ⏱️ ~10 min

Bing powers Bing search, DuckDuckGo, and increasingly ChatGPT's web results -
so this also helps AEO. It's quick because you can import from Google.

- [ ] **2.1** Go to https://www.bing.com/webmasters and sign in.
- [ ] **2.2** Click **Import** and choose **Import from Google Search Console** (fastest - it copies your verified site and sitemap automatically). Approve the Google permission prompt.
- [ ] **2.3** If import doesn't work, click **Add site manually**, enter `https://www.123miniapps.online/`, verify by the DNS TXT method (same idea as Phase 1), then go to **Sitemaps** → submit `https://www.123miniapps.online/sitemap.xml`.

✅ Done when Bing shows your site and sitemap submitted.

---

## PHASE 3 - Fire IndexNow (instant Bing/Yandex crawl) ⏱️ ~2 min

Claude built this for you. Run it after every deploy that adds/changes pages.

- [ ] **3.1** On the VPS (or your PC, in the repo folder) run:
  ```
  python3 indexnow.py --all
  ```
- [ ] **3.2** You should see `HTTP 200` or `202` = accepted. (A `403` means the key file isn't live yet - re-check Phase 0.3, then retry.)

🔁 Re-run `python3 indexnow.py tools/your-new-page.html` whenever you add or update a page.

---

## PHASE 4 - Verify indexing & watch progress ⏱️ 5 min, then weekly 🔁

- [ ] **4.1** In Google, search `site:123miniapps.online` and note the number of results. Do this **weekly** - the number should climb toward ~200.
- [ ] **4.2** In Search Console, check the **Pages** report (Indexing → Pages) for anything under "Not indexed" and read the reason. Tell Claude if you see errors and he'll fix them.
- [ ] **4.3** After ~2 weeks, open Search Console → **Performance**. This shows the search queries you're appearing for. **Write down queries where you rank on page 2 (positions 11–20)** - those are your best content opportunities (see Phase 7).

---

## PHASE 5 - GEO / AEO: get cited by AI engines ⏱️ ~20 min setup, then ongoing 🔁

Modern ranking includes being the source AI assistants quote (ChatGPT,
Perplexity, Google AI Overviews). Freshness matters a lot: in 2026, the large
majority of AI citations come from pages updated within the last 6–12 months.

- [ ] **5.1** Confirm `llms.txt` is live (Phase 0.3). This file hands AI engines a clean map of your 96 tools + articles - it's already done.
- [ ] **5.2** Test your own visibility: open ChatGPT and Perplexity and ask natural questions your tools answer, e.g. *"free online tool to format JSON"*, *"browser password generator that doesn't send data to a server"*. Note whether 123MiniApps is mentioned. Re-check monthly.
- [ ] **5.3** For every important page, make sure the **first sentence directly answers the query** in plain language (your tool pages already do this - keep it up in new content).
- [ ] **5.4** Keep pages fresh: when you edit a tool or article, that "updated" signal helps AEO. Ask Claude to bump the article's `dateModified` when you refresh content.

> You don't need to install anything for GEO. It's mostly good SEO + clear
> answers + freshness + being referenced elsewhere (Phase 6).

---

## PHASE 6 - Backlinks & directory listings (the biggest off-site lever) ⏱️ ~2–3 hrs total, spread out 🔁

Backlinks and mentions are still the #1 authority signal, and they're also
how AI engines decide who's trustworthy enough to cite. Do a few per week.

- [ ] **6.1** Submit to free tool directories (create an account, add your site):
  - AlternativeTo (alternativeto.net)
  - Product Hunt (producthunt.com) - do a proper launch on a Tuesday–Thursday
  - SaaSHub, ToolFinder, and similar "free tools" listing sites
- [ ] **6.2** Post genuinely helpful answers on Reddit (r/webdev, r/productivity), Quora, and forums **where your tool actually solves the question** - link to the specific tool page, not the homepage. (Don't spam; add value or it backfires.)
- [ ] **6.3** Find "best free online tools" listicles (search `best free JSON formatter`, `best online password generator`) and email the authors suggesting your tool for inclusion.
- [ ] **6.4** Set up social profiles (X, a simple Facebook/LinkedIn page) and share individual tools. These create early signals and Pinterest pins (below).
- [ ] **6.5** Pinterest: create tall (1000×1500) pin images for your best tools/articles, each linking to that page. Pinterest sends steady long-tail traffic to utility sites.

🔁 Aim for **2–3 new backlinks or mentions per week**. This is slow, compounding work - the single biggest driver of long-term ranking.

---

## PHASE 7 - Content cadence (turns rankings into traffic) ⏱️ ongoing 🔁

Google and AI engines reward sites that keep publishing helpful, specific content.

- [ ] **7.1** From Phase 4.3, pick a "page 2" query. Ask Claude to write a focused article targeting it. One strong 1,500–3,000 word article beats five thin ones.
- [ ] **7.2** Publish on a steady rhythm you can sustain - e.g. **one article per week**. Consistency matters more than volume.
- [ ] **7.3** Every new article should: answer the question in the first 2 sentences, use clear question-style H2 headings, link to 2–3 related tools, and link to/from 2–3 related articles.
- [ ] **7.4** After publishing, run Phase 3 (IndexNow) and request indexing in Search Console (Phase 1.8) for the new URL.

---

## PHASE 8 - Your ongoing routine (pin this) 🔁

**Weekly (15 min):**
- [ ] Check `site:123miniapps.online` count in Google.
- [ ] Glance at Search Console → Performance for new queries + page-2 chances.
- [ ] Publish or commission 1 article; add 2–3 backlinks/mentions.
- [ ] Run `python3 indexnow.py --all` if you changed anything.

**Monthly (30 min):**
- [ ] Test AI visibility (Phase 5.2) in ChatGPT + Perplexity.
- [ ] Review Search Console Pages report for indexing errors.
- [ ] Refresh 1–2 older articles/tools (update a stat, add a section) for the freshness signal.

---

## What to hand back to Claude (he does these for you)

You never touch code. Just ask Claude to:
- Write or refresh articles (give him the topic/query).
- Add or remove a tool.
- Fix any Search Console indexing error you find.
- Bump `dateModified` on refreshed content.
- Regenerate `llms.txt` and the sitemap after changes (`build-llms.py`, `build-sitemap.py`).
- Add the Adsterra codes when they arrive.

---

### Quick reference - your accounts to create
1. Google Search Console - https://search.google.com/search-console
2. Bing Webmaster Tools - https://www.bing.com/webmasters
3. Pinterest (business) - https://pinterest.com
4. Product Hunt / AlternativeTo - for directory backlinks

**Order of impact (if you only do a few):** Phase 1 (Google) → Phase 6 (backlinks) → Phase 7 (content) → Phase 2/3 (Bing/IndexNow) → Phase 5 (AEO).

---

## Appendix A - Making your GitHub repo private (optional)

You can make the repo private anytime. Your live site is unaffected (it runs
from the copy already on your VPS, not from GitHub). A private repo only hides
your source code and build scripts, not the website itself.

**Important:** once the repo is private, the VPS can no longer `git pull`
anonymously. Give it read access ONCE with a read-only Deploy Key first.

1. On the **VPS**, create a key (no passphrase, so pulls stay automatic):
   ```
   ssh-keygen -t ed25519 -C "vps-deploy-123miniapps" -f ~/.ssh/id_ed25519_deploy -N ""
   cat ~/.ssh/id_ed25519_deploy.pub
   ```
2. Copy the printed line. In **GitHub → repo → Settings → Deploy keys →
   Add deploy key**, paste it, title it "VPS", leave **Allow write access
   UNCHECKED**, and save.
3. Back on the **VPS**, switch the remote to SSH and use that key:
   ```
   printf 'Host github.com\n  IdentityFile ~/.ssh/id_ed25519_deploy\n  IdentitiesOnly yes\n' >> ~/.ssh/config
   cd /opt/123miniapps
   git remote set-url origin git@github.com:shkinternational2025-lgtm/123miniapps.git
   git pull
   ```
   The first pull asks to trust GitHub's host key - type `yes`.
4. Now flip the repo to private: **GitHub → repo → Settings → Danger Zone →
   Change visibility → Private**.

Your PC pushes keep working with no changes. Never share the private key file
(`id_ed25519_deploy` without `.pub`) - only the `.pub` version goes to GitHub.

---

## Appendix B - How the site now behaves (for reference)

- **Tools are online-only.** Every tool loads fresh from the server each time,
  so it always shows the latest version and always loads its ads, and each use
  is a real, counted visit. Nothing is cached for offline use; an offline user
  sees a "reconnect" screen. (CSS/JS are still cached for speed.)
- **Adding/removing tools or articles:** just ask Claude. After any change,
  Claude regenerates the sitemap and `llms.txt`; you then push, pull on the
  VPS, and run `python3 indexnow.py --all`.
- **When Adsterra codes arrive:** hand them to Claude to wire in.
