from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from templates.messages import reply_message, reply_message_out_time, reply_message_weekend
from templates.duty_configmap import work_stop_hour, work_start_hour, active_days
import datetime
import os


TOKEN = os.getenv('TELEGRAM_TOKEN')
DUTY_BOT_NAME = os.getenv('DUTY_BOT_NAME')


async def handle_mention(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """The function handle_mention now checks for the presence of the duty bot name in the message, 
    the day of the week, and the current time to send appropriate replies."""

    if DUTY_BOT_NAME in update.message.text:
        if datetime.datetime.today().weekday() < active_days:
            if work_start_hour <= datetime.datetime.now().hour < work_stop_hour:
                await update.message.reply_text(reply_message())
            else:
                await update.message.reply_text(reply_message_out_time())
        else:
            await update.message.reply_text(reply_message_weekend())


def telegram_bot():
    """Function sets up the Telegram bot application with the necessary handlers and runs the polling loop."""

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.Entity("mention"), handle_mention))
    application.run_polling(3)
