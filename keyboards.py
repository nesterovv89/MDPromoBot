from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_1 = InlineKeyboardButton(text='Записаться на мастер-класс', callback_data='mk')
btn_0 = InlineKeyboardButton(text='Записаться на мастер-класс', callback_data='mk_prev')
btn_2 = InlineKeyboardButton(text='Помогите нам стать лучше', callback_data='pool')
btn_3 = InlineKeyboardButton(text='Главное меню', callback_data='mm')
btn_4 = InlineKeyboardButton(text='Рецепт', callback_data='recipe')
btn_5 = InlineKeyboardButton(text='Ещё рецепты', callback_data='recipe_2')

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[btn_4],
                     [btn_0],
                     [btn_2],
                     ]
)

keyboard_2 = InlineKeyboardMarkup(
    inline_keyboard=[[btn_3]]
)

keyboard_3 = InlineKeyboardMarkup(
    inline_keyboard=[[btn_0],
                     [btn_2],
                     [btn_5],
                     [btn_3],
                     ]
)

keyboard_4 = InlineKeyboardMarkup(
    inline_keyboard=[[btn_1]]
)