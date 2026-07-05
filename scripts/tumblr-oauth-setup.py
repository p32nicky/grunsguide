#!/usr/bin/env python3
"""
Interactive Tumblr OAuth setup.
Gets user tokens and saves them for posting.
"""

import json
from pathlib import Path

try:
    import pytumblr
except ImportError:
    print("Installing pytumblr...")
    import subprocess
    subprocess.check_call(["pip", "install", "pytumblr", "-q"])
    import pytumblr

CONSUMER_KEY = "0DSLOcnqeLENlBKT1FWYU6gNya7O9ua7zJZi7d1Qn6LL8WpHj9"
CONSUMER_SECRET = "oTWpPau5X5VvxAjv6AxhcWuvwenQQNRIIGIojhoj5dn6PXHXL0"
TOKEN_FILE = Path(__file__).parent / "tumblr-tokens.json"

def main():
    print("Tumblr OAuth Setup")
    print("=" * 50)

    # Step 1: Get request token
    client = pytumblr.TumblrRestClient(CONSUMER_KEY, CONSUMER_SECRET)
    auth_url = client.get_authorize_url(CONSUMER_KEY, CONSUMER_SECRET)

    print(f"\n1. Visit this URL to authorize:")
    print(f"   {auth_url}\n")

    input("Press Enter after authorizing...")

    # Step 2: Get verifier from user
    verifier = input("Enter the verifier code from the page: ").strip()

    # Step 3: Get access tokens
    try:
        user_token, user_secret = client.get_access_token(CONSUMER_KEY, CONSUMER_SECRET, verifier)

        tokens = {
            "user_token": user_token,
            "user_secret": user_secret,
            "consumer_key": CONSUMER_KEY,
            "consumer_secret": CONSUMER_SECRET
        }

        TOKEN_FILE.write_text(json.dumps(tokens, indent=2))
        print(f"\n✓ Tokens saved to {TOKEN_FILE}")
        print("You can now post to Tumblr!")
    except Exception as e:
        print(f"\nFailed to get tokens: {e}")
        print("Try again or check the verifier code.")

if __name__ == "__main__":
    main()
