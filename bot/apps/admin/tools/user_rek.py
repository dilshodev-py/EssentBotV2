from aiogram import types, F
from aiogram.fsm.context import FSMContext
from bot.apps.admin.state.main import AdminState
from bot.buttons.inline import tools
from db.model import User
from utils.dispatcher import dp
from aiogram.utils.markdown import hbold


@dp.callback_query(lambda call: str(call.data).__eq__("user_rek"))
async def user_rek_handler(call: types.CallbackQuery, state : FSMContext):
    await state.set_state(AdminState.id)
    await call.message.edit_caption(caption="User id kiriting ✍🏻")



@dp.message(AdminState.id , F.text.isnumeric())
async def user_id_handler(msg : types.Message , state : FSMContext):
    user = await User.get(int(msg.text))
    data = await state.get_data()
    data.update({"id": int(msg.text)})
    await state.set_data(data)
    if user: await msg.answer("User topildi 🤩 Xabarni yuboring ✍🏻")
    else: await msg.answer("User topilmadi 😞")
    if user: await state.set_state(AdminState.message)
    else: await state.clear()

@dp.message(AdminState.message)
async def message_handler(msg : types.Message , state : FSMContext):
    data = await state.get_data()
    await msg.copy_to(data.get("id"))
    await state.clear()
    text = hbold("Mofaqiyatli habar jo'natildi 🥳")
    photo = "https://telegra.ph/file/aa2b1d86875d64203013b.png"
    await msg.answer_photo(photo, caption=text, reply_markup=tools())
