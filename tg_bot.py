import logging
import os
from uuid import uuid4

from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from telegram.ext import (
    filters,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    InlineQueryHandler,
)


#%% Загружаем секреты
BOT_TOKEN = os.getenv("TG_TEST_BOT_TOKEN")


#%% Логгирование
logging.basicConfig(
    filename='tg.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)


#%% Обработчики

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me, babe!"
    )


# Сообщение
async def count_symbols(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    n = len(update.message.text)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Количество символов в твоей фразе: {n}'
    )


# Команда от пользователя с параметрами
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    text_caps = ' '.join(context.args).upper()
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_caps
    )


# Подсказки inline пользователю, который вводит @имяботаbot
async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.extend([
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Посчитать количество символов',
            input_message_content=InputTextMessageContent(len(query))
        ),
    ])
    
    await context.bot.answer_inline_query(update.inline_query.id, results)



# Неизвестные команды
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Я не знаю такой команды :("
    )


#%%
if __name__ == '__main__':
    
    # Создаём приложение (Updater будет создан автоматически)
    application = ApplicationBuilder().token(BOT_TOKEN).build()
   
    #
    ## /start
    #
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    #
    ## текстовое сообщение
    #
    count_symbols_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND),
        count_symbols
    )
    application.add_handler(count_symbols_handler)
    
    #
    ## /caps с параметрами
    #
    caps_handler = CommandHandler('caps', caps)
    application.add_handler(caps_handler)
    
    #
    ## inline подсказка для использования бота в разных чатах
    #
    inline_caps_handler = InlineQueryHandler(inline_caps)
    application.add_handler(inline_caps_handler)
    
    #
    ## Неизвестная команда
    #
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    
    
    
    
    
    # Запускаем бота (выход = CTRL+c)
    application.run_polling()
