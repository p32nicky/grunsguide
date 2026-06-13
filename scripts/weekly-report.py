#!/usr/bin/env python3
"""
Generate weekly performance report (HTML).
Reads posting logs + tracks top performers.
Run weekly or on demand: python weekly-report.py
Saves to: ../reports/weekly-report-YYYY-WXX.html
"""

import json
import csv
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

REDDIT_LOG = Path(__file__).parent / "reddit-posting-log.csv"
SUBSTACK_LOG = Path(__file__).parent / "substack-posting-log.csv"
REPORTS_DIR = Path(__file__).parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

def load_posts(log_file):
    """Load posts from CSV log."""
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
                        "source": "Reddit" if "reddit.com" in row[3] else "Substack",
                    })
                except Exception:
                    pass
    return posts

def get_week_posts(posts, days=7):
    """Filter posts from past N days."""
    cutoff = datetime.now() - timedelta(days=days)
    return [p for p in posts if p["timestamp"] >= cutoff]

def count_by_topic(posts):
    """Count posts by topic (extract from slug)."""
    topics = defaultdict(int)
    for p in posts:
        # Extract topic from slug: "gr-ns-for-X" -> "X"
        slug = p["slug"]
        if "gr-ns-for-" in slug:
            topic = slug.replace("gr-ns-for-", "").replace("-", " ").title()
            topics[topic] += 1
        elif "complete-guide" in slug:
            topic = slug.replace("complete-guide-", "").replace("-", " ").title()
            topics[topic] += 1
    return topics

def calculate_metrics(posts):
    """Calculate basic metrics."""
    by_source = defaultdict(int)
    for p in posts:
        by_source[p["source"]] += 1
    return {
        "total_posts": len(posts),
        "by_source": dict(by_source),
        "avg_posts_per_day": len(posts) / 7 if posts else 0,
    }

def generate_html(week_posts, all_posts, metrics):
    """Generate HTML report."""
    now = datetime.now()
    week_num = now.isocalendar()[1]
    year = now.year

    topics = count_by_topic(week_posts)
    top_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:5]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grüns Weekly Report - Week {week_num}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; border-radius: 8px; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h1 {{ color: #2d5016; margin-top: 0; border-bottom: 2px solid #d4af37; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .metric {{ background: #f9f9f9; padding: 15px; border-left: 4px solid #d4af37; border-radius: 4px; }}
        .metric-value {{ font-size: 28px; font-weight: bold; color: #2d5016; }}
        .metric-label {{ font-size: 12px; color: #999; text-transform: uppercase; margin-top: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th {{ background: #f0f0f0; padding: 12px; text-align: left; font-weight: 600; color: #333; border-bottom: 2px solid #ddd; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background: #f9f9f9; }}
        .source-reddit {{ color: #ff4500; font-weight: 600; }}
        .source-substack {{ color: #0066cc; font-weight: 600; }}
        .recommendations {{ background: #f0f8ff; border-left: 4px solid #0066cc; padding: 15px; border-radius: 4px; margin: 20px 0; }}
        .recommendations h3 {{ margin-top: 0; color: #0066cc; }}
        ul {{ line-height: 1.8; }}
        .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Grüns Weekly Performance Report</h1>
        <p><strong>Week {week_num}, {year}</strong> | Generated {now.strftime('%Y-%m-%d %H:%M UTC')}</p>

        <h2>Key Metrics</h2>
        <div class="metrics">
            <div class="metric">
                <div class="metric-value">{metrics['total_posts']}</div>
                <div class="metric-label">Posts This Week</div>
            </div>
            <div class="metric">
                <div class="metric-value">{metrics['avg_posts_per_day']:.1f}</div>
                <div class="metric-label">Posts/Day Average</div>
            </div>
            <div class="metric">
                <div class="metric-value">{metrics['by_source'].get('Reddit', 0)}</div>
                <div class="metric-label">Reddit Posts</div>
            </div>
            <div class="metric">
                <div class="metric-value">{metrics['by_source'].get('Substack', 0)}</div>
                <div class="metric-label">Substack Posts</div>
            </div>
        </div>

        <h2>Top Topics Posted</h2>
        <table>
            <thead>
                <tr><th>Topic</th><th>Posts</th></tr>
            </thead>
            <tbody>
"""
    for topic, count in top_topics:
        html += f"                <tr><td>{topic}</td><td>{count}</td></tr>\n"

    html += """            </tbody>
        </table>

        <h2>Recent Posts</h2>
        <table>
            <thead>
                <tr><th>When</th><th>Source</th><th>Title</th></tr>
            </thead>
            <tbody>
"""
    for p in sorted(week_posts, key=lambda x: x["timestamp"], reverse=True)[:10]:
        time_ago = (datetime.now() - p["timestamp"]).total_seconds()
        if time_ago < 3600:
            when = f"{int(time_ago/60)}m ago"
        elif time_ago < 86400:
            when = f"{int(time_ago/3600)}h ago"
        else:
            when = f"{int(time_ago/86400)}d ago"

        source_class = f"source-{p['source'].lower()}"
        title = p["title"][:60] + "..." if len(p["title"]) > 60 else p["title"]

        html += f'                <tr><td>{when}</td><td><span class="{source_class}">{p["source"]}</span></td><td>{title}</td></tr>\n'

    html += """            </tbody>
        </table>

        <div class="recommendations">
            <h3>Recommendations</h3>
            <ul>
"""

    # Smart recommendations
    if metrics['total_posts'] > 50:
        html += "                <li><strong>Pace is strong.</strong> 50+ posts/week means high visibility. Monitor for Reddit spam warnings.</li>\n"
    elif metrics['total_posts'] > 0:
        html += f"                <li><strong>Current pace:</strong> {metrics['total_posts']} posts/week. Consider scaling to 70+ for faster growth.</li>\n"

    if top_topics:
        top_topic = top_topics[0][0]
        html += f"                <li><strong>Top topic this week:</strong> '{top_topic}' posted {top_topics[0][1]}x. Consider creating more variations of this angle.</li>\n"

    html += """                <li><strong>Conversion tracking:</strong> Run <code>python scripts/conversion-dashboard.py</code> to correlate posts with sales.</li>
                <li><strong>Next steps:</strong> Pinterest integration (2-3x traffic potential) + subreddit expansion to diversify sources.</li>
            </ul>
        </div>

        <div class="footer">
            <p>Grüns Automation Report | All data from reddit-posting-log.csv & substack-posting-log.csv</p>
            <p>View all posts: <a href="https://grunsgummies.site">grunsgummies.site</a></p>
        </div>
    </div>
</body>
</html>
"""
    return html

def main():
    reddit = load_posts(REDDIT_LOG)
    substack = load_posts(SUBSTACK_LOG)
    all_posts = sorted(reddit + substack, key=lambda p: p["timestamp"])

    week_posts = get_week_posts(all_posts, days=7)
    metrics = calculate_metrics(week_posts)

    html = generate_html(week_posts, all_posts, metrics)

    # Save with week number in filename
    now = datetime.now()
    week_num = now.isocalendar()[1]
    year = now.year
    filename = f"weekly-report-{year}-W{week_num:02d}.html"
    filepath = REPORTS_DIR / filename

    filepath.write_text(html, encoding="utf-8")
    print(f"Report saved: {filepath}")
    print(f"Open in browser: file://{filepath.absolute()}")

if __name__ == "__main__":
    main()
