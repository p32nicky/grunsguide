@echo off
cd /d C:\grunssite
python scripts/post-to-reddit.py --limit 2 >> C:\grunssite\reddit-task.log 2>&1
