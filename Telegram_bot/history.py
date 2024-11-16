# -*- coding: utf-8 -*-
import sqlite3

def record_query(user_id, query):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO history (user_id, query) VALUES (?, ?)
    ''', (user_id, query))

    conn.commit()
    conn.close()

def get_user_history(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT query FROM history
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 10
    ''', (user_id,))

    history = cursor.fetchall()

    conn.close()
    return history

async def history(update, context):
    user_id = update.effective_user.id

    user_history = get_user_history(user_id)

    await send_user_history(update, context, user_history)


async def send_user_history(update, context, user_history):
    if user_history:
        history_text = "\n".join(f"{i + 1}. {query}" for i, (query,) in enumerate(user_history))
    else:
        history_text = "У вас пока нет истории запросов."

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"История запросов:\n{history_text}"
    )
