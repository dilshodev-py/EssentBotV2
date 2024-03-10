from aiogram import types, F
from aiogram.fsm.context import FSMContext

from bot.apps.users.state.main import TestState
from bot.apps.utils import write_text_for_go_test, shuffle_test, text_shablon_test, test_result_text
from bot.buttons.inline import users_test_menu, start_stop, test_abcd
from bot.buttons.keyboard import essential_menu, main_menu
from bot.buttons.text import test
from db.model import TestSection
from utils.dispatcher import dp
from aiogram.utils.markdown import hbold


@dp.message(F.text.__eq__(test))
async def book_handler(msg: types.Message, state : FSMContext):
    photo = "https://telegra.ph/file/dd5488f52098b8ff07f6d.png"
    tests_section = await TestSection.get_all()
    data = {"test_section" : [] , "tests" : tests_section}
    await state.set_data(data)
    await state.set_state(TestState.test_section)
    await msg.answer_photo(photo=photo, caption="Test bo'limi !", reply_markup=users_test_menu(data.get("tests") , data.get("test_section")))


@dp.callback_query(lambda call : call.data.startswith("test_section_"))
async def test_section_handler(call : types.CallbackQuery , state : FSMContext):
    id = int(call.data.split("test_section_")[1])
    data = await state.get_data()
    if not id in data['test_section']: data['test_section'].append(id)
    else: data['test_section'].remove(id)
    await state.set_data(data)
    await state.set_state(TestState.test_section)
    await call.message.edit_caption(reply_markup=users_test_menu(data.get("tests") , data.get("test_section")))


@dp.callback_query(lambda call : call.data.__eq__("go_test"), TestState.test_section)
async def go_vocab_handler(call : types.CallbackQuery , state : FSMContext):
    data = await state.get_data()
    click_unit = data.get("test_section")
    text = await write_text_for_go_test(click_unit)
    await state.set_state(TestState.start_stop)
    await call.message.edit_caption(caption=text, reply_markup=start_stop())


@dp.callback_query(lambda call : call.data.__eq__("start"))
async def start_test_handler(call : types.CallbackQuery , state : FSMContext):
    data = await state.get_data()
    shuffle_tests = await shuffle_test(data.get("test_section"))
    test = shuffle_tests[0]
    data.update({"tests": shuffle_tests, "step": 0, "right": 0, "wrong": 0 , "true_val":test.right})
    await state.set_data(data)
    await call.message.delete()
    await state.set_state(TestState.test_check)
    text = text_shablon_test(test)
    await call.message.answer(text=text , reply_markup=test_abcd())


@dp.callback_query(TestState.test_check)
async def test_option_handler(call : types.CallbackQuery , state : FSMContext):
    data = await state.get_data()
    tests = data.get('tests')
    if call.data == data.get("true_val") : data["right"] += 1
    else: data["wrong"] += 1
    if call.data == data.get("true_val") : await call.message.answer("🟢 to'g'ri javob 🤩")
    else:  await call.message.answer(f"🔴 xatto | to'gri javob : {hbold(data.get('true_val'))}")
    if len(tests) > data.get('step')+1:
        data["step"] += 1
        test = tests[data.get("step")]
        data["true_val"] = test.right
        await state.set_data(data)
        test = tests[data.get("step")]
        await call.message.delete()
        await state.set_state(TestState.test_check)
        text = text_shablon_test(test)
        await call.message.answer(text=text, reply_markup=test_abcd())
    else:
        right = data.get('right')
        wrong = data.get('wrong')
        await state.set_state()

        text = await test_result_text(call, right, wrong)
        await call.message.delete()
        await state.set_state(TestState.test_section)
        await call.message.answer(text=text, reply_markup=main_menu())





