from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from config import TOKEN
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


def unset_timer(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Хорошо, вернулся сейчас!' if job_removed else 'Нет активного таймера.'
    update.message.reply_text(text)


def task(context):
    job = context.job
    context.bot.send_message(job.context, text='Вернулся!')


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update, context):
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
        text = f'Вернусь через {due} секунд!'
        if job_removed:
            text += ' Старая задача удалена.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set_timer <секунд>')


def start(update, context):
    reply_keyboard = [['/get_me', '/set_timer 5'],
                      ['/close', '/unset_timer']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Ку-ку", reply_markup=markup)


def get_me(update, context):
    update.message.reply_text("Арсений")


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
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(CommandHandler("set_timer", set_timer))
    dp.add_handler(CommandHandler("unset_timer", unset_timer))
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


