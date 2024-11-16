from high import get_json_data
from config import url, headers

async def find_cheapest_product(update, context):
    try:
        data = get_json_data(url, headers)
        if data:
            cheapest_product = min(data, key=lambda x: x.get('price', 0))
            await send_cheapest_product(update, context, cheapest_product)
        else:
            return None

    except FileNotFoundError:
        print(f"Файл не найден.")
        return None

async def send_cheapest_product(update, context, cheapest_product):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Найден товар : {cheapest_product['name']}\nЦена: {cheapest_product['price']}"
             f"\n{cheapest_product['description']}\n{cheapest_product['img']}"
    )
