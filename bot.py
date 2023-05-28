import telebot
from dotenv import dotenv_values
from prometheus_client import start_http_server, Counter

config = dotenv_values(".env")
bot_key = config.get("BOT_KEY")

start_counter = Counter('total_starts', "Total number of /start command")

bot = telebot.TeleBot(bot_key, parse_mode=None)


@bot.message_handler(func=lambda m: True)
def echo_all_and_monitor(message):
    if message.text == "/start":
        start_counter.inc()
        bot.reply_to(message, "Hello. I'm here!")

    bot.reply_to(message, "Your message has been received!")


start_http_server(9091)
bot.infinity_polling()
