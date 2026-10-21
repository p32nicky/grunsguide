#!/usr/bin/env python3
"""
Post Grüns articles to r/Grunsgummies on Reddit.
Tracks posted articles to avoid duplicates + logs timestamp+title for conversion tracking.
Usage: python post-to-reddit.py [--delay 30] [--limit 5]
"""

import json
import os
import random
import time
import argparse
from pathlib import Path
from datetime import datetime

try:
    import praw
except ImportError:
    print("ERROR: praw not installed. Run: pip install praw")
    exit(1)

# ── Config ──────────────────────────────────────────────────────────────────
REDDIT_CLIENT_ID     = os.environ.get("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET", "")
REDDIT_USERNAME      = os.environ.get("REDDIT_USERNAME", "")
REDDIT_PASSWORD      = os.environ.get("REDDIT_PASSWORD", "")
REDDIT_USER_AGENT    = f"grunsgummies-poster/1.0 by {REDDIT_USERNAME or 'gruns'}"

if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD]):
    raise SystemExit("Set REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET / REDDIT_USERNAME / "
                     "REDDIT_PASSWORD environment variables (do not hardcode credentials).")

SUBREDDIT      = "Grunsgummies"
# Live site. NOT grunsgummies.site — that domain is parked/dead, so linking to
# it sent every Reddit reader to a dead page.
SITE_BASE      = "https://grunssite.vercel.app"
AFFILIATE_LINK = "https://www.gruns.co/pages/vip?snowball=NICK67621"

ARTICLES_DIR   = Path(__file__).parent.parent / "content" / "articles"
POSTED_FILE    = Path(__file__).parent / "reddit-posted.json"
POSTING_LOG    = Path(__file__).parent / "reddit-posting-log.csv"

# ── Helpers ──────────────────────────────────────────────────────────────────

def load_posted() -> set:
    if POSTED_FILE.exists():
        return set(json.loads(POSTED_FILE.read_text(encoding="utf-8")))
    return set()

def save_posted(posted: set):
    POSTED_FILE.write_text(
        json.dumps(sorted(posted), indent=2),
        encoding="utf-8"
    )

def log_post(slug: str, title: str, reddit_url: str):
    """Log post timestamp for conversion tracking."""
    with open(POSTING_LOG, "a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp},{slug},{title},{reddit_url}\n")

