from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from loader import dp
from keyboards.default.tvmenu import menutv
from aiogram import bot
import requests
from datetime import datetime
from bs4 import BeautifulSoup

today = datetime.now().strftime("%Y-%m-%d")

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

                # Check if the class is 'flex text-sm text-[#EA580C] font-semibold' and add ✅
                if class_name == 'flex text-sm text-gray-400':
                    title_text = f"<s>{title_text}</s>"

                time_title_pairs.append((time_text, title_text))

            all_time_title_pairs.extend(time_title_pairs)

        # Prepare a single message with all time and title pairs
        message_text = '\n'.join([f"🕔 {time},  ➖ {title}" for time, title in all_time_title_pairs])

        # Send the single message
        sent_message = await msg.answer('🔹🔹🔹🔹🔹🔹'+text+'🔹🔹🔹🔹🔹🔹'+'\n\n' + message_text+'\n\n'+'©️tvinfo.uz')


