# Tumblr OAuth Setup

Tumblr posting requires a one-time manual OAuth authorization.

## Quick Start

1. **Run the token getter:**
   ```
   cd C:\grunssite
   python scripts/get-tumblr-tokens.py
   ```

2. **When prompted:**
   - A browser window opens with Tumblr's authorization page
   - Click to authorize the app
   - Copy the verifier code (4-6 character code shown on the page)
   - Paste it into the terminal and press Enter

3. **Done!**
   - Tokens are saved to `scripts/tumblr-tokens.json`
   - Tumblr posting is now automated

## Troubleshooting

- **Browser doesn't open:** Copy the URL shown in terminal and visit it manually in your browser
- **No verifier code shown:** Make sure you authorized the app (click the authorize button)
- **401 errors when posting:** Tokens expired or invalid - rerun the token getter

## How it works

- `get-tumblr-tokens.py` - One-time setup to get OAuth tokens
- `post-to-tumblr.py` - Automated poster using saved tokens
- Runs every 30 minutes via Windows Task Scheduler

## Manual posting

Test posting with:
```
python scripts/post-to-tumblr.py --limit 1 --dry-run   # Preview
python scripts/post-to-tumblr.py --limit 1              # Actually post
```
