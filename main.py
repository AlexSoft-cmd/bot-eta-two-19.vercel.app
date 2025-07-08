import asyncio
import logging
import json

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, CommandObject

# --- Конфигурация ---
# Ваш токен от @BotFather
API_TOKEN = "7977339121:AAEybX7kfWMzQXMnsZhjLUunsyMra1vsly8" 

# ✅ ВАША НАСТОЯЩАЯ ССЫЛКА НА MINI APP
MINIAPP_URL = "https://bot-eta-two-19.vercel.app"

# --- Инициализация бота и диспетчера ---
dp = Dispatcher()
bot = Bot(token=API_TOKEN)


# --- Обработчики ---
@dp.message(CommandStart())
async def send_welcome(message: types.Message, command: CommandObject):
    lang = command.args
    
    if lang and lang.lower().strip() == "en":
        text = "Welcome! Click the button below to open the order form."
        button_text = "🛒 Open Mini App"
    else:
        text = "Добро пожаловать! Нажмите кнопку ниже, чтобы открыть форму заказа."
        button_text = "🛒 Открыть Mini App"

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=button_text, web_app=types.WebAppInfo(url=MINIAPP_URL))]
        ]
    )
    await message.answer(text, reply_markup=kb)


@dp.message(lambda message: message.web_app_data)
async def webapp_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        
        reply = f"""✅ Заказ получен:
Имя: {data['name']}
Email: {data['email']}
Продукт: {data['product']}
Сумма: {data['amount']} ILS

💳 Платеж (эмуляция): принят."""

        await message.answer(reply)
        
    except Exception as e:
        logging.error(f"Ошибка при обработке данных из Web App: {e}")
        await message.answer("❌ Ошибка при обработке данных.")


# --- Функция запуска бота ---
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")