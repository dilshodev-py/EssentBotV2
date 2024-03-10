from aiogram import types, F
from aiogram.fsm.context import FSMContext
from bot.apps.admin.state.main import AdminSettingsState, AdminTestState
from bot.apps.utils import read_document_test
from bot.buttons.inline import test_menu, ignore, test_inline
from bot.buttons.text import test, BACK, admin_test
from db.model import TestSection, Test
from utils.dispatcher import dp


@dp.callback_query(lambda call: call.data.__eq__("ignore"), AdminTestState.test_title)
@dp.callback_query(lambda call: call.data.__eq__(BACK), AdminTestState.test)
async def ignore_handler(call: types.CallbackQuery, state: FSMContext):
    tests_section = await TestSection.get_all()
    await state.set_state(AdminTestState.test_section)
    await call.message.edit_text("test 📚", reply_markup=test_menu(tests_section))


@dp.message(F.text.__eq__(admin_test), AdminSettingsState.settings_menu)
async def test_settings_handler(msg: types.Message, state: FSMContext):
    tests_section = await TestSection.get_all()
    await state.set_state(AdminTestState.test_section)
    await msg.answer("test 📚", reply_markup=test_menu(tests_section))


@dp.callback_query(lambda call: call.data.__eq__('add_test_section'), AdminTestState.test_section)
async def add_test_section_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminTestState.test_title)
    await call.message.edit_text(text="Test Mavzusini kiriting ✍🏻", reply_markup=ignore())


@dp.message(AdminTestState.test_title)
async def test_section_title_handler(msg: types.Message, state: FSMContext):
    await TestSection.create(title=msg.text)
    tests_section = await TestSection.get_all()
    await state.set_state(AdminTestState.test_section)
    await msg.answer("test 📚", reply_markup=test_menu(tests_section))



@dp.callback_query(lambda call: call.data.__eq__("ignore"), AdminTestState.add_test)
async def ignore_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tests = await Test.get_test_section_id(data.get('test_section_id'))
    await state.set_state(AdminTestState.test)
    await call.message.edit_text(f"Count test {len(tests)}", reply_markup=test_inline())

@dp.callback_query(lambda call : call.data.startswith("test_"), AdminTestState.test_section)
async def test_section_handler(call : types.CallbackQuery , state : FSMContext):
    id = int(call.data.split("_")[1])
    data = await state.get_data()
    data.update({"test_section_id" : id})
    await state.set_data(data)
    tests = await Test.get_test_section_id(id)
    await state.set_state(AdminTestState.test)
    await call.message.edit_text(f"Count test {len(tests)}", reply_markup=test_inline())

@dp.callback_query(lambda call : call.data.__eq__("add_tests"), AdminTestState.test)
async def add_tests_handler(call : types.CallbackQuery , state : FSMContext):
    await state.set_state(AdminTestState.add_test)
    await call.message.edit_text("Test yozilgan excel file tashlang 🗃", reply_markup=ignore())


@dp.message(F.content_type.in_('document') , AdminTestState.add_test)
async def test_document_handler(msg : types.Message , state : FSMContext):
    data = await state.get_data()
    file = await msg.bot.get_file(msg.document.file_id)
    file = await msg.bot.download_file(file.file_path)
    is_save = await read_document_test(file , data.get("test_section_id"))
    tests = await Test.get_test_section_id(data.get('test_section_id'))
    await state.set_state(AdminTestState.test)
    if is_save:await msg.answer(f"Mofaqiyatli saqlandi 🤩\nCount test {len(tests)}", reply_markup=test_inline())
    else: await msg.answer(f"Saqlashda xatolik 😞 \nCount test {len(tests)}", reply_markup=test_inline())



@dp.callback_query(lambda call : call.data.__eq__("delete_test_section"))
async def delete_section_handler(call : types.CallbackQuery , state : FSMContext):
    data = await state.get_data()
    await TestSection.delete(data.get("test_section_id"))
    tests_section = await TestSection.get_all()
    await state.set_state(AdminTestState.test_section)
    await call.message.edit_text("test 📚", reply_markup=test_menu(tests_section))

