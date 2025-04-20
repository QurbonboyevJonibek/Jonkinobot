
```python
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "7542357877:AAEYHE6FL77W-VOJoVxqOrHVrn26S5nqABY"
TELEGRAM_CHANNEL = "@it_is_maylife"
YOUTUBE_LINK = "https://youtube.com/your_channel"
INSTAGRAM_LINK = "https://instagram.com/your_account"
CORRECT_CODE = "12345"  # Change this to your desired code

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start_handler(message: types.Message):
        # First, send the video
        await message.answer_video(
            video="your_video_file_id",  # Replace with actual video file_id
            caption="Welcome to our bot! Please follow our channels:"
        )
        
        # Create subscription buttons
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Telegram Channel 📢", url=TELEGRAM_CHANNEL)],
            [InlineKeyboardButton(text="YouTube Channel 🎥", url=YOUTUBE_LINK)],
            [InlineKeyboardButton(text="Instagram Page 📸", url=INSTAGRAM_LINK)],
            [InlineKeyboardButton(text="Check Subscription ✅", callback_data="check_sub")]
        ])
        
        await message.answer("Please subscribe to our channels:", reply_markup=markup)

    @dp.callback_query(lambda c: c.data == "check_sub")
    async def check_subscription(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        
        # Check if user is subscribed to the Telegram channel
        try:
            member = await bot.get_chat_member(TELEGRAM_CHANNEL, user_id)
            if member.status in ['member', 'administrator', 'creator']:
                await callback_query.message.answer("Please enter the code:")
            else:
                await callback_query.message.answer("Siz hali obuna bo'lmagan siz")
        except Exception:
            await callback_query.message.answer("Siz hali obuna bo'lmagan siz")
        
        await callback_query.answer()

    @dp.message()
    async def check_code(message: types.Message):
        if message.text == CORRECT_CODE:
            # Send the video when correct code is entered
            await message.answer_video(
                video="your_reward_video_file_id",  # Replace with actual video file_id
                caption="Congratulations! Here's your video!"
            )
        else:
            await message.answer("Incorrect code. Please try again.")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
```
