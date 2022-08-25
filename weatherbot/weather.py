import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import emoji
# Сюда добавляем различные адреса и токены
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
GEOCODER_URL = 'http://api.openweathermap.org/geo/1.0/direct'
TOKEN = '5405186249:AAFPpnF82ALDCgRVcgtC6Mb_CuTu-MM8IR4'
API_KEY = 'b448c5c1c0caf3f11a51a8d88801141d'

# Формируем клавиатуру
keyboard = ReplyKeyboardMarkup([['Погода в Чебоксарах', 'Погода в Ибресях', 'Погода в Бугуянах']],
                               resize_keyboard=True)


def get_data():
    GEO_PARAMS1 = {'q': 'Чебоксары',
                   'limit': 5,
                   'appid': API_KEY}
    response = requests.get(GEOCODER_URL, params=GEO_PARAMS1).json()

    lat = response[0]['lat']
    lon = response[0]['lon']

    WEATHER_PARAMS1 = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }

    data1 = requests.get(url=WEATHER_URL, params=WEATHER_PARAMS1).json()

    # разбираем ответ, например:
    # data1 = response[0].get('url')
    return (data1 )

def get_data2():
    GEO_PARAMS2 = {'q': 'Ибреси',
                   'limit': 5,
                   'appid': API_KEY}
    response2 = requests.get(GEOCODER_URL, params=GEO_PARAMS2).json()

    lat2 = response2[0]['lat']
    lon2 = response2[0]['lon']

    WEATHER_PARAMS2 = {
        'lat': lat2,
        'lon': lon2,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }

    data2 = requests.get(url=WEATHER_URL, params=WEATHER_PARAMS2).json()

    # разбираем ответ, например:
    # data1 = response[0].get('url')
    return (data2 )

def get_data3():
    GEO_PARAMS3 = {'q': 'Бугуян',
                   'limit': 5,
                   'appid': API_KEY}
    response3 = requests.get(GEOCODER_URL, params=GEO_PARAMS3).json()

    lat3 = response3[0]['lat']
    lon3 = response3[0]['lon']

    WEATHER_PARAMS3 = {
        'lat': lat3,
        'lon': lon3,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }

    data3 = requests.get(url=WEATHER_URL, params=WEATHER_PARAMS3).json()

    # разбираем ответ, например:
    # data1 = response[0].get('url')
    return (data3 )


def action_1(update, context):
    chat_id = update.effective_chat.id
    data1 = get_data()
    description=data1['weather'][0]['description']
    temp = data1['main']['temp']
    feels_like = data1['main']['feels_like']

    #(emoji.emojize('Python is :thumbs_up:'))
    text = f'{description.capitalize()}.Температура {temp}, ощущается как {feels_like}👍💛.'
    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard
    )


def action_2(update, context):
    chat_id = update.effective_chat.id
    # Если нужны какие то данные до делаем запрос
    data2 = get_data2()
    description = data2['weather'][0]['description']
    temp2 = data2['main']['temp']
    feels_like2 = data2['main']['feels_like']
    text2 = f'{description.capitalize()}. Температура {temp2}, ощущается как {feels_like2}👍💛. '
    context.bot.send_message(
        chat_id=chat_id,
        text=text2,
        reply_markup=keyboard
    )


def action_3(update, context):
    chat_id = update.effective_chat.id
    # Если нужны какие то данные до делаем запрос
    data3 = get_data3()
    description = data3['weather'][0]['description']
    temp = data3['main']['temp']
    feels_like = data3['main']['feels_like']
    text = f'{description.capitalize()}.Температура {temp}, ощущается как {feels_like}👍💛. '
    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard
    )


def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text='Привет, я буду показывать тебе погоду!',
        reply_markup=keyboard
    )


def main():
    updater = Updater(token=TOKEN)
    # Добавляем обработку команд
    updater.dispatcher.add_handler(CommandHandler('start', start))
    # Или добавляем обработку текста
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text(('Погода в Чебоксарах',)), action_1))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text(('Погода в Ибресях',)), action_2))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text(('Погода в Бугуянах',)), action_3))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
