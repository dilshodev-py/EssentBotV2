from aiogram import types, F

from bot.apps.users.state.main import BookState
from bot.buttons.keyboard import books_user_menu
from bot.buttons.text import book, BACK
from utils.dispatcher import dp


@dp.message(F.text.__eq__(book))
async def book_handler(msg: types.Message):
    photo = "https://telegra.ph/file/ad89b0680ecb4de36638b.png"
    await msg.answer_photo(photo=photo, caption="Book bo'limi !", reply_markup=books_user_menu())
