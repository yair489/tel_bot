import json
import random
from telebot.types import ReplyKeyboardMarkup, KeyboardButton ,InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from dataclasses import asdict
from cls_word_user import Word , User

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
        if existing_user["_id"] == user._id:
            print("User already exists!")
            return

    # if not exist
    user_data = {
        "_id": user._id,
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
    users_data = get_user_byid(user_id)
    if not users_data:
        return []
    return (users_data.learned_words)

def get_learned_words_list(user_id):
    all_word_list = get_learned_words_byid(user_id)
    for word_dic in all_word_list:
        return [word_dic[ "word_id"] for word_dic in all_word_list]


def get_new_words(user_id):
    learn_word = set(get_learned_words_list(user_id))
    with open("word_heb_arabic.json", "r", encoding="utf-8") as file:
        words = json.load(file)
    # for word in words:
    count = 0
    while True:
        count += 1
        if count == 100:
            break

        word = random.choice(words)
        if word["word_id"] not in learn_word:
            return Word(**word)
    return "No words found!"




# @bot.message_handler(commands=['start'])
# def start(message):
#     user_id = message.chat.id
#     username = message.chat.username or "Unknown"
#     first_name = message.chat.first_name or "Unknown"
#     last_name = message.chat.last_name or ""
#
#     '''save user in object and save him in json'''
#     user = User(_id= user_id , username =username)
#     add_user_to_json(user)
#     # welcome_message = (
#     #     "Hello! I’m your Language Learning Bot. 📚\n\n"
#     #     "🔹 Learn new words\n"
#     #     "🔹 Take quizzes based on words you've learned\n"
#     #     "🔹 View all learned words\n\n"
#     #     "Click a button to get started!"
#     # )
#     user_info = (f"👤 User Info:\n"
#                  f"🆔 ID: {user_id}\n"
#                  f"👤 Username: {username}\n"
#                  f"📛 Name: {first_name} {last_name}\n")
#
#     bot.send_message(user_id, user_info)
#
#     welcome_message = "What would you like to do?"
#     from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#
#     keyboard = InlineKeyboardMarkup()
#     keyboard.row(InlineKeyboardButton("📖 Learn a Word", callback_data="learn"),
#                  InlineKeyboardButton("🎮 Play a Game", callback_data="game"))
#     keyboard.row(InlineKeyboardButton("📚 View Learned Words", callback_data="view_words"))
#
#     # # יצירת תפריט כפתורים תחתון
#     # keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
#     # keyboard.row(KeyboardButton("📖 Learn a Word" ), KeyboardButton("🎮 Play a Game"))
#     # keyboard.row(KeyboardButton("📚 View Learned Words"))
#
#     bot.send_message(user_id, welcome_message, reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    username = message.chat.username or "Unknown"
    first_name = message.chat.first_name or "Unknown"
    last_name = message.chat.last_name or ""

    '''save user in object and save him in json'''
    user = User(_id= user_id , username =username)
    add_user_to_json(user)

    user_id = message.chat.id
    send_main_menu(user_id)


def send_main_menu(user_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("📖 Learn a Word", callback_data="learn"),
                 InlineKeyboardButton("🎮 Play a Game", callback_data="game"))
    keyboard.row(InlineKeyboardButton("📚 View Learned Words", callback_data="view_words"))
    bot.send_message(user_id, "Choose an option:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "learn")
def learn_word(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    new_word = get_new_words(user_id)
    bot.send_message(user_id, f"📖 Learning a new word\n{new_word.word_id} translate: {new_word.meaning}")
    send_main_menu(user_id)


@bot.callback_query_handler(func=lambda call: call.data == "game")
def play_game(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    new_word = get_new_words(user_id)
    options = new_word.similar_words + [new_word.meaning]
    random.shuffle(options)
    keyboard = InlineKeyboardMarkup()
    for option in options:
        keyboard.row(
            InlineKeyboardButton(option, callback_data=f"answer_{option}_{new_word.meaning}_{new_word.word_id}"))
    bot.send_message(user_id, f"❓ What is the meaning of '{new_word.word_id}'?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"))
def check_answer(call):
    user_id = call.message.chat.id
    chosen_answer = call.data.split("_")
    bot.delete_message(user_id, call.message.message_id)
    correct_answer = chosen_answer[2]
    word_id = chosen_answer[3]

    if chosen_answer[1] == correct_answer:
        response = f"✅ Correct! 🎉\n {word_id} is: {correct_answer}"
    else:
        response = f"❌ Wrong!\n The translate for {word_id} is: {correct_answer}"

    bot.send_message(user_id, response)
    send_main_menu(user_id)


@bot.callback_query_handler(func=lambda call: call.data == "view_words")
def view_words(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    learned_words = get_learned_words_list(user_id)  # פונקציה להחזיר מילים שנלמדו
    words_text = "\n".join(learned_words) if learned_words else "You haven't learned any words yet."
    bot.send_message(user_id, f"📚 Learned Words:\n{words_text}")
    send_main_menu(user_id)
#
# @bot.message_handler(func=lambda message: message.text == "📖 Learn a Word")
# def learn_word(message):
#     #delete message
#     user_id = message.chat.id
#     bot.delete_message(user_id, message.message_id)
#
#     user_id = message.chat.id
#     new_word = get_new_words(user_id)
#     bot.send_message(user_id, f"📖 Learning a new word\n{new_word.word_id} translate: {new_word.meaning}")
#
# @bot.message_handler(func=lambda message: message.text == "🎮 Play a Game")
# def play_game(message):
#     # Delete the initial message
#     user_id = message.chat.id
#     bot.delete_message(user_id, message.message_id)
#
#     # Get a new word for the user
#     new_word = get_new_words(user_id)
#
#     # Create a list of answers with the correct answer and 3 wrong answers
#     options = new_word.similar_words + [new_word.meaning]
#     random.shuffle(options)  # Shuffle the answers
#
#     print(new_word.word_id)
#     # Create an inline keyboard with buttons for each option
#     keyboard = InlineKeyboardMarkup()
#     for option in options:
#         keyboard.row(InlineKeyboardButton(option, callback_data=f"answer_{option}_{new_word.meaning}_{new_word.word_id}"))
#
#     # Send the message with the word and the options
#     bot.send_message(user_id, f"❓ What is the meaning of '{new_word.word_id}'?", reply_markup=keyboard)
#
# # Function to handle when the user selects an answer
# @bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"))
# def check_answer(call):
#     user_id = call.message.chat.id
#     chosen_answer = call.data.split("_")
#
#     # Delete the message with the question and options
#     bot.delete_message(user_id, call.message.message_id)
#
#     # Check if the chosen answer is correct
#     new_word = get_new_words(user_id)  # Retrieve the current word again (this could be optimized)
#     correct_answer = new_word.meaning
#
#     if chosen_answer[1] == chosen_answer[2]:
#         bot.send_message(user_id, f"✅ Correct! 🎉\n {chosen_answer[3]} is : {chosen_answer[2]}")
#     else:
#         bot.send_message(user_id, f"❌ Wrong!\n The translate for {chosen_answer[3]} is: {chosen_answer[2]}")






if __name__ == "__main__":
    bot.polling(none_stop=True)
