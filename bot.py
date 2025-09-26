import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = '8427974527:AAGojt9xvZq4aN1xP1595_fUTLhaRaG3iPQ'

# دیکشنری ابجد کبیر (تصحیح شده - حمزه حذف شد)
ABJAD_KABIR = {
    'ا': 1, 'آ': 1, 'أ': 1, 'إ': 1,  # حمزه حذف شد
    'ب': 2, 'پ': 2,
    'ج': 3, 'چ': 3,
    'د': 4,
    'ه': 5, 'ة': 5,
    'و': 6,
    'ز': 7, 'ژ': 7,
    'ح': 8,
    'ط': 9,  # ط فقط 9 هست - اصلاح شد
    'ی': 10, 'ي': 10, 'ئ': 10,  # ئ هم ی حساب میشه
    'ک': 20, 'ك': 20, 'گ': 20,  # گ اضافه شد
    'ل': 30,
    'م': 40,
    'ن': 50,
    'س': 60,
    'ع': 70,
    'ف': 80,
    'ص': 90,
    'ق': 100,
    'ر': 200,
    'ش': 300,
    'ت': 400,  # ط از اینجا حذف شد
    'ث': 500,
    'خ': 600,
    'ذ': 700,
    'ض': 800,
    'ظ': 900,
    'غ': 1000
}

# تابع برای محاسبه ابجد صغیر (رقم یکان)
def calculate_saghir_value(kabir_value):
    """محاسبه ارزش ابجد صغیر از کبیر"""
    while kabir_value > 9:
        kabir_value = sum(int(digit) for digit in str(kabir_value))
    return kabir_value

# تولید خودکار ابجد صغیر از کبیر
ABJAD_SAGHIR = {char: calculate_saghir_value(value) for char, value in ABJAD_KABIR.items()}

# ابجد وسیط (جمع ارقام)
def calculate_wasit_value(kabir_value):
    """محاسبه ابجد وسیط - جمع ارقام"""
    return sum(int(digit) for digit in str(kabir_value))

ABJAD_WASIT = {char: calculate_wasit_value(value) for char, value in ABJAD_KABIR.items()}

def calculate_abjad(text, abjad_type="کبیر"):
    """محاسبه ابجد برای متن ورودی"""
    total = 0
    details = []

    if abjad_type == "کبیر": 
        abjad_dict = ABJAD_KABIR 
    elif abjad_type == "صغیر": 
        abjad_dict = ABJAD_SAGHIR 
    elif abjad_type == "وسیط": 
        abjad_dict = ABJAD_WASIT 
    else: 
        abjad_dict = ABJAD_KABIR 

    for char in text:
        if char in abjad_dict:
            value = abjad_dict[char]
            total += value
            details.append(f"{char}: {value}")
        elif char == ' ':
            continue  # نادیده گرفتن فاصله
        else:
            details.append(f"{char}: 0 (حرف نامعتبر)")
    
    return total, details

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور شروع ربات"""
    welcome_text = """
🕌 ربات محاسبه گر ابجد حرفه‌ای - نسخه تصحیح شده

🔢 انواع محاسبات موجود:
• ابجد کبیر (اصلی) - مقادیر کامل
• ابجد صغیر (رقم یکان) - مقادیر تک رقمی
• ابجد وسیط (جمع ارقام) - جمع ارقام هر عدد

📝 دستورات موجود:
/start - راهنمای ربات
/help - راهنمای استفاده
/kabir - محاسبه ابجد کبیر
/saghir - محاسبه ابجد صغیر
/wasit - محاسبه ابجد وسیط
/calculate - محاسبه همه انواع

✨ نوآوری‌ها:

