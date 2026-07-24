#!/usr/bin/env python3
"""
Post Grüns articles to Bluesky (@healthygummies.bsky.social).
Original AI-generated articles -> short native hook + clickable links.
Tracks posted articles to avoid duplicates + logs timestamp+title for conversion tracking.

Setup:
  pip install atproto
  set BLUESKY_HANDLE=healthygummies.bsky.social
  set BLUESKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx   (make one at bsky.app -> Settings -> App Passwords)

Usage:
  python post-to-bluesky.py --limit 5 --delay 90
  python post-to-bluesky.py --dry-run --limit 5
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import os
import random
import time
import argparse
from pathlib import Path
from datetime import datetime

try:
    from atproto import Client, client_utils
except ImportError:
    print("ERROR: atproto not installed. Run: pip install atproto")
    exit(1)

# -- Config -------------------------------------------------------------------
BLUESKY_HANDLE       = os.environ.get("BLUESKY_HANDLE", "healthygummies.bsky.social")
BLUESKY_APP_PASSWORD = os.environ.get("BLUESKY_APP_PASSWORD", "")

if not BLUESKY_APP_PASSWORD:
    raise SystemExit(
        "Set BLUESKY_APP_PASSWORD env var (do NOT hardcode). "
        "Create an app password at bsky.app -> Settings -> App Passwords."
    )

SITE_BASE      = "https://grunssite.vercel.app"
AFFILIATE_LINK = "https://www.gruns.co/pages/vip?snowball=NICK67621"

ARTICLES_DIR   = Path(__file__).parent.parent / "content" / "articles"
POSTED_FILE    = Path(__file__).parent / "bluesky-posted.json"
POSTING_LOG    = Path(__file__).parent / "bluesky-posting-log.csv"

MAX_LEN        = 300  # Bluesky grapheme limit

# -- Helpers ------------------------------------------------------------------

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
            articles.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"  SKIP {f.name}: {e}")
    return articles

# Native-sounding hooks (no clickbait spam). Seeded by slug so an article
# always gets the same hook -> stable, non-random-looking.
HOOK_PATTERNS = [
    "{t}? Here's what I dug into 👇",
    "Been researching this: {t}.",
    "Quick one on {t} — worth a read if you're into greens.",
    "{t}. Short honest breakdown:",
    "Looked into {t} so you don't have to.",
    "{t} — what actually matters, minus the hype.",
    "If you've wondered about {t}, this covers it:",
    "{t}. My notes 👇",
]

def clean_title(article: dict) -> str:
    title = article.get("title", article.get("slug", "")).strip()
    # Trim trailing SEO tails like ": Antioxidant Superfood Guide"
    for sep in (":", "—", "|"):
        if sep in title:
            head = title.split(sep)[0].strip()
            if len(head) >= 12:
                title = head
                break
    return title

def build_hook(article: dict) -> str:
    t = clean_title(article)
    rng = random.Random(article.get("slug", ""))
    hook = rng.choice(HOOK_PATTERNS).format(t=t)
    # Leave room for the two link anchors added after (~28 chars incl spacing)
    return hook[:MAX_LEN - 40].rstrip()

def build_post(article: dict):
    """Return a TextBuilder: hook + clickable 'Read the guide' + 'Try Grüns'."""
    slug = article.get("slug", "")
    url  = f"{SITE_BASE}/articles/{slug}"
    hook = build_hook(article)

    tb = client_utils.TextBuilder()
    tb.text(hook + "\n\n")
    tb.link("Read the guide →", url)
    tb.text("   ")
    tb.link("Try Grüns", AFFILIATE_LINK)
    return tb, url

# -- Main ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Post Grüns articles to Bluesky")
    parser.add_argument("--delay",  type=int, default=90,
                        help="Seconds between posts (default: 90)")
    parser.add_argument("--limit",  type=int, default=0,
                        help="Max posts this run (0 = all remaining)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be posted without posting")
    args = parser.parse_args()

    posted   = load_posted()
    articles = load_articles()
    valid    = [a for a in articles if not a.get("error") and a.get("body", "").strip()]
    pending  = [a for a in valid if a.get("slug") not in posted]

    print(f"Articles total:   {len(articles)}")
    print(f"Already posted:   {len(posted)}")
    print(f"Pending to post:  {len(pending)}")

    if not pending:
        print("Nothing to post. All done!")
        return

    if args.limit:
        pending = pending[:args.limit]
        print(f"Limiting to:      {len(pending)} posts this run")

    if args.dry_run:
        print("\n-- DRY RUN --")
        for a in pending:
            tb, url = build_post(a)
            print(f"\n  {a['slug']}")
            print(f"  TEXT ({len(tb.build_text())} chars):")
            print("  " + tb.build_text().replace("\n", "\n  "))
        return

    client = Client()
    profile = client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)
    print(f"\nPosting as {profile.display_name or BLUESKY_HANDLE} (@{BLUESKY_HANDLE})\n")

    done = 0
    for i, article in enumerate(pending):
        slug = article.get("slug", "")
        tb, url = build_post(article)
        text = tb.build_text()
        print(f"[{i+1}/{len(pending)}] Posting: {slug} ({len(text)} chars)")

        try:
            resp = client.send_post(tb)
            # Build a public URL for the post
            rkey = resp.uri.split("/")[-1]
            post_url = f"https://bsky.app/profile/{BLUESKY_HANDLE}/post/{rkey}"
            posted.add(slug)
            save_posted(posted)
            log_post(slug, clean_title(article), post_url)
            done += 1
            print(f"  OK Posted: {post_url}")
        except Exception as e:
            print(f"  FAIL Error: {e}")
            if "rate" in str(e).lower():
                print("  Rate limited - waiting 600s...")
                time.sleep(600)
                continue

        if i < len(pending) - 1:
            print(f"  Waiting {args.delay}s...")
            time.sleep(args.delay)

    print(f"\nDone! Posted {done} article(s) to Bluesky.")

if __name__ == "__main__":
    main()
