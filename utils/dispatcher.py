import os

from aiogram import Dispatcher , Bot
from aiogram.enums import ParseMode
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
dp = Dispatcher()

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)