from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

yes_or_no = InlineKeyboardMarkup(row_width=2,inline_keyboard=[

    [
        InlineKeyboardButton(text="Degen Call 🎲", callback_data="Degen"),
    ],
    [
        InlineKeyboardButton(text="Alpha Call 👑", callback_data="Alpha"),
    ],
    [
        InlineKeyboardButton(text="No ⛔️", callback_data="no"),
    ]
])
