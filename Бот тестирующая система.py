import requests
import json
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from config import TOKEN
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

sl = {}
answers = []
counter = 1
testlen = 0
ontest = False


def onmessage(update, context):
    global counter, sl, answers, ontest
    if ontest:
        answers.append(update.message.text.lower())
        if counter == len(sl['test']):
            counter = 1
            right = 0
            for ans, rht in zip(answers, sl['test']) :
                if ans == rht['response']:
                    right += 1
            update.message.reply_text("Тест завершён. Чтобы пройти тест снова снова дайте команду /start. Количество правильных ответов:"
                                      f" {right} из {testlen}")
            answers.clear()
            sl.clear()
            ontest = False
        else:
            update.message.reply_text(f"{sl['test'][counter]['question']}")
            counter += 1


def accept(update, context):
    global testlen, sl, ontest
    ontest = True
    with open("test.json") as f:
        sl = json.load(f)
    testlen = len(sl['test'])
    update.message.reply_text("Первый вопрос: " + sl['test'][0]['question'])


def decline(update, context):
    update.message.reply_text("Хорошо, до свидания!")


def stop(update, context):
    global ontest
    ontest = False
    update.message.reply_text("Тест прерван. Чтобы начать заново наберите команду /start")


def start(update, context):
    with open("test.json") as f:
        sl = json.load(f)
    testln = len(sl['test'])
    keyboard = [['/accept', '/decline']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(f"Хотите пройти тест? Количество вопросов: {testln}",
                              reply_markup=markup)


def get_me(update, context):
    update.message.reply_text("Арсений")


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("get_me", get_me))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("accept", accept))
    dp.add_handler(CommandHandler("decline", decline))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(MessageHandler(Filters.text, onmessage))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()