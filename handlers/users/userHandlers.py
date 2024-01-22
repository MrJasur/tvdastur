from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Command

from data.config import ADMINS
from loader import dp, db, bot

@dp.message_handler(Command('ism'))
async def reply_ism(msg: types.Message):
    await msg.answer(f'Sizning iusmingiz {msg.from_user.full_name}')


@dp.message_handler(Command('users_count'))
async def user_soni(msg: types.Message):
    count = db.count_users()[0]
    print(count)
    all_users = db.select_all_users()
    message = f"Bazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=message)

from aiogram import types  # Assuming you are using aiogram library


@dp.message_handler(commands=['users_name'])
async def user_username(msg: types.Message):
    user = msg.from_user
    admin = user.id
    all_users = db.select_all_users()
    print(all_users)

    # Extracting usernames from the tuples and formatting the message
    names_with_numbers = [f"{i+1}. {user[0]} - {user[1]}\n" for i, user in enumerate(all_users)]
    # usernames = [user[1] for user in all_users]

    message = f"Admin ID: {admin}\nUsers: \n\n{''.join(names_with_numbers)}"
    await bot.send_message(chat_id=ADMINS[0], text=message)



