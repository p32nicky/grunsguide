#!/usr/bin/env python3
"""
Post Gruns articles to grunsgummies.substack.com.
Posts ONE article per run (schedule every 10 min for drip posting).
Tracks posted articles in substack-posted.json.
Usage: python substack-post.py [--limit 1] [--dry-run]
"""

import json
import re
import argparse
from pathlib import Path

import requests

# -- Config -------------------------------------------------------------------
LLI = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjUxOTU2OTQ1MiwiaWF0IjoxNzgxMjk4MTUxLCJleHAiOjE3ODM4OTAxNTEsImF1ZCI6Imxpa2VseS1sb2dnZWQtaW4ifQ.ttVikvbvx-QpMUvo30CHmCkkW9wNt2-B7uMgfJTmGCk"
SID = "s%3AHg7-xK0Js_WkafIs0RZotwK8JkEdP7p6.ZKBjno3QRoufHXE2vnIVI95x3PCTZ4H%2BipRJm3ZRNnQ"

PUB_URL        = "https://grunsgummies.substack.com"
USER_ID        = 519569452
SITE_BASE      = "https://grunsgummies.site"
AFFILIATE_LINK = "https://www.gruns.co/pages/vip?snowball=NICK67621"

ARTICLES_DIR = Path(__file__).parent.parent / "content" / "articles"
POSTED_FILE  = Path(__file__).parent / "substack-posted.json"

# Pouch product image (uploaded to Substack CDN) — used as cover + in-article
COVER_IMAGE = "https://substack-post-media.s3.amazonaws.com/public/images/8f34fd40-8009-4da6-81a3-a37d7ff515d8_1000x988.jpeg"

# -- HTML -> ProseMirror ------------------------------------------------------

def text_node(text, marks=None):
    node = {"type": "text", "text": text}
    if marks:
        node["marks"] = marks
    return node

def parse_inline(html):
    """Convert inline HTML (strong, a, em) to ProseMirror text nodes."""
    nodes = []
    pattern = re.compile(r'<strong>(.*?)</strong>|<b>(.*?)</b>|<em>(.*?)</em>|<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', re.S)
    pos = 0
    for m in pattern.finditer(html):
        if m.start() > pos:
            plain = strip_tags(html[pos:m.start()])
            if plain:
                nodes.append(text_node(plain))
        if m.group(1) is not None or m.group(2) is not None:
            t = strip_tags(m.group(1) or m.group(2))
            if t:
                nodes.append(text_node(t, [{"type": "strong"}]))
        elif m.group(3) is not None:
            t = strip_tags(m.group(3))
            if t:
                nodes.append(text_node(t, [{"type": "em"}]))
        elif m.group(4) is not None:
            t = strip_tags(m.group(5))
            if t:
                nodes.append(text_node(t, [{"type": "link", "attrs": {"href": m.group(4)}}]))
        pos = m.end()
    if pos < len(html):
        plain = strip_tags(html[pos:])
        if plain:
            nodes.append(text_node(plain))
    return nodes

def strip_tags(html):
    text = re.sub(r"<[^>]+>", "", html)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#39;", "'").replace("&quot;", '"').replace("&nbsp;", " ")
    return text.strip()

