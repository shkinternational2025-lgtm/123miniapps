# 123MiniApps — Go Live: Step-by-Step (Baby Steps)

Everything to take the site from your PC to a live HTTPS website on your
Hostinger VPS, plus GitHub auto-deploy. Follow the parts in order.

Replace these placeholders throughout:
- `YOUR_DOMAIN` → your real domain (e.g. `123miniapps.online`)
- `YOUR_VPS_IP` → your VPS IP address (from the Hostinger panel)
- `YOU` → your GitHub username

**Big-picture decision first:** your site is **static** (plain HTML/CSS/JS,
no backend). So the simplest, fastest, most secure setup is **Nginx serving
files directly — no Docker.** Docker adds moving parts and makes HTTPS harder
for zero benefit here. Part D covers Docker anyway, but I recommend skipping it.

---

## PART A — Put the code on GitHub

### A1. Make a GitHub account
Go to github.com and sign up (free). Verify your email.

### A2. Install Git on your PC
Download from git-scm.com → run the installer → accept the defaults.
Open a new terminal (PowerShell) and check it works:
```
git --version
```

### A3. Tell Git who you are (once)
```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### A4. Turn your site folder into a Git repository
In PowerShell, go into the site folder and initialise it:
```
cd "D:\My Final Projects\Claude AI tools\123miniapps Opus 4.8\123miniapps"
git init
git add .
git commit -m "Initial commit - 123MiniApps"
```

### A5. Create an empty repository on GitHub
On github.com → click the **+** (top right) → **New repository** →
name it `123miniapps` → keep it **Private** (or Public, your choice) →
do NOT tick "Add a README" → click **Create repository**.

### A6. Connect your folder to GitHub and push
GitHub shows you commands after creating the repo. They look like this:
```
git remote add origin https://github.com/YOU/123miniapps.git
git branch -M main
git push -u origin main
```
The first push asks you to sign in to GitHub in a browser popup — do it.
Your code is now on GitHub. **From now on, to save changes:**
```
git add .
git commit -m "describe what changed"
git push
```

---

## PART B — Point your domain at the VPS (DNS)

You can do DNS either at your **domain registrar** or via **Cloudflare**
(recommended — free CDN + security). Pick ONE.

### Option 1 — DNS at your registrar / Hostinger
Log in where you manage the domain → find **DNS / Nameservers / DNS Zone**.
Create two **A records**:

| Type | Name (Host) | Value / Points to | TTL  |
|------|-------------|-------------------|------|
| A    | `@`         | `YOUR_VPS_IP`     | Auto |
| A    | `www`       | `YOUR_VPS_IP`     | Auto |

Save. DNS can take 15 minutes to a few hours to spread worldwide.

### Option 2 — Cloudflare (recommended)
1. Make a free account at cloudflare.com → **Add a site** → enter `YOUR_DOMAIN`.
2. Cloudflare scans your existing records → continue.
3. Cloudflare gives you **two nameservers** (like `xxx.ns.cloudflare.com`).
4. At your registrar, replace the domain's nameservers with those two.
5. Back in Cloudflare, add the same two **A records** as the table above,
   and set the cloud icon to **Proxied** (orange).
6. In Cloudflare → **SSL/TLS** → set mode to **Full (strict)** (works with
   the Let's Encrypt certificate you'll install in Part E).

Check DNS has propagated (from your PC):
```
nslookup YOUR_DOMAIN
```
When it returns `YOUR_VPS_IP`, you're ready.

---

## PART C — Prepare the VPS and put the site on it

### C1. Connect to the VPS
From your PC's terminal (use the IP + root password from Hostinger):
```
ssh root@YOUR_VPS_IP
```
Type `yes` if asked to trust the host, then the password.

### C2. Update the server and install what you need
```
apt update && apt upgrade -y
apt install -y nginx git ufw fail2ban certbot python3-certbot-nginx
```

### C3. Turn on the firewall (allow SSH + web only)
```
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable
```
Type `y` to confirm.

### C4. Get the site onto the VPS (from GitHub — matches Part A)
```
mkdir -p /var/www/123miniapps
git clone https://github.com/YOU/123miniapps.git /var/www/123miniapps
```
(For a private repo it will ask for a GitHub username + a Personal Access
Token as the password — create one at github.com → Settings → Developer
settings → Personal access tokens → Tokens (classic) → give it `repo` scope.)

### C5. Tell Nginx to serve the folder
```
nano /etc/nginx/sites-available/123miniapps
```
Paste this (the fuller version with caching/compression is in
`VPS-DEPLOYMENT.md`):
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name YOUR_DOMAIN www.YOUR_DOMAIN;
    root /var/www/123miniapps;
    index index.html;

    location / { try_files $uri $uri/ =404; }
    error_page 404 /404.html;

    # Never cache the service worker, so updates reach visitors
    location = /service-worker.js { add_header Cache-Control "no-cache"; }

    # Security headers
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
}
```
Save in nano: press `Ctrl+O`, `Enter`, then `Ctrl+X`.

