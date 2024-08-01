import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# استبدل هذا بالتوكن الخاص بك
TOKEN = '7308571255:AAEya15VJIyWaVnjyP7SZYthTTs3LhB_GqY'
# استبدل هذا بمعرف المشرف الخاص بك
ADMIN_CHAT_ID = '6953783111'
# استبدل هذا بمعرف المجموعة الخاصة بك
GROUP_ID = '@mahala25'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! أرسل رسالتك وسيقوم المطور بمراجعتها للنشر في المجموعة.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # إعداد معلومات المستخدم
    user_name = message.from_user.first_name
    user_username = message.from_user.username
    user_id = message.from_user.id

    # رسالة إلى المشرف مع أزرار الموافقة أو الرفض
    markup = InlineKeyboardMarkup()
    approve_button = InlineKeyboardButton("موافقة", callback_data=f"approve:{user_id}:{message.message_id}")
    reject_button = InlineKeyboardButton("رفض", callback_data=f"reject:{user_id}:{message.message_id}")
    markup.add(approve_button, reject_button)

    # إرسال الرسالة إلى المشرف مع اسم المستخدم واسم المستخدم الفعلي
    bot.send_message(
        ADMIN_CHAT_ID, 
        f"رسالة من {user_name} (@{user_username}):\n{message.text}", 
        reply_markup=markup
    )
    bot.reply_to(message, "تم إرسال رسالتك إلى المطور للمراجعة.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('approve') or call.data.startswith('reject'))
def handle_callback_query(call):
    action, user_id, message_id = call.data.split(':')
    user_id = int(user_id)
    message_id = int(message_id)

    if action == 'approve':
        try:
            # نشر الرسالة في المجموعة
            bot.forward_message(GROUP_ID, user_id, message_id)
            bot.send_message(user_id, "تمت الموافقة على رسالتك ونشرها في المجموعة.")
            bot.answer_callback_query(call.id, "تمت الموافقة على الرسالة ونشرها في المجموعة.")
        except telebot.apihelper.ApiTelegramException as e:
            bot.send_message(ADMIN_CHAT_ID, f"خطأ: لا يمكن نشر الرسالة في المجموعة. تأكد من أن البوت عضو في المجموعة ولديه الأذونات اللازمة. تفاصيل الخطأ: {e}")
    elif action == 'reject':
        bot.send_message(user_id, "تم رفض رسالتك.")
        bot.answer_callback_query(call.id, "تم رفض الرسالة.")

# تشغيل البوت باستخدام polling
bot.remove_webhook()
bot.polling(none_stop=True)
