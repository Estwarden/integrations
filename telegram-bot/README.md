# EstWarden Telegram Bot

Query Baltic threat data from Telegram.

## Commands

| Command | What |
|---------|------|
| `/start` | Welcome + help |
| `/threat` | Current threat level + CTI score |
| `/report` | Today's intelligence summary |
| `/narr` | Active narrative classifications |
| `/camps` | Detected influence campaigns |

## Run

```bash
pip install python-telegram-bot
TELEGRAM_BOT_TOKEN=your-token python3 bot.py
```

## Docker

```bash
docker run -e TELEGRAM_BOT_TOKEN=your-token \
  python:3.12-slim sh -c \
  "pip install python-telegram-bot && python3 /app/bot.py"
```
