import re

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from config import config
from db import request
from main import start

admin_ids = [375959767]
#, 505958678, 314310391
router = Router()
dp = Dispatcher()
bot = Bot(token=config.bot_token.get_secret_value())