Enable the site and remove the default:
```
ln -s /etc/nginx/sites-available/123miniapps /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx
```
`nginx -t` must say "syntax is ok" and "test is successful".

### C6. Check it works over HTTP
In your browser go to `http://YOUR_DOMAIN`. The site should load (still
plain http — HTTPS is the next part).

---

## PART D — (OPTIONAL) Docker — should you use it?

**Recommendation: skip Docker for this site.** It's static files; Nginx on the
host (Part C) is simpler, faster to set up, and makes HTTPS a one-liner.
Docker mainly helps when you have a complex app with dependencies — you don't.

If you still want it (e.g. to learn, or to run several sites in containers):

### D1. Install Docker on the VPS
```
curl -fsSL https://get.docker.com | sh
```

### D2. Add a `Dockerfile` in your project (on your PC), then push to GitHub
```dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html
```

### D3. On the VPS, build and run the container
```
cd /var/www/123miniapps
docker build -t 123miniapps .
docker run -d --name 123miniapps --restart unless-stopped -p 80:80 123miniapps
```
Now the site is served by Nginx **inside** the container on port 80.

**The catch — HTTPS with Docker is harder.** You can't just run `certbot
--nginx` against a container. You'd run a second "reverse proxy" container
(e.g. `nginx-proxy` + `acme-companion`, or Caddy, or Traefik) to handle the
certificate. That's real extra complexity — which is exactly why, for a static
site, the host-Nginx approach in Part C + E is the better path. If you go
Docker, tell me and I'll give you the full reverse-proxy + auto-HTTPS setup.

---

## PART E — Convert HTTP → HTTPS (free, automatic)

This uses the host Nginx from Part C (not Docker). One command does it all:
```
certbot --nginx -d YOUR_DOMAIN -d www.YOUR_DOMAIN
```
Answer the prompts:
- Enter your email (for renewal reminders).
- Agree to the terms (`Y`).
- When asked about redirecting HTTP to HTTPS, choose **Redirect** (option 2).

Certbot automatically edits your Nginx config, installs a free Let's Encrypt
certificate, and sets up auto-renewal. Confirm renewal works:
```
certbot renew --dry-run
```

Now visit `https://YOUR_DOMAIN` — you'll see the padlock. Google requires
HTTPS, and your service worker only fully works over HTTPS, so this step also
"fixes" the local `file://` issues you saw — on the live site everything works.

Certificates renew themselves every ~90 days; you don't need to do anything.

---

## PART F — Turn on GitHub auto-deploy (optional but great)

Your project already includes `.github/workflows/deploy.yml`. Once set up,
every `git push` rebuilds the pages, runs the tests, and copies the site to
your VPS automatically.

### F1. Make an SSH deploy key (on your PC)
```
ssh-keygen -t ed25519 -f deploy_key -C "github-deploy"
```
(Press Enter for no passphrase.) This creates two files: `deploy_key`
(private) and `deploy_key.pub` (public).

### F2. Put the PUBLIC key on the VPS
Copy the contents of `deploy_key.pub` and, on the VPS:
```
echo "PASTE_THE_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
```

### F3. Add 4 secrets on GitHub
On github.com → your repo → **Settings** → **Secrets and variables** →
**Actions** → **New repository secret**. Add these four:

| Name          | Value                                             |
|---------------|---------------------------------------------------|
| `VPS_HOST`    | `YOUR_VPS_IP`                                      |
| `VPS_USER`    | `root`                                             |
| `VPS_PATH`    | `/var/www/123miniapps`                            |
| `VPS_SSH_KEY` | the **entire contents** of the private `deploy_key` file |

### F4. Deploy
Just push:
```
git add .
git commit -m "deploy"
git push
```
Watch it run under the repo's **Actions** tab. Green check = live.

---

## After you're live — the launch checklist

- [ ] `https://YOUR_DOMAIN` loads with a padlock.
- [ ] `https://YOUR_DOMAIN/sitemap.xml` opens (200 URLs).
- [ ] Submit the sitemap in **Google Search Console** (add a Domain property,
      verify by DNS TXT record, then Sitemaps → submit `sitemap.xml`).
- [ ] Add the site to **Bing Webmaster Tools** too.
- [ ] Run the homepage through pagespeed.web.dev — aim for green.
- [ ] (If monetising) add your ad code and update the Privacy/Cookies pages.

That's the whole path: **GitHub → DNS → VPS + Nginx → HTTPS → auto-deploy.**
For the fuller Nginx config (gzip, long-cache headers) and security hardening
(SSH keys, disabling password login, backups), see `VPS-DEPLOYMENT.md`.
