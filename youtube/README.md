# Grüns YouTube Uploader (isolated)

Fully separate from the Tours Explorer / reddit-poster uploader. Nothing is
shared — own folder, own OAuth client, own token, own dedupe log, and a hard
channel lock that **refuses to upload to any channel except the Grüns one**.

## One-time setup

1. **Create a fresh OAuth client** (this is the only manual step):
   - Google Cloud Console → create/select a project for Grüns
   - APIs & Services → Library → enable **YouTube Data API v3**
   - APIs & Services → Credentials → Create Credentials → **OAuth client ID** →
     Application type **Desktop app**
   - Download the JSON, save it here as: `gruns_client_secret.json`
   - (OAuth consent screen: add your Google account as a Test User)

2. **Authorize + lock the channel:**
   ```
   python gruns_youtube_auth.py
   ```
   A browser opens — sign in and **pick the dedicated Grüns channel**. It prints
   the channel, asks you to confirm, then writes `channel_lock.json`. Done once.

## Daily use

```
python gruns_youtube_upload.py --private        # test: uploads unlisted
python gruns_youtube_upload.py --limit 5        # 5 public
python gruns_youtube_upload.py                  # up to DAILY_LIMIT public
python gruns_youtube_upload.py <slug>.mp4       # one specific video
```

- Reads videos from `C:/Users/nickd/Downloads/grunsvideos`
- Title/description pulled from each video's source article in `content/articles`
- Appends affiliate link: `https://www.gruns.co/pages/vip?snowball=NICK67621`
- Tracks uploads in `gruns_uploaded.json` (never re-posts)

## Cross-post guard

Every run checks the authed channel ID against `channel_lock.json`. If they
don't match (e.g. token drifted to Tours Explorer or personal), it **aborts
before uploading anything**. This is the safety that the old shared-token setup
lacked.
