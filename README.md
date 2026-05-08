# One Man Support

**A tiny Telegram helpdesk for indie makers, solo developers, and small app teams.**

One Man Support turns one Telegram bot into support for all your apps. Users tap **Contact Support**, send a message, and you reply from Telegram. No dashboard, no login, no monthly helpdesk bill.

## Why

Most solo developers do not need Zendesk, Intercom, or a full ticketing system. They need a simple way to know when a user has a problem and reply quickly.

Email gets buried. Forms feel cold. In-app chat SDKs add weight and cost. Telegram already gives you instant notifications, rich media, voice messages, and replies from your phone.

## How It Works

```text
User taps Contact Support
        ↓
Telegram bot opens with app context
        ↓
User sends text, screenshot, video, voice, or file
        ↓
You receive it in Telegram with app name + user info
        ↓
You reply inline
        ↓
User gets your reply
```

## Features

- **Multi-app support**: one bot handles all your apps.
- **Deep links**: `t.me/YourBot?start=app_myapp` opens support for a specific app.
- **Rich media**: screenshots, videos, voice messages, documents, and stickers.
- **Reply routing**: reply to the forwarded message and the user gets your response.
- **Persistent state**: remembers user app context across restarts.
- **Simple deployment**: one Python file and one dependency.
- **Configurable apps**: edit `bot.py` or use `APP_CONFIG_FILE=apps.example.json`.
- **Zero SaaS cost**: host it on your own server, VPS, Raspberry Pi, Docker, or PM2.

## Install

```bash
git clone https://github.com/naif824/one-man-support.git
cd one-man-support
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```bash
BOT_TOKEN=your-telegram-bot-token
ADMIN_CHAT_ID=your-telegram-user-id
APP_CONFIG_FILE=apps.example.json
```

Run:

```bash
export $(cat .env | xargs)
python3 bot.py
```

## Setup

### 1. Create a Telegram bot

Message [@BotFather](https://t.me/BotFather):

```text
/newbot
```

Choose a name and username, then copy the bot token.

### 2. Get your Telegram user ID

Message [@userinfobot](https://t.me/userinfobot). It replies with your numeric user ID.

### 3. Configure your apps

Use `apps.example.json`:

```json
{
  "myapp": {
    "name": "My App",
    "emoji": "📱"
  },
  "other": {
    "name": "Other",
    "emoji": "💬"
  }
}
```

The key becomes your deep-link slug:

```text
https://t.me/YourBot?start=app_myapp
```

## Deployment

### PM2

```bash
pm2 start ecosystem.config.cjs
pm2 save
```

### Docker

```bash
cp .env.example .env
docker compose up -d --build
```

### systemd

Copy `one-man-support.service.example` to your server, edit paths and environment values, then:

```bash
sudo systemctl enable --now one-man-support
```

## Bot Commands

| Command | Description |
| --- | --- |
| `/start` | Choose an app or enter through a deep link |
| `/apps` | Show configured app deep links |

## Add To Your App

Use a normal link:

```text
https://t.me/YourBot?start=app_myapp
```

Good places:

- app settings screen
- help page
- website footer
- App Store / Play Store support URL
- onboarding email

## Who It Is For

- indie iOS and Android developers
- solo SaaS builders
- makers with multiple small apps
- small teams who live in Telegram
- people who want support without support software

## What It Is Not

One Man Support is intentionally small. It is not a full CRM, ticketing suite, analytics dashboard, or team inbox.

If you need assignments, SLAs, macros, reports, and a web dashboard, use a real helpdesk. If you want users to reach you fast and you want to reply from your phone, this is enough.

## Test

```bash
python3 -m unittest -v
python3 -m py_compile bot.py
```

## Security Notes

- Keep `BOT_TOKEN` private.
- Keep `.env` out of git.
- Use a private `ADMIN_CHAT_ID`.
- Run one bot per trusted owner or forward to a private Telegram group.
- User messages and routing state are stored under `data/`.

## License

MIT
