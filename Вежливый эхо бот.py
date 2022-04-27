from telegram.ext import Updater, MessageHandler, Filters


def echo(update, context):
    update.message.reply_text("Я получил сообщение <" + update.message.text + ">")


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()