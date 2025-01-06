from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from .addshop import cmd_addshop
from .delshop import del_shop
from .report import get_report
from .shops import cmd_shops

router = Router()


def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить магазин", callback_data="addshop")],
        [InlineKeyboardButton(text="Удалить магазин", callback_data="delshop")],
        [InlineKeyboardButton(text="Получить отчет", callback_data="report")],
        [InlineKeyboardButton(text="Список магазинов", callback_data="shops")]
    ])
    return keyboard


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = "Доступные команды:\n"
    keyboard = get_inline_keyboard()
    await message.answer(help_text, reply_markup=keyboard)


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для работы с магазинами Wildberries. Чем могу помочь?")
    keyboard = get_inline_keyboard()
    await message.answer("Вот что я могу сделать:", reply_markup=keyboard)


@router.callback_query(lambda c: c.data == 'addshop')
async def handle_addshop(callback_query: types.CallbackQuery, state: FSMContext):
    await cmd_addshop(callback_query, state)
    await callback_query.answer("Вы выбрали добавить магазин.")


@router.callback_query(lambda c: c.data == 'delshop')
async def handle_delshop(callback_query: CallbackQuery):
    await del_shop(callback_query.message)
    await callback_query.answer("Вы выбрали удалить магазин.")


@router.callback_query(lambda c: c.data == 'report')
async def handle_report(callback_query: types.CallbackQuery, state: FSMContext):
    await get_report(callback_query.message, state)

    await callback_query.answer("Вы запросили отчет.")


@router.callback_query(lambda c: c.data == 'shops')
async def handle_shops(callback_query: types.CallbackQuery):
    await cmd_shops(callback_query.message)
    await callback_query.answer("Вы запросили список магазинов.")
