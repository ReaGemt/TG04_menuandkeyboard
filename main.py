import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router  # Импортируем роутер с хендлерами

# Загрузка переменных окружения
load_dotenv()

# Получаем токен бота из переменных окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Регистрация роутера с хендлерами в диспетчере
dp.include_router(router)

# Функция для корректного завершения работы бота
async def shutdown_handler():
    logging.info("Процесс завершён. Бот остановлен корректно.")
    await bot.session.close()

# Запуск бота
async def main():
    logging.info("Запуск бота...")
    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Получен сигнал прерывания. Завершение работы бота...")
    finally:
        await shutdown_handler()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот был остановлен пользователем.")
