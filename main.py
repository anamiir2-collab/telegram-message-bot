import os
import asyncio
from telegram import Bot
from pymongo import MongoClient

# 1. قراءة البيانات من GitHub Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
MESSAGE_TEXT = os.getenv("MESSAGE_TEXT", "رسالة تذكيرية جديدة! 📢")

async def send_broadcast():
    if not TELEGRAM_TOKEN or not MONGO_URI:
        print("❌ خطأ: لم يتم العثور على TELEGRAM_TOKEN أو MONGO_URI في Secrets!")
        return

    # الاتصال ببوت التليجرام
    bot = Bot(token=TELEGRAM_TOKEN)
    
    # الاتصال بقاعدة بيانات MongoDB Atlas
    client = MongoClient(MONGO_URI)
    db = client["telegram_bot_db"]
    users_collection = db["users"]

    # جلب جميع المستخدمين من الداتابيز
    users = list(users_collection.find({}, {"_id": 0, "chat_id": 1}))
    
    if not users:
        print("⚠️ لم يتم العثور على أي مستخدمين داخل قاعدة البيانات!")
        return

    print(f"📡 جاري إرسال الرسالة إلى {len(users)} مستخدم...")

    success_count = 0
    fail_count = 0

    # التكرار على كل مستخدم وإرسال الرسالة له
    for user in users:
        chat_id = user.get("chat_id")
        if chat_id:
            try:
                await bot.send_message(chat_id=chat_id, text=MESSAGE_TEXT)
                success_count += 1
                await asyncio.sleep(0.05)  # تفادي حظر تليجرام للرسائل السريعة
            except Exception as e:
                print(f"❌ فشل الإرسال إلى {chat_id}: {e}")
                fail_count += 1

    print(f"✅ اكتملت الإذاعة!\nنجاح: {success_count} | فشل: {fail_count}")

if __name__ == "__main__":
    asyncio.run(send_broadcast())
