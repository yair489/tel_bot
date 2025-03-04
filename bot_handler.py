import logging
from datetime import datetime
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from private.user_manager import UserManager
from private.word_manager import WordManager
from private.game_manger import GameManager
from private.model import User, Group
import random
from gtts import gTTS
from private.bot_secretes import TOKEN

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)
user_manager = UserManager()
word_manager = WordManager()
game_manager = GameManager()



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
        logger.info("start group act")
        chat_id = message.chat.id  # שולף את ה-chat_id של הצ'אט
        user_id = message.from_user.id  # שולף את ה-user_id של המשתמש

        bot.send_message(chat_id, "👋 Hello group! To start a game, use /game")

@bot.message_handler(func=lambda msg: msg.text == "📖 Learn a Word")
def learn_word(message):
    user_id = message.chat.id
    new_word = word_manager.get_new_word(message.chat.id, user_manager)

    if new_word:
        # button Inline
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="🔊 השמע את המילה", callback_data=f"say_{new_word.word_id}")
        keyboard.add(button)

        # שליחת הודעה עם הכפתור
        bot.send_message(
            message.chat.id,
            f"📖 New word:\n{new_word.word_id} translates to: {new_word.meaning}",
            reply_markup=keyboard
        )

        # שמירת המילה של המשתמש
        user_manager.add_or_update_learned_word(user_id=user_id, word=new_word)
        user_manager.increment_total_words(user_id)
    else:
        bot.send_message(message.chat.id, "No new words available.")


# פונקציה שתשמע את המילה
@bot.callback_query_handler(func=lambda call: call.data.startswith("say_"))
def say_word(call):
    word_to_say = call.data.split("_", 1)[1]  # חילוץ המילה מה-callback_data
    tts = gTTS(text=word_to_say, lang='ar')  # המרה לטקסט מדובר lang='iw'
    tts.save("word.mp3")

    # שליחת קובץ האודיו למשתמש
    with open("word.mp3", "rb") as audio:
        bot.send_audio(call.message.chat.id, audio)

    bot.answer_callback_query(call.id, "🔊 המילה הושמעה!")
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
        user_manager.increase_user_score(call.message.chat.id, 1)
    else:
        bot.send_message(call.message.chat.id, f"❌ Wrong! The correct answer for {word_id} is: {correct_answer}")
    user_manager.increment_total_quiz(call.message.chat.id)
    update_fields_score = {
        "total_quiz": {"$inc": 1}  # -total_quiz 1
    }
    # self.user_manager.update_user(call.message.chat.id , update_fields=update_fields_score)

@bot.message_handler(func=lambda msg: msg.text == "View Learned Words 📚")
def view_words(message):
    user_id = message.from_user.id
    learned_words = user_manager.get_learned_words_obj(user_id)
    st = "📚 Learned Words:\n"
    st += f"{'word_id':<10} {'translate':<10} {'correct'}\n"
    st += "-" * 30 + "\n"

    for word in learned_words:
        st += f"{"/"+word.word_id:<10} {'->':<10} {word.correct}\n"
    bot.send_message(message.chat.id, st)


##################################################
# @bot.message_handler(func=lambda message: message.chat.type in ["group", "supergroup"])
# def block_group_messages(message):
#     """ חוסם הודעות בקבוצה שלא קשורות לפקודות הבוט """
#     try:
#         bot.delete_message(message.chat.id, message.message_id)
#     except Exception as e:
#         print(f"Failed to delete message: {e}")
# @bot.message_handler(commands=['game'])
# def group_game(message):
#     logger.info("Group game func")
#     chat_type = message.chat.type
#     user_id = message.chat.id
#
#     if chat_type in ["group", "supergroup"]:
#         bot.send_message(user_id, "🎮 Starting a group game!")
#         # כאן אפשר להוסיף את הלוגיקה של המשחק בקבוצה
#
#     else:
#         bot.send_message(user_id, "❌ This command is only available in groups!")


import random
import time
from threading import Timer
from telebot import types


# פונקציה לבחירת שאלה רנדומלית
def get_random_question():
    logger.info("Getting random get_random_question")
    words = word_manager.load_words()
    random_word = random.choice(words)
    game_manager.new_question(random_word.word_id,  random_word.meaning , random_word.similar_words)
    logger.info(f"Random word {words=} , {random_word=}")

    # random.shuffle(options)



# הפונקציה לניהול המשחק בקבוצה
@bot.message_handler(commands=['game'])
def group_game(message):
    logger.info("Group game func")
    chat_type = message.chat.type
    chat_id = message.chat.id
    user_from = message.from_user.id

    if chat_type in ["group", "supergroup"]:

        bot.send_message(chat_id, "🎮 Starting a group game!")
        game_manager.add_group(chat_id)

        for i in range(5):
            show_question(chat_id)
            time.sleep(5)


        # game_manager.update_scores_failure(1005165332 , 1 ,2)

    else:
        bot.send_message(chat_id, "❌ This command is only available in groups!")


def show_question(chat_id):
    # random ques
    get_random_question()

    logger.info(f"add to list in show_question on {logger.name}")

    game_manager.options.append(game_manager.answer)  # הוספת התשובה הנכונה
    options = game_manager.options[:]  # יצירת רשימה חדשה כדי שלא יהיה שינוי על הרשימה המקורית
    random.shuffle(options)

    print(game_manager.options)
    random.shuffle(game_manager.options)

    # שלח את השאלה עם אפשרויות
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for option in game_manager.options:
        logger.info(f" {option=} keybord")
        keyboard.add(option)

    bot.send_message(chat_id,
                     f"📝 Question: {game_manager.question} - ???\nChoose the correct translation:",
                     reply_markup=keyboard)

    # 60 second
    Timer(5, handle_timeout).start()

# הפונקציה לטיפול בזמן שאלה
def handle_timeout():
    pass

@bot.message_handler(func=lambda msg: msg.text in game_manager.options)
def handle_answer(message):
    logger.info(message)
    pass



