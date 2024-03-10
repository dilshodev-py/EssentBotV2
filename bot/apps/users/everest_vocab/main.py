from random import shuffle

from aiogram import types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold, hitalic

from bot.apps import vocab_test_result
from bot.apps.users.state.main import UserEverestVocab, BookState
from bot.buttons.keyboard import main_menu
from db.model import EverestVocab
from utils.dispatcher import dp


@dp.message(Command('everest_vocab'))
async def start_handler(msg : types.Message , state : FSMContext):
    data = await state.get_data()
    vocabs = await EverestVocab.get_all()
    shuffle(vocabs)
    data.update({"vocab": vocabs , "step": 0 , "right" : 0 , "wrong" : 0})
    await state.set_data(data)
    vocab = vocabs[0]
    await msg.delete()
    await state.set_state(UserEverestVocab.vocab_check)
    await msg.answer(text = f"{hbold('⚠️UZB ➡️ENG')}\nUZB : {hitalic(vocab.uzb)}")

@dp.message(UserEverestVocab.vocab_check)
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
        await state.set_state(UserEverestVocab.vocab_check)
        await msg.answer(text=f"{hbold('⚠️UZB ➡️ENG')}\nUZB : {hitalic(vocab.uzb)}")
    else:
        right = data.get('right')
        wrong = data.get('wrong')*-1
        await state.set_state(UserEverestVocab.finish)
        text = await vocab_test_result(msg, right , wrong)
        await state.set_state(BookState.essential_menu)
        await msg.answer(text=text, reply_markup=main_menu())