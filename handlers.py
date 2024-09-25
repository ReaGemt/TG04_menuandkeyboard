import logging
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import keyboards as kb
from aiogram.exceptions import TelegramAPIError

# Создаем роутер для хендлеров
router = Router()


# Команда /start с выводом меню
@router.message(CommandStart())
async def start(message: Message):
    logging.info(f"Пользователь {message.from_user.id} ({message.from_user.first_name}) запустил бота.")
    await message.answer("Выберите действие:", reply_markup=kb.menu_keyboard)


# Обработка кнопки "Привет"
@router.message(F.text == "Привет")
async def say_hello(message: Message):
    logging.info(f"Пользователь {message.from_user.id} ({message.from_user.first_name}) нажал 'Привет'.")
    await message.answer(f"Привет, {message.from_user.first_name}!")


# Обработка кнопки "Пока"
@router.message(F.text == "Пока")
async def say_goodbye(message: Message):
    logging.info(f"Пользователь {message.from_user.id} ({message.from_user.first_name}) нажал 'Пока'.")
    await message.answer(f"До свидания, {message.from_user.first_name}!")


# Команда /links для показа кнопок с ссылками
@router.message(F.text == "/links")
async def show_links(message: Message):
    logging.info(f"Пользователь {message.from_user.id} запросил ссылки.")
    await message.answer("Выберите ссылку:", reply_markup=kb.links_keyboard)


# Команда /dynamic для показа кнопки "Показать больше"
@router.message(F.text == "/dynamic")
async def show_dynamic(message: Message):
    logging.info(f"Пользователь {message.from_user.id} запросил динамическое меню.")
    await message.answer("Нажмите, чтобы показать больше опций:", reply_markup=kb.dynamic_keyboard)


# Обработка нажатия на кнопку "Показать больше"
@router.callback_query(F.data == "show_more")
async def show_more_options(callback_query: CallbackQuery):
    logging.info(f"Пользователь {callback_query.from_user.id} нажал 'Показать больше'.")
    await callback_query.message.edit_text("Выберите опцию:", reply_markup=kb.more_options_keyboard)


# Обработка опции 1
@router.callback_query(F.data == "option_1")
async def select_option_1(callback_query: CallbackQuery):
    logging.info(f"Пользователь {callback_query.from_user.id} выбрал 'Опция 1'.")
    await callback_query.answer("Вы выбрали Опцию 1")
    await callback_query.message.answer("Опция 1 выбрана")


# Обработка опции 2
@router.callback_query(F.data == "option_2")
async def select_option_2(callback_query: CallbackQuery):
    logging.info(f"Пользователь {callback_query.from_user.id} выбрал 'Опция 2'.")
    await callback_query.answer("Вы выбрали Опцию 2")
    await callback_query.message.answer("Опция 2 выбрана")


# Обработчик ошибок
@router.errors()
async def error_handler(update, exception):
    logging.error(f"Ошибка при обработке апдейта {update}: {exception}")

    if isinstance(exception, TelegramAPIError):
        logging.error(f"API ошибка Telegram: {exception}")
    else:
        logging.error(f"Неизвестная ошибка: {exception}")
    return True
