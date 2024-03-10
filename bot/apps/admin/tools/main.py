from aiogram import types
from aiogram.utils.markdown import hbold
from bot.apps.utils import is_admin
from bot.buttons.inline import tools
from bot.buttons.text import tools_admin
from utils.dispatcher import dp


@dp.message(lambda msg : is_admin(msg),lambda msg: str(msg.text).__eq__(tools_admin))
async def tools_handler(msg: types.Message):
    text = hbold("Barcha xizmatlar ro'yxati")
    photo = "https://telegra.ph/file/aa2b1d86875d64203013b.png"
    await msg.answer_photo(photo,caption=text , reply_markup=tools())








