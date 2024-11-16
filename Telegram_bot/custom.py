import json
import requests
import telebot
from config import Bot_TOKEN
from telegram.ext import ConversationHandler
from history import record_query
from high import get_json_data
from config import headers, url

bot = telebot.TeleBot(Bot_TOKEN)

STEP1 = 1
async def custom_json(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Какая пицца/десерт вас интересует. Введите название!')
    return STEP1


def search_product_json(product_name):
    params = {'name': product_name}

    try:
        data = get_json_data(url, headers)
        for product in data:
            if product.get('name') == product_name:
                return product
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

async def search_json(update, context):
    user_data = {}

    user_input = update.message.text

    product_name = user_input
    found_product_api = search_product_json(product_name)

    if found_product_api:
        await update.message.reply_text(f"Найден товар : {found_product_api['name']}\nЦена: {found_product_api['price']}"
                                        f"\n{found_product_api['description']}\n{found_product_api['img']}")
        record_query(update.effective_user.id, product_name)
        return ConversationHandler.END
    else:
        await update.message.reply_text(f"Товар с именем '{product_name}' не найден.")
        record_query(update.effective_user.id, product_name)
        return ConversationHandler.END