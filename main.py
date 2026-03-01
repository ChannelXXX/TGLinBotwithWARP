import os
import asyncio
from pyrogram import Client, filters
from dotenv import load_dotenv

load_dotenv()

app = Client(
    "render_bot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

# Local Server သို့ ချိတ်ဆက်ရန် အရေးကြီးသောအပိုင်း
app.api_server = type("ApiServer", (), {
    "base": "http://localhost:8081/bot",
    "file": "http://localhost:8081/file/bot"
})()

@app.on_message((filters.video | filters.document) & filters.private)
async def handle_video(client, message):
    file = message.video or message.document
    status = await message.reply_text("⏳ **Generating 2GB Support Link...**")
    
    try:
        # Local API ကြောင့် 20MB ထက်ကြီးလည်း file_path ရပါပြီ
        file_info = await client.get_file(file.file_id)
        
        worker_url = os.getenv("WORKER_URL").rstrip('/')
        stream_link = f"{worker_url}/{file.file_id}?path={file_info.file_path}"
        
        await status.edit_text(f"✅ **Success!**\n\n🔗 `{stream_link}`")
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")

app.run()
