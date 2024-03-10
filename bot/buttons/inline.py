from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.buttons.text import update, BACK


def update_statist():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=update, callback_data="update")]])


def tools():
    inlines = [
        [InlineKeyboardButton(text="👤 Userga ✍🏻 yuborish 📨", callback_data="user_rek")],
        [InlineKeyboardButton(text="👥 Barchaga ✍🏻 yuborish (tools) 📨", callback_data="users_rek")],
        [InlineKeyboardButton(text="🚻 Foydalanuvchini bloklash🚫", callback_data="user_block")],
        [InlineKeyboardButton(text="🚻 Foydalanuvchini blokdan olish ⭕", callback_data="user_unblock")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inlines)


def admin_account():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Admin 👨🏻‍💻", url="https://t.me/Dilshod_Absaitov")]])


def books_menu(books):
    inlines = []
    tmp = []
    for book in books:
        tmp.append(InlineKeyboardButton(text=book.name, callback_data=f"book_{book.id}"))
        if len(tmp) == 2:
            inlines.append(tmp)
            tmp = []
    inlines.append(tmp)
    inlines.append([InlineKeyboardButton(text="Book add ➕", callback_data="add_book")])
    inlines.append([InlineKeyboardButton(text=BACK, callback_data=BACK)])
    return InlineKeyboardMarkup(inline_keyboard=inlines)


def units_menu(units):
    inlines = []
    tmp = []
    units.sort(key=lambda unit: unit.unit)
    for unit in units:
        tmp.append(InlineKeyboardButton(text=f"Unit {unit.unit}", callback_data=f"unit_{unit.id}"))
        if len(tmp) == 2:
            inlines.append(tmp)
            tmp = []
    inlines.append(tmp)
    inlines.append([InlineKeyboardButton(text="Add Unit ➕", callback_data="add_unit")])
    inlines.append([InlineKeyboardButton(text="Delete Book  🗑", callback_data="delete_book")])
    inlines.append([InlineKeyboardButton(text=BACK, callback_data=BACK)])
    return InlineKeyboardMarkup(inline_keyboard=inlines)


def users_unit_menu(units, click_unit):
    inlines = []
    tmp = []
    units.sort(key=lambda unit: unit.unit)
    for unit in units:
        if unit.id in click_unit:
            text = f"U-{unit.unit}✅"
        else:
            text = f"Unit {unit.unit}"
        tmp.append(InlineKeyboardButton(text=text, callback_data=f"unit_{unit.id}"))
        if len(tmp) == 4:
            inlines.append(tmp)
            tmp = []
    inlines.append(tmp)
    if click_unit: inlines.append([InlineKeyboardButton(text="GO 🟢", callback_data="go_vocab")])
    inlines.append([InlineKeyboardButton(text=BACK, callback_data=BACK)])
    return InlineKeyboardMarkup(inline_keyboard=inlines)


def vocabulary_inline():
    inlines = []
    inlines.append([InlineKeyboardButton(text="Add Vocabulary ➕", callback_data="add_vocabulary")])
    inlines.append([InlineKeyboardButton(text="Delete Unit 🗑", callback_data="delete_unit")])
    inlines.append([InlineKeyboardButton(text=BACK, callback_data=BACK)])
    return InlineKeyboardMarkup(inline_keyboard=inlines)


def test_inline():
    inlines = []
    inlines.append([InlineKeyboardButton(text="Add Tests ➕", callback_data="add_tests")])
    inlines.append([InlineKeyboardButton(text="Delete TestSection 🗑", callback_data="delete_test_section")])
    inlines.append([InlineKeyboardButton(text=BACK, callback_data=BACK)])
    return InlineKeyboardMarkup(inline_keyboard=inlines)


def test_menu(tests):
    inlines = []
    tmp = []
    tests.sort(key=lambda test: test.id)
    for test in tests:
        tmp.append(InlineKeyboardButton(text=f"{test.title}", callback_data=f"test_{test.id}"))
        if len(tmp) == 2:
            inlines.append(tmp)
            tmp = []
    inlines.append(tmp)
    inlines.append([InlineKeyboardButton(text="Add TestSection ➕", callback_data="add_test_section")])
    inlines.append([InlineKeyboardButton(text=BACK, callback_data=BACK)])
    return InlineKeyboardMarkup(inline_keyboard=inlines)


def essential_prev_next(session_book, book, count_book:int):
    if session_book == 1:
        inlines = [[InlineKeyboardButton(text=book.name, callback_data=f"click_{book.id}"),
                    InlineKeyboardButton(text="next ➡️", callback_data=f"next_{session_book + 1}")]]
    elif session_book == count_book:
        inlines = [[InlineKeyboardButton(text="⬅️prev", callback_data=f"prev_{session_book - 1}"),
                    InlineKeyboardButton(text=book.name, callback_data=f"click_{book.id}")]]
    else:
        inlines = [[InlineKeyboardButton(text="⬅️prev", callback_data=f"prev_{session_book - 1}"),
                    InlineKeyboardButton(text=book.name, callback_data=f"click_{book.id}"),
                    InlineKeyboardButton(text="next ➡️", callback_data=f"next_{session_book + 1}")]]
    inlines.append([InlineKeyboardButton(text="STOP ⛔️", callback_data="ignore")])
    return InlineKeyboardMarkup(inline_keyboard=inlines)


def ignore():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Bekor qilish", callback_data="ignore")]])


def close_win():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Oynani yopish 👆", callback_data="close_win")]])


def start_stop():
    start = InlineKeyboardButton(text="Start 🟢", callback_data="start")
    stop = InlineKeyboardButton(text="STOP 🔴", callback_data="stop")
    return InlineKeyboardMarkup(inline_keyboard=[[start, stop]])


def users_test_menu(tests, test_section):
    inlines = []
    tmp = []
    tests.sort(key=lambda test: test.id)
    for test in tests:
        short_name = "".join(map(lambda x: x[0].upper(), test.title.split()))
        if test.id in test_section:
            text = f"{short_name}✅"
        else:
            text = f"{test.title}"
        tmp.append(InlineKeyboardButton(text=text, callback_data=f"test_section_{test.id}"))
        if len(tmp) == 2:
            inlines.append(tmp)
            tmp = []
    inlines.append(tmp)
    if test_section: inlines.append([InlineKeyboardButton(text="GO 🟢", callback_data="go_test")])
    inlines.append([InlineKeyboardButton(text=BACK, callback_data=BACK)])
    return InlineKeyboardMarkup(inline_keyboard=inlines)


def test_abcd():
    a = InlineKeyboardButton(text="a", callback_data="a")
    b = InlineKeyboardButton(text="b", callback_data="b")
    c = InlineKeyboardButton(text="c", callback_data="c")
    d = InlineKeyboardButton(text="d", callback_data="d")
    inlines = [
        [a, b, c, d]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inlines)


def admin_btn():
    admin_in = InlineKeyboardButton(text = "Admin 👨🏻‍💻" , url="https://t.me/Dilshod_Absaitov")
    return InlineKeyboardMarkup(inline_keyboard=[[admin_in]])
