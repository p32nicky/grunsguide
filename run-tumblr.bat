@echo off
cd /d C:\grunssite
pip install requests requests-oauthlib -q
python scripts/post-to-tumblr.py --limit 1 >> C:\grunssite\tumblr-task.log 2>&1
