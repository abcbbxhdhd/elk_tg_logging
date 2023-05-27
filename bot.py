import telebot
from dotenv import dotenv_values
import json
import logging
from logstash_async.handler import AsynchronousLogstashHandler

config = dotenv_values(".env")
host = config.get("LOGSTASH_HOST")
port = int(config.get("LOGSTASH_PORT"))
bot_key = config.get("BOT_KEY")

logger = logging.getLogger('bot-logging')
logger.setLevel(logging.INFO)
async_handler = AsynchronousLogstashHandler(host, port, database_path=None)

bot = telebot.TeleBot(bot_key, parse_mode=None)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    messageInfo = {
        "chatId": message.chat.id,
        "fromUsername": message.from_user.username,
        "message": message.text
    }
    print(json.dumps(messageInfo))
    bot.reply_to(message, "Your message has been received!")


bot.infinity_polling()
