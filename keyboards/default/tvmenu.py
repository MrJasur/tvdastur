from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
menutv = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Sevimli-Tv'),
            KeyboardButton(text='Zor-Tv'),
            KeyboardButton(text='Milliy-Tv')
        ],
        [
            KeyboardButton(text='Mening-Yurtim'),
            KeyboardButton(text='FTVuz'),
            KeyboardButton(text='RenessansTV')
        ],
[
            KeyboardButton(text='Kinoteatr'),
            KeyboardButton(text='Yoshlar'),
            KeyboardButton(text='Toshkent')
        ],
[
            KeyboardButton(text='Mahalla'),
            KeyboardButton(text='Uzbekistan'),
            KeyboardButton(text='Sport-Tv')
        ],
[
            KeyboardButton(text='Uzbekistan-24'),
            KeyboardButton(text='UzReport'),
            KeyboardButton(text='Aqlvoy')
        ],
[
            KeyboardButton(text='Bolajon'),
            KeyboardButton(text='Navo'),
            KeyboardButton(text='KinoteatrUz')
        ],
[
            KeyboardButton(text='Madaniyat-va-Marifat'),
            KeyboardButton(text='Dunyo-Boylab'),
        ],
    ],
    resize_keyboard=True
)