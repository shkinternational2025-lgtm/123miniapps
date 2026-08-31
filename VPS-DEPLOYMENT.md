# 123MiniApps — VPS Deployment Guide (Hostinger, Ubuntu)

**Read this first — the one thing ChatGPT got wrong for your site.**

Your site is **100% static** — plain HTML, CSS and JavaScript that runs in the
visitor's browser. There is **no Node.js app, no server process, no database,
no Docker container** to keep running. That means you can ignore every step in
the other guide about `npm start`, `pm2`, `docker compose up`, and
`proxy_pass http://localhost:3000`. Those are for sites with a backend. Yours
doesn't have one — that's the whole privacy design.

For a static site, the web server (Nginx) simply hands the files to the browser.
That makes deployment **simpler, faster, cheaper and more secure** than what the
other guide describes. Follow the steps below instead.

---

## Overview of what you'll do

1. Point your domain at the VPS (DNS).
2. Harden the server (firewall, SSH keys, Fail2Ban).
3. Install Nginx.
4. Upload the site files.
5. Configure Nginx (static serving + compression + caching + security headers).
6. Add free HTTPS (Let's Encrypt).
7. (Optional) Put Cloudflare in front for CDN + DDoS protection.
8. Set up automatic backups.

Total time: about 45–60 minutes.

---

## Step 0 — Connect to your VPS

From your PC (PowerShell or terminal):

```bash
ssh root@YOUR_VPS_IP
```

Use the IP and root password from your Hostinger VPS dashboard. (We'll replace
password login with SSH keys in Step 2.)

---

## Step 1 — Point the domain at the VPS (DNS)

In whatever controls your domain's DNS (Hostinger hPanel, or Cloudflare if you
do Step 7), create two **A records**:

| Type | Name | Value          | TTL   |
|------|------|----------------|-------|
| A    | `@`  | YOUR_VPS_IP    | Auto  |
| A    | `www`| YOUR_VPS_IP    | Auto  |

DNS can take 15 minutes to a few hours to propagate. Check with:

```bash
dig +short 123miniapps.online
```

When it returns your VPS IP, you're ready. (You can do the rest while waiting.)

---

## Step 2 — Update and harden the server

```bash
# Update everything
sudo apt update && sudo apt upgrade -y

# Install the essentials (note: NO nodejs, NO docker needed)
sudo apt install -y nginx git ufw fail2ban curl unattended-upgrades

# Firewall — allow SSH + web only
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'      # opens ports 80 and 443
sudo ufw enable
sudo ufw status                  # confirm

# Fail2Ban (auto-bans repeated SSH brute-force attempts)
sudo systemctl enable --now fail2ban

# Automatic security updates
sudo dpkg-reconfigure -plow unattended-upgrades
```

### SSH keys (do this — it's the biggest security win)

On **your own PC** (not the VPS), if you don't already have a key:

```bash
ssh-keygen -t ed25519 -C "you@example.com"
```

Copy it to the VPS:

```bash
ssh-copy-id root@YOUR_VPS_IP
# (Windows without ssh-copy-id: paste the contents of ~/.ssh/id_ed25519.pub
#  into /root/.ssh/authorized_keys on the VPS)
```

Then disable password login on the VPS:

```bash
sudo nano /etc/ssh/sshd_config
```

Set these lines:

```
PasswordAuthentication no
PermitRootLogin prohibit-password
```

Restart SSH: `sudo systemctl restart ssh`
**Keep your current session open and test a new login in a second terminal
before closing it**, so you don't lock yourself out.

---

## Step 3 — Create the web directory

```bash
sudo mkdir -p /var/www/123miniapps
sudo chown -R $USER:$USER /var/www/123miniapps
```

---

## Step 4 — Upload the site

Pick **one** method.

### Method A — Git (recommended: easy updates + rollback)

Push your project to a GitHub repo first, then on the VPS:

```bash
cd /var/www/123miniapps
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git .
```

