from aiogram import types, F
from aiogram.fsm.context import FSMContext
from bot.apps.admin.state.main import AdminState
from db.model import User
from utils.dispatcher import dp


@dp.callback_query(lambda call: str(call.data).__eq__("user_unblock"))
async def user_rek_handler(call: types.CallbackQuery, state : FSMContext):
    await state.set_state(AdminState.unblock_id)
    await call.message.edit_caption(caption="User id kiriting ✍🏻")

@dp.message(AdminState.unblock_id , F.text.isnumeric())
async def user_id_handler(msg : types.Message , state : FSMContext):
    user = await User.get(int(msg.text))
    data = await state.get_data()
    data.update({"id": int(msg.text)})
    await state.set_data(data)
    if user: await msg.answer("User topildi 🤩 Block dan olindi ⭕️")
    else: await msg.answer("User topilmadi 😞")
    if user: await User.update(int(msg.text), is_active = True)
    await state.clear()