from aiogram import types
from aiogram.utils.markdown import hcode
from bot.apps.utils import is_admin, today_yesterday
from bot.buttons.inline import update_statist
from bot.buttons.text import statistik_admin, static_text
from db.model import User
from utils.dispatcher import dp


@dp.message(lambda msg : is_admin(msg),lambda msg: str(msg.text).__eq__(statistik_admin))
async def statistik_handler(msg: types.Message):
    users = await User.get_all()
    today, yesterday = await today_yesterday(users)
    text = hcode(static_text.format(len(users) , today , yesterday))
    await msg.answer_photo("https://telegra.ph/file/78fb32ab221b24de14451.png" , caption= text,reply_markup=update_statist())

@dp.callback_query(lambda msg : is_admin(msg),lambda clb : str(clb.data).__eq__("update"))
async def update_handler(call : types.CallbackQuery):
    users = await User.get_all()
    today, yesterday = await today_yesterday(users)
    text = hcode(static_text.format(len(users), today , yesterday))
    await call.message.edit_caption(caption=text)
    await call.message.edit_reply_markup(reply_markup=update_statist())
    await call.answer(text="update")