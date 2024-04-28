import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.filters import Command
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

#import keyboards as k
#import videos as v
from config import config
#from db import createtables, profile

load_dotenv()

router = Router()

@router.message(Command('id_v'))
async def handle_video(message: types.Message):
    video_id = message.video.file_id
    await message.reply(f"ID вашего видео: {video_id}")

@router.message(Command('id_p'))
async def handle_photo(message: types.Message):
    photo_id = message.photo[-1].file_id
    await message.reply(f"ID вашего фото: {photo_id}")
