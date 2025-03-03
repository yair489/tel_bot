import telebot
import random
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

TOKEN = "7861450739:AAHPeoXzDOoMVvPzGQ5U30C1BJ7d2elKHhg"
bot = telebot.TeleBot(TOKEN)

# Load word and user data
WORDS_FILE = "word_heb_arabic.json"
USERS_FILE = "users.json"

with open(WORDS_FILE, "r", encoding="utf-8") as f:
    WORDS = json.load(f)

with open(USERS_FILE, "r", encoding="utf-8") as f:
    USERS = json.load(f)

def save_users():
    """ Save users data to the file. """
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(USERS, f, indent=4, ensure_ascii=False)

def get_user(user_id):
    """ Retrieve or create user profile. """
    for user in USERS:
        if user["_id"] == user_id:
            return user
    new_user = {
        "_id": user_id,
        "username": "Unknown",
        "language_target": "arabic",
        "language_native": "hebrew",
        "score": 0,
        "total_quiz": 0,
        "total_words": 0,
        "learned_words": []
    }
    USERS.append(new_user)
    save_users()
    return new_user

@bot.message_handler(commands=["start"])
def start(message):
    """ Sends a welcome message with available commands. """
    user = get_user(message.chat.id)

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
    """ Learn a new word and store it in the user's profile. """
    user = get_user(call.message.chat.id)

    learned_word_ids = {entry["word_id"] for entry in user["learned_words"]}
    available_words = [word for word in WORDS if word["word_id"] not in learned_word_ids]

    if not available_words:
        bot.send_message(call.message.chat.id, "🎉 You've learned all available words!")
        return

    word_data = random.choice(available_words)
    word_id = word_data["word_id"]

    # Update user's learned words
    user["learned_words"].append({
        "word_id": word_id,
        "correct": False,
        "date_time": datetime.now().strftime("%d.%m.%Y")
    })
    user["total_words"] += 1
    save_users()

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
