import json
import os
from pathlib import Path
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

USERS_FILE = Path("users.json")
TABLE_IMAGE = Path("static/table.png")

WELCOME_TEXT = "Добро пожаловать! Нажмите на кнопку из меню."
INFO_TEXT = (
    "Привет, это информационный бот ФК КДВ!\n"
    "Подпишись на наш паблик - @boroda_tomsk_youtube"
)

NEXT_MATCH = (
    "✈️ // 28 сентября (вск)\n"
    "Крылья-Советов-2 (Самара)- ФК КДВ\n"
    "23-ий тур Leon 2 Лига Б\n"
    "@boroda_tomsk_youtube"
)
NEXT_MATCH_URL = "https://fnl.pro/leon-b/matches/48960"

PREV_MATCH = (
    "🏠 // Техническая победа\n"
    "21 сентября\n"
    "ФК КДВ 3 - 0 Соколь (Казань)\n"
    "22-ой тур Leon 2 Лига Б\n"
    "@boroda_tomsk_youtube"
)
PREV_MATCH_URL = "https://fnl.pro/leon-b/matches/48943"

FREE_SHIRT = 'Розыгрыш формы ФК КДВ в моем ТГ-канале @boroda_tomsk_youtube'
FREE_SHIRT_URL = 'https://t.me/boroda_tomsk_youtube/632'


def save_user(user_id: int, username: str):
    users = []
    if USERS_FILE.exists():
        users = json.loads(USERS_FILE.read_text())
    if not any(u["id"] == user_id for u in users):
        users.append({"id": user_id, "username": username})
        USERS_FILE.write_text(json.dumps(users, indent=2))


def safe_send(bot: Bot, chat_id: int, text: str = None, reply_markup=None, photo: Path = None):
    try:
        if photo:
            with open(photo, "rb") as f:
                bot.send_photo(chat_id=chat_id, photo=f, caption=text)
        else:
            bot.send_message(chat_id=chat_id, text=text,
                             reply_markup=reply_markup)
    except Exception as e:
        print(f"Не смог отправить сообщение {chat_id}: {e}")


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    save_user(chat_id, username)

    keyboard = [
        ["Перезапустить бота", "Инфо"],
        ["Актуальная таблица"],
        ["Предыдущий матч", "Ближайший матч"],
        ["Розыгрыш формы ФК КДВ"]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=False)
    safe_send(context.bot, chat_id, WELCOME_TEXT, reply_markup=reply_markup)


def handle_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    text = update.message.text
    save_user(chat_id, username)

    if text == "Перезапустить бота":
        start(update, context)
    elif text == "Инфо":
        safe_send(context.bot, chat_id, INFO_TEXT)
    elif text == "Актуальная таблица":
        if TABLE_IMAGE.exists():
            safe_send(context.bot, chat_id,
                      "🏆 Актуальная таблица Leon Лига Б, группа 4 \n@boroda_tomsk_youtube",
                      photo=TABLE_IMAGE)
        else:
            safe_send(context.bot, chat_id, "Файл таблицы не найден.")
    elif text == "Ближайший матч":
        buttons = [[InlineKeyboardButton(
            "Ссылка на матч", url=NEXT_MATCH_URL)]]
        markup = InlineKeyboardMarkup(buttons)
        safe_send(context.bot, chat_id, NEXT_MATCH, reply_markup=markup)
    elif text == "Предыдущий матч":
        buttons = [[InlineKeyboardButton(
            "Статистика матча", url=PREV_MATCH_URL)]]
        markup = InlineKeyboardMarkup(buttons)
        safe_send(context.bot, chat_id, PREV_MATCH, reply_markup=markup)
    elif text == "Розыгрыш формы ФК КДВ":
        buttons = [[InlineKeyboardButton(
            "Розыгрыш формы ФК КДВ", url=FREE_SHIRT_URL)]]
        markup = InlineKeyboardMarkup(buttons)
        safe_send(context.bot, chat_id, FREE_SHIRT, reply_markup=markup)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~
                   Filters.command, handle_message))

    print("Бот запущен")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
