import logging
from datetime import datetime
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from private.user_manager import UserManager
from private.word_manager import WordManager
from private.cls_word_user import User
import random

TOKEN = "7739208491:AAEpzCxss5m2iPGgKgSVoZFSA1soTDjwido"

# class BotHandler:
#     def __init__(self):
#         self.bot = telebot.TeleBot(TOKEN)
#         self.user_manager = UserManager()
#         self.word_manager = WordManager()
#         self.register_handlers()
#
#     def register_handlers(self):
#         @self.bot.message_handler(commands=['start'])
#         def start(message):
#             chat_type = message.chat.type  # 'private', 'group', 'supergroup'
#             user_id = message.chat.id
#             if chat_type == "private":
#                 user = User(id=user_id, username=message.chat.username or "Unknown", full_name=message.chat.first_name or "Unknown")
#                 print(user)
#                 self.user_manager.add_user(user)
#
#                 keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
#                 keyboard.row(KeyboardButton("📖 Learn a Word"), KeyboardButton("🎮 Play a Game"))
#                 keyboard.row(KeyboardButton("View Learned Words 📚"), KeyboardButton("not work yet"))
#
#                 self.bot.send_message(user_id, "Welcome! Choose an option:", reply_markup=keyboard)
#
#             elif chat_type in ["group", "supergroup"]:
#                 self.bot.send_message(user_id, "👋 Hello group! To start a game, use /game")
#
#         @self.bot.message_handler(func=lambda msg: msg.text == "📖 Learn a Word")
#         def learn_word(message):
#             new_word = self.word_manager.get_new_word(message.chat.id, self.user_manager)
#             if new_word:
#                 self.bot.send_message(message.chat.id, f"📖 New word:\n{new_word.word_id} translates to: {new_word.meaning}")
#                 self.user_manager.add_or_update_learned_word(user_id=message.chat.id,word=new_word)
#             else:
#                 self.bot.send_message(message.chat.id, "No new words available.")
#
#         @self.bot.message_handler(func=lambda msg: msg.text == "🎮 Play a Game")
#         def play_game(message):
#             new_word = self.word_manager.get_new_word(message.chat.id, self.user_manager)
#             if not new_word:
#                 self.bot.send_message(message.chat.id, "No new words available.")
#                 return
#
#             options = new_word.similar_words + [new_word.meaning]
#             random.shuffle(options)
#
#             keyboard = InlineKeyboardMarkup()
#             for option in options:
#                 keyboard.row(InlineKeyboardButton(option, callback_data=f"answer_{option}_{new_word.meaning}_{new_word.word_id}"))
#
#             self.bot.send_message(message.chat.id, f"❓ What is the meaning of '{new_word.word_id}'?", reply_markup=keyboard)
#
#         @self.bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"))
#         def check_answer(call):
#             data = call.data.split("_")
#             chosen_answer, correct_answer, word_id = data[1], data[2], data[3]
#             flag_if_correct_answer = False
#             self.bot.delete_message(call.message.chat.id, call.message.message_id)
#             if chosen_answer == correct_answer:
#                 flag_if_correct_answer = True
#                 self.bot.send_message(call.message.chat.id, f"✅ Correct! 🎉\n {word_id} means: {correct_answer}")
#                 today_date = datetime.today().strftime('%d.%m.%Y')
#                 update_fields_date_time = {
#                     "learned_words.$[].date_time": today_date  ,# עדכון ה-date_time לכל המילים
#                     "score" : {"$inc": 1}
#                 }
#                 # self.user_manager.update_user(call.message.chat.id , update_fields=update_fields_date_time)
#             else:
#                 self.bot.send_message(call.message.chat.id, f"❌ Wrong! The correct answer for {word_id} is: {correct_answer}")
#
#             update_fields_score = {
#                 "total_quiz": {"$inc": 1}  # -total_quiz 1
#             }
#             # self.user_manager.update_user(call.message.chat.id , update_fields=update_fields_score)
#
#         @self.bot.message_handler(func=lambda msg: msg.text == "View Learned Words 📚")
#         def view_words(message):
#             learned_words = self.user_manager.get_learned_words_list(message.chat.id)
#             words_text = "\n".join(learned_words) if learned_words else "You haven't learned any words yet."
#             self.bot.send_message(message.chat.id, f"📚 Learned Words:\n{words_text}")
#
#
#         ##################################################
#         @self.bot.message_handler(commands=['game'])
#         def group_game(message):
#             chat_type = message.chat.type
#             user_id = message.chat.id
#
#             if chat_type in ["group", "supergroup"]:
#                 self.bot.send_message(user_id, "🎮 Starting a group game!")
#                 # כאן אפשר להוסיף את הלוגיקה של המשחק בקבוצה
#
#             else:
#                 self.bot.send_message(user_id, "❌ This command is only available in groups!")
#
#         @self.bot.message_handler(func=lambda message: message.chat.type in ["group", "supergroup"])
#         def block_group_messages(message):
#             """ חוסם הודעות בקבוצה שלא קשורות לפקודות הבוט """
#             try:
#                 self.bot.delete_message(message.chat.id, message.message_id)
#             except Exception as e:
#                 print(f"Failed to delete message: {e}")
#         #######################################################
#
#     def run(self):
#         self.bot.polling(none_stop=True)
bot = telebot.TeleBot(TOKEN)
user_manager = UserManager()
word_manager = WordManager()


