from aiogram import types, F
from aiogram.fsm.context import FSMContext


from bot.apps.admin.state.main import AdminSettingsState, AdminBookState
from bot.buttons.inline import units_menu, books_menu, ignore
from bot.buttons.text import BACK
from db.model import Book, Unit
from utils.dispatcher import dp


@dp.callback_query(lambda call : call.data.__eq__(BACK),AdminBookState.vocabulary)
@dp.callback_query(lambda call : call.data.__eq__("ignore"),AdminBookState.unit_num)
async def ignore_handler(call: types.CallbackQuery , state : FSMContext):
    data = await state.get_data()
    book = await Book.get(data.get("book_id"))
    units = await Unit.get_book_id(book.id)
    await state.set_state(AdminBookState.unit)
    await call.message.delete()
    await call.message.answer_photo(photo=book.photo, caption=book.name, reply_markup=units_menu(units))


@dp.callback_query(lambda call : call.data.startswith("book_"),AdminSettingsState.book)
async def book_handler(call : types.CallbackQuery , state : FSMContext):
    id = int(call.data.split("_")[1])
    data = await state.get_data()
    data.update({"book_id" : id})
    await state.set_data(data)
    book = await Book.get(id)
    units = await Unit.get_book_id(book.id)
    await state.set_state(AdminBookState.unit)
    await call.message.delete()
    await call.message.answer_photo(photo=book.photo, caption = book.name, reply_markup=units_menu(units))

@dp.callback_query(lambda call : call.data.__eq__("delete_book"),AdminBookState.unit)
async def delete_book(call: types.CallbackQuery , state : FSMContext):
    data = await state.get_data()
    await Book.delete(data.get("book_id"))
    books = await Book.get_all()
    await call.message.delete()
    await state.set_state(AdminSettingsState.book)
    await call.message.answer("Mofaqiyatli kitob o'chirildi 📔", reply_markup=books_menu(books))


@dp.callback_query(lambda call : call.data.__eq__("add_unit"), AdminBookState.unit)
async def add_unit_handler(call : types.CallbackQuery , state : FSMContext):
    await state.set_state(AdminBookState.unit_num)
    await call.message.answer("Unit raqamini kiriting ✍🏻", reply_markup=ignore())
    await call.message.delete()

@dp.message(F.text.isdigit(),AdminBookState.unit_num)
async def unit_num_handler(msg : types.Message, state : FSMContext):
    data = await state.get_data()
    await Unit.create(unit = int(msg.text) , book_id = data.get("book_id"))
    units = await Unit.get_book_id(data.get("book_id"))
    book = await Book.get(data.get("book_id"))
    await state.set_state(AdminBookState.unit)
    await msg.answer_photo(photo=book.photo,caption="Mofaqiyatli unit qo'shildi 🤩", reply_markup=units_menu(units))







