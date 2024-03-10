from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.apps.admin.state.main import AdminState
from bot.apps.utils import send_message
from bot.buttons.inline import tools
from bot.buttons.text import mission_message
from db.model import User
from utils.dispatcher import dp
from aiogram.utils.markdown import hbold



@dp.callback_query(lambda call: str(call.data).__eq__("users_rek"))
async def users_rek_handler(call: types.CallbackQuery, state : FSMContext):
    await state.set_state(AdminState.for_users_message)
    await call.message.edit_caption(caption="🤩 Reklama havolasini yuboring ✍🏻")



@dp.message(AdminState.for_users_message)
async def for_users_message_handler(msg : types.Message , state : FSMContext):
    users = await User.get_all()
    mission = await msg.answer(hbold(mission_message.format(0,0)))
    await send_message(msg ,mission, users)
    await state.clear()
    text = hbold("Mofaqiyatli habar jo'natildi 🥳")
    photo = "https://telegra.ph/file/aa2b1d86875d64203013b.png"
    await msg.answer_photo(photo, caption=text, reply_markup=tools())



