
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "7542357877:AAEYHE6FL77W-VOJoVxqOrHVrn26S5nqABY"
TELEGRAM_CHANNEL = "@it_is_maylife"
YOUTUBE_LINK = "https://youtube.com/your_channel"
INSTAGRAM_LINK = "https://instagram.com/your_account"

# Dictionary of video IDs and their corresponding codes
VIDEOS = {
    "12345": "video_file_id_1",
    "67890": "video_file_id_2",
    "11111": "video_file_id_3",
    # Add more codes and video IDs as needed
}

WELCOME_VIDEO = "welcome_video_file_id"  # Your welcome video file_id

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start_handler(message: types.Message):
        await message.answer_video(
            video=WELCOME_VIDEO,
            caption="Welcome! Please follow our channels to access the videos:"
        )
        
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Telegram Channel 📢", url=TELEGRAM_CHANNEL)],
            [InlineKeyboardButton(text="YouTube Channel 🎥", url=YOUTUBE_LINK)],
            [InlineKeyboardButton(text="Instagram Page 📸", url=INSTAGRAM_LINK)],
            [InlineKeyboardButton(text="Check Subscription ✅", callback_data="check_sub")]
        ])
        
        await message.answer("Subscribe to our channels:", reply_markup=markup)

    @dp.callback_query(lambda c: c.data == "check_sub")
    async def check_subscription(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        
        try:
            member = await bot.get_chat_member(TELEGRAM_CHANNEL, user_id)
            if member.status in ['member', 'administrator', 'creator']:
                await callback_query.message.answer(
                    "Enter any of the following codes to access different videos:\n"
                    "1️⃣ First video: 12345\n"
                    "2️⃣ Second video: 67890\n"
                    "3️⃣ Third video: 11111"
                )
            else:
                await callback_query.message.answer("Siz hali obuna bo'lmagan siz")
        except Exception:
            await callback_query.message.answer("Siz hali obuna bo'lmagan siz")
        
        await callback_query.answer()

    @dp.message()
    async def check_code(message: types.Message):
        if message.text in VIDEOS:
            await message.answer_video(
                video=VIDEOS[message.text],
                caption="Enjoy your video! 🎉"
            )
        else:
            await message.answer("Incorrect code. Please try again.")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
