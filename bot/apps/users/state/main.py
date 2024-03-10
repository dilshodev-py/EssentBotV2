from aiogram.fsm.state import StatesGroup, State


class BookState(StatesGroup):
    essential_menu = State()
    prev_next = State()
    units = State()
    close_win = State()
    try_units = State()
    start_stop = State()
    vocab_check = State()
    finish = State()

class TestState(StatesGroup):
    test_section = State()
    start_stop = State()
    test_check = State()
    finish = State()

class UserEverestVocab(StatesGroup):
    vocab_check = State()
    finish = State()