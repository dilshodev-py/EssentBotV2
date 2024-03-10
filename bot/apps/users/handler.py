from aiogram import F
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from bot.apps.users.state.main import TestState
from bot.apps.utils import send_to_admin
from bot.buttons.inline import admin_account, admin_btn
from bot.buttons.keyboard import main_menu
from bot.buttons.text import text, BACK, start_admin, admin
from db.model import User
from utils.dispatcher import dp
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types.input_media_photo import InputMediaPhoto


@dp.callback_query(lambda call : call.data.__eq__(BACK) , TestState.test_section)
async def back_handler(call : types.CallbackQuery , state : FSMContext):
    photo = "https://telegra.ph/file/1a7306b3e0b4bc3e0e9a5.png"
    await call.message.edit_media(media=InputMediaPhoto(media=photo, caption=text.format(call.message.from_user.full_name)))
    await call.message.answer(text = BACK , reply_markup=main_menu())


@dp.message(F.text.__eq__(BACK))
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    user = await User.get(id_=message.from_user.id)
    if not user:
        await User.create(id=message.from_user.id, fullname=f"{message.from_user.full_name}")
        user = await User.get(id_=message.from_user.id)
    if not user.is_active:
        text_ = "Siz admin tomonidan block qilingansiz"
        await message.answer(text=text_, reply_markup=admin_account())
        await message.answer("Adminga murojat qiling", reply_markup=ReplyKeyboardRemove())
    else:
        admin_text = start_admin.format(f"t.me/{message.from_user.username}", message.from_user.id)
        await send_to_admin(message, admin_text)
        photo = "https://telegra.ph/file/1a7306b3e0b4bc3e0e9a5.png"
        await message.answer_photo(photo, caption=text.format(user.fullname), reply_markup=main_menu())


@dp.message(F.text.__eq__(admin))
async def admin_handler(msg : types.Message):
    await msg.answer_photo("https://telegra.ph/file/9ba431c849d4fc7978b3e.png", reply_markup=admin_btn())
    await msg.answer("Assosiy bo'lim", reply_markup=main_menu())


