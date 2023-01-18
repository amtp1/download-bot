from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start_markup = ReplyKeyboardMarkup(resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="YouTube or YouTube Music")], [KeyboardButton(text="Instagram Stories")],
        [KeyboardButton(text="❗️Help")]
    ]
)

stream_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Audio", callback_data="audio")],
        [InlineKeyboardButton(text="Video", callback_data="video")]
    ]
)
