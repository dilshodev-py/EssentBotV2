from bot.apps.users.state.main import BookState
from bot.apps.utils import shuffle_vocab, vocab_test_result
from bot.buttons.keyboard import essential_menu
from utils.dispatcher import dp
from aiogram.fsm.context import FSMContext
from aiogram import types , F
from aiogram.utils.markdown import hbold , hitalic



@dp.callback_query(lambda call : call.data.__eq__("start") , BookState.start_stop)
async def start_handler(call : types.CallbackQuery , state : FSMContext):
    data = await state.get_data()
    shuffle_vocabs = await shuffle_vocab(data.get("click_unit"))
    data.update({"vocab": shuffle_vocabs , "step": 0 , "right" : 0 , "wrong" : 0})
    await state.set_data(data)
    vocab = shuffle_vocabs[0]
    await call.message.delete()
    await state.set_state(BookState.vocab_check)
    await call.message.answer(text = f"{hbold('⚠️UZB ➡️ENG')}\nUZB : {hitalic(vocab.uzb)}")

@dp.message(BookState.vocab_check)
async def vocab_check(msg : types.Message , state : FSMContext):
    data = await state.get_data()
    vocabs = data.get("vocab")
    step = data.get("step")
    right = vocabs[step].eng.strip()
    if  right.lower() == msg.text.lower(): data["right"] += 1
    else : data["wrong"] -= 1
    if  right.lower() == msg.text.lower(): await msg.answer("🟢 RIGHT")
    else: await msg.answer(f"🔴 WRONG\n {hbold('Right : ' + right)}")
    data["step"] += 1
    await state.set_data(data)
    if len(vocabs) > step + 1:
        vocab = vocabs[step + 1]
        await state.set_state(BookState.vocab_check)
        await msg.answer(text=f"{hbold('⚠️UZB ➡️ENG')}\nUZB : {hitalic(vocab.uzb)}")
    else:
        right = data.get('right')
        wrong = data.get('wrong')*-1
        await state.set_state(BookState.finish)
        text = await vocab_test_result(msg, right , wrong, 'Essential Vocab')
        await state.set_state(BookState.essential_menu)
        await msg.answer(text = text, reply_markup=essential_menu())








