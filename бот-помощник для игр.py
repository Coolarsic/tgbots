import random

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from config import TOKEN
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

time = 0


def unset_timer(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Хорошо, вернулся сейчас!' if job_removed else 'Нет активного таймера.'
    update.message.reply_text(text)


def task(context):
    global time
    job = context.job
    reply_keyboard = [['/close']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    context.bot.send_message(job.context, text=f'{time} секунд истекло', reply_markup=markup)


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update, context):
    global time
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Извините, не умеем возвращаться в прошлое')
            return
        job_removed = remove_job_if_exists(
            str(chat_id),
            context
        )
        context.job_queue.run_once(
            task,
            due,
            context=chat_id,
            name=str(chat_id)
        )
        text = f'Засёк {due} секунд!'
        time = due
        if job_removed:
            text += ' Старая задача удалена.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set_timer <секунд>')


def start(update, context):
    reply_keyboard = [['/dice', '/timer']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Begin', reply_markup=markup)


def timer(update, context):
    reply_keyboard = [['/set_timer 30', '/set_timer 60'],
                      ['/set_timer 300', '/return']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Выбрать время", reply_markup=markup)


def dice(update, context):
    reply_keyboard = [['/throw_6', '/throw_6_2'],
                      ['/throw_20', '/return']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Рандомный кубик", reply_markup=markup)


def get_me(update, context):
    update.message.reply_text("Арсений")


def close(update, context):
    timer()


def throw_6(update, context):
    update.message.reply_text(str(random.randint(1, 6)))


def throw_6_2(update, context):
    update.message.reply_text(str(random.randint(1, 6)) + " " + str(random.randint(1, 6)))


def throw_20(update, context):
    update.message.reply_text(str(random.randint(1, 20)))


def echo(update, context):
    update.message.reply_text(update.message.text)


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("get_me", get_me))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("close", timer))
    dp.add_handler(CommandHandler("set_timer", set_timer))
    dp.add_handler(CommandHandler("unset_timer", unset_timer))
    dp.add_handler(CommandHandler("timer", timer))
    dp.add_handler(CommandHandler("return", start))
    dp.add_handler(CommandHandler("dice", dice))
    dp.add_handler(CommandHandler("throw_6", throw_6))
    dp.add_handler(CommandHandler("throw_6_2", throw_6_2))
    dp.add_handler(CommandHandler("throw_20", throw_20))
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


