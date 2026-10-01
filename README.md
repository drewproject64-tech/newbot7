# SB24TimeBot

Production-ready Telegram time utility bot for @SB24TimeBot.

## Main functions

Exactly three primary functions:
- Current Time
- World Clock
- Time Zone Converter

No external links, redirects, payments, gambling, betting, casino, prize, or real-money gaming features.

## Setup

Python 3.12+ is recommended.

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export BOT_TOKEN="YOUR_BOT_TOKEN"
python -m app.main
```

On Windows PowerShell:
```
$env:BOT_TOKEN="YOUR_BOT_TOKEN"
python -m app.main
```

## Render

The included render.yaml creates a Python background worker. Set the BOT_TOKEN environment variable in Render.

## Bot profile

Name, username, About text, Description, and welcome message are centralized in app/config.py. On startup the bot applies the supported profile settings through Telegram Bot API methods.

Telegram Ads moderation is independent of this application; this project is designed to align the destination with its actual functionality, but approval cannot be guaranteed.
