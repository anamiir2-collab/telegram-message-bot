import os
import random
import telebot

# جلب بيانات البوت والـ IDs من الـ Secrets
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
CHANNEL_CHAT_ID = os.environ.get('CHANNEL_CHAT_ID')

# لو عندك أشخاص تانين عايز يوصلهم الخاص، حط الـ IDs بتاعتهم هنا مفصولة بفواصل
# مثال في الـ Secret: 8979274360,123456789,987654321
USER_IDS = os.environ.get('USER_IDS', '')

bot = telebot.TeleBot(BOT_TOKEN)

def send_random_message():
    # 1. قراءة الرسائل العشوائية من ملف messages.txt
    if not os.path.exists('messages.txt'):
        print("ملف messages.txt غير موجود!")
        return

    with open('messages.txt', 'r', encoding='utf-8') as f:
        messages = [line.strip() for line in f if line.strip()]

    if not messages:
        print("ملف messages.txt فارغ!")
        return

    random_msg = random.choice(messages)

    # 2. تجميع كل الـ IDs اللي هنبعتلهم في قائمة واحدة بدون تكرار
    recipients = set()

    # إضافة شاتك الشخصي الأساسي
    if CHAT_ID:
        recipients.add(CHAT_ID.strip())

    # إضافة القناة أو الجروب
    if CHANNEL_CHAT_ID:
        recipients.add(CHANNEL_CHAT_ID.strip())

    # إضافة قائمة الأشخاص الإضافيين (لو موجودة في الـ Secret اللي اسمه USER_IDS)
    if USER_IDS:
        for uid in USER_IDS.split(','):
            if uid.strip():
                recipients.add(uid.strip())

    # 3. إرسال الرسالة لكل القائمة
    print(f"جاري إرسال الرسالة إلى {len(recipients)} مستقبلين...")
    for target_id in recipients:
        try:
            bot.send_message(target_id, random_msg)
            print(f"تم الإرسال بنجاح إلى: {target_id}")
        except Exception as e:
            print(f"فشل الإرسال إلى {target_id}: {e}")

if __name__ == '__main__':
    send_random_message()
