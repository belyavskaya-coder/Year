import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, filters
)

# 🔑 Загружаем .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
GROUP_LINK = "https://t.me/pavliktour"

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env")

# 📝 Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# === КНОПКИ ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главная страница с кнопками"""
    keyboard = [
        [InlineKeyboardButton("🌿 О Сочи — по-моему", callback_data="about")],
        [InlineKeyboardButton("🗺 Экскурсии", callback_data="tours")],
        [InlineKeyboardButton("💌 Связаться / Забронировать", url=GROUP_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome = (
        "🌊 Привет! Я — Павлик, ваш гид по Сочи.\n\n"
        "Я не делаю «стандартные» туры. \n"
        "Я — создаю тихие, осмысленные прогулки:\n"
        "→ без толп,\n"
        "→ с остановками у водопадов,\n"
        "→ с рассказами, которые запомнятся.\n\n"
        "Выберите, что вас интересует:"
    )
    await update.message.reply_text(welcome, reply_markup=reply_markup)


# === ОБРАБОТЧИК КНОПОК ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        text = (
            "🌿 Сочи — не только море.\n\n"
            "Я живу здесь с 2015 года. И знаю: настоящая душа Сочи —\n"
            "→ в предгорьях,\n"
            "→ в туманных ущельях,\n"
            "→ в запахе рододендронов после дождя.\n\n"
            "Я — не гид-«говорилка». Я — ваш спутник.\n"
            "Для тех, кто хочет почувствовать Кавказ — а не просто сфоткаться.\n\n"
            "P.S. Люблю животных 🐕"
        )
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="main")]]
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == "tours":
        text = (
            "🗺 Доступные экскурсии:\n\n"
            "1️⃣ В горы на высоту 2320 (2–3 ч)\n"
            "— тихий лес, 2 водопада, омут для купания (летом)\n"
            "— подходит для семей с детьми от 4 лет\n\n"
            "2️⃣ Роза Хутор (4–5 ч)\n"
            "3️⃣ Утренняя тропа в Мацесте (1.5 ч)\n"
            "— рассказы о местной культуре\n"
            "— можно с детьми \n\n"
            "Все маршруты — малыми и большими группами.\n"
            "Гибкое расписание. Индивидуальные запросы — приветствуются."
        )
        keyboard = [
            [InlineKeyboardButton("📞 Забронировать", url=GROUP_LINK)],
            [InlineKeyboardButton("⬅️ Назад", callback_data="main")]
        ]
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif query.data == "main":
        # Возвращаемся в главное меню
        await start(query, context)



async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not CHANNEL_ID:
        await update.message.reply_text("❌ CHANNEL_ID не указан в .env")
        return

    text = " ".join(context.args) if context.args else "🌿 Новая экскурсия скоро! Следите за обновлениями."
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
        await update.message.reply_text("✅ Пост опубликован в канал!")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")


# === ЗАПУСК ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("post", post))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("✅ Бот запущен и готов к работе.")
    app.run_polling()


if __name__ == "__main__":
    main()
