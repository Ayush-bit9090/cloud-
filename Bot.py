from pyrogram import Client, filters, idle
import asyncio
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

SAVE_FOLDER = "downloads"
os.makedirs(SAVE_FOLDER, exist_ok=True)

app = Client(
    "storage_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("✅ Bot is online!")

@app.on_message(filters.private)
async def save_file(client, message):

    if (
        message.photo
        or message.video
        or message.document
        or message.audio
    ):

        await message.download(
            file_name=SAVE_FOLDER
        )

        await message.reply_text("✅ File saved!")

async def main():
    await app.start()
    print("Bot started")
    await idle()

asyncio.run(main())
