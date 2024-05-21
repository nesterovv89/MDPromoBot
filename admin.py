import os

from aiogram import Bot, types, Router
from aiogram.filters import Command
from aiogram.filters import BaseFilter, Command
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import config
from db import users

load_dotenv()

admin_ids = os.getenv('ADMINS')
admin_ids = list(map(int, admin_ids.split(',')))
router = Router()
bot = Bot(token=config.bot_token.get_secret_value())

@router.message(Command('id_v'))
async def handle_video(message: types.Message):
    video_id = message.video.file_id
    await message.reply(f"ID вашего видео: {video_id}")

@router.message(Command('id_p'))
async def handle_photo(message: types.Message):
    photo_id = message.photo[-1].file_id
    await message.reply(f"ID вашего фото: {photo_id}")


class IsAdmin(BaseFilter):
    def __init__(self, admin_ids) -> None:
        self.admin_ids = admin_ids
    
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids
    
class Mailing(StatesGroup):
    draft = State()

@router.message(Command('mailing'), IsAdmin(admin_ids))
async def create_message(message: types.Message, state: FSMContext):
    await message.answer('Напишите сообщение для рассылки')
    await state.set_state(Mailing.draft)

@router.message(Command('stop_mailing'), IsAdmin(admin_ids))
async def cancel_mailing(message: types.Message, state: FSMContext):
    await message.answer('Рассылка отменена')
    await state.clear()

@router.message(IsAdmin(admin_ids), Mailing.draft)
async def mailing(message: types.Message, state: FSMContext):
    state_message = message.text
    chat_id = message.chat.id
    user_ids = await users()
    members = len(user_ids)
    for member in user_ids:
        user_id = member
        if message.text:
            await bot.send_message(user_id, state_message)
        if message.photo:
            await bot.send_photo(user_id, photo=message.photo[0].file_id, caption=message.caption)
        if message.video:
            await bot.send_video(user_id, video=message.video.file_id, caption=message.caption)
    await message.answer(f'Рассылка успешно завершена!, отправлено {members} сообщений')
    await state.clear()
