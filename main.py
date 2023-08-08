import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

# Вставьте свой токен, который вы получили от @BotFather
BOT_TOKEN = '6120933903:AAGtlv7oBE-UrrIYTJoqvxTw2tKIlwUFkHg'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, который поможет тебе выбрать одно или несколько слов из списка. Просто отправь мне список слов через запятую, а затем укажи сколько случайных вариантов ты хочешь получить (не более 10).")

@dp.message_handler(lambda message: message.text and ',' in message.text)
async def choose_from_list(message: types.Message):
    words = message.text.split(',')
    try:
        num_choices = 3  # Значение по умолчанию
        if message.text.count(',') > 1:
            parts = message.text.split(',')
            num_choices = int(parts[-1].strip())
            words = parts[:-1]

        num_choices = min(num_choices, len(words))  # Не более, чем количество слов в списке
        chosen_words = random.sample(words, num_choices)
        chosen_text = "\n".join([f"• {word.strip()}" for word in chosen_words])

        await message.reply(f"Я выбрал для тебя {num_choices} {'вариант' if num_choices == 1 else 'варианта'}:\n{chosen_text}", parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await message.reply("Произошла ошибка при выборе вариантов. Пожалуйста, убедитесь, что вы отправили список через запятую, а затем укажите количество случайных вариантов.", parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
