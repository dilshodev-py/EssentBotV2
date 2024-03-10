from bot.apps.admin.state.main import AdminSettingsState
from bot.buttons.text import panel_grammar
from utils.dispatcher import dp
from aiogram import types, F
from aiogram.fsm.context import FSMContext


@dp.message(F.text.__eq__(panel_grammar), AdminSettingsState.settings_menu)
async def settings_handler(msg : types.Message, state : FSMContext):
    await msg.answer("Level tanlang !")