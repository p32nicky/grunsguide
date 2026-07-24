#!/usr/bin/env python3
"""
Simple Tumblr OAuth - get tokens without complexity.
Run once, authorize in browser, tokens saved to tumblr-tokens.json
"""

import json
import webbrowser
from pathlib import Path
from urllib.parse import parse_qs

try:
    from requests_oauthlib import OAuth1Session
except:
    import subprocess
    subprocess.check_call(["pip", "install", "requests-oauthlib", "-q"])
    from requests_oauthlib import OAuth1Session

CONSUMER_KEY = "e4rMsYwSleTU0KJbBwI9zmUrU8geNqn1wydvk2xokUPBhtLzfN"
CONSUMER_SECRET = "B7QKyPFgrHQZshMtF4ykUzNeOx8OEir65dHUKw8WC1nfXjb9vC"
TOKEN_FILE = Path(__file__).parent / "tumblr-tokens.json"
TEMP_REQ = Path(__file__).parent / ".tumblr-req.json"

REQUEST_TOKEN_URL = "https://www.tumblr.com/oauth/request_token"
AUTHORIZE_URL = "https://www.tumblr.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://www.tumblr.com/oauth/access_token"

# Step 1: Get request token and save it
print("Step 1: Getting request token...")
oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
r = oauth.post(REQUEST_TOKEN_URL, timeout=10)
creds = parse_qs(r.content.decode())
req_token = creds['oauth_token'][0]
req_secret = creds['oauth_token_secret'][0]

# SAVE request token+secret for later
TEMP_REQ.write_text(json.dumps({"req_token": req_token, "req_secret": req_secret}))

print(f"  Request token saved: {req_token[:15]}...")

# Step 2: Direct to auth URL
auth_url = f"{AUTHORIZE_URL}?oauth_token={req_token}"
print(f"\nStep 2: Opening browser...")
print(f"  URL: {auth_url}\n")
webbrowser.open(auth_url)

# Step 3: Wait for user to authorize and get verifier
input("After authorizing, paste the verifier code below and press Enter...\nVerifier: ")
verifier = input().strip()

if not verifier:
    print("[FAIL] No verifier provided")
    exit(1)

# Step 4: Load saved request token and exchange
print(f"\nStep 3: Exchanging verifier for access tokens...")
saved = json.loads(TEMP_REQ.read_text())
req_token = saved["req_token"]
req_secret = saved["req_secret"]

oauth = OAuth1Session(
    CONSUMER_KEY,
    client_secret=CONSUMER_SECRET,
    resource_owner_key=req_token,
    resource_owner_secret=req_secret,
    verifier=verifier
)

r = oauth.post(ACCESS_TOKEN_URL, timeout=10)

if r.status_code != 200:
    print(f"[FAIL] HTTP {r.status_code}")
    print(f"  {r.text[:100]}")
    exit(1)

creds = parse_qs(r.content.decode())
user_token = creds.get('oauth_token', [None])[0]
user_secret = creds.get('oauth_token_secret', [None])[0]

if not user_token or not user_secret:
    print(f"[FAIL] Missing tokens in response")
    print(f"  {r.text}")
    exit(1)

# Step 5: Save access tokens
tokens = {
    "consumer_key": CONSUMER_KEY,
    "consumer_secret": CONSUMER_SECRET,
    "user_token": user_token,
    "user_secret": user_secret
}

TOKEN_FILE.write_text(json.dumps(tokens, indent=2))
TEMP_REQ.unlink(missing_ok=True)

print(f"\n[SUCCESS] Tokens saved to tumblr-tokens.json")
print(f"[SUCCESS] Ready to post!")
