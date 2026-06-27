"""Upload Grüns videos from Downloads/grunsvideos to the LOCKED Grüns channel.

Hard isolation from every other project:
  - uses gruns_token.json in THIS folder only (never a shared token.json)
  - refuses to run unless the authed channel == channel_lock.json (set by
    gruns_youtube_auth.py). This is what prevents cross-posting to Tours Explorer.

Title/description come from each video's source article JSON (matched by slug).

Usage:
  python gruns_youtube_upload.py                 # upload up to DAILY_LIMIT new
  python gruns_youtube_upload.py --limit 5
  python gruns_youtube_upload.py <slug>.mp4      # one specific file
  python gruns_youtube_upload.py --private       # upload unlisted (test)
"""
import os, sys, glob, json, re, argparse, html
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

HERE       = os.path.dirname(os.path.abspath(__file__))
TOKEN      = os.path.join(HERE, "gruns_token.json")
LOCK       = os.path.join(HERE, "channel_lock.json")
LOG        = os.path.join(HERE, "gruns_uploaded.json")
VIDEOS     = r"C:/Users/nickd/Downloads/grunsvideos"
ARTICLES   = r"C:/grunssite/content/articles"
AFFILIATE  = "https://www.gruns.co/pages/vip?snowball=NICK67621"  # canonical (redirect target)
SHORT_LINK = "https://grunsgummies.site/vip"  # branded, no-truncation; redirects to AFFILIATE
SCOPES     = ["https://www.googleapis.com/auth/youtube.upload",
              "https://www.googleapis.com/auth/youtube.force-ssl"]
DAILY_LIMIT = 10
CATEGORY    = "26"   # Howto & Style
BASE_TAGS   = ["gruns", "greens", "greensgummies", "superfood", "nutrition", "wellness", "health"]


def fix_text(s):
    if not s: return ""
    s = s.replace("�", "ü").replace("�", "ü")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def load_lock():
    if not os.path.exists(LOCK):
        sys.exit("[ABORT] channel not locked. Run gruns_youtube_auth.py first.")
    return json.load(open(LOCK))


def service(lock):
    if not os.path.exists(TOKEN):
        sys.exit("[ABORT] no gruns_token.json. Run gruns_youtube_auth.py first.")
    creds = Credentials.from_authorized_user_info(
        json.load(open(TOKEN, encoding="utf-8-sig")), SCOPES)
    if not creds.valid:
        creds.refresh(Request())
        open(TOKEN, "w").write(creds.to_json())
    yt = build("youtube", "v3", credentials=creds)
    # HARD GUARD — abort if the token is not the locked Grüns channel
    items = yt.channels().list(part="snippet", mine=True).execute().get("items", [])
    if not items:
        sys.exit("[ABORT] token has no channel — re-auth.")
    cid, name = items[0]["id"], items[0]["snippet"]["title"]
    if cid != lock["channel_id"]:
        sys.exit(f"[ABORT] WRONG CHANNEL: '{name}' ({cid}). "
                 f"Locked to '{lock['channel_name']}' ({lock['channel_id']}). "
                 f"Refusing to upload — this is the cross-post guard.")
    print(f"[channel OK] {name} ({cid})")
    return yt


def post_first_comment(yt, video_id):
    text = (f"\U0001f449 Try Grüns VIP (greens gummies): {SHORT_LINK}\n\n"
            "Affiliate link — we may earn a small commission at no extra cost to you.")
    try:
        yt.commentThreads().insert(part="snippet", body={"snippet": {
            "videoId": video_id,
            "topLevelComment": {"snippet": {"textOriginal": text}}}}).execute()
        print("     + first comment posted (affiliate link)")
    except Exception as e:
        print(f"     comment failed: {str(e)[:140]}")


def article_for(slug):
    p = os.path.join(ARTICLES, slug + ".json")
    if not os.path.exists(p):
        return None
    return json.load(open(p, encoding="utf-8", errors="replace"))


def meta_for(mp4):
    slug = os.path.splitext(os.path.basename(mp4))[0]
    a = article_for(slug)
    title = fix_text(a["title"]) if a else slug.replace("-", " ").title()
    meta  = fix_text(a.get("metaDescription", "")) if a else ""
    title = (title[:95]).strip()
    tags  = list(dict.fromkeys(BASE_TAGS + [w.lower() for w in re.findall(r"[A-Za-z]{4,}", title)]))[:15]
    # Affiliate link FIRST so it stays above YouTube's "...more" fold and never
    # gets truncated in the collapsed description preview.
    desc = (f"\U0001f449 Try Grüns VIP (greens gummies): {SHORT_LINK}\n\n"
            f"{title}\n\n{meta}\n\n"
            "Affiliate link — we may earn a small commission at no extra cost to you.\n"
            "This is general information, not medical advice.\n\n"
            + " ".join("#" + t for t in tags))
    return title, desc[:4900], tags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", help="specific <slug>.mp4 to upload")
    ap.add_argument("--limit", type=int, default=DAILY_LIMIT)
    ap.add_argument("--private", action="store_true", help="upload unlisted (testing)")
    args = ap.parse_args()

    lock = load_lock()
    yt = service(lock)
    log = json.load(open(LOG)) if os.path.exists(LOG) else {}

    if args.target:
        targets = [args.target if os.path.isabs(args.target) else os.path.join(VIDEOS, args.target)]
    else:
        mp4s = sorted(glob.glob(os.path.join(VIDEOS, "*.mp4")))
        targets = [m for m in mp4s if os.path.basename(m) not in log][:args.limit]

    privacy = "unlisted" if args.private else "public"
    print(f"Uploading {len(targets)} video(s) as {privacy} to {lock['channel_name']}...")
    n = 0
    for m in targets:
        fn = os.path.basename(m)
        try:
            title, desc, tags = meta_for(m)
            body = {"snippet": {"title": title, "description": desc, "tags": tags,
                                "categoryId": CATEGORY},
                    "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False}}
            media = MediaFileUpload(m, chunksize=-1, resumable=True, mimetype="video/mp4")
            resp = yt.videos().insert(part="snippet,status", body=body, media_body=media).execute()
            vid = resp["id"]
            watch = f"https://www.youtube.com/watch?v={vid}"
            post_first_comment(yt, vid)
            log[fn] = {"id": vid, "watch": watch, "title": title, "privacy": privacy}
            json.dump(log, open(LOG, "w"), indent=1)
            print(f"[OK] {fn[:50]}\n     {watch}")
            n += 1
        except Exception as e:
            print(f"[FAIL] {fn[:50]}: {str(e)[:160]}")
    print(f"\nDone. {n} uploaded to {lock['channel_name']}.")


if __name__ == "__main__":
    main()
