from aiogram import types, F
from aiogram.filters.command import Command

from bot.apps.admin.state.main import AdminSettingsState
from bot.apps.utils import is_admin
from bot.buttons.keyboard import admin_menu
from bot.buttons.text import BACK
from utils.dispatcher import dp


@dp.message(F.text.__eq__(BACK),AdminSettingsState.settings_menu)
@dp.message(lambda msg : is_admin(msg), Command("panel"))
async def admin_handler(msg: types.Message):
    await msg.answer("Admin bo'limiga hush kelibsiz !", reply_markup=admin_menu())








