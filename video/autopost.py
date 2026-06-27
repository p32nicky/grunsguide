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


def load_posted():
    if POSTED_FILE.exists():
        try:
            return set(json.loads(POSTED_FILE.read_text(encoding="utf-8")))
        except Exception:
            return set()
    return set()


def pick_next(posted):
    for f in sorted(mk.ARTICLES_DIR.glob("*.json")):
        slug = f.stem
        if slug in posted:
            continue
        try:
            a = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        if a.get("error") or not (a.get("body") or "").strip():
            continue
        parsed = mk.parse_article(a)
        if parsed["title"]:
            return slug, parsed
    return None, None


def main():
    posted = load_posted()
    slug, parsed = pick_next(posted)
    if not slug:
        print("No pending articles — all caught up.")
        return 0

    print(f"=== Rendering: {parsed['title']} ({slug}) ===")
    props = mk.build_props(parsed, slug)
    if not mk.render(slug, props):
        print(f"[FAIL] render failed for {slug}")
        return 1
    mp4 = str(mk.OUT_DIR / f"{slug}.mp4")
    print(f"Rendered {mp4}")

    # --- upload (channel-locked) ---
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
    print(f"[OK] uploaded https://www.youtube.com/watch?v={vid}")

    # --- record so we never repost ---
    posted.add(slug)
    POSTED_FILE.parent.mkdir(parents=True, exist_ok=True)
    POSTED_FILE.write_text(json.dumps(sorted(posted), indent=1), encoding="utf-8")
    print(f"Marked posted: {slug}  (total posted: {len(posted)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
