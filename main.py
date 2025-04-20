from aiogram import Bot, Dispatcher, types   
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils import executor

API_TOKEN = "7542357877:AAEYHE6FL77W-VOJoVxqOrHVrn26S5nqABY"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Salom! Bu sinov uchun bot.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)