from aiogram.fsm.state import StatesGroup , State
class AdminState(StatesGroup):
    block_id = State()
    unblock_id = State()
    id = State()
    message = State()
    for_users_message = State()

class AdminSettingsState(StatesGroup):
    settings_menu = State()
    book = State()

class AdminBookState(StatesGroup):
    name = State()
    icon = State()
    photo = State()
    unit = State()
    unit_num = State()
    vocabulary = State()
    vocab_file = State()

class AdminTestState(StatesGroup):
    test_section = State()
    test_title = State()
    test = State()
    add_test = State()

class AdminEverestVocabState(StatesGroup):
    vocabulary = State()
    vocab_file = State()
    back = State()





