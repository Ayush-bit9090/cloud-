from flask import Flask
from threading import Thread

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

import os

# =========================
# KEEP RENDER ALIVE
# =========================

web_app = Flask('')

@web_app.route('/')
def home():
    return "Bot is running"

def run_web():
    web_app.run(host='0.0.0.0', port=10000)

Thread(target=run_web).start()

# =========================
# BOT TOKEN
# =========================

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# =========================
# SAVE FOLDER
# =========================

SAVE_FOLDER = "downloads"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✅ Bot is online!"
    )

# =========================
# SAVE FILES
# =========================

async def save_media(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message
    file = None

    if message.photo:
        file = await message.photo[-1].get_file()

    elif message.video:
        file = await message.video.get_file()

    elif message.document:
        file = await message.document.get_file()

    elif message.audio:
        file = await message.audio.get_file()

    if file:

        path = os.path.join(
            SAVE_FOLDER,
            file.file_unique_id
        )

        await file.download_to_drive(path)

        await update.message.reply_text(
            "✅ File saved!"
        )

# =========================
# RUN BOT
# =========================

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.PHOTO
        | filters.VIDEO
        | filters.Document.ALL
        | filters.AUDIO,
        save_media
    )
)

print("Bot started")

app.run_polling()
