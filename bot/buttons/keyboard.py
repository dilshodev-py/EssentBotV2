from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.buttons.text import book, IELTS, games, admin, statistik_admin, settings_admin, tools_admin, book, test, \
    BACK, essential, MEMORIZE, TO_TRY, panel_book, admin_test, panel_grammar, EVEREST_VOCAB


def main_menu():
    keyboards = [
        [KeyboardButton(text=book) , KeyboardButton(text=IELTS)],
        [KeyboardButton(text=test) , KeyboardButton(text=admin)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboards ,resize_keyboard=True, one_time_keyboard=True)


def admin_menu():
    keyboards = [
        [KeyboardButton(text=statistik_admin), KeyboardButton(text=settings_admin)],
        [KeyboardButton(text=tools_admin)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboards ,resize_keyboard=True)

def settings_menu():
    keyboards = [
        [KeyboardButton(text = panel_book) , KeyboardButton(text = admin_test) , KeyboardButton(text = panel_grammar)],
        [KeyboardButton(text = IELTS), KeyboardButton(text = EVEREST_VOCAB), KeyboardButton(text= BACK)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboards ,resize_keyboard=True,one_time_keyboard=True)

def books_user_menu():
    keyboards = [
        [KeyboardButton(text = essential) , KeyboardButton(text = "Book2")],
        [KeyboardButton(text = "Book3") , KeyboardButton(text = BACK)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboards , resize_keyboard=True, one_time_keyboard=True)

def essential_menu():
    keyboards = [
        [KeyboardButton(text = MEMORIZE) , KeyboardButton(text = TO_TRY)],
        [KeyboardButton(text = BACK)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboards , resize_keyboard=True, one_time_keyboard=True)

