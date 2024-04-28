from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_1 = InlineKeyboardButton(text='Записаться на мастер-класс', callback_data='mk')
btn_2 = InlineKeyboardButton(text='Помогите нам стать лучше', callback_data='pool')

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[btn_1],
                     [btn_2]
                     ]
)
