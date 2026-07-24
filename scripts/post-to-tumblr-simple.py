#!/usr/bin/env python3
"""
Post to Tumblr using consumer-only auth (app credentials).
Simpler approach without user OAuth.
"""

import json
import re
import argparse
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "requests", "-q"])
    import requests

CONSUMER_KEY = "e4rMsYwSleTU0KJbBwI9zmUrU8geNqn1wydvk2xokUPBhtLzfN"
CONSUMER_SECRET = "B7QKyPFgrHQZshMtF4ykUzNeOx8OEir65dHUKw8WC1nfXjb9vC"
BLOG_NAME = "grunsgummies"

SITE_BASE = "https://grunsgummies.site"
AFFILIATE_LINK = "https://www.gruns.co/pages/vip?snowball=NICK67621"

ARTICLES_DIR = Path(__file__).parent.parent / "content" / "articles"
POSTED_FILE = Path(__file__).parent / "tumblr-posted.json"
POSTING_LOG = Path(__file__).parent / "tumblr-posting-log.csv"

def load_posted() -> set:
    if POSTED_FILE.exists():
        return set(json.loads(POSTED_FILE.read_text(encoding="utf-8")))
    return set()

def save_posted(posted: set):
    POSTED_FILE.write_text(json.dumps(sorted(posted), indent=2), encoding="utf-8")

def log_post(slug: str, title: str, post_url: str):
    with open(POSTING_LOG, "a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp},{slug},{title},{post_url}\n")

def load_articles():
    articles = []
    for f in sorted(ARTICLES_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            articles.append(data)
        except Exception as e:
            print(f"  SKIP {f.name}: {e}")
    return articles

def strip_tags(html):
    text = re.sub(r"<[^>]+>", "", html)
    return text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    posted = load_posted()
    articles = load_articles()
    valid = [a for a in articles if not a.get("error") and a.get("body", "").strip()]
    pending = [a for a in valid if a.get("slug") not in posted]

    print(f"Valid: {len(articles)} | Posted: {len(posted)} | Pending: {len(pending)}")

    if not pending:
        print("Nothing to post.")
        return

    batch = pending[:args.limit]

    if args.dry_run:
        for a in batch:
            print(f"  WOULD POST: {a['title']}")
        return

    for a in batch:
        try:
            title = a["title"]
            body = strip_tags(a.get("body", ""))[:250]
            slug = a["slug"]

            # Build post
            post_body = f"{body}...\n\n[Read full]({SITE_BASE}/articles/{slug})\n\n[Try Gruns VIP]({AFFILIATE_LINK})"

            # Post to Tumblr v2 API
            url = f"https://api.tumblr.com/v2/blog/{BLOG_NAME}.tumblr.com/posts"
            data = {
                "type": "text",
                "title": title,
                "body": post_body,
                "tags": "gruns,greens,gummies",
                "state": "published",
                "api_key": CONSUMER_KEY
            }

            r = requests.post(url, data=data, timeout=10)

            if r.status_code in (200, 201):
                response = r.json()
                post_id = response.get("response", {}).get("id")
                if post_id:
                    posted.add(slug)
                    save_posted(posted)
                    log_post(slug, title, f"https://{BLOG_NAME}.tumblr.com/post/{post_id}")
                    print(f"  OK: {title}")
                else:
                    print(f"  FAIL: {title} -- no ID")
            else:
                print(f"  FAIL: {title} -- HTTP {r.status_code}")
        except Exception as e:
            print(f"  FAIL: {a['title']} -- {e}")

if __name__ == "__main__":
    main()
