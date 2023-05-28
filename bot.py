import telebot
from dotenv import dotenv_values
import json
import logging
from cloudwatch import cloudwatch

config = dotenv_values(".env")
region = config.get("REGION")
bot_key = config.get("BOT_KEY")
aws_access_key_id = config.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = config.get("AWS_SECRET_ACCESS_KEY")
log_group = config.get("LOG_GROUP")
log_stream = config.get("LOG_STREAM")

handler = cloudwatch.CloudwatchHandler(
    log_group=log_group,
    access_id=aws_access_key_id,
    access_key=aws_secret_access_key,
    region=region,
    log_stream=log_stream
)
logger = logging.getLogger('bot_logger')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

bot = telebot.TeleBot(bot_key, parse_mode=None)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    messageInfo = {
        "chatId": message.chat.id,
        "fromUsername": message.from_user.username,
        "message": message.text
    }
    logger.info(json.dumps(messageInfo, ensure_ascii=False))
    bot.reply_to(message, "Your message has been received!")


bot.infinity_polling()
