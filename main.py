import asyncio
import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ChatType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.getenv('TOKEN')

GRUP_ID_2='-5018213536'
GRUP_ID_1='-5004537976'

bot = Bot(token=TOKEN)
dp = Dispatcher()

GROUP_1_ID = -5004537976
GROUP_2_ID = -5018213536

@dp.message()
async def hello(message: types.Message):
    if message.chat.id == GROUP_1_ID:
        await message.copy_to(GROUP_2_ID)

    elif message.chat.id == GROUP_2_ID:
        await message.copy_to(GROUP_1_ID)



@dp.message(lambda m: "start" in m.text.lower() or "/start" in m.text.lower())
async def menu_handler(message: types.Message):
    if message.chat.type == "private":
        await message.answer()
        '''создай группу
добавь бота  в группу
сделай бота админом
отправь контакт собеседника'''
    else:
        await message.answer(
            'бот переводчик'
        )

        await message.answer(
            'бот переводчик'
        )


@dp.message(lambda m: "start" in m.text.lower() or "/start" in m.text.lower())
async def menu_handler(message: types.Message):
    if message.chat.type == "private":
     await message.answer(
        "📋 выберите язык"
    )






@dp.message(lambda m: "start" in m.text.lower() or "/start" in m.text.lower())
async def menu_handler(message: types.Message):
    kb = [
        [types.KeyboardButton(text="руски"), types.KeyboardButton(text="арабски")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        "📋 выберите язык",
        reply_markup=keyboard
    )


@dp.message(lambda m: "id" in m.text.lower() or "/id" in m.text.lower())
async def get_chat_id(message: types.Message):
    await message.answer(f"Ваш ID: {message.chat.id}")


@dp.message()
async def hello(message: types.Message):
    await message.send_copy(message.from_user.id)


async def main():
    logger.info("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())