def html_to_prosemirror(html, slug):
    """Convert article HTML to a ProseMirror doc."""
    content = []
    # Product image at top of article
    content.append({
        "type": "captionedImage",
        "content": [{
            "type": "image2",
            "attrs": {
                "src": COVER_IMAGE,
                "fullscreen": False,
                "imageSize": "normal",
                "height": 988,
                "width": 1000,
            },
        }],
    })
    # Remove the first h1 (title shown separately)
    html = re.sub(r"<h1[^>]*>.*?</h1>", "", html, count=1, flags=re.S)

    block_re = re.compile(
        r"<(h2|h3|h4|p)[^>]*>(.*?)</\1>|<ul[^>]*>(.*?)</ul>|<ol[^>]*>(.*?)</ol>",
        re.S,
    )
    for m in block_re.finditer(html):
        if m.group(1):  # heading or paragraph
            tag, inner = m.group(1), m.group(2)
            inline = parse_inline(inner)
            if not inline:
                continue
            if tag == "p":
                content.append({"type": "paragraph", "content": inline})
            else:
                level = int(tag[1])
                content.append({"type": "heading", "attrs": {"level": level}, "content": inline})
        else:  # list
            list_html = m.group(3) or m.group(4)
            items = []
            for li in re.findall(r"<li[^>]*>(.*?)</li>", list_html, re.S):
                inline = parse_inline(li)
                if inline:
                    items.append({"type": "list_item", "content": [{"type": "paragraph", "content": inline}]})
            if items:
                ltype = "bullet_list" if m.group(3) else "ordered_list"
                content.append({"type": ltype, "content": items})

    # Footer: links back to site + affiliate
    content.append({"type": "paragraph", "content": [
        text_node("Read more guides: ", None),
        text_node(f"{SITE_BASE}/articles/{slug}", [{"type": "link", "attrs": {"href": f"{SITE_BASE}/articles/{slug}"}}]),
    ]})
    content.append({"type": "paragraph", "content": [
        text_node("Try Gruns VIP: ", [{"type": "strong"}]),
        text_node(AFFILIATE_LINK, [{"type": "link", "attrs": {"href": AFFILIATE_LINK}}]),
    ]})

    return {"type": "doc", "content": content}

# -- Substack API -------------------------------------------------------------

def make_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
        "Referer": f"{PUB_URL}/publish/posts",
        "Content-Type": "application/json",
    })
    s.cookies.set("substack.sid", SID, domain=".substack.com")
    s.cookies.set("substack.lli", LLI, domain=".substack.com")
    return s

def post_article(s, article):
    title = article["title"]
    meta  = article.get("metaDescription", "")[:140]
    doc   = html_to_prosemirror(article.get("body", ""), article["slug"])

    # 1. Create draft
    draft_payload = {
        "draft_title": title,
        "draft_subtitle": meta,
        "draft_body": json.dumps(doc),
        "draft_bylines": [{"id": USER_ID, "is_guest": False}],
        "type": "newsletter",
        "audience": "everyone",
        "cover_image": COVER_IMAGE,
    }
    r = s.post(f"{PUB_URL}/api/v1/drafts", json=draft_payload)
    r.raise_for_status()
    draft_id = r.json()["id"]

    # 2. Publish (send=False so subscribers don't get emailed every 10 min)
    r2 = s.post(f"{PUB_URL}/api/v1/drafts/{draft_id}/publish", json={"send": False})
    r2.raise_for_status()
    return r2.json().get("canonical_url", f"{PUB_URL}/p/{draft_id}")

# -- Main ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    posted = set()
    if POSTED_FILE.exists():
        posted = set(json.loads(POSTED_FILE.read_text(encoding="utf-8")))

    articles = []
    for f in sorted(ARTICLES_DIR.glob("*.json")):
        try:
            a = json.loads(f.read_text(encoding="utf-8"))
            if not a.get("error") and a.get("body", "").strip():
                articles.append(a)
        except Exception:
            pass

    pending = [a for a in articles if a["slug"] not in posted]
    print(f"Valid articles: {len(articles)} | Posted: {len(posted)} | Pending: {len(pending)}")

    if not pending:
        print("Nothing to post.")
        return

    batch = pending[:args.limit]
    if args.dry_run:
        for a in batch:
            print(f"WOULD POST: {a['title']}")
        return

    s = make_session()
    for a in batch:
        try:
            url = post_article(s, a)
            posted.add(a["slug"])
            POSTED_FILE.write_text(json.dumps(sorted(posted), indent=2), encoding="utf-8")
            print(f"OK Posted: {a['title']} -> {url}")
        except Exception as e:
            print(f"FAIL: {a['title']} -- {e}")

if __name__ == "__main__":
    main()
