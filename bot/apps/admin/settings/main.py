from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.apps.admin.state.main import AdminSettingsState, AdminBookState, AdminTestState, AdminEverestVocabState
from bot.buttons.keyboard import settings_menu
from bot.buttons.text import settings_admin, BACK
from utils.dispatcher import dp

@dp.callback_query(lambda call : call.data.__eq__('ignore') , AdminEverestVocabState.vocab_file)
@dp.callback_query(lambda call : call.data.__eq__(BACK) , AdminSettingsState.book)
@dp.callback_query(lambda call : call.data.__eq__(BACK) , AdminTestState.test_section)
async def back_handler(call: types.CallbackQuery , state :FSMContext):
    await call.message.delete()
    await call.message.answer("Settings 👨🏻‍💻", reply_markup=settings_menu())
    await state.set_state(AdminSettingsState.settings_menu)

@dp.message(lambda msg : str(msg.text).__eq__(settings_admin))
async def settings_handler(msg: types.Message, state : FSMContext):
    await state.set_state(AdminSettingsState.settings_menu)
    await msg.answer("Settings 👨🏻‍💻", reply_markup=settings_menu())
