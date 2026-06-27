"""One-time YouTube OAuth for the GRÜNS channel — fully isolated from any other
project. Run this once, sign in, and pick the dedicated Grüns brand channel.

It saves gruns_token.json IN THIS FOLDER ONLY and writes the authed channel ID
into channel_lock.json. The uploader refuses to run unless it matches.

Usage:  python gruns_youtube_auth.py
Prereq: place your Grüns OAuth client as  gruns_client_secret.json  in this folder.
"""
import json, os, sys
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

HERE = os.path.dirname(os.path.abspath(__file__))
CLIENT = os.path.join(HERE, "gruns_client_secret.json")
TOKEN  = os.path.join(HERE, "gruns_token.json")
LOCK   = os.path.join(HERE, "channel_lock.json")
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    if not os.path.exists(CLIENT):
        sys.exit(f"[MISSING] {CLIENT}\n"
                 "Create a fresh OAuth client (Desktop app) in Google Cloud Console "
                 "for the Grüns project, download the JSON, and save it here as "
                 "gruns_client_secret.json — then re-run.")
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT, SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent",
                                  authorization_prompt_message=
                                  ">>> A browser will open. Sign in and PICK THE GRÜNS CHANNEL <<<")
    with open(TOKEN, "w", encoding="utf-8") as f:
        f.write(creds.to_json())

    yt = build("youtube", "v3", credentials=creds)
    ch = yt.channels().list(part="snippet", mine=True).execute().get("items", [])
    if not ch:
        sys.exit("[ABORT] this login has no YouTube channel. Re-run and pick the Grüns brand account.")
    cid, name = ch[0]["id"], ch[0]["snippet"]["title"]
    json.dump({"channel_id": cid, "channel_name": name}, open(LOCK, "w"), indent=2)
    print("\n" + "=" * 60)
    print(f"  AUTHED + LOCKED CHANNEL : {name}")
    print(f"  Channel ID              : {cid}")
    print("=" * 60)
    print("\n>>> VERIFY this is the dedicated Grüns channel (NOT personal / Tours Explorer).")
    print(">>> If it's WRONG, run:  python gruns_youtube_auth.py  again and pick the right one.")

if __name__ == "__main__":
    main()
