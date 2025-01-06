from datetime import datetime, timedelta
import pytz
from aiogram import types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import requests
from My_projects.Telegram_bot_Wildberries.utils.config import load_shops

router = Router()


class ReportState(StatesGroup):
    shop_name = State()
    start_date = State()
    end_date = State()


@router.message(Command("report"))
async def get_report(message: types.Message, state: FSMContext):
    config = load_shops()

    if not config:
        await message.answer("У вас нет добавленных магазинов.")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=shop['name'], callback_data=f"report_{shop['name']}")
    ] for shop in config])

    await message.answer("Выберите магазин", reply_markup=keyboard)


@router.callback_query(lambda call: call.data.startswith('report_'))
async def choose_period(call, state: FSMContext):
    shop_name = call.data[7:]
    await state.update_data(shop_name=shop_name)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Сегодня", callback_data=f"period_shop_today"),
        InlineKeyboardButton(text="Вчера", callback_data=f"period_shop_yesterday"),
        InlineKeyboardButton(text="Последние 7 дней", callback_data=f"period_shop_last7"),
        InlineKeyboardButton(text="Произвольный период", callback_data=f"period_shop_custom")
    ]])
    await call.message.edit_text("Выберите период для отчета:", reply_markup=keyboard)


def fetch_sales_data(shop_name, start_date, end_date, flag=0):
    config = load_shops()

    shop = next((s for s in config if s["name"] == shop_name), None)
    if not shop:
        return None, "Магазин не найден."


    url = "https://statistics-api.wildberries.ru/api/v1/supplier/sales"
    params = {
        "dateFrom": start_date,
        "dateTo": end_date,
        "flag": flag
    }
    headers = {
        "Authorization": shop['api_key']
    }


    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return None, "Ошибка при запросе к API Wildberries."

    return response.json(), None


@router.callback_query(lambda call: call.data.startswith('period_'))
async def generate_report(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    print(f"Полученные данные из callback: {data}")

    try:
        parts = data.split("_", 2)
        print(f"Разделенные данные: {parts}")

        if len(parts) < 3:
            await call.message.edit_text("Неверный формат данных. Попробуйте снова.")
            return

        _, _, period = parts
        print(f"Извлечённый период: {period}")
    except ValueError:
        await call.message.edit_text("Ошибка при разборе данных. Попробуйте снова.")
        return

    state_data = await state.get_data()
    shop_name = state_data.get("shop_name")

    tz = pytz.timezone('Europe/Moscow')
    if period == "today":
        start_date = datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S')
        end_date = datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S')
    elif period == "yesterday":
        start_date = (datetime.now(tz) - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
        end_date = start_date
    elif period == "last7":
        start_date = (datetime.now(tz) - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S')
        end_date = datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S')
    elif period == "custom":
        await call.message.edit_text("Введите начальную дату в формате YYYY-MM-DD:")
        await state.set_state(ReportState.start_date)
        return
    else:
        await call.message.edit_text("Неверный выбор периода. Попробуйте снова.")
        return

    sales_data, error = fetch_sales_data(shop_name, start_date, end_date)
    if error:
        await call.message.edit_text(error)
        return

    if sales_data and "data" in sales_data:
        sales = sales_data["data"]
        total_sales = sum(item['totalPrice'] for item in sales)
        total_count = len(sales)

        report = f"""
        *Отчет по продажам магазина*
        Период: с {start_date} по {end_date}
        Общая сумма продаж: {total_sales} ₽
        Количество продаж: {total_count}
        """

        await call.message.edit_text(report, parse_mode="Markdown")
    else:
        await call.message.edit_text("Данные о продажах не найдены.")


@router.message(ReportState.start_date)
async def get_start_date(message: types.Message, state: FSMContext):
    start_date_str = message.text.strip()

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        await state.update_data(start_date=start_date)

        await message.answer("Введите конечную дату в формате YYYY-MM-DD:")
        await state.set_state(ReportState.end_date)
    except ValueError:
        await message.answer("Неверный формат даты. Попробуйте снова в формате YYYY-MM-DD.")


@router.message(ReportState.end_date)
async def get_end_date(message: types.Message, state: FSMContext):
    end_date_str = message.text.strip()

    try:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        data = await state.get_data()
        start_date = data['start_date']

        if end_date < start_date:
            await message.answer("Конечная дата не может быть раньше начальной. Попробуйте снова.")
            return

        await state.update_data(end_date=end_date)

        await message.answer("Пожалуйста, подождите, я формирую отчет...")
        shop_name = data['shop_name']
        sales_data, error = fetch_sales_data(shop_name, start_date, end_date)
        if error:
            await message.answer(error)
            return

        if sales_data and "data" in sales_data:
            sales = sales_data["data"]
            total_sales = sum(item['totalPrice'] for item in sales)
            total_count = len(sales)

            report = f"""
            *Отчет по продажам магазина*
            Период: с {start_date} по {end_date}
            Общая сумма продаж: {total_sales} ₽
            Количество продаж: {total_count}
            """
            await message.answer(report, parse_mode="Markdown")
        else:
            await message.answer("Данные о продажах не найдены.")

    except ValueError:
        await message.answer("Неверный формат даты. Попробуйте снова в формате YYYY-MM-DD.")
