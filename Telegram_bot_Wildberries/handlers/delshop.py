from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from My_projects.Telegram_bot_Wildberries.utils.config import load_shops, save_shops

router = Router()


@router.message(F.text == "/delshop")
async def del_shop(message: types.Message):
    config = load_shops()

    if not config:
        await message.reply("У вас нет добавленных магазинов.")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=shop['name'], callback_data=f"del_{shop['name']}")]
        for shop in config
    ])

    await message.answer("Выберите магазин для удаления:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("del_"))
async def confirm_delete(call: CallbackQuery):
    shop_name = call.data[4:]

    shops = load_shops()

    updated_shops = [shop for shop in shops if shop['name'] != shop_name]

    save_shops(updated_shops)

    await call.message.edit_text(f"Магазин '{shop_name}' успешно удален.")
