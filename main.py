
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "7542357877:AAEYHE6FL77W-VOJoVxqOrHVrn26S5nqABY"
TELEGRAM_CHANNEL = "it_is_maylife"  # Channel username without @
TELEGRAM_CHANNEL_URL = "https://t.me/it_is_maylife"  # Full URL for button
#YOUTUBE_LINK = "https://youtube.com/your_channel"
INSTAGRAM_LINK = "https://www.instagram.com/jonkino2025?igsh=MXJ5bXdxb3MzOHZseQ=="

# Dictionary of video IDs and their corresponding codes
VIDEOS = {
    "2010": "BAACAgUAAxkBAAO8aAU6cv7_a-2NVRLoKsC1kWNztzEAAhUWAAICaslXuiQzgntowsQ2BA",
    "2011": "BAACAgUAAxkBAAO-aAU67JlEFvDkTt5X-HrEkMsdCOIAAqYUAALtXSlUOZ5D2Z365T02BA",
    "2012": "BAACAgUAAxkBAAPEaAYlQmxNmoAsVZa7QNmorjBJ4fsAArwcAAJNEzFUyC0ceuww1YM2BA",
}

# Use a direct URL for welcome message instead of video
async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start_handler(message: types.Message):
        # Start with a text message instead of video
        await message.answer("JonKINO botga xush kelibsiz!")
        
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Telegram Channel 📢", url=TELEGRAM_CHANNEL_URL)],
           # [InlineKeyboardButton(text="YouTube Channel 🎥", url=YOUTUBE_LINK)],
            [InlineKeyboardButton(text="Instagram Page 📸", url=INSTAGRAM_LINK)],
            [InlineKeyboardButton(text="Tekshirish ✅", callback_data="check_sub")]
        ])
        
        await message.answer("Kanallarga obuna bo'ling va \n Tekshirishni bosing:", reply_markup=markup)

    @dp.callback_query(lambda c: c.data == "check_sub")
    async def check_subscription(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        
        try:
            member = await bot.get_chat_member(f"@{TELEGRAM_CHANNEL}", user_id)
            if member.status in ['member', 'administrator', 'creator']:
                await callback_query.answer("Subscription verified!")
                try:
                    await callback_query.message.edit_text(
                        "Kino tomosha qilish uchun kodni kiriting."
                    )
                except:
                    await bot.send_message(
                        callback_query.from_user.id,
                        "Kino kodini kiriting ."
                    )
            else:
                await callback_query.answer("Avval obuna bo'ling!", show_alert=True)
        except Exception as e:
            print(f"Error checking subscription: {e}")
            await callback_query.answer("Botdan foydalanish uchun avval obuna bo'ling!", show_alert=True)

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
                    caption="Siz izlagan kod! 🎉"
                )
            except Exception as e:
                await message.answer("Bu kod uchun video topilmadi. Iltimos, to'g'ri kodni kiriting.")
        else:
            await message.answer("Noto'g'ri kod kiritdingiz. Iltimos, to'g'ri kodni kiriting.")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"Bot crashed with error: {e}")
            print("Restarting bot in 5 seconds...")
            asyncio.run(asyncio.sleep(5))  # Properly handle async sleep
