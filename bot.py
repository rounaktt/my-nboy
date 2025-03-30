import requests
import telebot

# 🚨 Replace this with your NEW bot token after revoking the old one!
BOT_TOKEN = "7724913384:AAHH3TQJ7TJ2BuQiXaNPjJ8JxHY0srrVXnc"


bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Send me any link, and I'll track all redirects for you.")

@bot.message_handler(func=lambda message: True)
def track_redirects(message):
    url = message.text.strip()
    
    if not (url.startswith("http://") or url.startswith("https://")):
        bot.reply_to(message, "⚠ Please send a valid URL starting with http:// or https://")
        return

    try:
        session = requests.Session()
        response = session.get(url, allow_redirects=True)
        
        if response.history:
            redirect_chain = "🔗 **Redirect Chain:**\n"
            for resp in response.history:
                redirect_chain += f"{resp.status_code} ➝ {resp.url}\n"
            redirect_chain += f"\n✅ **Final URL:** {response.url}"
        else:
            redirect_chain = f"✅ No redirects detected. Final URL: {response.url}"
        
        bot.reply_to(message, redirect_chain)

    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"❌ Error: {e}")

bot.polling()
