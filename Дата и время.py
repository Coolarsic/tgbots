from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from config import TOKEN
from time import asctime


def get_me(update, context):
    update.message.reply_text("Арсений")


def echo(update, context):
    update.message.reply_text(update.message.text)


def date(update, context):
    update.message.reply_text(' '.join(asctime().split()[:3]) + " " + asctime().split()[4])


def time(update, context):
    update.message.reply_text(asctime().split()[3])


def main():
    print(asctime())
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("time", time))
    dp.add_handler(CommandHandler("date", date))
    dp.add_handler(CommandHandler("get_me", date))
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


