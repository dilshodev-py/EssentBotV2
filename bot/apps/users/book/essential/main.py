from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from bot.apps.users.state.main import BookState
from bot.apps.utils import write_text, write_text_for_go_vocab
from bot.buttons.inline import essential_prev_next, users_unit_menu, close_win, start_stop
from bot.buttons.keyboard import essential_menu
from bot.buttons.text import essential, MEMORIZE, BACK, TO_TRY
from db.model import Book, Unit, Vocabulary
from utils.dispatcher import dp
from aiogram.types.input_media_photo import InputMediaPhoto


@dp.message(F.text.__eq__(essential))
async def essential_user_handler(msg: types.Message, state: FSMContext):
    photo = "https://telegra.ph/file/4c60f0f213a795c75f8de.png"
    text = hbold("Eng Ko'p ishlatiladigan So'lar to'plangan bo'lim 📕")
    await state.set_state(BookState.essential_menu)
    await msg.answer_photo(photo=photo, caption=text, reply_markup=essential_menu())

@dp.callback_query(lambda call : call.data.__eq__("stop") , BookState.start_stop)
@dp.callback_query(lambda call : call.data.__eq__("close_win") , BookState.close_win)
@dp.callback_query(lambda call : call.data.__eq__(BACK), BookState.units)
@dp.callback_query(lambda call : call.data.__eq__(BACK), BookState.try_units)
@dp.callback_query(lambda call : call.data.__eq__("ignore"), BookState.prev_next)
async def ignore_handler(call : types.CallbackQuery , state : FSMContext):
    photo = "https://telegra.ph/file/4c60f0f213a795c75f8de.png"
    text = hbold("Eng Ko'p ishlatiladigan So'zlar to'plangan bo'lim 📕")
    await call.message.delete()
    await state.set_state(BookState.essential_menu)
    await call.message.answer_photo(photo=photo, caption=text, reply_markup=essential_menu())

@dp.message(F.text.__eq__(TO_TRY) , BookState.essential_menu)
@dp.message(F.text.__eq__(MEMORIZE), BookState.essential_menu)
async def memorize_handler(msg: types.Message, state: FSMContext):
    books = await Book.get_all()
    session_book = 1
    books.sort(key=lambda book: book.id)
    book = books[session_book - 1]
    await state.set_data({"books" : books, "method" : msg.text})
    await state.set_state(BookState.prev_next)
    await msg.answer_photo(photo=book.photo, caption=book.name, reply_markup=essential_prev_next(session_book, book, len(books)))



@dp.callback_query(lambda call : call.data.startswith("next_"), BookState.prev_next)
@dp.callback_query(lambda call : call.data.startswith("prev_"), BookState.prev_next)
async def next_handler(call : types.CallbackQuery , state : FSMContext):
    session_book = int(call.data.split("_")[1])
    data = await state.get_data()
    books = data.get("books")
    book = books[session_book - 1]
    await state.set_state(BookState.prev_next)
    await call.message.edit_media(media=InputMediaPhoto(media=book.photo , caption=book.name), reply_markup=essential_prev_next(session_book, book, len(books)))



@dp.callback_query(lambda call : call.data.startswith("click_"))
async def click_book_handler(call : types.CallbackQuery , state : FSMContext):
    id = int(call.data.split("_")[1])
    book = await Book.get(id)
    units = await Unit.get_book_id(id)
    data = await state.get_data()
    data.update({"units" : units , "book": book , "click_unit" : []})
    await state.set_data(data)
    click_unit = []
    if data.get("method") == TO_TRY : await state.set_state(BookState.try_units)
    if data.get("method") == MEMORIZE : await state.set_state(BookState.units)
    await call.message.edit_reply_markup(reply_markup=users_unit_menu(units, click_unit))

@dp.callback_query(lambda call : call.data.startswith("unit_"), BookState.units)
async def unit_click(call : types.CallbackQuery , state : FSMContext):
    id = int(call.data.split('_')[1])
    data = await state.get_data()
    vocabularies = await Vocabulary.get_unit_id(id)
    caption = write_text(vocabularies , data.get("book").icon)
    await state.set_state(BookState.close_win)
    await call.message.edit_caption(caption=caption, reply_markup=close_win())


@dp.callback_query(lambda call : call.data.startswith("unit_"), BookState.try_units)
async def click_unit(call : types.CallbackQuery , state : FSMContext):
    id = int(call.data.split('_')[1])
    data = await state.get_data()
    if not id in data['click_unit']: data['click_unit'].append(id)
    else: data['click_unit'].remove(id)
    markup = users_unit_menu(data.get("units"), data.get("click_unit"))
    await state.set_data(data)
    await state.set_state(BookState.try_units)
    await call.message.edit_reply_markup(inline_message_id=call.inline_message_id,reply_markup=markup)


@dp.callback_query(lambda call : call.data.__eq__("go_vocab"), BookState.try_units)
async def go_vocab_handler(call : types.CallbackQuery , state : FSMContext):
    data = await state.get_data()
    click_unit = data.get("click_unit")
    text = await write_text_for_go_vocab(click_unit)
    await state.set_state(BookState.start_stop)
    await call.message.edit_caption(caption=text, reply_markup=start_stop())
















