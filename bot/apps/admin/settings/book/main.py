from aiogram import F, types
from aiogram.fsm.context import FSMContext

from bot.apps.admin.state.main import AdminSettingsState, AdminBookState
from bot.apps.utils import check_url
from bot.buttons.inline import books_menu, ignore
from bot.buttons.text import book, BACK, panel_book
from db.model import Book
from utils.dispatcher import dp


@dp.callback_query(lambda call: call.data.__eq__(BACK), AdminBookState.unit)
@dp.callback_query(lambda call: call.data.__eq__("ignore"), AdminBookState.photo)
@dp.callback_query(lambda call: call.data.__eq__("ignore"), AdminBookState.name)
async def ignore_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    books = await Book.get_all()
    await state.set_state(AdminSettingsState.book)
    await call.message.answer("Books 📚", reply_markup=books_menu(books))


@dp.message(F.text.__eq__(panel_book), AdminSettingsState.settings_menu)
async def book_settings_handler(msg: types.Message, state: FSMContext):
    books = await Book.get_all()
    await state.set_state(AdminSettingsState.book)
    await msg.answer("Books 📚", reply_markup=books_menu(books))


@dp.callback_query(lambda call: call.data.__eq__("add_book"), AdminSettingsState.book)
async def add_book_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Kitob nomini kiriting ✍🏻", reply_markup=ignore())
    await state.set_state(AdminBookState.name)

@dp.message(AdminBookState.name)
async def book_name_handler(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    data.update({"name": msg.text})
    await state.set_data(data)
    await state.set_state(AdminBookState.icon)
    text = "Kitob uchun belgi kiriting ! .🔰.🔻.🔸.🔹"
    await msg.answer(text, reply_markup=ignore())



@dp.message(AdminBookState.icon)
async def book_name_handler(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    data.update({"icon": msg.text.split(".")[1]})
    await state.set_data(data)
    await state.set_state(AdminBookState.photo)
    text = "https://telegra.ph/ \n👆quydagi link orqali kitob rasmini joylab linkini yuboring !"
    await msg.answer(text, reply_markup=ignore())


@dp.message(AdminBookState.photo)
async def book_photo(msg: types.Message, state: FSMContext):
    is_url = await check_url(msg.text)
    if not is_url:
        await msg.answer("Uzr bunday linkda rasm joylanmagan !😞 \nQayta urinib ko'ring 🔄", reply_markup=ignore())
    else:
        data = await state.get_data()
        await Book.create(name=data.get("name"), photo=msg.text, icon = data.get('icon'))
        await state.set_state(AdminSettingsState.book)
        books = await Book.get_all()
        await msg.answer("Mofaqiyatli saqlandi 🤩", reply_markup=books_menu(books))
