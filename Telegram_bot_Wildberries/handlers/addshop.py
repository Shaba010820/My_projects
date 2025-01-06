import logging
import requests
from aiogram import types
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from My_projects.Telegram_bot_Wildberries.utils.config import load_shops, save_shops

router = Router()


class ShopForm(StatesGroup):
    waiting_for_api_key = State()
    waiting_for_shop_name = State()


def validate_api_key(api_key):
    url = "https://common-api.wildberries.ru/ping"
    headers = {"Authorization": api_key}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при подключении к API Wildberries: {e}")
        return False


@router.message(Command('addshop'))
async def cmd_addshop(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите API ключ магазина:")

    await state.set_state(ShopForm.waiting_for_api_key)


@router.message(ShopForm.waiting_for_api_key)
async def process_api_key(message: types.Message, state: FSMContext):
    api_key = message.text

    shops = load_shops()

    existing_shop_by_api_key = next((shop for shop in shops if shop["api_key"] == api_key), None)
    if existing_shop_by_api_key:
        await message.answer("Магазин с таким API ключом уже существует.")
        await state.clear()
        return

    if not validate_api_key(api_key):
        await message.answer("API ключ невалиден. Пожалуйста, проверьте его и попробуйте снова.")
        await state.set_state(ShopForm.waiting_for_api_key)
        return

    await state.update_data(api_key=api_key)

    await message.answer("API ключ подтвержден. Теперь введите имя магазина:")

    await state.set_state(ShopForm.waiting_for_shop_name)


@router.message(ShopForm.waiting_for_shop_name)
async def process_shop_name(message: types.Message, state: FSMContext):
    shop_name = message.text

    user_data = await state.get_data()
    api_key = user_data['api_key']

    shops = load_shops()
    shops.append({"name": shop_name, "api_key": api_key})
    save_shops(shops)

    await message.answer(f"Магазин '{shop_name}' успешно добавлен.")

    await state.clear()
