#!/usr/bin/env python3
"""
Tumblr OAuth callback catcher.
Starts a local HTTP server that captures the OAuth callback and extracts the verifier.
"""

import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import webbrowser

try:
    from requests_oauthlib import OAuth1Session
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "requests-oauthlib", "-q"])
    from requests_oauthlib import OAuth1Session

CONSUMER_KEY = "e4rMsYwSleTU0KJbBwI9zmUrU8geNqn1wydvk2xokUPBhtLzfN"
CONSUMER_SECRET = "B7QKyPFgrHQZshMtF4ykUzNeOx8OEir65dHUKw8WC1nfXjb9vC"
TOKEN_FILE = Path(__file__).parent / "tumblr-tokens.json"

REQUEST_TOKEN_URL = "https://www.tumblr.com/oauth/request_token"
AUTHORIZE_URL = "https://www.tumblr.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://www.tumblr.com/oauth/access_token"

captured_verifier = None
captured_req_token = None
captured_req_secret = None
req_token = None
req_secret = None

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global captured_verifier, captured_req_token, captured_req_secret, req_token, req_secret

        # Parse the callback URL
        query = urlparse(self.path).query
        params = parse_qs(query)

        captured_verifier = params.get('oauth_verifier', [None])[0]
        captured_req_token = params.get('oauth_token', [None])[0]
        captured_req_secret = req_secret  # Use the one from earlier

        if captured_verifier:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            html = f"""
            <html>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>Success!</h1>
            <p>Authorization complete. You can close this window.</p>
            <p style="color: green; font-weight: bold;">Verifier: {captured_verifier}</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            print(f"\n[OK] Got verifier: {captured_verifier}")
        else:
            self.send_response(400)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"No verifier in callback")

    def log_message(self, format, *args):
        pass  # Suppress logs

def main():
    global captured_verifier, req_token, req_secret

    print("Getting request token...")
    oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = oauth.post(REQUEST_TOKEN_URL, timeout=10)
    creds = parse_qs(r.content.decode())
    req_token = creds['oauth_token'][0]
    req_secret = creds['oauth_token_secret'][0]

    # SAVE request token + secret for exchange
    STATE_FILE = Path(__file__).parent / ".callback-state.json"
    STATE_FILE.write_text(json.dumps({"req_token": req_token, "req_secret": req_secret}))

    print(f"[OK] Request token: {req_token[:20]}...")

    # Start callback server
    server = HTTPServer(('127.0.0.1', 8888), CallbackHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print("[OK] Callback server listening on http://127.0.0.1:8888")

    # Build auth URL (without callback, since Tumblr doesn't use it)
    auth_url = f"{AUTHORIZE_URL}?oauth_token={req_token}"
    print(f"\n[URL] {auth_url}\n")

    print("Opening browser...")
    webbrowser.open(auth_url)

    print("Waiting for authorization (max 60 seconds)...\n")

    # Wait for callback
    import time
    for i in range(60):
        if captured_verifier:
            break
        time.sleep(1)

    server.shutdown()

    if not captured_verifier:
        print("[FAIL] Timeout - no verifier received")
        print("Manual workaround: Visit the URL above, authorize, look for the verifier code")
        return

    # Exchange for tokens
    print(f"\nExchanging verifier for access tokens...")
    try:
        # Use the saved request secret (from when we created the request token)
        oauth = OAuth1Session(
            CONSUMER_KEY,
            client_secret=CONSUMER_SECRET,
            resource_owner_key=req_token,  # Use the one we created
            resource_owner_secret=req_secret,  # Use the matching secret
            verifier=captured_verifier
        )
        r = oauth.post(ACCESS_TOKEN_URL, timeout=10)

        if r.status_code != 200:
            print(f"[FAIL] HTTP {r.status_code}")
            return

        creds = parse_qs(r.content.decode())
        user_token = creds['oauth_token'][0]
        user_secret = creds['oauth_token_secret'][0]

        tokens = {
            "consumer_key": CONSUMER_KEY,
            "consumer_secret": CONSUMER_SECRET,
            "user_token": user_token,
            "user_secret": user_secret
        }

        TOKEN_FILE.write_text(json.dumps(tokens, indent=2))
        print(f"[OK] Tokens saved!")
        print(f"[OK] Ready to post!")

    except Exception as e:
        print(f"[FAIL] {e}")

if __name__ == "__main__":
    main()
