#!/usr/bin/env python3
"""
Post a short Substack Note about Gruns (schedule 2x/day).
Picks a random template + random article link.
Usage: python substack-note.py [--dry-run]
"""

import json
import random
import argparse
from pathlib import Path

import requests

LLI = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjUxOTU2OTQ1MiwiaWF0IjoxNzgxMjk4MTUxLCJleHAiOjE3ODM4OTAxNTEsImF1ZCI6Imxpa2VseS1sb2dnZWQtaW4ifQ.ttVikvbvx-QpMUvo30CHmCkkW9wNt2-B7uMgfJTmGCk"
SID = "s%3AHg7-xK0Js_WkafIs0RZotwK8JkEdP7p6.ZKBjno3QRoufHXE2vnIVI95x3PCTZ4H%2BipRJm3ZRNnQ"

SITE_BASE      = "https://grunsgummies.site"
AFFILIATE_LINK = "https://www.gruns.co/pages/vip?snowball=NICK67621"
ARTICLES_DIR   = Path(__file__).parent.parent / "content" / "articles"

TEMPLATES = [
    "Confession: I used to buy bags of spinach with the best intentions and throw out a sad green puddle two weeks later. Switching to a daily greens gummy was me finally admitting who I am — and honestly, my energy has never been better.",
    "Three weeks into taking Gruns every morning and the biggest surprise isn't the energy — it's that the 3pm slump just... stopped showing up. I didn't realize how much I was relying on that second coffee until I didn't need it.",
    "My partner laughed at me for buying 'adult gummy bears.' Now they steal them out of my pack every morning. The strawberry taste is genuinely good, which feels illegal for something with kale in it.",
    "Real talk: I tried green powders for two years. Choked them down, cleaned the blender, hated every second. A gummy pack I can toss in my bag and actually look forward to? That's the version of healthy I can stick with.",
    "The thing nobody tells you about greens supplements: consistency beats everything. I never skipped a day of Gruns because they taste like candy. I skipped my powder constantly because it tasted like a lawn.",
    "Took Gruns on a two-week trip — no fridge, no blender, no excuses. First vacation ever where I didn't come home feeling like my gut was staging a protest.",
    "Started taking Gruns mostly for the gut health stuff. Stayed because my skin looked noticeably better after a month and a half. The prebiotics are doing something, I swear.",
    "I'm the person who forgets vitamins exist by day 4. Somehow I'm 60 days into a Gruns streak. Turns out the trick was making the healthy thing the treat.",
    "Did the math today: a Gruns pack works out to about $1.50/day. My old smoothie habit was $9 a pop and half the nutrients. Should've switched ages ago.",
    "Bloating after every meal used to be my normal. A few weeks of daily prebiotics and fiber from these gummies and I forgot that was ever a thing. Wild what gut health actually does.",
    "My toddler thinks my Gruns pack is candy and honestly? Same. Sneaking 60+ superfoods into something that tastes like strawberry gummies is the best trick I've pulled on myself.",
    "Hot take: the best supplement isn't the one with the fanciest ingredients. It's the one you'll actually take every single day. For me that bar is 'tastes like a snack' — and that's the whole reason this works.",
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Random article for the link
    articles = []
    for f in ARTICLES_DIR.glob("*.json"):
        try:
            a = json.loads(f.read_text(encoding="utf-8"))
            if not a.get("error") and a.get("body", "").strip():
                articles.append(a)
        except Exception:
            pass

    note_text = random.choice(TEMPLATES)
    article = random.choice(articles) if articles else None

    content = [
        {"type": "paragraph", "content": [{"type": "text", "text": note_text}]},
    ]
    # Sometimes include an article link, naturally worded
    if article and random.random() < 0.5:
        url = f"{SITE_BASE}/articles/{article['slug']}"
        content.append({"type": "paragraph", "content": [
            {"type": "text", "text": "I wrote more about this here: "},
            {"type": "text", "text": article["title"], "marks": [{"type": "link", "attrs": {"href": url}}]},
        ]})
    content.append({"type": "paragraph", "content": [
        {"type": "text", "text": "(If you want to try them, this link gets you the VIP price: "},
        {"type": "text", "text": "gruns.co VIP", "marks": [{"type": "link", "attrs": {"href": AFFILIATE_LINK}}]},
        {"type": "text", "text": ")"},
    ]})

    body_json = {"type": "doc", "attrs": {"schemaVersion": "v1"}, "content": content}

    if args.dry_run:
        print("WOULD POST NOTE:", note_text)
        return

    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
        "Referer": "https://substack.com/home",
        "Content-Type": "application/json",
    })
    s.cookies.set("substack.sid", SID, domain=".substack.com")
    s.cookies.set("substack.lli", LLI, domain=".substack.com")

    r = s.post("https://substack.com/api/v1/comment/feed", json={
        "bodyJson": body_json,
        "tabId": "for-you",
        "surface": "feed",
        "replyMinimumRole": "everyone",
    })
    if r.status_code == 200:
        print(f"OK Note posted: {note_text[:60]}...")
    else:
        print(f"FAIL ({r.status_code}): {r.text[:200]}")

if __name__ == "__main__":
    main()
