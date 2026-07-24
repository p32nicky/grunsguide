#!/usr/bin/env python3
"""
Exchange Tumblr verifier code for access tokens.
After authorizing at the URL, use this to complete the exchange.

Usage: python tumblr-exchange-token.py <request_token> <request_secret> <verifier>
"""

import json
import sys
from pathlib import Path

try:
    from requests_oauthlib import OAuth1Session
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "requests-oauthlib", "-q"])
    from requests_oauthlib import OAuth1Session

CONSUMER_KEY = "e4rMsYwSleTU0KJbBwI9zmUrU8geNqn1wydvk2xokUPBhtLzfN"
CONSUMER_SECRET = "B7QKyPFgrHQZshMtF4ykUzNeOx8OEir65dHUKw8WC1nfXjb9vC"
TOKEN_FILE = Path(__file__).parent / "tumblr-tokens.json"
ACCESS_TOKEN_URL = "https://www.tumblr.com/oauth/access_token"

if len(sys.argv) != 4:
    print("Usage: python tumblr-exchange-token.py <request_token> <request_secret> <verifier>")
    sys.exit(1)

req_token, req_secret, verifier = sys.argv[1], sys.argv[2], sys.argv[3]

print(f"Exchanging verifier for access tokens...")

try:
    oauth = OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=req_token,
        resource_owner_secret=req_secret,
        verifier=verifier
    )
    r = oauth.post(ACCESS_TOKEN_URL, timeout=10)

    if r.status_code != 200:
        print(f"[FAIL] HTTP {r.status_code}: {r.text[:100]}")
        sys.exit(1)

    from urllib.parse import parse_qs
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
    print(f"[OK] Tokens saved to {TOKEN_FILE}")
    print(f"[OK] Ready to post!")

except Exception as e:
    print(f"[FAIL] {e}")
    sys.exit(1)
