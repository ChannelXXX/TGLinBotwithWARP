import os
from pyrogram import Client, filters
from dotenv import load_dotenv

load_dotenv()

# Environment Variables များကို စစ်ဆေးခြင်း
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    print("❌ Error: API_ID, API_HASH or BOT_TOKEN is missing in Environment Variables!")
    # Render variables မထည့်ရသေးရင် ပိတ်မသွားအောင် ခဏစောင့်ခိုင်းမယ်
    import time
    time.sleep(3600)

app = Client(
    "render_bot",
    api_id=int(API_ID),
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Local API ချိတ်ဆက်မှု
app.api_server = type("ApiServer", (), {
    "base": "http://localhost:8081/bot",
    "file": "http://localhost:8081/file/bot"
})()

@app.on_message((filters.video | filters.document) & filters.private)
async def handle_video(client, message):
    file = message.video or message.document
    status = await message.reply_text("⏳ **Generating 2GB Support Link...**")
    try:
        file_info = await client.get_file(file.file_id)
        worker_url = os.getenv("WORKER_URL", "").rstrip('/')
        stream_link = f"{worker_url}/{file.file_id}?path={file_info.file_path}"
        await status.edit_text(f"✅ **Success!**\n\n🔗 `{stream_link}`")
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")

print("🚀 Bot is starting with Local API...")
app.run()