✅ محاسبه دقیق حرف گ (گاف)
✅ ارزش صحیح ط (9 نه 400)
✅ محاسبه ئ مانند ی
✅ ابجد صغیر بر اساس رقم یکان
✅ ابجد وسیط بر اساس جمع ارقام
❌ حمزه حذف شده (جزو حروف محاسبه نمی‌شود)
"""

    keyboard = [
        ['/kabir', '/saghir'],
        ['/wasit', '/calculate'],
        ['/help']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور راهنمایی"""
    help_text = """
📚 راهنمای استفاده از ربات ابجد - نسخه تصحیح شده

🔤 حروف پشتیبانی شده:

تمام حروف فارسی و عربی

حرف گ (گاف) با ارزش 20 در کبیر

حرف ئ با ارزش ی (10 در کبیر)

ط فقط 9 (نه 400)

❌ حمزه (ء) حذف شده و محاسبه نمی‌شود

1️⃣ ابجد کبیر (/kabir):
مقادیر اصلی و کامل ابجد
مثال: محمد = م(40) + ح(8) + م(40) + د(4) = 92

2️⃣ ابجد صغیر (/saghir):
رقم یکان ارزش کبیر
مثال: محمد = 4+0=4, 8, 4+0=4, 4 → 4+8+4+4=20 → 2+0=2

3️⃣ ابجد وسیط (/wasit):
جمع ارقام ارزش کبیر
مثال: محمد = 4+0=4, 8, 4+0=4, 4 → 4+8+4+4=20

🎯 نکات فنی:
فاصله و علائم نادیده گرفته می‌شوند
حروف لاتین محاسبه نمی‌شوند
محاسبات بر اساس استانداردهای دقیق ابجد
"""
    await update.message.reply_text(help_text)

async def kabir_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور محاسبه ابجد کبیر"""
    context.user_data['waiting_for'] = 'kabir'
    await update.message.reply_text("📝 لطفاً متن مورد نظر برای محاسبه ابجد کبیر را ارسال کنید:")

async def saghir_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور محاسبه ابجد صغیر"""
    context.user_data['waiting_for'] = 'saghir'
    await update.message.reply_text("📝 لطفاً متن مورد نظر برای محاسبه ابجد صغیر را ارسال کنید:")

async def wasit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور محاسبه ابجد وسیط"""
    context.user_data['waiting_for'] = 'wasit'
    await update.message.reply_text("📝 لطفاً متن مورد نظر برای محاسبه ابجد وسیط را ارسال کنید:")

async def calculate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """محاسبه همه انواع ابجد"""
    context.user_data['waiting_for'] = 'all'
    await update.message.reply_text("📝 لطفاً متن مورد نظر برای محاسبه همه انواع ابجد را ارسال کنید:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بررسی پیام کاربر"""
    if 'waiting_for' not in context.user_data:
        await update.message.reply_text("لطفاً ابتدا از منوی دستورات یک گزینه را انتخاب کنید.")
        return
    
    text = update.message.text
    waiting_for = context.user_data['waiting_for']
    
    if waiting_for == 'kabir':
        total, details = calculate_abjad(text, "کبیر")
        result = f"🔢 ابجد کبیر: {total}\n\n📊 جزئیات:\n" + "\n".join(details)
        await update.message.reply_text(result)
    
    elif waiting_for == 'saghir':
        total, details = calculate_abjad(text, "صغیر")
        result = f"🔢 ابجد صغیر: {total}\n\n📊 جزئیات:\n" + "\n".join(details)
        await update.message.reply_text(result)
    
    elif waiting_for == 'wasit':
        total, details = calculate_abjad(text, "وسیط")
        result = f"🔢 ابجد وسیط: {total}\n\n📊 جزئیات:\n" + "\n".join(details)
        await update.message.reply_text(result)
    
    elif waiting_for == 'all':
        total_kabir, details_kabir = calculate_abjad(text, "کبیر")
        total_saghir, details_saghir = calculate_abjad(text, "صغیر")
        total_wasit, details_wasit = calculate_abjad(text, "وسیط")
        
        result = f"""
📊 نتایج محاسبه برای متن: "{text}"

🔷 ابجد کبیر: {total_kabir}
🔸 ابجد صغیر: {total_saghir}
🔹 ابجد وسیط: {total_wasit}
        """
        await update.message.reply_text(result)
    
    # پاک کردن وضعیت انتظار
    context.user_data.pop('waiting_for', None)

def main():
    """تابع اصلی"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # اضافه کردن هندلرهای دستورات
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("kabir", kabir_command))
    application.add_handler(CommandHandler("saghir", saghir_command))
    application.add_handler(CommandHandler("wasit", wasit_command))
    application.add_handler(CommandHandler("calculate", calculate_command))
    
    # هندلر برای پیام‌های متنی
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 ربات فعال شد...")
    application.run_polling()

if __name__ == "__main__":
    main()
