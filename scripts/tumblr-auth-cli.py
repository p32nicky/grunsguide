#!/usr/bin/env python3
"""
Tumblr auth CLI - provide verifier as argument
Usage: python tumblr-auth-cli.py <verifier_code>
"""

import json
import sys
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
STATE_FILE = Path(__file__).parent / ".oauth-state.json"

if len(sys.argv) != 2:
    print("Usage: python tumblr-auth-cli.py <verifier_code>")
    sys.exit(1)

verifier = sys.argv[1].strip()

if not STATE_FILE.exists():
    print("[FAIL] No saved state. Run the authorization script first")
    sys.exit(1)

print("Exchanging verifier for access tokens...")
saved = json.loads(STATE_FILE.read_text())
req_token = saved["req_token"]
req_secret = saved["req_secret"]

oauth = OAuth1Session(
    CONSUMER_KEY,
    client_secret=CONSUMER_SECRET,
    resource_owner_key=req_token,
    resource_owner_secret=req_secret,
    verifier=verifier
)

r = oauth.post("https://www.tumblr.com/oauth/access_token", timeout=10)

if r.status_code != 200:
    print(f"[FAIL] HTTP {r.status_code}: {r.text[:100]}")
    sys.exit(1)

creds = parse_qs(r.content.decode())
user_token = creds.get('oauth_token', [None])[0]
user_secret = creds.get('oauth_token_secret', [None])[0]

if not user_token or not user_secret:
    print(f"[FAIL] No tokens: {r.text[:100]}")
    sys.exit(1)

tokens = {
    "consumer_key": CONSUMER_KEY,
    "consumer_secret": CONSUMER_SECRET,
    "user_token": user_token,
    "user_secret": user_secret
}

TOKEN_FILE.write_text(json.dumps(tokens, indent=2))
STATE_FILE.unlink(missing_ok=True)

print(f"[SUCCESS] Tokens saved!")
print(f"[SUCCESS] Ready to post!")
