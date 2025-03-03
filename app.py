from dataclasses import dataclass, field
import json
from dataclasses import asdict
from dataclasses import dataclass, field
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = "7861450739:AAHPeoXzDOoMVvPzGQ5U30C1BJ7d2elKHhg"


@dataclass
class Word:
    word_id: str
    meaning: str
    similar_words: list
    sentence_with_word : str

@dataclass
class User:
    id: int
    username: str
    language_target: str = "arabic"
    language_native: str = "hebrew"
    score: int = 0
    total_quiz: int = 0
    total_words: int = 0
    learned_words: list = field(default_factory=list)




bot = telebot.TeleBot(TOKEN)


def add_user_to_json(user: User):
    #  read users.json
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []  # if not find

    # check if exist
    for existing_user in users:
        if existing_user["_id"] == user.id:
            print("User already exists!")
            return

    # if not exist
    user_data = {
        "_id": user.id,
        "username": user.username,
        "language_target": user.language_target,
        "language_native": user.language_native,
        "score": user.score,
        "total_quiz": user.total_quiz,
        "total_words": user.total_words,
        "learned_words": user.learned_words
    }

    users.append(user_data)

    # שמירה מחדש לקובץ users.json
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

    print("User added successfully!")
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

def edit_quiz_data():
    pass
def add_learnd_words_to_user():
    pass
def edit_learned_words_to_user():
    pass
def get_learned_words_byid(user_id):
    pass

def get_new_words(user_id):
    learn_word = []#set(get_learned_words_byid(user_id))
    with open("word_heb_arabic.json.json", "r", encoding="utf-8") as file:
        words = json.load(file)
    for word in words:
        if word not in learn_word:
            return Word(**word)
    return "No words found!"




@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    username = message.chat.username or "Unknown"
    first_name = message.chat.first_name or "Unknown"
    last_name = message.chat.last_name or ""

    '''save user in object and save him in json'''
    user = User(id= user_id , username =username)
    add_user_to_json(user)

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
    user_id = call.message.from_user.id
    get_new_words(user_id)
    bot.send_message(user_id , "📖 Learning a new word...")


@bot.callback_query_handler(func=lambda call: call.data == "game")
def play_game(call):
    bot.send_message(call.message.chat.id, "🎮 Starting a game...")


if __name__ == "__main__":
    bot.polling(none_stop=True)