@bot.message_handler(commands=['start'])
def start(message):
    chat_type = message.chat.type  # 'private', 'group', 'supergroup'
    user_id = message.chat.id
    if chat_type == "private":
        user = User(id=user_id, username=message.chat.username or "Unknown", full_name=message.chat.first_name or "Unknown")
        print(user)
        user_manager.add_user(user)

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        keyboard.row(KeyboardButton("📖 Learn a Word"), KeyboardButton("🎮 Play a Game"))
        keyboard.row(KeyboardButton("View Learned Words 📚"), KeyboardButton("not work yet"))

        bot.send_message(user_id, "Welcome! Choose an option:", reply_markup=keyboard)

    elif chat_type in ["group", "supergroup"]:
        bot.send_message(user_id, "👋 Hello group! To start a game, use /game")

@bot.message_handler(func=lambda msg: msg.text == "📖 Learn a Word")
def learn_word(message):
    new_word = word_manager.get_new_word(message.chat.id, user_manager)
    if new_word:
        bot.send_message(message.chat.id, f"📖 New word:\n{new_word.word_id} translates to: {new_word.meaning}")
        user_manager.add_or_update_learned_word(user_id=message.chat.id,word=new_word)
    else:
        bot.send_message(message.chat.id, "No new words available.")

@bot.message_handler(func=lambda msg: msg.text == "🎮 Play a Game")
def play_game(message):
    new_word = word_manager.get_new_word(message.chat.id, user_manager)
    if not new_word:
        bot.send_message(message.chat.id, "No new words available.")
        return

    options = new_word.similar_words + [new_word.meaning]
    random.shuffle(options)

    keyboard = InlineKeyboardMarkup()
    for option in options:
        keyboard.row(InlineKeyboardButton(option, callback_data=f"answer_{option}_{new_word.meaning}_{new_word.word_id}"))

    bot.send_message(message.chat.id, f"❓ What is the meaning of '{new_word.word_id}'?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"))
def check_answer(call):
    data = call.data.split("_")
    chosen_answer, correct_answer, word_id = data[1], data[2], data[3]
    flag_if_correct_answer = False
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if chosen_answer == correct_answer:
        flag_if_correct_answer = True
        bot.send_message(call.message.chat.id, f"✅ Correct! 🎉\n {word_id} means: {correct_answer}")
        today_date = datetime.today().strftime('%d.%m.%Y')
        update_fields_date_time = {
            "learned_words.$[].date_time": today_date  ,# עדכון ה-date_time לכל המילים
            "score" : {"$inc": 1}
        }
        # self.user_manager.update_user(call.message.chat.id , update_fields=update_fields_date_time)
    else:
        bot.send_message(call.message.chat.id, f"❌ Wrong! The correct answer for {word_id} is: {correct_answer}")

    update_fields_score = {
        "total_quiz": {"$inc": 1}  # -total_quiz 1
    }
    # self.user_manager.update_user(call.message.chat.id , update_fields=update_fields_score)

@bot.message_handler(func=lambda msg: msg.text == "View Learned Words 📚")
def view_words(message):
    learned_words = user_manager.get_learned_words_list(message.chat.id)
    words_text = "\n".join(learned_words) if learned_words else "You haven't learned any words yet."
    bot.send_message(message.chat.id, f"📚 Learned Words:\n{words_text}")


##################################################
@bot.message_handler(func=lambda message: message.chat.type in ["group", "supergroup"])
def block_group_messages(message):
    """ חוסם הודעות בקבוצה שלא קשורות לפקודות הבוט """
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"Failed to delete message: {e}")
@bot.message_handler(commands=['game'])
def group_game(message):
    chat_type = message.chat.type
    user_id = message.chat.id

    if chat_type in ["group", "supergroup"]:
        bot.send_message(user_id, "🎮 Starting a group game!")
        # כאן אפשר להוסיף את הלוגיקה של המשחק בקבוצה

    else:
        bot.send_message(user_id, "❌ This command is only available in groups!")

