import telebot
from config import Bot_TOKEN
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3
from low import find_cheapest_product
from high import find_most_expensive_product
from custom import custom_json, search_json
from history import history


bot = telebot.TeleBot(Bot_TOKEN)
async def start(update, context):
    user = update.message.from_user
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Привет, {user.first_name}!, я Бот-помощник, буду помогать вам с выбором десертов!')
    await show_menu(update, context)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                query TEXT
            )
        ''')
    conn.commit()
    conn.close()
async def show_menu(update, context):
    keyboard = [
        [InlineKeyboardButton("/low - функция поиска десерта с самой низкой стоимостью", callback_data='button1')],
        [InlineKeyboardButton("/high - функция поиска десерта с самой высокой стоимостью", callback_data='button2')],
        [InlineKeyboardButton('history - фукнция получения истории по последним 10 запросам', callback_data='button3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите опцию:', reply_markup=reply_markup)
    await update.message.reply_text('Также наберите функцию "/custom" для поиска товаров по названию')

async def button_click(update, context):
    query = update.callback_query
    if query:
        await query.answer()
        if query.data == 'button1':
            await find_cheapest_product(update, context)
        elif query.data == 'button2':
            await find_most_expensive_product(update, context)
        elif query.data == 'button3':
            await history(update, context)
