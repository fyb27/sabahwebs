#!/usr/bin/env python3
"""Mirror the live sabahwebs.com blog posts + their same-origin assets into this project."""
import os, re, html, urllib.parse, urllib.request, sys

BASE = "https://sabahwebs.com"
ROOT = os.path.dirname(os.path.abspath(__file__))
HEADERS = {"User-Agent": "Mozilla/5.0 (mirror script)"}

SLUGS = [
    "24-hour-clinic-jalan-penampang-kota-kinabalu",
    "how-much-does-seo-cost-in-malaysia",
    "ai-seo-malaysia",
    "how-long-does-seo-take-to-work-the-honest-answer",
    "why-your-sabah-business-needs-a-website-in-2026",
    "what-is-orou-sapulot",
    "why-orou-sapulot-is-the-most-important",
    "top-5-reasons-to-visit-orou-sapulot-in-2026",
    "orou-sapulot-sabahs-best-kept-secret-for-eco-travellers",
    "the-best-scaffolding-in-kota-kinabalu-kk",
]

# pages to fetch: (page_url, local_path)
PAGES = [(f"{BASE}/blog/{s}.html", os.path.join(ROOT, "blog", f"{s}.html")) for s in SLUGS]
PAGES.append((f"{BASE}/blog/index.html", os.path.join(ROOT, "blog", "index.html")))

downloaded = set()   # absolute URLs already fetched
failures = []

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def safe_local_path(abs_url):
    """Map an absolute same-origin URL to a local path under ROOT, preserving structure."""
    p = urllib.parse.urlparse(abs_url)
    if p.netloc != "sabahwebs.com":
        return None
    path = urllib.parse.unquote(p.path).lstrip("/")
    if not path or path.endswith("/"):
        return None
    return os.path.join(ROOT, *path.split("/"))

def save(local_path, data):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(data)

def download_asset(abs_url):
    if abs_url in downloaded:
        return
    downloaded.add(abs_url)
    local = safe_local_path(abs_url)
    if not local:
        return
    if os.path.exists(local):
        # still parse CSS even if exists
        if local.endswith(".css"):
            parse_css(local, abs_url)
        return
    try:
        # re-encode the path for the request (handles spaces etc.)
        p = urllib.parse.urlparse(abs_url)
        enc_path = urllib.parse.quote(urllib.parse.unquote(p.path))
        req_url = f"{p.scheme}://{p.netloc}{enc_path}"
        if p.query:
            req_url += "?" + p.query
        data = fetch(req_url)
        save(local, data)
        print("  asset", local.replace(ROOT, "").lstrip("\\/"))
        if local.endswith(".css"):
            parse_css(local, abs_url)
    except Exception as e:
        failures.append((abs_url, str(e)))

ATTR_RE = re.compile(r'\b(href|src|srcset)\s*=\s*"([^"]+)"', re.I)
CSS_URL_RE = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)')

def extract_refs_html(text):
    refs = []
    for m in ATTR_RE.finditer(text):
        attr = m.group(1).lower()
        val = html.unescape(m.group(2)).strip()
        if attr == "srcset":
            # comma-separated "url [descriptor]" candidates; URL may contain spaces
            for part in val.split(","):
                cand = part.strip()
                if not cand:
                    continue
                # strip a trailing size descriptor like "500w" or "2x"
                cand = re.sub(r'\s+\d+(?:\.\d+)?[wx]$', '', cand).strip()
                if cand:
                    refs.append(cand)
        else:
            # href/src: keep the whole value (filenames may contain spaces)
            if val:
                refs.append(val)
    return refs

def parse_css(local_css_path, css_abs_url):
    try:
        with open(local_css_path, "r", encoding="utf-8", errors="ignore") as f:
            css = f.read()
    except Exception:
        return
    for m in CSS_URL_RE.finditer(css):
        ref = html.unescape(m.group(1)).strip()
        if ref.startswith("data:"):
            continue
        abs_url = urllib.parse.urljoin(css_abs_url, ref)
        download_asset(abs_url)

def process_page(page_url, local_path):
    try:
        data = fetch(page_url)
    except Exception as e:
        failures.append((page_url, str(e)))
        return
    save(local_path, data)
    print("PAGE", local_path.replace(ROOT, "").lstrip("\\/"))
    text = data.decode("utf-8", errors="ignore")
    for ref in extract_refs_html(text):
        if ref.startswith(("data:", "mailto:", "tel:", "#", "javascript:")):
            continue
        abs_url = urllib.parse.urljoin(page_url, ref)
        # only mirror same-origin assets (skip live html pages & external origins)
        pr = urllib.parse.urlparse(abs_url)
        if pr.netloc != "sabahwebs.com":
            continue
        # skip other blog html pages (we fetch those separately) and root nav pages
        if pr.path.endswith(".html") or pr.path in ("", "/") or pr.path.rstrip("/") == "/blog":
            continue
        # only mirror assets that live under a host-named top directory (e.g. cdn.prod.website-files.com/...)
        parts = urllib.parse.unquote(pr.path).lstrip("/").split("/")
        if len(parts) < 2 or "." not in parts[0]:
            continue
        download_asset(abs_url)

for page_url, local_path in PAGES:
    process_page(page_url, local_path)

print("\n=== summary ===")
print("assets downloaded:", len([u for u in downloaded if safe_local_path(u)]))
print("failures:", len(failures))
for u, e in failures[:25]:
    print("  FAIL", u, "::", e)
