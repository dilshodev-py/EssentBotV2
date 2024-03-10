from bot.apps.admin.state.main import AdminBookState
from bot.apps.utils import create_text_vocab, read_excel
from bot.buttons.inline import vocabulary_inline, units_menu, ignore
from db.model import Unit, Vocabulary, Book
from utils.dispatcher import dp
from aiogram import types , F
from aiogram.fsm.context import FSMContext



@dp.callback_query(lambda call : call.data.__eq__("ignore"),AdminBookState.vocab_file)
async def ignore_handler(call : types.CallbackQuery , state : FSMContext):
    data = await state.get_data()
    id = data.get("unit_id")
    await call.message.delete()
    await state.set_state(AdminBookState.vocabulary)
    unit = await Unit.get(id)
    vocabularies = await Vocabulary.get_unit_id(id)
    text = await create_text_vocab(vocabularies)
    await call.message.answer(f"Unit {unit.unit}\n{text}", reply_markup=vocabulary_inline())


@dp.callback_query(lambda call : call.data.startswith("unit_"),AdminBookState.unit)
async def book_handler(call : types.CallbackQuery , state : FSMContext):
    id = int(call.data.split("_")[1])
    data = await state.get_data()
    data.update({"unit_id" :id })
    await state.set_data(data)
    await call.message.delete()
    await state.set_state(AdminBookState.vocabulary)
    unit = await Unit.get(id)
    vocabularies = await Vocabulary.get_unit_id(id)
    text = await create_text_vocab(vocabularies)
    await call.message.answer(f"Unit {unit.unit}\n{text}", reply_markup=vocabulary_inline())

@dp.callback_query(lambda call : call.data.__eq__("delete_unit"), AdminBookState.vocabulary)
async def delete_unit_handler(call : types.CallbackQuery , state : FSMContext):
    data = await state.get_data()
    await Unit.delete(data.get("unit_id"))
    book = await Book.get(data.get("book_id"))
    units = await Unit.get_book_id(book.id)
    await state.set_state(AdminBookState.unit)
    await call.message.delete()
    await call.message.answer_photo(photo=book.photo, caption="Mofaqiyatli unit o'chirildi 😊", reply_markup=units_menu(units))

@dp.callback_query(lambda call : call.data.__eq__("add_vocabulary") , AdminBookState.vocabulary)
async def add_vocab_handler(call : types.CallbackQuery , state :FSMContext):
    await call.message.delete()
    await state.set_state(AdminBookState.vocab_file)
    await call.message.answer("Vocabulary yozilgan excel file tashlang 🗃", reply_markup=ignore())

@dp.message(F.content_type.in_("document") , AdminBookState.vocab_file)
async def vocab_file_handler(msg : types.Message , state : FSMContext):
    data = await state.get_data()
    file = await msg.bot.get_file(msg.document.file_id)
    file = await msg.bot.download_file(file.file_path)
    await read_excel(file , data.get("unit_id"))
    await state.set_state(AdminBookState.vocabulary)
    unit = await Unit.get(data.get("unit_id"))
    vocabularies = await Vocabulary.get_unit_id(unit.id)
    text = await create_text_vocab(vocabularies)
    await msg.answer(f"Unit {unit.unit}\n{text}", reply_markup=vocabulary_inline())

