@echo off
cd /d C:\grunssite
python scripts/substack-post.py --limit 1 >> C:\grunssite\substack-task.log 2>&1
