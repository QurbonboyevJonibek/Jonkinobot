
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "7542357877:AAEYHE6FL77W-VOJoVxqOrHVrn26S5nqABY"
TELEGRAM_CHANNEL = "it_is_maylife"  # Channel username without @
TELEGRAM_CHANNEL_URL = "https://t.me/it_is_maylife"  # Full URL for button
#YOUTUBE_LINK = "https://youtube.com/your_channel"
INSTAGRAM_LINK = "https://instagram.com/your_account"

# Dictionary of video IDs and their corresponding codes
VIDEOS = {
    "12345": "BAACAgUAAxkBAAO4aAU0U7yegniUZVei55tmCT_zXSYAAtIcAAKwRShU6ByfaHOR7uM2BA",
    "2010" : "BAACAgUAAxkBAAO-aAU67JlEFvDkTt5X-HrEkMsdCOIAAqYUAALtXSlUOZ5D2Z365T02BA",
    "2011": "BAACAgUAAxkBAAO-aAU67JlEFvDkTt5X-HrEkMsdCOIAAqYUAALtXSlUOZ5D2Z365T02BA",
}

# Use a direct URL for welcome message instead of video
async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start_handler(message: types.Message):
        # Start with a text message instead of video
        await message.answer("Welcome! Please follow our channels to access the videos:")
        
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Telegram Channel 📢", url=TELEGRAM_CHANNEL_URL)],
           # [InlineKeyboardButton(text="YouTube Channel 🎥", url=YOUTUBE_LINK)],
            [InlineKeyboardButton(text="Instagram Page 📸", url=INSTAGRAM_LINK)],
            [InlineKeyboardButton(text="Check Subscription ✅", callback_data="check_sub")]
        ])
        
        await message.answer("Subscribe to our channels:", reply_markup=markup)

    @dp.callback_query(lambda c: c.data == "check_sub")
    async def check_subscription(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        
        try:
            member = await bot.get_chat_member(f"@{TELEGRAM_CHANNEL}", user_id)
            if member.status in ['member', 'administrator', 'creator']:
                await callback_query.answer("Subscription verified!")
                try:
                    await callback_query.message.edit_text(
                        "Enter any of the following codes to access different videos:\n"
                        "12345 - Video 1\n"
                        "2010 - Video 2\n"
                        "2011 - Video 3"
                    )
                except:
                    await bot.send_message(
                        callback_query.from_user.id,
                        "Enter any of the following codes to access different videos:\n"
                        "12345 - Video 1\n"
                        "2010 - Video 2\n"
                        "2011 - Video 3"
                    )
            else:
                await callback_query.answer("Please subscribe first!", show_alert=True)
        except Exception as e:
            print(f"Error checking subscription: {e}")
            await callback_query.answer("Please subscribe to our channel first!", show_alert=True)

    @dp.message()
    async def handle_message(message: types.Message):
        if message.video:
            file_id = message.video.file_id
            await message.reply(f"Video file_id: `{file_id}`", parse_mode="Markdown")
            return
            
        if message.text in VIDEOS:
            try:
                await message.answer_video(
                    video=VIDEOS[message.text],
                    caption="Enjoy your video! 🎉"
                )
            except Exception as e:
                await message.answer("Sorry, this video is currently unavailable.")
        else:
            await message.answer("Incorrect code. Please try again.")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