def load_articles():
    articles = []
    for f in sorted(ARTICLES_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            articles.append(data)
        except Exception as e:
            print(f"  SKIP {f.name}: {e}")
    return articles

def load_search_queries():
    """Real Google queries this site gets impressions for (from Search Console).

    Reddit ranks well in Google, so titling a post the way people actually
    search can capture that traffic directly — far better than the generic
    "X — honest review" shape, which matches nothing anyone types.
    """
    qf = Path(__file__).parent / "search-queries.json"
    if not qf.exists():
        return []
    try:
        return json.loads(qf.read_text(encoding="utf-8")).get("queries", [])
    except Exception:
        return []


SEARCH_QUERIES = load_search_queries()


def query_title(article: dict):
    """Return a search-query-shaped title, but only if the article genuinely
    covers that topic — every match token must be present. A title that
    oversells what the post links to would just burn trust."""
    # Match on slug + title only. The `keywords` field is broad SEO filler, so
    # including it made generic tokens fire on unrelated articles — "vegan"
    # matched an article about international shipping, "benefit" matched one
    # about kale. A title that misdescribes what it links to burns more trust
    # than a generic title ever would.
    haystack = " ".join([
        article.get("slug", ""),
        article.get("title", ""),
    ]).lower().replace(" ", "-")

    best = None
    for q in SEARCH_QUERIES:
        tokens = q.get("match", [])
        if tokens and all(t.lower() in haystack for t in tokens):
            # prefer the highest-demand query this article can honestly answer
            if best is None or q.get("impressions", 0) > best.get("impressions", 0):
                best = q
    return best["title"] if best else None


def seo_title(article: dict) -> str:
    """Build a search-friendly title (people google 'gruns review reddit' etc)."""
    matched = query_title(article)
    if matched:
        return matched[:300]

    title = article.get("title", article.get("slug", ""))
    # Strip clunky generated prefixes
    for prefix in ("Complete guide: ", "Why Grüns for ", "Grüns solution for ", "Does Grüns help with "):
        if title.startswith(prefix):
            title = title[len(prefix):].rstrip("?").strip()
            title = title[0].upper() + title[1:] if title else title
            break

    patterns = [
        "Grüns review: {t}",
        "{t} — my honest take on Grüns",
        "{t} | does Grüns actually work?",
        "My experience with Grüns: {t}",
        "{t} — what I found after researching Grüns gummies",
        "Honest Grüns gummies review: {t}",
        "{t} (Grüns 2026 review)",
        "Is Grüns worth it? {t}",
    ]
    # Seed by slug so the same article always gets the same title
    rng = random.Random(article.get("slug", ""))
    chosen = rng.choice(patterns)
    full = chosen.format(t=title)
    # Avoid double-Grüns awkwardness when title already starts with Grüns
    if title.lower().startswith("grüns") or title.lower().startswith("gruns"):
        full = title + " — honest review"
    return full[:300]

def build_post_text(article: dict) -> str:
    """Build Reddit post body (selftext) from article data."""
    meta = article.get("metaDescription", "")
    slug = article.get("slug", "")

    lines = []
    if meta:
        lines.append(meta)
    lines.append("")
    if slug:
        lines.append(f"**Read the full article:** {SITE_BASE}/articles/{slug}")
        lines.append("")
        lines.append("---")
    lines.append(f"*Try Grüns VIP →* {AFFILIATE_LINK}")

    return "\n".join(lines)

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Post Grüns articles to Reddit")
    parser.add_argument("--delay",  type=int, default=60,
                        help="Seconds between posts (default: 60)")
    parser.add_argument("--limit",  type=int, default=0,
                        help="Max posts this run (0 = all remaining)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be posted without actually posting")
    args = parser.parse_args()

    posted   = load_posted()
    articles = load_articles()
    # Skip articles that failed generation (have error or empty body)
    valid    = [a for a in articles if not a.get("error") and a.get("body", "").strip()]
    pending  = [a for a in valid if a.get("slug") not in posted]

    # Post the articles that answer real Google queries FIRST, highest demand
    # first. Default slug order buried the money queries ("Grüns vs Ritual",
    # "Kids vs adult") hundreds of posts deep — months away at 5/day.
    def demand(a):
        t = query_title(a)
        if not t:
            return 0
        for q in SEARCH_QUERIES:
            if q["title"] == t:
                return q.get("impressions", 1)
        return 1
    pending.sort(key=lambda a: (-demand(a), a.get("slug", "")))

    matched = sum(1 for a in pending if query_title(a))
    print(f"Articles total:   {len(articles)}")
    print(f"Already posted:   {len(posted)}")
    print(f"Pending to post:  {len(pending)}  ({matched} with search-query titles, queued first)")

    if not pending:
        print("Nothing to post. All done!")
        return

    if args.limit:
        pending = pending[:args.limit]
        print(f"Limiting to:      {len(pending)} posts this run")

    if args.dry_run:
        print("\n-- DRY RUN --")
        for a in pending:
            print(f"  WOULD POST: {a['title']}")
        return

    # Connect to Reddit
    reddit = praw.Reddit(
        client_id     = REDDIT_CLIENT_ID,
        client_secret = REDDIT_CLIENT_SECRET,
        username      = REDDIT_USERNAME,
        password      = REDDIT_PASSWORD,
        user_agent    = REDDIT_USER_AGENT,
    )

    sub = reddit.subreddit(SUBREDDIT)
    print(f"\nPosting to r/{SUBREDDIT} as u/{REDDIT_USERNAME}\n")

    for i, article in enumerate(pending):
        slug  = article.get("slug", "")
        title = seo_title(article)
        body  = build_post_text(article)

        print(f"[{i+1}/{len(pending)}] Posting: {title}")

        try:
            submission = sub.submit(title=title, selftext=body)
            posted.add(slug)
            save_posted(posted)
            reddit_url = f"https://reddit.com{submission.permalink}"
            log_post(slug, title, reddit_url)
            print(f"  OK Posted: {reddit_url}")
        except praw.exceptions.RedditAPIException as e:
            print(f"  FAIL Reddit API error: {e}")
            # If rate limited, wait longer
            if "RATELIMIT" in str(e).upper():
                wait = 600
                print(f"  Rate limited - waiting {wait}s...")
                time.sleep(wait)
                continue
        except Exception as e:
            print(f"  FAIL Error: {e}")

        if i < len(pending) - 1:
            print(f"  Waiting {args.delay}s...")
            time.sleep(args.delay)

    print(f"\nDone! Posted {len(pending)} article(s) to r/{SUBREDDIT}.")

if __name__ == "__main__":
    main()
