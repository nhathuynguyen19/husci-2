#!/bin/bash
echo "🔃 Starting FastAPI and Discord bot..."

# Chạy FastAPI ở nền
python3 main_api.py &

# Chạy Discord bot ở foreground để giữ container sống
python3 main_bot.py
