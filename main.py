import os
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# .env ဖိုင်ကနေ Data တွေဖတ်မယ် (Koyeb မှာတင်ရင် Environment Variables ထဲထည့်ရမယ်)
load_dotenv()

API_ID = int(os.getenv("API_ID", "12345")) # my.telegram.org ကယူပါ
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
MONGO_URL = os.getenv("MONGO_URL", "your_mongodb_connection_string")
WORKER_URL = os.getenv("WORKER_URL", "https://your-worker.username.workers.dev")

# MongoDB ချိတ်ဆက်ခြင်း
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client.my_bot_db
collection = db.videos

app = Client("my_video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("မင်္ဂလာပါ! ဗီဒီယိုတစ်ခုခုပို့ပေးပါ။ ကျွန်တော် Link ထုတ်ပေးပါ့မယ်။")

@app.on_message(filters.video | filters.document)
async def handle_video(client, message):
    # Video ဖိုင်ဖြစ်မဖြစ် စစ်ဆေးမယ်
    file = message.video or message.document
    if not file.mime_type.startswith("video/"):
        return await message.reply_text("ဗီဒီယိုဖိုင်ပဲ ပို့ပေးပါ။")

    msg = await message.reply_text("Link ထုတ်ပေးနေပါပြီ... ခဏစောင့်ပါ။")

    # Telegram ရဲ့ File Path ကိုယူမယ်
    file_id = file.file_id
    file_info = await client.get_messages(message.chat.id, message.id)
    
    # ဒီနေရာမှာ telegram ကပေးတဲ့ file_path ကိုယူဖို့ bot api တိုက်ရိုက်ခေါ်ရတာမျိုးရှိနိုင်ပါတယ်
    # အလွယ်ဆုံးနည်းကတော့ file_id ကိုသုံးပြီး worker ကနေတဆင့် stream လုပ်တာပါ
    
    # MongoDB ထဲမှာ သိမ်းမယ်
    await collection.insert_one({
        "user_id": message.from_user.id,
        "file_id": file_id,
        "file_name": file.file_name or "video.mp4"
    })

    # Cloudflare Worker Link ဖန်တီးမယ်
    # မှတ်ချက် - Cloudflare Worker ဘက်မှာ file_id နဲ့ stream လုပ်မယ့် logic ပါရပါမယ်
    stream_link = f"{WORKER_URL}/{file_id}"

    await msg.edit_text(
        f"✅ **ဗီဒီယို Link ရပါပြီ!**\n\n"
        f"📂 ဖိုင်အမည်: `{file.file_name}`\n"
        f"🔗 Link: {stream_link}\n\n"
        f"⚠️ သတိပေးချက်: Link အလုပ်မလုပ်ရင် ခဏနေမှပြန်ကြိုးစားပါ။"
    )

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
