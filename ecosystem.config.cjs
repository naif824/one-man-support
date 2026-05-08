module.exports = {
  apps: [
    {
      name: "one-man-support",
      script: "bot.py",
      interpreter: "python3",
      env: {
        BOT_TOKEN: "your-telegram-bot-token",
        ADMIN_CHAT_ID: "your-telegram-user-id",
        APP_CONFIG_FILE: "apps.example.json"
      },
      time: true,
      max_memory_restart: "256M"
    }
  ]
};
