from aiogram import F
from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.apps.admin.state.main import AdminEverestVocabState, AdminSettingsState
from bot.apps.utils import everest_vocab_excel
from bot.buttons.inline import ignore
from bot.buttons.keyboard import settings_menu
from bot.buttons.text import EVEREST_VOCAB
from utils.dispatcher import dp


@dp.message(lambda msg : str(msg.text).__eq__(EVEREST_VOCAB) , AdminSettingsState.settings_menu)
async def add_vocab_handler(msg : types.Message , state :FSMContext):
    await msg.delete()
    await state.set_state(AdminEverestVocabState.vocab_file)
    await msg.answer("Vocabulary yozilgan excel file tashlang 🗃", reply_markup=ignore())

@dp.message(F.content_type.in_("document") , AdminEverestVocabState.vocab_file)
async def vocab_file_handler(msg : types.Message , state : FSMContext):
    file = await msg.bot.get_file(msg.document.file_id)
    file = await msg.bot.download_file(file.file_path)
    await everest_vocab_excel(file)
    await state.set_state(AdminSettingsState.settings_menu)
    await msg.answer('Mofaqiyatli saqlandi ✅', reply_markup=settings_menu())
