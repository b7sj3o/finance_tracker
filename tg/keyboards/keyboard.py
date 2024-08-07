from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Register", callback_data="register")],
            [InlineKeyboardButton(text="Login", callback_data="login")]
        ]
    )
    return keyboard
