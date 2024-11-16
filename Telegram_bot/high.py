from config import headers, url
import requests

def get_json_data(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

async def find_most_expensive_product(update, context):
    try:
        data = get_json_data(url, headers)

        if data:
            most_expensive_product = max(data, key=lambda x: x.get('price', 0))
            await send_most_expensive_product(update, context, most_expensive_product)
        else:
            return None
    except FileNotFoundError:
        print(f"Файл не найден.")
        return None

async def send_most_expensive_product(update, context, most_expensive_product):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Найден товар : {most_expensive_product['name']}\nЦена: {most_expensive_product['price']}"
             f"\n{most_expensive_product['description']}\n{most_expensive_product['img']}"
    )