# One Man Support

Support for indie makers who'd rather ship than manage tickets.

You ship apps. You don't have a support team. You don't need Zendesk, Intercom, or a ticketing system with 47 features you'll never use. You just need to know when a user has a problem and reply fast.

This is a single Python file that turns your Telegram into a helpdesk. Users message the bot, you get it on your phone with context (which app, who sent it), you reply inline, they get your reply back. No dashboard. No login. No monthly fee. Just your phone.

## Why

I ship 7 apps solo. I tried support emails — they get buried. I tried forms — nobody fills them. I tried third-party tools — they cost money and add complexity for something that should be simple.

What I actually do when a user has a problem is pick up my phone and reply. So I built a bot that fits that workflow. One Telegram bot handles all my apps. Each app gets a deep link. Users tap "Contact Support" in the app or on the landing page, type their message, and I reply from my couch.

It's been running in production across all my apps. It works.

## How it works

```
User opens bot → picks app → sends message
                                    ↓
                          You get it in your Telegram
                          (with app name + user info)
                                    ↓
                          You reply to that message
                                    ↓
                          User gets your reply back
```

## Features

- **Multi-app** — one bot, all your apps. Users pick which app they need help with
- **Deep links** — `t.me/YourBot?start=app_myapp` skips the picker, drop it in your app or website
- **Media** — users can send screenshots, videos, voice messages, documents, stickers
- **Reply with anything** — text, photos, voice — whatever you reply with goes back to them
- **Persistent** — survives restarts, remembers which user messaged about which app
- **Single file** — one Python file, no database, no framework, no config files
- **Zero cost** — Telegram bots are free, hosting is a $5 VPS or even a Raspberry Pi

## Setup

Takes about 3 minutes.

### 1. Create a Telegram bot

Message [@BotFather](https://t.me/BotFather) on Telegram:
- Send `/newbot`
- Pick a name and username
- Copy the token

### 2. Get your chat ID

Message [@userinfobot](https://t.me/userinfobot) on Telegram — it replies with your user ID.

### 3. Add your apps

Edit the `APPS` dict in `bot.py`:

```python
APPS = {
    "myapp":    {"name": "My App",    "emoji": "📱"},
    "tracker":  {"name": "Tracker",   "emoji": "📊"},
    "notes":    {"name": "Notes Pro", "emoji": "📝"},
    "other":    {"name": "Other",     "emoji": "💬"},
}
```

### 4. Run

```bash
pip install -r requirements.txt

BOT_TOKEN=xxx ADMIN_CHAT_ID=xxx python3 bot.py
```

Or with a `.env` file:

```bash
cp .env.example .env
# edit .env with your values

export $(cat .env | xargs) && python3 bot.py
```

### 5. Keep it running

With PM2:
```bash
BOT_TOKEN=xxx ADMIN_CHAT_ID=xxx pm2 start bot.py --name support --interpreter python3
pm2 save
```

With systemd:
```bash
# /etc/systemd/system/support-bot.service
[Unit]
Description=One Man Support Bot

[Service]
ExecStart=/usr/bin/python3 /path/to/bot.py
Environment=BOT_TOKEN=xxx
Environment=ADMIN_CHAT_ID=xxx
Restart=always

[Install]
WantedBy=multi-user.target
```

## Adding to your app or website

Drop a "Contact Support" button that opens:

```
https://t.me/YourBot?start=app_myapp
```

This deep link skips the app picker and goes straight to messaging. Put it in your app's settings screen, your landing page footer, or your App Store description.

Run `/apps` in the bot to see all your deep links.

## Commands

| Command | Description |
|---------|-------------|
| `/start` | App picker (or direct entry via deep link) |
| `/apps` | List all apps with their deep links |

## Who this is for

- Indie developers shipping multiple apps
- Solo makers who want user feedback without infrastructure
- Anyone who thinks support tools shouldn't cost more than the apps they support

## License

MIT