To update later: `cd /var/www/123miniapps && git pull` — done.

### Method B — Direct upload with rsync/scp (no GitHub)

From **your PC**, in the folder that contains `index.html`:

```bash
# rsync (best — only sends changed files)
rsync -avz --delete ./ root@YOUR_VPS_IP:/var/www/123miniapps/

# or scp
scp -r ./* root@YOUR_VPS_IP:/var/www/123miniapps/
```

Either way, confirm on the VPS:

```bash
ls /var/www/123miniapps      # you should see index.html, tools/, assets/, blog/, pages/, sitemap.xml ...
```

> **Important:** upload the `assets/css/main.min.css` file (the concatenated
> stylesheet). You do **not** need `main.css`, the individual CSS files, the
> `build-*.py` scripts, the `test/` folder, or the `*.md` guides on the server —
> they're development files. Uploading them does no harm but serves no purpose.

---

## Step 5 — Configure Nginx (static + fast + secure)

```bash
sudo nano /etc/nginx/sites-available/123miniapps
```

Paste this (it serves files directly — no proxy, plus gzip, caching and
security headers, which cover ChatGPT's Phase 18 performance points):

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name 123miniapps.online www.123miniapps.online;

    root /var/www/123miniapps;
    index index.html;

    # Serve the file, or fall back to a 404 page
    location / {
        try_files $uri $uri/ =404;
    }

    # --- Compression (big speed win) ---
    gzip on;
    gzip_vary on;
    gzip_min_length 256;
    gzip_types text/plain text/css application/javascript application/json
               image/svg+xml application/manifest+json application/xml;

    # --- Caching: hash-free static assets cached long, HTML revalidated ---
    location ~* \.(css|js|svg|png|jpg|jpeg|gif|webp|ico|woff2?)$ {
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
    }
    location ~* \.html$ {
        add_header Cache-Control "no-cache";
    }

    # Service worker must never be cached, or updates won't reach users
    location = /service-worker.js {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    # --- Security headers ---
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

    # Custom 404 page (404.html ships with the site)
    error_page 404 /404.html;
}
```

Enable it and reload:

```bash
sudo ln -s /etc/nginx/sites-available/123miniapps /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default   # remove the placeholder site
sudo nginx -t                                  # test config — must say "ok"
sudo systemctl reload nginx
```

Visit `http://123miniapps.online` — the site should load (still http for now).

---

## Step 6 — Free HTTPS (Let's Encrypt)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d 123miniapps.online -d www.123miniapps.online
```

Answer the prompts (enter your email, agree, and choose to redirect HTTP→HTTPS).
Certbot edits your Nginx config and sets up auto-renewal. Verify renewal works:

```bash
sudo certbot renew --dry-run
```

Your site is now `https://123miniapps.online`. Google requires HTTPS — done.

---

## Step 7 — Cloudflare (optional but recommended)

Free tier gives you a global CDN, DDoS protection, and extra caching.

1. Create a free Cloudflare account, add `123miniapps.online`.
2. Cloudflare gives you two **nameservers** — set them at your domain registrar
   (this replaces Hostinger's DNS; move the two A records into Cloudflare).
3. In Cloudflare SSL/TLS settings, set mode to **Full (strict)** (works with the
   Let's Encrypt cert you installed).
4. Turn on **Auto Minify** (off for HTML if you prefer), **Brotli**, and
   **Always Use HTTPS**.

You can skip this and add it any time later.

---

## Step 8 — Backups

Because the site is static, a backup is just a copy of the files. Simplest
approach — a weekly tarball plus Hostinger's own VPS snapshots:

```bash
# One-off manual backup
sudo tar czf ~/123miniapps-backup-$(date +%F).tar.gz -C /var/www 123miniapps
```

Automate weekly with cron:

```bash
crontab -e
# add this line — Sunday 3am:
0 3 * * 0 tar czf /root/backups/site-$(date +\%F).tar.gz -C /var/www 123miniapps
```

(`mkdir -p /root/backups` first.) Also enable **weekly snapshots** in the
Hostinger VPS panel — that backs up the whole server, not just the files.

---

## Automated deploys (GitHub Actions)

A workflow ships at `.github/workflows/deploy.yml`. Once your code is on GitHub,
every push to `main` will rebuild the generated pages, run the full test suite,
and rsync the site to your VPS automatically — no manual upload.

One-time setup: in GitHub → repo → **Settings → Secrets and variables → Actions**,
add four secrets:

- `VPS_HOST` — your VPS IP (e.g. `203.0.113.10`)
- `VPS_USER` — SSH user (e.g. `root` or a dedicated `deploy` user)
- `VPS_PATH` — web root (e.g. `/var/www/123miniapps`)
- `VPS_SSH_KEY` — a **private** SSH key whose public half is in the server's
  `~/.ssh/authorized_keys`. Generate a dedicated deploy key with
  `ssh-keygen -t ed25519 -f deploy_key`, put `deploy_key.pub` on the server, and
  paste the contents of `deploy_key` (the private file) into this secret.

The workflow deploys only the runtime files — it excludes the Python build
scripts, tests, the individual dev CSS files (only `main.min.css` is served),
the `.md` guides, and the `admin/` folder.

## The blog editor (click-to-write)

`admin/blog-editor.html` is a local authoring tool: open it in your browser,
write an article, preview it live, and it generates a complete, schema-correct
article file plus the build-pipeline entry. It has no backend and stores nothing.

Two ways to publish what it produces:

1. **Quick:** click *Download article HTML*, drop the file in `blog/`, add the
   sitemap line it gives you, add a card link on `blog/index.html`, then push.
2. **Recommended:** click *Copy build entry*, paste it into `POSTS` in
   `blog_posts.py`, and run `python build-blog.py` — the index, article and
   internal links regenerate together and stay in sync.

Keep the editor local, or upload it: it's `noindex` and disallowed in
`robots.txt`, and the deploy workflow excludes it by default. It exposes nothing
sensitive (no backend, no keys), so it's harmless either way.

## Updating the site later

- **If you used Git:** `cd /var/www/123miniapps && git pull`
- **If you used rsync:** re-run the same `rsync` command from your PC.

After any update that changes the service worker or assets, bump the `VERSION`
in `service-worker.js` (you're already at 2.2.0) so returning visitors get the
new files instead of the cached old ones.

---

## Post-deploy checklist (matches your AdSense goals)

Once live, confirm:

- [ ] `https://123miniapps.online` loads with a padlock (valid SSL).
- [ ] `https://123miniapps.online/sitemap.xml` opens and lists 112 URLs.
- [ ] `https://123miniapps.online/robots.txt` opens.
- [ ] Footer legal links work: About, Contact, Privacy, Terms, **Disclaimer,
      Cookies, DMCA** (all now present — this is what AdSense reviewers look for).
- [ ] Run the homepage through https://pagespeed.web.dev — aim for green Core
      Web Vitals (the gzip + caching config above helps you get there).
- [ ] Submit the sitemap in Google Search Console (see LAUNCH-PLAYBOOK.md).
- [ ] Test a few tools on mobile.

---

## What you do NOT need (ignore in the other guide)

- ❌ Node.js / npm on the server — the site has no backend.
- ❌ PM2 — nothing to keep alive.
- ❌ Docker / Docker Compose — no app to containerise.
- ❌ `proxy_pass` to a port — Nginx serves the files directly.
- ❌ A CMS or admin dashboard — the site is generated by your Python build
      scripts on your PC, then uploaded. That's simpler and has a smaller attack
      surface than a live CMS. (If you later want a click-to-write blog admin,
      that's a real project — but it's optional, not required to launch or to
      get AdSense.)

Keeping it static is a feature, not a limitation: fewer moving parts means less
to secure, less to break, and faster pages.
