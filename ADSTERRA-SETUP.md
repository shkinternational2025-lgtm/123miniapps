# Turning on Adsterra ads (baby steps)

Your site is **ad-ready but ads are OFF**. Nothing loads, nothing tracks, and your
pages look exactly as they do now — until you paste your own Adsterra codes into
**one file**: `assets/js/ads.js`.

You do **not** need to edit 200 pages. Every page already loads `ads.js`, and every
blog article + the homepage already has an invisible `<div class="ad-slot">` waiting
for a banner. Fill in the config once and it switches on everywhere.

---

## Step 1 — Make an Adsterra account

1. Go to https://adsterra.com and sign up as a **Publisher**.
2. Add your website: `https://www.123miniapps.online` (do this **after** it is live on
   your domain — Adsterra verifies the domain, so `file://` or `localhost` will not work).
3. Wait for the site to be **approved** (usually a few hours to a couple of days).

## Step 2 — Create your ad units

In the Adsterra dashboard, open **Websites → your site → Add new ad unit**. The two that
earn the most for a tools/blog site:

| Ad unit | What it does | Where it shows on your site |
|---|---|---|
| **Social Bar** *(recommended first)* | A small sticky bar/notification. Highest earner, no layout changes. | Site-wide, every page |
| **Native Banner** *(optional)* | A banner blended into content. | Inside blog articles + homepage (the `.ad-slot` boxes) |

For each unit Adsterra gives you a small snippet. You only need the **script `src` URL**
from it (it looks like `//pl00000.effectivegatecpm.com/xx/yy/zz/invoke.js`), and for the
Native Banner also the **container id** (looks like `container-abc123`).

## Step 3 — Paste the codes into `assets/js/ads.js`

Open `assets/js/ads.js` and fill in the quotes near the top:

```js
window.ADSTERRA = window.ADSTERRA || {
  // Social Bar / Popunder — the site-wide one:
  siteScriptUrl: '//pl00000.effectivegatecpm.com/xx/yy/zz/invoke.js',

  // Native Banner — optional, fills the in-content boxes:
  bannerScriptUrl: '//pl11111.effectivegatecpm.com/aa/bb/cc/invoke.js',
  bannerContainerId: 'container-abc123'
};
```

Rules:
- **Leave a value as `''` to keep that ad type off.** Want only the Social Bar? Fill
  `siteScriptUrl`, leave the two banner lines empty.
- Paste the URL exactly as Adsterra gives it. Leading `//` is fine; the loader handles it.
- Don't touch anything below the `})();` — that's the machinery.

## Step 4 — Bust the cache so browsers pick up the change

Because browsers cache JS aggressively, bump the version number once so everyone gets the
new `ads.js`. From the `123miniapps` folder run this (Git Bash / WSL / Mac):

```bash
grep -rl "v=2.8.0" --include=*.html --include=*.py --include=*.js . \
  | while read f; do sed -i 's/v=2\.8\.0/v=2.9.0/g' "$f"; done
sed -i "s/const VERSION = '2.8.0'/const VERSION = '2.9.0'/" service-worker.js
```

(If you re-run the Python build scripts, they already emit the current version, so just
change the version string in them too.)

## Step 5 — Upload and check

1. Upload the changed files to your server (or `git push` if you set up auto-deploy).
2. Open your live site in a **private window**. You should see the Social Bar appear.
3. Blog articles / homepage will show the Native Banner where the `.ad-slot` boxes are.

---

## Important — keep it honest and safe

- **Your tool data stays private either way.** Ads run in a separate script; the text,
  files and results inside your tools are still processed only in the visitor's browser
  and are never sent to Adsterra. Do not change that — it's your whole selling point.
- **Your Privacy and Cookie pages already disclose advertising.** They name Adsterra and
  explain that ad networks may set cookies. That disclosure is required by AdSense/Adsterra
  policy and by GDPR/CCPA — leave it in.
- **A cookie-consent banner is now built in.** The moment you fill in an Adsterra script URL,
  a consent banner appears on every page and the ad scripts do **not** load until the visitor
  clicks **Accept**. If they click **Reject**, no ad scripts load and no ad cookies are set.
  While the config is empty (ads off), the banner never shows and the site stays cookieless —
  so there is nothing extra for you to install. (For very high EU/UK volume a full IAB-TCF CMP
  is the gold standard, but this banner covers the basic accept/reject requirement.)
- **Don't click your own ads** and don't ask others to — it gets accounts banned.

## To turn ads back OFF

Set the three values back to `''` in `assets/js/ads.js`, bump the version (Step 4), and
re-upload. Everything returns to a clean, ad-free site instantly.
