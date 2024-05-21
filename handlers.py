import os

from aiogram import Bot, F, types, Router
from aiogram.filters import Command
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from states import ToState, Pool
import keyboards as k
import images as i
import texts as t
import re

from aiogram import Bot, F
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery, Message

from config import config
from db import request
from db import profile, pooling, check_user_existence


router = Router()
admin_ids = os.getenv('ADMINS')
admin_ids = list(map(int, admin_ids.split(',')))
bot = Bot(token=config.bot_token.get_secret_value())

@router.message(Command('start'))
async def start(message: types.Message):
    name = message.from_user.full_name
    #text = t.CONGRATULATION caption=f'{name}, {text}', 
    await message.answer_photo(photo=i.START, reply_markup=k.keyboard, parse_mode=ParseMode.MARKDOWN)
    await profile(user_id=message.from_user.id, name=message.from_user.full_name, surname=message.from_user.last_name)
    #await message.answer_video(video=v.START_1)
    #await asyncio.sleep(4)
    #await message.answer_video(video=v.START_2, reply_markup=k.keyboard)
    #await profile(user_id=message.from_user.id, name=message.from_user.full_name, surname=message.from_user.last_name)

@router.callback_query(F.data == 'recipe')
async def recipe(callback: types.CallbackQuery):
    await callback.message.answer_video(video=i.HOW_VIDEO, reply_markup=k.keyboard_3) 

#@dp.callback_query(F.data == 'recipe_2')
#async def recipe_2(callback: types.CallbackQuery):
#    await callback.message.answer_video(video=random.choice(recipes), reply_markup=k.keyboard_3) 


@router.callback_query(F.data == 'mm')
async def main_menu(callback: CallbackQuery):
    await callback.message.answer(text='Главное Меню:', reply_markup=k.keyboard)

@router.callback_query(F.data == 'mk_prev')
async def main_menu(callback: CallbackQuery):
    await callback.message.answer_photo(photo=i.MK, caption=t.MK, reply_markup=k.keyboard_4, parse_mode=ParseMode.MARKDOWN)


@router.callback_query(StateFilter(None), F.data == 'mk')
async def name(callback: CallbackQuery, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Главное меню')]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
    await callback.message.answer(
            text='Введите ваше имя:',
            reply_markup=keyboard
        )
    await state.set_state(ToState.name)

@router.message(ToState.name)
async def age(message: Message, state: FSMContext):
    if message.text == 'Главное меню':
        await start(message)
        await state.set_state(None)
    else:    
        await state.update_data(name=message.text.capitalize())
        await message.answer(
            text='Укажите возраст ребёнка:',
        )
        await state.set_state(ToState.age)


@router.message(ToState.age)
async def comment(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Главное меню')]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
    if message.text == 'Главное меню':
        await start(message)
        await state.set_state(None)
    else:
        await state.update_data(age=message.text.lower())
        await message.answer(
            text='Укажите свой номер в формате "+00000000000"',
            reply_markup=keyboard
        )
        await state.set_state(ToState.comment)

@router.message(ToState.comment)
async def result(message: Message, state: FSMContext):
    if message.text == 'Главное меню':
        await start(message)
        await state.set_state(None)
    elif re.match(r'^\+?\d+$', message.text):
        k_2 = ReplyKeyboardRemove()
        await state.update_data(comment=message.text.lower())
        user_data = await state.get_data()
        await message.answer(
            text=f"Ваше имя ***{user_data['name']}***, возраст {user_data['age']}, контактный номер {user_data['comment']}\n"
                f'С вами свяжутся в ближайшее время',
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=k_2
        )
        text=f"Заявка на МК: Имя {user_data['name']}, возраст {user_data['age']}, контактный номер {user_data['comment']}\n"
        await request(user_id=message.from_user.id, name=user_data['name'], age=user_data['age'], contact=user_data['comment'])
        for admin in admin_ids:
            await bot.send_message(admin, text=text)
        await start(message)
        await state.set_state(None)
    else:
        await message.answer(text='Пожалуйста, введите свой номер в правильном формате.')


@router.callback_query(StateFilter(None), F.data == 'pool')
async def name(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if not await check_user_existence(user_id):
        if callback.data == 'pool':
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Игры настольные, шахматы'), KeyboardButton(text='Архитектурный клуб, мастер-класс')],
                    [KeyboardButton(text='Живопись, мастер-класс'), KeyboardButton(text='Йога-утро')],
                    [KeyboardButton(text='Научные опыты'), KeyboardButton(text='Арт-терапия для детей')],
                    [KeyboardButton(text='Коммуникационный тренинг'), KeyboardButton(text='Ваш вариант')],
                    [KeyboardButton(text='Главное меню')],
                ],
                resize_keyboard=True,
                one_time_keyboard=True,
            )
            await callback.message.answer('Какой формат мероприятий для вас интересен?', reply_markup=keyboard)
            await state.set_state(Pool.what)
    else:
        keyboard_markup = ReplyKeyboardRemove()
        await callback.message.answer(text=f'Вы уже проходили опрос.', reply_markup=keyboard_markup)

@router.message(Pool.what)
async def custom_option(message: types.Message, state: FSMContext):
    #keyboard_markup = ReplyKeyboardRemove()
    keyboard_mm = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text='Главное меню')]
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
    if message.text == 'Главное меню':
        await start(message)
        await state.set_state(None)
    elif message.text == 'Ваш вариант':
        await message.answer('Введите ваш вариант:', reply_markup=keyboard_mm)
        await state.set_state(Pool.what)
    else: 
        await state.update_data(what=message.text.capitalize())
        await message.answer('Укажите возраст ребёнка:', reply_markup=keyboard_mm)
        await state.set_state(Pool.age)

@router.message(Pool.age)
async def result(message: Message, state: FSMContext):
    if message.text == 'Главное меню':
        await start(message)
        await state.set_state(None)
    else:
        await state.update_data(age=message.text.lower())
        user_data = await state.get_data()
        keyboard_markup = ReplyKeyboardRemove()
        await message.answer(
            text='Благодарим Вас за участие в опросе! Ваше мнение очень важно для нас!', reply_markup=keyboard_markup
        )
        text=f"Опрос: Желает посещать: {user_data['what']}, возраст: {user_data['age']}, id_tg: {message.from_user.id}\n"
        await pooling(user_id=message.from_user.id, what=user_data['what'], age=user_data['age'])
        for admin in admin_ids:
            await bot.send_message(admin, text=text)
        await start(message)
        await state.clear()
