import os
import telebot
import openai

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! أنا بوت يعمل بتقنية ChatGPT. أرسل لي سؤالاً.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي ولطيف، ملتزم بالسياسات الأخلاقية."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message['content']
        bot.reply_to(message, reply)
    except openai.error.OpenAIError as e:
        if "rate limit" in str(e).lower():
            bot.reply_to(message, "عذراً، لقد تجاوزت الحد المسموح به من الطلبات. يرجى المحاولة لاحقاً.")
        else:
            bot.reply_to(message, f"حدث خطأ في واجهة برمجة تطبيقات OpenAI: {e}")
    except Exception as e:
        bot.reply_to(message, "عذراً، حدث خطأ. يرجى المحاولة مرة أخرى لاحقاً.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
