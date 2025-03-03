from dataclasses import dataclass, field
import json
from dataclasses import asdict


TOKEN = "7861450739:AAHPeoXzDOoMVvPzGQ5U30C1BJ7d2elKHhg"


@dataclass
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
    language_target: str = "arabic"
    language_native: str = "hebrew"
    score: int = 0
    total_quiz: int = 0
    total_words: int = 0
    learned_words: list = field(default_factory=list)


import telebot
import random
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

TOKEN = "7861450739:AAHPeoXzDOoMVvPzGQ5U30C1BJ7d2elKHhg"
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
def get_learned_words_byid(user_id, users_data):
    for user in users_data:
        if isinstance(user, dict) and user.get('_id') == user_id:
            learned_words = [word['word_id'] for word in user['learned_words']]
            return learned_words
    return None

def get_new_words(user_id):
    learn_word = set(get_learned_words_byid(user_id))
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

    welcome_message = (
        "Hello! I’m your Language Learning Bot. 📚\n\n"
        "🔹 Learn new words\n"
        "🔹 Take quizzes based on words you've learned\n"
        "🔹 View all learned words\n\n"
        "Click a button to get started!"
    )
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("📖 Learn a Word", callback_data="learn"),
        InlineKeyboardButton("🧠 Take a Quiz", callback_data="quiz"),
        InlineKeyboardButton("📚 View Learned Words", callback_data="view_words")
    )

    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "learn")
def learn_word(call):
    user_id = call.message.from_user.id
    get_new_words(user_id)
    bot.send_message(user_id , "📖 Learning a new word...")

    response = f"📝 Word: {word_id}\n📖 Meaning: {word_data['meaning']}\n✍ Example: {word_data['sentence_with_word']}"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🧠 Take a Quiz", callback_data="quiz"),
        InlineKeyboardButton("📖 Learn Another Word", callback_data="learn")
    )

    bot.send_message(call.message.chat.id, response, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "quiz")
def quiz(call):
    """ Generate a quiz from learned words. """
    user = get_user(call.message.chat.id)

    if not user["learned_words"]:
        bot.send_message(call.message.chat.id, "❗ You haven't learned any words yet. Click 'Learn a Word' first!")
        return

    learned_words = [word["word_id"] for word in user["learned_words"]]
    question_data = random.choice([word for word in WORDS if word["word_id"] in learned_words])

    correct_meaning = question_data["meaning"]
    all_meanings = [entry["meaning"] for entry in WORDS if entry["word_id"] != question_data["word_id"]]
    wrong_answers = random.sample(all_meanings, min(3, len(all_meanings)))
    options = wrong_answers + [correct_meaning]
    random.shuffle(options)

    # Store correct answer in user data
    user["correct_answer"] = correct_meaning
    save_users()

    keyboard = InlineKeyboardMarkup()
    for option in options:
        keyboard.add(InlineKeyboardButton(option, callback_data=f"quiz_answer_{option}"))

    bot.send_message(call.message.chat.id, f"🧠 Quiz Time!\n\nWhat does '{question_data['word_id']}' mean?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("quiz_answer_"))
def check_answer(call):
    """ Check quiz answer and update the user data. """
    selected_answer = call.data.replace("quiz_answer_", "")
    user = get_user(call.message.chat.id)
    correct_answer = user.get("correct_answer", "")

    if selected_answer == correct_answer:
        response = "✅ Correct! Well done! 🎉"
        user["score"] += 1
    else:
        response = f"❌ Wrong! The correct answer was: {correct_answer}."

    user["total_quiz"] += 1
    save_users()

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("📖 Learn a Word", callback_data="learn"),
        InlineKeyboardButton("🧠 Take Another Quiz", callback_data="quiz")
    )

    bot.answer_callback_query(call.id)
    bot.edit_message_text(f"{response}\n\nWhat would you like to do next?", chat_id=call.message.chat.id,
                          message_id=call.message.message_id, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "view_words")
def view_learned_words(call):
    """ Display all learned words and their meanings. """
    user = get_user(call.message.chat.id)

    if not user["learned_words"]:
        bot.send_message(call.message.chat.id, "📖 You haven't learned any words yet!")
        return

    learned_word_ids = {entry["word_id"] for entry in user["learned_words"]}
    learned_words = [word for word in WORDS if word["word_id"] in learned_word_ids]

    response = "📚 Learned Words:\n"
    for word in learned_words:
        response += f"\n📝 {word['word_id']} - 📖 {word['meaning']}"

    bot.send_message(call.message.chat.id, response)

bot.polling()
