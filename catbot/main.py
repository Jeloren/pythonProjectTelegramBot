import logging
import os
import sys

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, TelegramError
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

CAT_URL = 'https://api.thecatapi.com/v1/images/search'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                              '%(funcName)s - %(lineno)d - %(message)s')
# handler = logging.StreamHandler(sys.stdout)
# handler = logging.FileHandler('main.log', encoding='utf-8')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

keyboard = ReplyKeyboardMarkup([['Давай котика', 'Об авторе']],
                               resize_keyboard=True)


def get_new_image():
    logger.info(f'Начато выполнение запроса к API {CAT_URL}.')
    try:
        response = requests.get(CAT_URL).json()
        cat_image = response[0].get('url')
        logger.info(
            f'Запрос к API {CAT_URL} выполнен.')
        return cat_image
    except Exception as error:
        logger.error(f'Не удалось выполнить запрос к API. Ошибка: {error}.')
        return None


def get_cat(update, context):
    chat_id = update.effective_chat.id
    logger.info(f'Пользователь с id: {chat_id} запросил изображение котика.')
    image = get_new_image()
    if not image:
        text = 'Не могу пока отправить котика, попробуй позже.'
        try:
            context.bot.send_photo(
                chat_id=chat_id,
                text=text,
                reply_markup=keyboard
            )
            logger.info(f'Отправлено сообщение пользователю с id: {chat_id} ')
        except TelegramError as error:
            logger.error(
                f'Не удалось отправить сообщение пользователю с id: '
                f'{chat_id}. '
                f'Ошибка: {error}.')
    try:
        context.bot.send_photo(
            chat_id=chat_id,
            photo=image,
            reply_markup=keyboard
        )
        logger.info(f'Отправлено сообщение пользователю с id: {chat_id} ')
    except TelegramError as error:
        logger.error(
            f'Не удалось отправить сообщение пользователю с id: {chat_id}. '
            f'Ошибка: {error}.')


def start(update, context):
    chat_id = update.effective_chat.id
    logger.info(f'Пользователь с id: {chat_id} запустил бота.')
    name = update.message.chat.first_name
    text = f'Привет, {name}. Я буду отправлять тебе котиков'
    try:
        context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard
        )
        logger.info(f'Отправлено сообщение пользователю с id: {chat_id} ')
    except TelegramError as error:
        logger.error(
            f'Не удалось отправить сообщение пользователю с id: {chat_id}. '
            f'Ошибка: {error}.')


def about(update, context):
    chat_id = update.effective_chat.id
    logger.info(f'Пользователь с id: {chat_id} '
                 f'запросил информацию об авторе.')
    text = 'Автор этого бота просто гений!'
    try:
        context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard
        )
        logger.info(f'Отправлено сообщение пользователю с id: {chat_id} ')
    except TelegramError as error:
        logger.error(
            f'Не удалось отправить сообщение пользователю с id: {chat_id}. '
            f'Ошибка: {error}.')


def main():
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        logger.critical('Токен не обнаружен')
        sys.exit()
    updater = Updater(token=token)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text(('Давай котика',)), get_cat))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text(('Об авторе',)), about))
    updater.start_polling()
    updater.idle()
    logger.info(f'Бот запущен')


if __name__ == '__main__':
    main()