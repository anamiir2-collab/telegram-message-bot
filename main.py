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

    # الاتصال بقاعدة بيانات MongoDB Atlas
    try:
        client = MongoClient(MONGO_URI)
        db = client["telegram_bot_db"]
        users_collection = db["users"]
    except Exception as e:
        print(f"❌ خطأ في الاتصال بقاعدة البيانات MongoDB: {e}")
        return

    # جلب جميع المستخدمين من الداتابيز
    users = list(users_collection.find({}, {"_id": 0, "chat_id": 1}))
    
    if not users:
        print("⚠️ لم يتم العثور على أي مستخدمين داخل قاعدة البيانات!")
        return

    print(f"📡 تم العثور على {len(users)} مستخدم. جاري الاتصال بتليجرام...")

    # استخدام Context Manager لتهيئة البوت وإغلاقه بشكل صحيح تلقائياً
    async with Bot(token=TELEGRAM_TOKEN) as bot:
        success_count = 0
        fail_count = 0

        for user in users:
            raw_chat_id = user.get("chat_id")
            if raw_chat_id:
                try:
                    # تحويل الـ chat_id لرقم صحيح
                    chat_id = int(str(raw_chat_id).strip())
                    
                    # إرسال الرسالة
                    await bot.send_message(chat_id=chat_id, text=MESSAGE_TEXT)
                    print(f"✅ تم الإرسال بنجاح إلى: {chat_id}")
                    success_count += 1
                    await asyncio.sleep(0.05)
                except Exception as e:
                    print(f"❌ فشل الإرسال إلى {raw_chat_id} | السبب: {e}")
                    fail_count += 1

        print(f"\n📊 اكتملت الإذاعة!\nنجاح: {success_count} | فشل: {fail_count}")

if __name__ == "__main__":
    asyncio.run(send_broadcast())
