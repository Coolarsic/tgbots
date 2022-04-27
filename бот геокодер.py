import requests
import json
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from config import TOKEN


API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def sendmsg(update, context):
    coords = get_coords(update.message.text)
    if type(coords).__name__ == 'str':
        update.message.reply_text(coords)
    elif coords == (None, None):
        update.message.reply_text("Ничего не найдено. Может быть, вы неправильно ввели запрос?")
    else:
        coord = list(map(str, coords))
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(coord)}&spn=0.005,0.005&l=sat&pt={','.join(coord)},pm2rdm"
        context.bot.send_photo(
            update.message.chat_id,
            map_request,
            caption="Нашёл:"
        )


def get_coords(address):
    toponym = geocode(address)
    if not toponym:
        return None, None
    elif type(toponym).__name__ == 'str':
        return

    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


def geocode(address):

    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_request, params=geocoder_params)

    try:
        json_response = response.json()
    except Exception:
        return f"""Ошибка выполнения запроса:
            {geocoder_request}
            Http статус: {response.status_code} {response.reason}"""

    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None



def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, sendmsg))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
