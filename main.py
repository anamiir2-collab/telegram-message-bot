import os
import json
import requests

# محاولة جلب التوكن من متغيّرات البيئة (GitHub Secrets) للحماية
# وفي حال عدم وجوده، يتم استخدام التوكن الافتراضي
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8948314451:AAFugRCSClG8vA4EeHFZDfeoRTFNvCuXfw0")

def load_users():
    """تحميل قائمة IDs المشتركين من ملف users.json"""
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
            return users
    except FileNotFoundError:
        print("⚠️ ملف users.json غير موجود! سيتم إنشاء قائمة فارغة.")
        return []
    except json.JSONDecodeError:
        print("❌ خطأ في تنسيق ملف users.json! تأكد من كتابة الـ IDs بشكل صحيح.")
        return []

def load_messages():
    """تحميل الرسائل من ملف messages.txt"""
    try:
        with open('messages.txt', 'r', encoding='utf-8') as f:
            # قراءة الأسطر وتجاهل الأسطر الفارغة
            lines = [line.strip() for line in f.readlines() if line.strip()]
            return lines
    except FileNotFoundError:
        print("❌ ملف messages.txt غير موجود!")
        return []
    except Exception as e:
        print(f"❌ خطأ أثناء قراءة ملف الرسائل: {e}")
        return []

def send_to_all(message, user_ids):
    """إرسال الرسالة لجميع المستخدمين المسجلين في القائمة"""
    if not user_ids:
        print("⚠️ لا يوجد مستخدمين لإرسال الرسالة لهم.")
        return

    success_count = 0
    fail_count = 0

    for user_id in user_ids:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": user_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            res_data = response.json()

            if response.status_code == 200 and res_data.get("ok"):
                print(f"✅ تم الإرسال بنجاح للمستخدم: {user_id}")
                success_count += 1
            else:
                error_desc = res_data.get("description", "خطأ غير معروف")
                print(f"❌ فشل الإرسال للمستخدم {user_id}: {error_desc}")
                fail_count += 1

        except Exception as e:
            print(f"❌ حدث خطأ أثناء الاتصال مع {user_id}: {e}")
            fail_count += 1

    print("-" * 30)
    print(f"📊 النتائج الإجمالية: تم إرسال {success_count} رسالة بنجاح | فشل {fail_count}")

if __name__ == "__main__":
    messages = load_messages()
    users = load_users()

    if not messages:
        print("❌ لم يتم العثور على أي رسائل لإرسالها.")
    else:
        # إرسال السطر الأول أو أول رسالة من الملف
        message_to_send = messages[0]
        print(f"📤 جاري بدء الإرسال للرسالة التالية:\n\"{message_to_send}\"\n")
        send_to_all(message_to_send, users)
