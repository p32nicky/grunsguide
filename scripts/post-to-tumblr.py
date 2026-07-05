#!/usr/bin/env python3
"""
Post Grüns articles to Tumblr (grunsgummies blog).
Posts ONE article per run (schedule every 30 min).
Tracks posted articles to avoid duplicates.
Usage: python post-to-tumblr.py [--limit 1] [--dry-run]
"""

import json
import re
import argparse
from pathlib import Path
from datetime import datetime

try:
    import pytumblr
except ImportError:
    print("ERROR: pytumblr not installed. Run: pip install pytumblr")
    exit(1)

# -- Config -------------------------------------------------------------------
BLOG_NAME = "grunsgummies.tumblr.com"
TOKEN_FILE = Path(__file__).parent / "tumblr-tokens.json"

# Load tokens
if not TOKEN_FILE.exists():
    print(f"ERROR: {TOKEN_FILE} not found. Run tumblr-oauth-setup.py first.")
    exit(1)

tokens = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))
OAUTH_CONSUMER_KEY = tokens["consumer_key"]
OAUTH_CONSUMER_SECRET = tokens["consumer_secret"]
OAUTH_USER_TOKEN = tokens["user_token"]
OAUTH_USER_SECRET = tokens["user_secret"]
SITE_BASE = "https://grunsgummies.site"
AFFILIATE_LINK = "https://www.gruns.co/pages/vip?snowball=NICK67621"

ARTICLES_DIR = Path(__file__).parent.parent / "content" / "articles"
POSTED_FILE = Path(__file__).parent / "tumblr-posted.json"
POSTING_LOG = Path(__file__).parent / "tumblr-posting-log.csv"

# -- Helpers ------------------------------------------------------------------

def load_posted() -> set:
    if POSTED_FILE.exists():
        return set(json.loads(POSTED_FILE.read_text(encoding="utf-8")))
    return set()

def save_posted(posted: set):
    POSTED_FILE.write_text(
        json.dumps(sorted(posted), indent=2),
        encoding="utf-8"
    )

def log_post(slug: str, title: str, post_url: str):
    """Log post timestamp for conversion tracking."""
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
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return text.strip()

# -- Main ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    posted = load_posted()
    articles = load_articles()
    valid = [a for a in articles if not a.get("error") and a.get("body", "").strip()]
    pending = [a for a in valid if a.get("slug") not in posted]

    print(f"Valid articles: {len(articles)} | Posted: {len(posted)} | Pending: {len(pending)}")

    if not pending:
        print("Nothing to post.")
        return

    batch = pending[:args.limit]

    if args.dry_run:
        for a in batch:
            print(f"WOULD POST: {a['title']}")
        return

    # Connect to Tumblr with user auth
    client = pytumblr.TumblrRestClient(
        OAUTH_CONSUMER_KEY,
        OAUTH_CONSUMER_SECRET,
        OAUTH_USER_TOKEN,
        OAUTH_USER_SECRET
    )

    for a in batch:
        try:
            title = a["title"]
            body = a.get("body", "").strip()
            slug = a["slug"]

            # Strip HTML from body for Tumblr text post
            body_text = strip_tags(body)[:500] + "..."

            # Build post content
            post_body = f"{body_text}\n\nRead full article: {SITE_BASE}/articles/{slug}\n\nTry Grüns VIP: {AFFILIATE_LINK}"

            # Post to Tumblr
            response = client.create_text(
                BLOG_NAME,
                state="published",
                title=title,
                body=post_body,
                tags=["gruns", "greens", "gummies", "supplement"]
            )

            if response.get("id"):
                posted.add(slug)
                save_posted(posted)
                post_url = f"https://{BLOG_NAME}/post/{response['id']}"
                log_post(slug, title, post_url)
                print(f"OK Posted: {title} -> {post_url}")
            else:
                print(f"FAIL: {title} -- {response}")
        except Exception as e:
            print(f"FAIL: {a['title']} -- {e}")

if __name__ == "__main__":
    main()
