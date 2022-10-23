from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import bot_setting
from handler.logic_message import get_update_avito_url, get_url, update_last_url
import time
import asyncio


def aexec(func):
    def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(func(update, context))
        loop.close()
    return wrapper


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    pass


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    update_message = get_update_avito_url(update.message.text)

    last_url = ''
    if update_message.amount == 1:
        await update.message.reply_text(update_message.output_text)

    avito_url = update_message.output_text

    while (True):
        if last_url == '':
            last_url = update_last_url(avito_url)
            await update.message.reply_text(last_url)
            await asyncio.sleep(30)

        output_message_at = get_url(avito_url, last_url=last_url)

        if output_message_at == '':
            await asyncio.sleep(60)
            continue
        else:
            await update.message.reply_text(output_message_at)
            await asyncio.sleep(60)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    TOKEN = bot_setting.get_tg_token()

    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

