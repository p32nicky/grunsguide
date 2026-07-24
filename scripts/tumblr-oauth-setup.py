#!/usr/bin/env python3
"""
Interactive Tumblr OAuth setup.
Gets user tokens and saves them for posting.
"""

import json
import webbrowser
from pathlib import Path
from urllib.parse import parse_qs, urlparse

try:
    from requests_oauthlib import OAuth1Session
except ImportError:
    print("Installing requests-oauthlib...")
    import subprocess
    subprocess.check_call(["pip", "install", "requests-oauthlib", "-q"])
    from requests_oauthlib import OAuth1Session

CONSUMER_KEY = "e4rMsYwSleTU0KJbBwI9zmUrU8geNqn1wydvk2xokUPBhtLzfN"
CONSUMER_SECRET = "B7QKyPFgrHQZshMtF4ykUzNeOx8OEir65dHUKw8WC1nfXjb9vC"
TOKEN_FILE = Path(__file__).parent / "tumblr-tokens.json"

REQUEST_TOKEN_URL = "https://www.tumblr.com/oauth/request_token"
AUTHORIZE_URL = "https://www.tumblr.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://www.tumblr.com/oauth/access_token"

def main():
    print("Tumblr OAuth Setup")
    print("=" * 50)

    # Step 1: Get request token
    oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET)

    try:
        r = oauth.post(REQUEST_TOKEN_URL)
        credentials = parse_qs(r.content.decode())
        resource_owner_key = credentials.get('oauth_token')[0]
        resource_owner_secret = credentials.get('oauth_token_secret')[0]
    except Exception as e:
        print(f"Failed to get request token: {e}")
        return

    # Step 2: Direct user to authorize
    auth_url = f"{AUTHORIZE_URL}?oauth_token={resource_owner_key}"
    print(f"\n1. Visit this URL to authorize:")
    print(f"   {auth_url}\n")
    print("Opening browser...")
    webbrowser.open(auth_url)

    input("Press Enter after authorizing...")

    # Step 3: Get verifier from user
    verifier = input("Enter the verifier code from the page: ").strip()

    # Step 4: Get access tokens
    try:
        oauth = OAuth1Session(
            CONSUMER_KEY,
            client_secret=CONSUMER_SECRET,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier
        )
        r = oauth.post(ACCESS_TOKEN_URL)
        credentials = parse_qs(r.content.decode())
        user_token = credentials.get('oauth_token')[0]
        user_secret = credentials.get('oauth_token_secret')[0]

        tokens = {
            "user_token": user_token,
            "user_secret": user_secret,
            "consumer_key": CONSUMER_KEY,
            "consumer_secret": CONSUMER_SECRET
        }

        TOKEN_FILE.write_text(json.dumps(tokens, indent=2))
        print(f"\nTokens saved to {TOKEN_FILE}")
        print("You can now post to Tumblr!")
    except Exception as e:
        print(f"\nFailed to get access tokens: {e}")
        print("Try again or check the verifier code.")

if __name__ == "__main__":
    main()
