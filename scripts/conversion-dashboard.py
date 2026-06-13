#!/usr/bin/env python3
"""
Correlate posts with sales dates to find top converters.
Sales dates: Jun 2, 4, 6, 8, 12 (from screenshot)
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta

REDDIT_LOG = Path(__file__).parent / "reddit-posting-log.csv"
SUBSTACK_LOG = Path(__file__).parent / "substack-posting-log.csv"

# Sales dates (from screenshot: Jun 2, 4, 6, 8, 12)
SALES_DATES = [
    datetime(2026, 6, 2),
    datetime(2026, 6, 4),
    datetime(2026, 6, 6),
    datetime(2026, 6, 8),
    datetime(2026, 6, 12),
]

def load_posts(log_file):
    posts = []
    if not log_file.exists():
        return posts
    with open(log_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 4:
                try:
                    posts.append({
                        "timestamp": datetime.fromisoformat(row[0]),
                        "slug": row[1],
                        "title": row[2],
                        "url": row[3],
                    })
                except Exception:
                    pass
    return posts

def find_posts_before_sales(posts, sales_dates):
    """Find posts posted in the ~24h before each sale."""
    converters = {}

    for sale_date in sales_dates:
        window_start = sale_date - timedelta(hours=24)
        window_end = sale_date + timedelta(hours=1)

        posts_in_window = [
            p for p in posts
            if window_start <= p["timestamp"] <= window_end
        ]

        if posts_in_window:
            date_str = sale_date.strftime("%Y-%m-%d")
            converters[date_str] = posts_in_window

    return converters

def main():
    reddit = load_posts(REDDIT_LOG)
    substack = load_posts(SUBSTACK_LOG)
    all_posts = sorted(reddit + substack, key=lambda p: p["timestamp"])

    print(f"\nCONVERSION TRACKING\n")
    print(f"Reddit posts logged:    {len(reddit)}")
    print(f"Substack posts logged:  {len(substack)}")
    print(f"Total posts tracked:    {len(all_posts)}")

    converters = find_posts_before_sales(all_posts, SALES_DATES)

    if converters:
        print(f"\nPOSTS LIKELY DRIVING SALES:\n")
        for date, posts in sorted(converters.items()):
            print(f"  Sale on {date}:")
            for p in posts:
                source = "Reddit" if REDDIT_LOG in str(p.get("url", "")) or "reddit.com" in p["url"] else "Substack"
                print(f"    [{source}] {p['title'][:70]}")
                print(f"      {p['url']}")
            print()
    else:
        print(f"\nNo posts found in sales windows. Logs may be empty or dates don't align.")

    # Show last 10 posts posted
    if all_posts:
        print(f"\nRECENT POSTS:\n")
        for p in all_posts[-10:]:
            source = "Reddit" if "reddit.com" in p["url"] else "Substack"
            print(f"  [{source}] {p['timestamp'].strftime('%Y-%m-%d %H:%M')} — {p['title'][:60]}")

if __name__ == "__main__":
    main()
