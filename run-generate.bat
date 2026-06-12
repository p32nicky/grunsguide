@echo off
cd /d C:\grunssite
call npx tsx scripts/generate-articles.ts >> C:\grunssite\generate-task.log 2>&1
