#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post Grüns articles to Tumblr (grunsgummies.tumblr.com).
Uses OAuth1 + photo posts (like london food tours).
Posts 1/run on schedule (hourly = 24 posts/day).
"""
import json
import re
import os
import sys
import requests
from requests_oauthlib import OAuth1
from pathlib import Path
from datetime import datetime

# Force UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

BLOG = "grunsgummies.tumblr.com"
API_URL = f"https://api.tumblr.com/v2/blog/{BLOG}/post"

# Load tokens
TOKEN_FILE = Path(__file__).parent / "tumblr-tokens.json"
if not TOKEN_FILE.exists():
    print("ERROR: tumblr-tokens.json not found")
    exit(1)

tokens = json.loads(TOKEN_FILE.read_text())
CONSUMER_KEY = tokens["consumer_key"]
CONSUMER_SECRET = tokens["consumer_secret"]
TOKEN = tokens["user_token"]
TOKEN_SECRET = tokens["user_secret"]

SITE_BASE = "https://grunssite.vercel.app"
AFFILIATE = "https://www.gruns.co/pages/vip?snowball=NICK67621"

ARTICLES_DIR = Path(__file__).parent.parent / "content" / "articles"
POSTED_FILE = Path(__file__).parent / "tumblr-posted.json"
LOG_FILE = Path(__file__).parent / "tumblr-posting-log.csv"

def _auth():
    return OAuth1(CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET)

def _strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").strip()

def load_posted() -> set:
    if POSTED_FILE.exists():
        return set(json.loads(POSTED_FILE.read_text(encoding='utf-8')))
    return set()

def save_posted(posted: set):
    POSTED_FILE.write_text(json.dumps(sorted(posted), indent=2, ensure_ascii=False), encoding='utf-8')

def log_post(slug: str, title: str, url: str):
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        ts = datetime.now().isoformat()
        f.write(f"{ts},{slug},{title},{url}\n")

def load_articles():
    articles = []
    for f in sorted(ARTICLES_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding='utf-8'))
            articles.append(data)
        except Exception as e:
            pass
    return articles

def post_article(article: dict) -> dict:
    """Post article to Tumblr as text post. Returns {id, url} or {error}."""
    title = article.get("title", "")
    body = article.get("body", "")
    slug = article.get("slug", "")

    # Body already has title in it, just use as-is
    caption = body
    caption += f"<br/><br/><hr/><br/>"
    caption += f"<a href=\"{AFFILIATE}\"><b>Try Grüns VIP →</b></a>"

    data = {
        "type": "text",
        "body": caption,
        "tags": "gruns,greens,gummies,supplement,health"
    }

    try:
        r = requests.post(API_URL, data=data, auth=_auth(), timeout=15)
        if r.status_code in (200, 201):
            post_id = r.json().get("response", {}).get("id", "")
            url = f"https://{BLOG}/post/{post_id}"
            return {"id": post_id, "url": url}
        return {"error": r.text[:300]}
    except Exception as e:
        return {"error": str(e)}

def main():
    posted = load_posted()
    articles = load_articles()
    valid = [a for a in articles if not a.get("error") and a.get("body", "").strip()]
    pending = [a for a in valid if a.get("slug") not in posted]

    print(f"Total: {len(articles)} | Posted: {len(posted)} | Pending: {len(pending)}")

    if not pending:
        print("All posted!")
        return

    # Post 1
    article = pending[0]
    result = post_article(article)

    if "id" in result:
        posted.add(article["slug"])
        save_posted(posted)
        log_post(article["slug"], article["title"], result["url"])
        print(f"[OK] Posted: {article['title']}")
        print(f"  URL: {result['url']}")
    else:
        print(f"[FAIL] Failed: {article['title']}")
        print(f"  Error: {result.get('error', '?')}")

if __name__ == "__main__":
    main()
