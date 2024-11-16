from telegram.ext import CommandHandler, ApplicationBuilder, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from start import start, button_click
from config import Bot_TOKEN
from custom import custom_json, search_json
from low import find_cheapest_product
from high import find_most_expensive_product
from custom import STEP1
from history import history

if __name__ == '__main__':
    application = ApplicationBuilder().token(Bot_TOKEN).build()
    start_handler = CommandHandler('start', start)
    high = CommandHandler('high', find_most_expensive_product)
    low = CommandHandler('low', find_cheapest_product)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('custom', custom_json)],
        states={
            STEP1: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_json)],
        },
        fallbacks=[],
        allow_reentry=True
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('history', history))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(start_handler)
    application.add_handler(low)
    application.add_handler(high)
    application.run_polling()






