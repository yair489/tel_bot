import json
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

TOKEN = "7861450739:AAHPeoXzDOoMVvPzGQ5U30C1BJ7d2elKHhg"
bot = telebot.TeleBot(TOKEN)

USER_DATA_FILE = "user.json"
WORD_LIST_FILE = "word_heb_arabic.json"

# Load user data from JSON file
def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist

# Load word list from JSON file
def load_word_list():
    try:
        with open(WORD_LIST_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist

# Get user data by user_id
def get_user_data(user_id):
    users = load_user_data()
    return next((user for user in users if user["_id"] == user_id), None)

# Get learned words for a user
def get_learned_words(user_id):
    user = get_user_data(user_id)
    if user:
        return user["learned_words"]
    return []

# Add learned word to user
def add_learned_word(user_id, word_id, correct):
    users = load_user_data()
    user = get_user_data(user_id)
    if user:
        learned_word = {
            "word_id": word_id,
            "correct": correct,
            "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        user["learned_words"].append(learned_word)
        with open(USER_DATA_FILE, "w") as file:
            json.dump(users, file, indent=4)

# Get a random word for learning (check if it hasn't been learned in the last month)
def get_random_word(user_id):
    word_list = load_word_list()  # Load the full word list from the word DB
    learned_words = get_learned_words(user_id)  # Get the words that the user has learned

    # If no words have been learned yet, allow the user to learn any word
    if not learned_words:
        if word_list:  # If there are words in the word list
            return word_list[0]  # Return the first word in the list (or you can randomize this)
        else:
            return None  # No words to learn, return None if the word list is empty

    # Otherwise, filter out learned words from the word list
    learned_word_ids = {learned_word['word_id'] for learned_word in learned_words}
    available_words = [word for word in word_list if word['word_id'] not in learned_word_ids]

    # Return the first available word or None if no word is available
    if available_words:
        return available_words[0]
    return None


# Start command - Ask for user's ID first
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Please provide your username:")
    bot.register_next_step_handler(message, ask_username, user_id)

def ask_username(message, user_id):
    username = message.text  # Get username
    user_info = {
        "_id": int(user_id),  # Use user-provided ID
        "username": username,
        "language_target": "Unknown",
        "language_native": "Unknown",
        "score": 0,
        "total_quiz": 0,
        "total_words": 0,
        "learned_words": []
    }

    # Save user info to JSON file
    users = load_user_data()
    users.append(user_info)
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

    user_info_message = f"👤 User Info:\n🆔 ID: {user_id}\n👤 Username: {username}\n"
    bot.send_message(user_id, user_info_message)

    # Ask user what they'd like to do next
    welcome_message = "What would you like to do?"
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("📖 Learn a Word", callback_data="learn"))
    keyboard.row(InlineKeyboardButton("🎮 Play a Game", callback_data="game"))
    keyboard.row(InlineKeyboardButton("📋 Show Learned Words", callback_data="show_learned"))

    bot.send_message(user_id, welcome_message, reply_markup=keyboard)

# Handler for learning a word
@bot.callback_query_handler(func=lambda call: call.data == "learn")
def learn_word(call):
    user_id = call.message.chat.id
    word = get_random_word(user_id)  # Fetch a random word to learn

    if word:
        word_message = f"Word to learn:\nWord: {word['word_id']}\nMeaning: {word['meaning']}\nSentence: {word['sentence_with_word']}"
        bot.send_message(user_id, word_message)

        # Mark the word as learned (you can modify it as correct or not after quiz)
        add_learned_word(user_id, word['word_id'], correct=True)
    else:
        bot.send_message(user_id, "Sorry, there are no words available to learn at this time.")

# Handler for playing a game (quiz)
@bot.callback_query_handler(func=lambda call: call.data == "game")
def play_game(call):
    user_id = call.message.chat.id
    learned_words = get_learned_words(user_id)

    if not learned_words:
        bot.send_message(user_id, "You haven't learned any words yet. Please learn some words first.")
        return

    # Choose a random learned word for the quiz
    word_to_quiz = learned_words[0]  # You can change this to a random learned word
    word_id = word_to_quiz['word_id']

    # Get the word details from the word list
    word_list = load_word_list()
    word = next((w for w in word_list if w['word_id'] == word_id), None)

    if word:
        word_message = f"Quiz time! What is the meaning of this word?\nWord: {word['word_id']}\n"
        bot.send_message(user_id, word_message)
        # You can also add buttons for the quiz answers if needed.
        # Here you can create a multiple-choice quiz for the user.
    else:
        bot.send_message(user_id, "Sorry, I couldn't find the word for the quiz.")

# Handler for showing learned words
@bot.callback_query_handler(func=lambda call: call.data == "show_learned")
def show_learned_words(call):
    user_id = call.message.chat.id
    learned_words = get_learned_words(user_id)

    if not learned_words:
        bot.send_message(user_id, "You have not learned any words yet.")
        return

    learned_message = "📋 List of Learned Words:\n"
    for learned_word in learned_words:
        learned_message += f"Word ID: {learned_word['word_id']}, Correct: {learned_word['correct']}, Date: {learned_word['date_time']}\n"

    bot.send_message(user_id, learned_message)

if __name__ == "__main__":
    bot.polling(none_stop=True)
