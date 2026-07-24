#!/usr/bin/env python3
"""
Simple Tumblr OAuth token getter.
Usage: python get-tumblr-tokens.py

1. Opens auth URL in browser
2. You authorize and copy the verifier code
3. Paste verifier code here to complete token exchange
4. Tokens saved to tumblr-tokens.json
"""

import json
import subprocess
from pathlib import Path
from urllib.parse import parse_qs

try:
    from requests_oauthlib import OAuth1Session
except ImportError:
    subprocess.check_call(["pip", "install", "requests-oauthlib", "-q"])
    from requests_oauthlib import OAuth1Session

CONSUMER_KEY = "e4rMsYwSleTU0KJbBwI9zmUrU8geNqn1wydvk2xokUPBhtLzfN"
CONSUMER_SECRET = "B7QKyPFgrHQZshMtF4ykUzNeOx8OEir65dHUKw8WC1nfXjb9vC"
TOKEN_FILE = Path(__file__).parent / "tumblr-tokens.json"

REQUEST_TOKEN_URL = "https://www.tumblr.com/oauth/request_token"
AUTHORIZE_URL = "https://www.tumblr.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://www.tumblr.com/oauth/access_token"

print("Getting Tumblr tokens...")

# Step 1: Get request token
oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
try:
    r = oauth.post(REQUEST_TOKEN_URL, timeout=10)
    creds = parse_qs(r.content.decode())
    req_token = creds.get('oauth_token')[0]
    req_secret = creds.get('oauth_token_secret')[0]
    print(f"[OK] Got request token: {req_token[:20]}...")
except Exception as e:
    print(f"[FAIL] Failed to get request token: {e}")
    exit(1)

# Step 2: Direct user to authorize
auth_url = f"{AUTHORIZE_URL}?oauth_token={req_token}"
print(f"\n1. Visit this URL to authorize:")
print(f"   {auth_url}\n")

# Try to open browser
try:
    import webbrowser
    webbrowser.open(auth_url)
    print("Browser opened (or visit URL above manually)\n")
except:
    print("Copy/paste the URL above in your browser\n")

# Step 3: Get verifier from user
input("Press Enter when you've authorized...")
verifier = input("Paste the verifier code from the page: ").strip()

if not verifier:
    print("No verifier provided!")
    exit(1)

# Step 4: Exchange for user tokens
try:
    oauth = OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=req_token,
        resource_owner_secret=req_secret,
        verifier=verifier
    )
    r = oauth.post(ACCESS_TOKEN_URL, timeout=10)
    creds = parse_qs(r.content.decode())
    user_token = creds.get('oauth_token')[0]
    user_secret = creds.get('oauth_token_secret')[0]

    tokens = {
        "consumer_key": CONSUMER_KEY,
        "consumer_secret": CONSUMER_SECRET,
        "user_token": user_token,
        "user_secret": user_secret
    }

    TOKEN_FILE.write_text(json.dumps(tokens, indent=2))
    print(f"\n[OK] Tokens saved to {TOKEN_FILE}")
    print(f"[OK] User token: {user_token[:20]}...")
    print("[OK] Ready to post!")

except Exception as e:
    print(f"\n[FAIL] Failed: {e}")
    print("Check the verifier code and try again")
    exit(1)
