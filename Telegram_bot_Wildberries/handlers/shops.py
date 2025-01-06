import json
from aiogram import types
from aiogram import Router
from aiogram.filters import Command

router = Router()


def load_shops():
    try:
        with open('config.json', 'r') as file:
            return json.load(file).get('shops', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


@router.message(Command('shops'))
async def cmd_shops(message: types.Message):
    shops = load_shops()

    if shops:
        response = "Список ваших магазинов:\n\n"
        for shop in shops:
            response += f"Название: {shop['name']}\n"
    else:
        response = "Нет сохраненных магазинов."

    await message.answer(response)
