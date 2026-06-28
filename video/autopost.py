"""Cloud auto-poster (runs in GitHub Actions): render the NEXT unposted Grüns
article into a video and upload it to the locked Grüns YouTube channel.

Tracking: youtube/gruns_posted.json holds the slugs already posted. Each run
does exactly one video, then appends its slug so the next run moves on.

All paths come from env (set by the workflow). Secrets (token, client, lock)
are written to youtube/ by the workflow from GitHub Secrets before this runs.
"""
import os, sys, json
from pathlib import Path
from googleapiclient.http import MediaFileUpload

HERE = Path(__file__).resolve().parent          # video/
ROOT = HERE.parent                                # repo root
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "youtube"))

import make_gruns_videos as mk
import gruns_youtube_upload as up

POSTED_FILE = Path(os.environ.get("GRUNS_POSTED_FILE", str(ROOT / "youtube" / "gruns_posted.json")))
FAILED_FILE = Path(os.environ.get("GRUNS_FAILED_FILE", str(ROOT / "youtube" / "gruns_failed.json")))


def _load_set(p):
    if p.exists():
        try:
            return set(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            return set()
    return set()


def _save_set(p, s):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(sorted(s), indent=1), encoding="utf-8")


def pick_next(skip):
    for f in sorted(mk.ARTICLES_DIR.glob("*.json")):
        slug = f.stem
        if slug in skip:
            continue
        try:
            a = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        if a.get("error") or not (a.get("body") or "").strip():
            continue
        parsed = mk.parse_article(a)
        if parsed["title"]:
            return slug, parsed, a
    return None, None, None


def post_to_reddit(title, meta, video_url):
    """Post the new video to r/Grunsgummies. Non-fatal — never blocks the run."""
    cid = os.environ.get("REDDIT_CLIENT_ID"); csec = os.environ.get("REDDIT_CLIENT_SECRET")
    user = os.environ.get("REDDIT_USERNAME"); pw = os.environ.get("REDDIT_PASSWORD")
    if not all([cid, csec, user, pw]):
        print("[reddit] credentials not set — skipping reddit post")
        return
    try:
        import praw
        reddit = praw.Reddit(client_id=cid, client_secret=csec, username=user,
                             password=pw, user_agent=f"grunsgummies-poster/1.0 by {user}")
        sub = reddit.subreddit("Grunsgummies")
        t = title.strip()
        post_title = (t if t.lower().startswith(("grüns", "gruns")) else f"Grüns review: {t}")[:300]
        # LINK post -> Reddit renders the YouTube video card (thumbnail + inline player).
        s = sub.submit(title=post_title, url=video_url)
        print(f"[reddit] posted https://reddit.com{s.permalink}")
        # Affiliate link in the first comment. Use the DIRECT gruns.co URL — Reddit
        # bans URL shorteners (is.gd) as "Banned Domain".
        try:
            s.reply(f"Try Grüns VIP → {up.AFFILIATE}")
            print("[reddit] + first comment posted")
        except Exception as ce:
            print(f"[reddit] comment failed (non-fatal): {str(ce)[:140]}")
    except Exception as e:
        print(f"[reddit] post failed (non-fatal): {str(e)[:200]}")


def main():
    posted = _load_set(POSTED_FILE)
    failed = _load_set(FAILED_FILE)
    slug, parsed, raw = pick_next(posted | failed)   # skip both done and known-bad
    if not slug:
        print("No pending articles — all caught up.")
        return 0

    print(f"=== Rendering: {parsed['title']} ({slug}) ===")
    props = mk.build_props(parsed, slug)
    if not mk.render(slug, props):
        # render failure: mark failed so the queue advances next run (no poison pill)
        failed.add(slug); _save_set(FAILED_FILE, failed)
        print(f"[FAIL] render failed for {slug} — skip-listed")
        return 1
    mp4 = str(mk.OUT_DIR / f"{slug}.mp4")
    print(f"Rendered {mp4}")

    # --- upload (channel-locked) ---
    try:
        lock = up.load_lock()
        yt = up.service(lock)
        title, desc, tags = up.meta_for(mp4)
        body = {"snippet": {"title": title, "description": desc, "tags": tags,
                            "categoryId": up.CATEGORY},
                "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}
        media = MediaFileUpload(mp4, chunksize=-1, resumable=True, mimetype="video/mp4")
        resp = yt.videos().insert(part="snippet,status", body=body, media_body=media).execute()
        vid = resp["id"]
        up.post_first_comment(yt, vid)
        watch = f"https://www.youtube.com/watch?v={vid}"
        print(f"[OK] uploaded {watch}")
        # Cross-post the new video to r/Grunsgummies (non-fatal)
        post_to_reddit(up.fix_text(raw.get("title", parsed["title"])),
                       up.fix_text(raw.get("metaDescription", "")), watch)
    except Exception as e:
        msg = str(e)
        # Quota/rate errors are transient — DON'T skip-list, just retry next run.
        transient = any(k in msg.lower() for k in ("quota", "ratelimit", "rate limit",
                        "exceeded", "uploadlimit", "503", "500", "timeout", "timed out"))
        if transient:
            print(f"[RETRY] transient upload error for {slug}, will retry next run: {msg[:200]}")
            return 1
        # Permanent error (e.g. bad metadata) — skip-list so it can't block the queue.
        failed.add(slug); _save_set(FAILED_FILE, failed)
        print(f"[SKIP] permanent upload error for {slug}, skip-listed: {msg[:200]}")
        return 1

    # --- record so we never repost ---
    posted.add(slug)
    _save_set(POSTED_FILE, posted)
    print(f"Marked posted: {slug}  (total posted: {len(posted)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
