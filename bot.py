"""
One Man Support — Route all your app support to your Telegram.
Users message the bot, you reply inline, they get the reply back.

Run: BOT_TOKEN=xxx ADMIN_CHAT_ID=xxx python3 bot.py
"""

import json
import os
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", "0"))

DATA_DIR = Path(__file__).parent / "data"
SESSIONS_FILE = DATA_DIR / "sessions.json"
FORWARDED_FILE = DATA_DIR / "forwarded.json"

# ── Configure your apps here ──────────────────────────────────
APPS = {
    "myapp":  {"name": "My App",  "emoji": "📱"},
    "other":  {"name": "Other",   "emoji": "💬"},
}
# ──────────────────────────────────────────────────────────────


def load_json(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


# Persistent state
sessions = load_json(SESSIONS_FILE)   # {user_id: {"app": "myapp", "name": "John"}}
forwarded = load_json(FORWARDED_FILE) # {admin_msg_id: user_chat_id}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args

    # Deep link: /start app_myapp
    if args and args[0].startswith("app_"):
        app_key = args[0].replace("app_", "")
        if app_key in APPS:
            sessions[str(user.id)] = {"app": app_key, "name": user.first_name}
            save_json(SESSIONS_FILE, sessions)
            app = APPS[app_key]
            await update.message.reply_text(
                f"Hi {user.first_name}! You're contacting support for {app['emoji']} {app['name']}.\n\n"
                f"Type your message and I'll get back to you soon."
            )
            return

    # No deep link — show app picker
    keyboard = []
    row = []
    for key, app in APPS.items():
        row.append(InlineKeyboardButton(f"{app['emoji']} {app['name']}", callback_data=f"pick_{key}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    current = sessions.get(str(user.id))
    hint = ""
    if current:
        cur_app = APPS.get(current["app"], APPS["other"])
        hint = f"\n\nCurrent app: {cur_app['emoji']} {cur_app['name']}"

    await update.message.reply_text(
        f"Hi {user.first_name}!\n\nChoose your app:{hint}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def pick_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    app_key = query.data.replace("pick_", "")
    if app_key not in APPS:
        return

    user = query.from_user
    sessions[str(user.id)] = {"app": app_key, "name": user.first_name}
    save_json(SESSIONS_FILE, sessions)
    app = APPS[app_key]

    await query.edit_message_text(f"{app['emoji']} {app['name']}\n\nType your message now.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message
    uid = str(user.id)

    if uid not in sessions:
        await message.reply_text("Please choose an app first: /start")
        return

    session = sessions[uid]
    app = APPS.get(session["app"], APPS["other"])

    header = (
        f"**{app['emoji']} {app['name']}**\n"
        f"**From:** {user.first_name} (@{user.username or 'no username'})\n"
        f"**User ID:** `{user.id}`\n\n"
    )

    # Handle different message types
    if message.text:
        admin_msg = await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=header + f"{message.text}",
            parse_mode="Markdown"
        )
    elif message.photo:
        admin_msg = await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=message.photo[-1].file_id,
            caption=header + (message.caption or "(photo)"),
            parse_mode="Markdown"
        )
    elif message.video:
        admin_msg = await context.bot.send_video(
            chat_id=ADMIN_CHAT_ID,
            video=message.video.file_id,
            caption=header + (message.caption or "(video)"),
            parse_mode="Markdown"
        )
    elif message.document:
        admin_msg = await context.bot.send_document(
            chat_id=ADMIN_CHAT_ID,
            document=message.document.file_id,
            caption=header + (message.caption or "(file)"),
            parse_mode="Markdown"
        )
    elif message.voice:
        admin_msg = await context.bot.send_voice(
            chat_id=ADMIN_CHAT_ID,
            voice=message.voice.file_id,
            caption=header + "(voice)",
            parse_mode="Markdown"
        )
    elif message.sticker:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=header + "(sticker)",
            parse_mode="Markdown"
        )
        admin_msg = await context.bot.send_sticker(
            chat_id=ADMIN_CHAT_ID,
            sticker=message.sticker.file_id,
        )
    else:
        admin_msg = await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=header + "(unsupported message type)",
            parse_mode="Markdown"
        )

    forwarded[str(admin_msg.message_id)] = user.id
    save_json(FORWARDED_FILE, forwarded)

    await message.reply_text("Message sent! I'll reply soon.")


async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """When you reply to a forwarded message, it goes back to the user."""
    message = update.message

    if message.chat_id != ADMIN_CHAT_ID:
        return
    if not message.reply_to_message:
        return

    replied_to_id = str(message.reply_to_message.message_id)
    if replied_to_id not in forwarded:
        await message.reply_text("Can't find original user for this message.")
        return

    user_id = forwarded[replied_to_id]

    try:
        if message.text:
            await context.bot.send_message(chat_id=user_id, text=message.text)
        elif message.photo:
            await context.bot.send_photo(
                chat_id=user_id,
                photo=message.photo[-1].file_id,
                caption=message.caption or ""
            )
        elif message.voice:
            await context.bot.send_voice(chat_id=user_id, voice=message.voice.file_id)
        elif message.document:
            await context.bot.send_document(
                chat_id=user_id,
                document=message.document.file_id,
                caption=message.caption or ""
            )
        elif message.video:
            await context.bot.send_video(
                chat_id=user_id,
                video=message.video.file_id,
                caption=message.caption or ""
            )
        else:
            await context.bot.send_message(chat_id=user_id, text="(reply)")
        await message.reply_text("Reply sent.")
    except Exception as e:
        await message.reply_text(f"Failed to send: {e}")


async def apps_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all supported apps with their deep links."""
    bot_info = await context.bot.get_me()
    bot_username = bot_info.username
    lines = ["**Supported Apps:**\n"]
    for key, app in APPS.items():
        if key != "other":
            lines.append(f"  {app['emoji']} {app['name']} — `t.me/{bot_username}?start=app_{key}`")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


def main():
    if not TOKEN:
        print("Set BOT_TOKEN environment variable")
        return
    if not ADMIN_CHAT_ID:
        print("Set ADMIN_CHAT_ID environment variable")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("apps", apps_command))
    app.add_handler(CallbackQueryHandler(pick_app, pattern="^pick_"))

    app.add_handler(MessageHandler(
        filters.Chat(ADMIN_CHAT_ID) & filters.REPLY,
        handle_admin_reply
    ))

    app.add_handler(MessageHandler(
        ~filters.COMMAND & ~filters.Chat(ADMIN_CHAT_ID),
        handle_message
    ))

    print("One Man Support is running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
