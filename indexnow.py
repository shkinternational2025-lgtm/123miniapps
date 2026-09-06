#!/usr/bin/env python3
# ============================================================
# indexnow.py - ping IndexNow (Bing, Yandex, and partners) so
# new or updated pages get crawled within minutes instead of
# waiting for the next natural crawl.
#
# IndexNow is the non-WordPress way to do instant indexing:
# one HTTPS POST with a list of URLs. Google does NOT use
# IndexNow (submit the sitemap in Search Console for Google),
# but Bing/Yandex/Seznam/Naver do, and that also feeds
# DuckDuckGo.
#
# Usage:
#   # submit every URL in the sitemap (use after a big update):
#   python3 indexnow.py --all
#
#   # submit specific pages (use after adding/editing a few):
#   python3 indexnow.py tools/new-tool.html blog/new-post.html
#
# Run this from the site root AFTER you have deployed, so the
# URLs are actually live when the crawler comes to fetch them.
# ============================================================

import sys
import re
import json
import urllib.request

HOST = "www.123miniapps.online"
BASE = f"https://{HOST}"
KEY = "76cd4323f3b048f7e5c46419eb98a9ea"
KEY_LOCATION = f"{BASE}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"


def urls_from_sitemap():
    xml = open("sitemap.xml", encoding="utf-8").read()
    return re.findall(r"<loc>\s*([^<]+?)\s*</loc>", xml)


def to_full(u):
    u = u.strip()
    if u.startswith("http"):
        return u
    return f"{BASE}/{u.lstrip('/')}"


def submit(urls):
    urls = [to_full(u) for u in urls if u.strip()]
    if not urls:
        print("No URLs to submit.")
        return
    # IndexNow accepts up to 10,000 URLs per request.
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"IndexNow: HTTP {resp.status} for {len(urls)} URL(s).")
            print("  200/202 = accepted. 403 = key file not reachable yet.")
    except urllib.error.HTTPError as e:
        print(f"IndexNow error: HTTP {e.code} - {e.read().decode('utf-8', 'ignore')}")
    except Exception as e:  # noqa: BLE001
        print(f"IndexNow request failed: {e}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    if args[0] == "--all":
        submit(urls_from_sitemap())
    else:
        submit(args)
