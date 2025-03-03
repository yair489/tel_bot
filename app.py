from dataclasses import dataclass, field
import json
from dataclasses import asdict
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7861450739:AAHPeoXzDOoMVvPzGQ5U30C1BJ7d2elKHhg"


class Word:
    def __init__(self , word , word_translate , wrong_trans , sent):
        self.word = word
        self.word_translate = word_translate
        self.wrong_trans = wrong_trans
        self.sent = sent

@dataclass
class User:
    _id: int
    username: str
    language_target: str
    language_native: str
    score: int
    total_quiz: int
    total_words: int
    learned_words: list

bot = telebot.TeleBot(TOKEN)

user_data = {}


def add_user_to_json():
    pass

def edit_quiz_data():
    pass

def add_learned_words_to_user():
    pass

def edit_learned_words_to_user():
    pass

def get_user_byid(user_id):
    try:
        with open("users.json" , "r") as file:
            users = json.load(file)
    except ModuleNotFoundError:
        users = []

    for exist_user in users:
        if exist_user["_id"] == user_id:
            return User(**exist_user)
    return None



def get_learned_words_byid(user_id):
    user = get_user_byid(user_id)
    if not user:
        return "User not found!"

    learned_words = user.learned_words
    if not learned_words:
        return "No learned words yet."

    return learned_words



@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    username = message.chat.username or "Unknown"
    first_name = message.chat.first_name or "Unknown"
    last_name = message.chat.last_name or ""

    user_info = (f"👤 User Info:\n"
                 f"🆔 ID: {user_id}\n"
                 f"👤 Username: {username}\n"
                 f"📛 Name: {first_name} {last_name}\n")

    bot.send_message(user_id, user_info)

    welcome_message = "What would you like to do?"
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("📖 Learn a Word", callback_data="learn"))
    keyboard.row(InlineKeyboardButton("🎮 Play a Game", callback_data="game"))

    bot.send_message(user_id, welcome_message, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "learn")
def learn_word(call):
    bot.send_message(call.message.chat.id, "📖 Learning a new word...")


@bot.callback_query_handler(func=lambda call: call.data == "game")
def play_game(call):
    bot.send_message(call.message.chat.id, "🎮 Starting a game...")


if __name__ == "__main__":
    bot.polling(none_stop=True)
