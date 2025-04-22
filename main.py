
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "7542357877:AAEYHE6FL77W-VOJoVxqOrHVrn26S5nqABY"
TELEGRAM_CHANNEL1 = "it_is_maylife"  # Channel username without @
TELEGRAM_CHANNEL2 = "JonGAME_1"  # Replace with your second channel
TELEGRAM_CHANNEL3 = "JonGAMEchat_1"  # Replace with your third channel

TELEGRAM_CHANNEL1_URL = "https://t.me/it_is_maylife"
TELEGRAM_CHANNEL2_URL = "https://t.me/JonGAME_1"  # Replace with actual URL
TELEGRAM_CHANNEL3_URL = "https://t.me/JonGAMEchat_1"  # Replace with actual URL

INSTAGRAM_LINK = "https://www.instagram.com/jonkino2025?igsh=MXJ5bXdxb3MzOHZseQ=="

# Dictionary of video IDs and their corresponding codes
VIDEOS = {
    "2010": ("BAACAgUAAxkBAAPKaAe9F89cG1XWI_nJO5TJqS3PoowAAm4VAAII7jhX94XSAt2hKow2BA", "Siz izlagan kino", "Shangchi 9 halqa filmi"),
    "2011": ("BAACAgUAAxkBAAO6aAU6AjWE-6W9t4y-HtAiRrKVWEEAAlcVAAII7jhXBhjGljDHjfQ2BA", "Black Adam"),
    "2012": ("BAACAgUAAxkBAAO8aAU6cv7_a-2NVRLoKsC1kWNztzEAAhUWAAICaslXuiQzgntowsQ2BA", "Avatar 2"),
    "2013": ("BAACAgUAAxkBAAPNaAe_WdNzE7ShBDOaERXI84Dq2cEAAoYUAAII7kBXYDcYJ2iQPDs2BA", "Venom 2"),
    "201": ("", ""),
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
            [InlineKeyboardButton(text="Telegram Channel 1 📢", url=TELEGRAM_CHANNEL1_URL)],
            [InlineKeyboardButton(text="Telegram Channel 2 📢", url=TELEGRAM_CHANNEL2_URL)],
            [InlineKeyboardButton(text="Telegram Channel 3 📢", url=TELEGRAM_CHANNEL3_URL)],
            [InlineKeyboardButton(text="Instagram 📸", url=INSTAGRAM_LINK)],
            [InlineKeyboardButton(text="Tekshirish ✅", callback_data="check_sub")]
        ])
        
        await message.answer("Kanallarga obuna bo'ling va \n Tekshirishni bosing:", reply_markup=markup)

    @dp.callback_query(lambda c: c.data == "check_sub")
    async def check_subscription(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        
        async def check_member_status(channel):
            try:
                member = await bot.get_chat_member(f"@{channel}", user_id)
                return member.status in ['member', 'administrator', 'creator']
            except Exception as e:
                print(f"Error checking {channel}: {e}")
                return False

        is_subscribed = await asyncio.gather(
            check_member_status(TELEGRAM_CHANNEL1),
            check_member_status(TELEGRAM_CHANNEL2),
            check_member_status(TELEGRAM_CHANNEL3)
        )

        if all(is_subscribed):
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Kodni kiriting ✍️", callback_data="enter_code")]
            ])
            await callback_query.message.edit_text(
                "Tabriklaymiz! Endi kino kodini kiritishingiz mumkin.",
                reply_markup=markup
            )
            await callback_query.answer("Obuna tekshirildi ✅", show_alert=True)
        else:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Telegram Channel 1 📢", url=TELEGRAM_CHANNEL1_URL)],
                [InlineKeyboardButton(text="Telegram Channel 2 📢", url=TELEGRAM_CHANNEL2_URL)],
                [InlineKeyboardButton(text="Telegram Channel 3 📢", url=TELEGRAM_CHANNEL3_URL)],
                [InlineKeyboardButton(text="Tekshirish ✅", callback_data="check_sub")]
            ])
            await callback_query.answer("Iltimos, barcha kanallarga obuna bo'ling! ❌", show_alert=True)
            await callback_query.message.edit_text(
                "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:",
                reply_markup=markup
            )

    @dp.message()
    async def handle_message(message: types.Message):
        if message.video:
            file_id = message.video.file_id
            await message.reply(f"Video file_id: `{file_id}`", parse_mode="Markdown")
            return
            
        if message.text in VIDEOS:
            try:
                video_id, video_name = VIDEOS[message.text]
                if video_id:
                    await message.answer_video(
                        video=video_id,
                        caption=f"{video_name} 🎉"
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
            print("Starting bot...")
            asyncio.run(main())
        except Exception as e:
            print(f"Bot crashed with error: {e}")
            print("Restarting bot in 5 seconds...")
            try:
                # Handle different types of errors
                if isinstance(e, (ConnectionError, TimeoutError)):
                    print("Connection error detected, waiting for internet...")
                asyncio.run(asyncio.sleep(5))
            except Exception:
                # If asyncio.run fails, use regular sleep
                import time
                time.sleep(5)
        print("Restarting bot...")
