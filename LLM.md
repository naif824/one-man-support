# LLM Guide: One Man Support

Use this file when an AI assistant is working on this repo.

## Purpose

One Man Support is a minimal Telegram-based support bot for indie makers.

Core flow:

1. User opens a Telegram deep link from an app.
2. Bot stores which app the user needs help with.
3. User sends a message/media.
4. Bot forwards it to the admin with app/user context.
5. Admin replies inline.
6. Bot routes the reply back to the user.

## Product Constraints

- Keep the project simple.
- Preserve the single-file bot experience where possible.
- Avoid adding a web dashboard or database unless explicitly requested.
- Do not commit real bot tokens, chat IDs, or production data.
- `.env` and `data/` must stay ignored.

## Important Files

- `bot.py`: main Telegram bot.
- `apps.example.json`: example app config.
- `.env.example`: required environment variables.
- `ecosystem.config.cjs`: PM2 example.
- `Dockerfile` and `docker-compose.yml`: Docker example.
- `test_bot.py`: helper tests.

## Validation

Run:

```bash
python3 -m unittest -v
python3 -m py_compile bot.py
```

## Design Principle

This is for solo builders who prefer replying from Telegram over managing a support dashboard.
