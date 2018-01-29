from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
import logging
import os
import config
from api_handler import ApiHandler

TOKEN = config.BOT_TOKEN
PORT = int(os.environ.get('PORT', '8443'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text("""
        Hi, I'm Crypto Price Bot!
        To ask about price just send the pairing you want to know, e.g. btc-usd
        To ask a price in a specific market add market's name after the pairing, e.g. btc-usd bitfinex
        For more command, ask /help
        """)

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text("""
        To ask about price just send the pairing you want to know, e.g. btc-usd
        To ask a price in a specific market add market's name after the pairing, e.g. btc-usd bitfinex
        To list all available markets on a certain pairing, put the pairing after market, e.g. market xlm-btc

        * Other available commands: *
        /about - version and bot's info
        """)

def about(bot, update):
    """Send a message when the command /about is issued."""
    update.message.reply_text("""
        CRYPTO PRICE BOT v1.0
        Created by @tobive
        Market's data taken from api.cryptonator.com
        """)

def process_message(bot, update):
    """Process user message and give correct response."""
    api_handler = ApiHandler()
    msg = api_handler.get_response(update.message.text)
    update.message.reply_text(msg)

def echo(bot, update):
    """Echoing the message after command."""
    msg = update.message.text.split(' ', 1)[1]
    update.message.reply_text(msg)

def alarm(bot, update):
    """Put alarm based on pairing and price. Format: </alarm> <pairing> <direction> <price>"""

    err_msg = """
        Unrecognized command. Please use the following format:
        </alarm> <pairing> <below/over> <price>
        e.g. /alarm xrp-usd over 2.23
        """
    msg = update.message.text.split(' ', 1)
    if len(msg) == 1:
        update.message.reply_text(err_msg)
    else:
        if msg[1].lower() == 'list':
            # -> list alarms
            update.message.reply_text(" --list the alarms-- ")
        elif len(msg[1].split(' ')) == 3:
            cmd = msg[1].split(' ')
            try:
                if '-' in cmd[0] and cmd[1].lower() in ['below', 'over'] and float(cmd[2]) > 0.0:
                    # ->add alarm
                    update.message.reply_text(" -- alarm added! -- ")
                else:
                    update.message.reply_text(err_msg)
            except ValueError:
                update.message.reply_text(err_msg)
        else:
            update.message.reply_text(err_msg)

def delete(bot, update):
    """Delete alarm from command. ID of the deleted thing is embedded in the command."""
    alarm_id = update.message.text.split('/del_alarm_')[1]
    # -> delete alarm
    update.message.reply_text(" -- Alarm with ID {} deleted -- ".format(alarm_id))

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("about", about))
    dp.add_handler(CommandHandler("alarm", alarm))
    dp.add_handler(CommandHandler("echo", echo))
    dp.add_handler(RegexHandler('^/del_', delete))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, process_message))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    # updater.bot.set_webhook("https://tobi-telegram-bot.herokuapp.com/" + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
