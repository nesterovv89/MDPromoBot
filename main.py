import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.filters import Command
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram.types import CallbackQuery

import keyboards as k
#import videos as v
import admin
import re

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from config import config
from db import request
import pool
from config import config
from db import createtables, profile, pooling

load_dotenv()


logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
#router = Router
admin_ids = [375959767]
#, 505958678, 314310391

@dp.message(Command('start'))
async def start(message: types.Message):
    name = message.from_user.full_name
    await message.answer_photo(photo='AgACAgIAAxkBAAMiZi3-jyfOKrgOKngKBNcWFwzE3rwAAn3dMRsg0HFJDsneiDV8n9cBAAMCAAN5AAM0BA', caption=f'Hey {name}. You are welcome', reply_markup=k.keyboard)
    await profile(user_id=message.from_user.id, name=message.from_user.full_name, surname=message.from_user.last_name)
    #await message.answer_video(video=v.START_1)
    #await asyncio.sleep(4)
    #await message.answer_video(video=v.START_2, reply_markup=k.keyboard)
    #await profile(user_id=message.from_user.id, name=message.from_user.full_name, surname=message.from_user.last_name)

class ToState(StatesGroup):
    name = State()
    age = State()
    comment = State()


@dp.callback_query(StateFilter(None), F.data == 'mk')
async def name(callback: CallbackQuery, state: FSMContext):
    if callback.message.text:
        await callback.message.edit_text(
                text='Введите ваше имя',
            )
    else:
        await callback.message.answer(
            text='Введите ваше имя:',
        )
    await state.set_state(ToState.name)

@dp.message(ToState.name)
async def age(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    await message.answer(
        text='Укажите возраст ребёнка:',
    )
    await state.set_state(ToState.age)


@dp.message(ToState.age)
async def comment(message: Message, state: FSMContext):
    await state.update_data(age=message.text.lower())
    await message.answer(
        text='Укажите свой номер в формате "+00000000000"',
    )
    await state.set_state(ToState.comment)

@dp.message(ToState.comment)
async def result(message: Message, state: FSMContext):
    if re.match(r'^\+?\d+$', message.text):
        await state.update_data(comment=message.text.lower())
        user_data = await state.get_data()
        await message.answer(
            text=f"Ваше имя ***{user_data['name']}***, возраст {user_data['age']}, контактный номер {user_data['comment']}\n"
                f'С вами свяжутся в ближайшее время',
            parse_mode=ParseMode.MARKDOWN
        )
        text=f"Заявка с бота на МК: Имя {user_data['name']}, возраст {user_data['age']}, контактный номер {user_data['comment']}\n"
        await request(user_id=message.from_user.id, name=user_data['name'], age=user_data['age'], contact=user_data['comment'])
        for admin in admin_ids:
            await bot.send_message(admin, text=text)
        await start(message)
        await state.clear()
    else:
        await message.answer(text='Пожалуйста, введите свой номер в правильном формате.')


class Pool(StatesGroup):
    what = State()
    age = State()
    wish = State()

@dp.callback_query(StateFilter(None), F.data == 'pool')
async def name(callback: CallbackQuery, state: FSMContext):
    if callback.message.text:
        await callback.message.edit_text(
                text='Чему сейчас обучается ваш ребенок?',
            )
    else:
        await callback.message.answer(
            text='Чему сейчас обучается ваш ребенок?',
        )
    await state.set_state(Pool.what)

@dp.message(Pool.what)
async def age(message: Message, state: FSMContext):
    await state.update_data(what=message.text.capitalize())
    await message.answer(
        text='Укажите возраст ребёнка:',
    )
    await state.set_state(Pool.age)

@dp.message(Pool.age)
async def comment(message: Message, state: FSMContext):
    await state.update_data(age=message.text.lower())
    await message.answer(
        text='Какой мастер-класс вы хотели бы посетить?',
    )
    await state.set_state(Pool.wish)

@dp.message(Pool.wish)
async def result(message: Message, state: FSMContext):
    await state.update_data(wish=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text='Благодарим Вас за участие в опросе! Ваше мнение очень важно для нас!'
    )
    text=f"Опрос: Сейчас посещает: {user_data['what']}, возраст: {user_data['age']}, Что бы хотели: {user_data['wish']}\n"
    await pooling(user_id=message.from_user.id, what=user_data['what'], age=user_data['age'], wish=user_data['wish'])
    for admin in admin_ids:
        await bot.send_message(admin, text=text)
    await start(message)
    await state.clear()

async def main():
    await createtables()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())