from aiogram import types
from loader import dp,bot,db
from keyboards.default.tvmenu import menutv
from data.config import ADMINS
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from aiogram.types import ParseMode
import pytz
import sqlite3
uzbekistan_time = datetime.now(pytz.timezone('Asia/Tashkent'))
today = uzbekistan_time.strftime("%Y-%m-%d")

@dp.message_handler(text='Tv Dasturlar')
async def show_tvdasturlar(msg: types.Message):
    await msg.answer('Kanallardan birini tanlang:', reply_markup=menutv)

async def get_schedule_entries(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all div elements with the specified classes
    class_names = ['flex text-sm text-gray-400', 'flex text-sm text-[#EA580C] font-semibold', 'flex text-sm']
    schedule_entries = {class_name: [] for class_name in class_names}

    for class_name in class_names:
        entries = soup.find_all('div', {'class': class_name})
        schedule_entries[class_name] = entries

    return schedule_entries

@dp.message_handler()
async def tv_handler(msg: types.Message):
    await bot.send_message(chat_id=ADMINS[0], text=f"{msg.from_user.full_name} botdan foydalandi.")
    name = msg.from_user.full_name
    username = msg.from_user.username
    try:
        db.add_user(id=msg.from_user.id,
                    name=name, Username=username)
    except sqlite3.IntegrityError as err:
        await bot.send_message(chat_id=ADMINS[0], text=err)

    text = msg.text
    result = text.lower()

    url = f'https://tvinfo.uz/{result}?date={today}'
    all_time_title_pairs = []

    schedule_entries = await get_schedule_entries(url)

    if schedule_entries:
        for class_name, entries in schedule_entries.items():
            time_title_pairs = []

            for entry in entries:
                time_text = entry.find('div', {'class': 'w-12 shrink-0'}).get_text(strip=True)
                title_text = entry.find('div', {'class': ''}).get_text(strip=True)

                # Check if the class is 'flex text-sm text-[#EA580C] font-semibold' and add ✅
                if class_name == 'flex text-sm text-[#EA580C] font-semibold':
                    title_text += ' ✅'

                # Check if
                if class_name == 'flex text-sm text-gray-400':
                    title_text = f"<s>{title_text}</s>"

                time_title_pairs.append((time_text, title_text))

            all_time_title_pairs.extend(time_title_pairs)

        # Prepare a single message with all time and title pairs
        message_text = '\n'.join([f"🕔 {time},  ➖ {title}" for time, title in all_time_title_pairs])

        forchannel = '🔹🔹🔹🔹🔹🔹'+text+'🔹🔹🔹🔹🔹🔹'+'\n\n' + message_text+'\n\n'+'📆'+today+'\n'+'©️tvinfo.uz'
        # Send the single message
        await msg.answer('🔹🔹🔹🔹🔹🔹'+text+'🔹🔹🔹🔹🔹🔹'+'\n\n'+ message_text+'\n\n'+'📆'+today+'\n'+'©️tvinfo.uz')
        admin = msg.from_user.id
        ADMIN = [1011037193]
        if admin in ADMIN:
            await dp.bot.send_message(chat_id=-1001261169916, text=f"{forchannel}", parse_mode=ParseMode.HTML)



