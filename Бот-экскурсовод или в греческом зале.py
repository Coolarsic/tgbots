import random

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from config import TOKEN
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def start(update, context):
    update.message.reply_text("Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!")
    return 2


def get_me(update, context):
    update.message.reply_text("Арсений")


def second_response(update, context):
    update.message.reply_text("В данном зале предствалены поколения различных ЭВМ. Здесь очень интересно, советуем всё внимательно осмотреть"
                        " только, пожалуйста, ничего не трогайте руками! Экспонаты очень старые...")
    update.message.reply_text("Далее можно пройти в зал номер 3, где представлены различные ОС.")
    return 3


def third_response(update, context):
    update.message.reply_text(
        "В данном зале предствалены различные OC: дистрибутивы linux(ubuntu, debian, arch), FreeBSD, OpenBSD, MSDOS, Windows 10, Windows 11, а также их структура. "
        "Здесь можно поработать за различными компьютерами, на которых устанвлены данные ОС. Только, пожайлуйста, не давайте команд наподобие sudo rm -rf / "
        "или же dd if=/dev/zero of=/dev/sda. Это сильно затруднит нам жизнь :-)")
    update.message.reply_text("Далее можно пройти в зал номер 4, где можно попрограммировать на различных языках программирования или же пойти на выход. "
                        "Чтобы завершить экскурсию, нажмите 5, в любом другом случае вас отправят в следующий зал.")
    return 4


def fourth_response(update, context):
    if update.message.text == '5':
        return 5
    else:
        update.message.reply_text("В данном зале представлены различные ЯПы: С++, Python, C, Asm, Rust, PHP, Java, JS, TS, Pascal, Basic, C#, Ruby, Go. Вы можете "
                        "написать программу на интересующес вас языке и опробовать её.")
        update.message.reply_text("В данном зале наша экскурсия, к сожалению, заканчивается. Всего доброго!")
    return 5


def ex(update, context):
    update.message.reply_text("Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!")
    return ConversationHandler.END


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("get_me", get_me))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            2: [MessageHandler(Filters.text, second_response)],
            3: [MessageHandler(Filters.text, third_response)],
            4: [MessageHandler(Filters.text, fourth_response)],
            5: [MessageHandler(Filters.text, ex)]
        },
        fallbacks=[]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
