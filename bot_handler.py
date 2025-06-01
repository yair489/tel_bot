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
        keyboard.row(KeyboardButton("View Learned Words 📚"))

        bot.send_message(user_id, "Welcome! Choose an option: \n https://t.me/+pW9RQz3MHRI2MTk0", reply_markup=keyboard)

    elif chat_type in ["group", "supergroup"]:
        logger.info("start group act")
        chat_id = message.chat.id  # -chat_id
        user_id = message.from_user.id  #-user_id

        bot.send_message(chat_id, "👋 Hello group! To start a game, use /game")

@bot.message_handler(func=lambda msg: msg.text == "📖 Learn a Word")
def learn_word(message):
    user_id = message.chat.id
    new_word = word_manager.get_new_word(message.chat.id, user_manager)

    if new_word:
        # button Inline
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="🔊 Hear the word.", callback_data=f"say_{new_word.word_id}")
        keyboard.add(button)

        # send message with botuuon
        bot.send_message(
            message.chat.id,
            f"📖 New word:\n{new_word.word_id} translates to: {new_word.meaning} \n\n sentence with word: \n{new_word.sentence_with_word}",
            reply_markup=keyboard
        )

        # save the word user
        user_manager.add_or_update_learned_word(user_id=user_id, word=new_word)
        user_manager.increment_total_words(user_id)
    else:
        bot.send_message(message.chat.id, "No new words available.")


# say the word function
@bot.callback_query_handler(func=lambda call: call.data.startswith("say_"))
def say_word(call):
    word_to_say = call.data.split("_", 1)[1]  # חילוץ המילה מה-callback_data
    tts = gTTS(text=word_to_say, lang='ar')  # המרה לטקסט מדובר lang='iw'
    tts.save("word.mp3")

    # send aduio to user
    with open("word.mp3", "rb") as audio:
        bot.send_audio(call.message.chat.id, audio)

    bot.answer_callback_query(call.id, "🔊 המילה הושמעה!")
@bot.message_handler(func=lambda msg: msg.text == "🎮 Play a Game")
def play_game(message):
    user_words = user_manager.get_learned_words_list(message.chat.id)
    if not user_words:
        bot.send_message(message.chat.id, f"You haven't learned anything yet, brother.")
        return
    user_word_random = random.choice(user_words)
    print(user_word_random)
    new_word = word_manager.get_word(user_word_random)
    print(new_word)

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


@bot.message_handler(func=lambda msg: msg.text == "View Learned Words 📚")
def view_words(message):
    user_id = message.from_user.id
    learned_words = user_manager.get_learned_words_obj(user_id)
    st = "📚 Learned Words:\n"
    # st += f"{'word_id':<10} {'translate':<10} {'correct'}\n"
    st += "-" * 30 + "\n"

    for word in learned_words:
        st += f"{"/"+word.word_id:<10} {'->':<10} {word.correct}\n"
    bot.send_message(message.chat.id, st)


##################################################
# @bot.message_handler(func=lambda message: message.chat.type in ["group", "supergroup"])
# def block_group_messages(message):
#
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
#
#
#     else:
#         bot.send_message(user_id, "❌ This command is only available in groups!")


import random
import time
from threading import Timer
from telebot import types


def get_random_question():
    logger.info("Getting random get_random_question")
    words = word_manager.load_words()
    random_word = random.choice(words)
    game_manager.new_question(random_word.word_id,  random_word.meaning , random_word.similar_words)
    logger.info(f"Random word {words=} , {random_word=}")

def get_py_answer():
     q, answer, opption = game_manager.py_ques()
     game_manager.new_question(q, answer, opption)
     logger.info(f"get_py_answer")
    # random.shuffle(options)



# manage the game
@bot.message_handler(commands=['game'])
def group_game(message):
    logger.info("Group game func")
    chat_type = message.chat.type
    chat_id = message.chat.id
    user_from = message.from_user.id

    if chat_type in ["group", "supergroup"]:

        bot.send_message(chat_id, "🎮 Starting a group game!")
        game_manager.add_group(chat_id)
        question_generator = game_manager.py_ques()  # create obj generator
        for i in range(5):
            show_question(chat_id , question_generator)
            time.sleep(5)


        for username, img_buffer in game_manager.generate_score_charts(game_manager.get_scores()):
            img_buffer.seek(0)
            bot.send_photo(username, img_buffer, caption=f"📊 Stats for {username}")

    else:
        bot.send_message(chat_id, "❌ This command is only available in groups!")


def show_question(chat_id , question_generator):
    # random ques
    # get_random_question()
    #
    # logger.info(f"add to list in show_question on {logger.name}")
    #
    # game_manager.options.append(game_manager.answer)
    # options = game_manager.options[:]
    # random.shuffle(options)
    #
    # print(game_manager.options)

    # get py ques
    # question_generator = game_manager.py_ques()  # create obj generator
    q, answer, options = next(question_generator)
    game_manager.new_question(q, answer, options)
    ########################
    random.shuffle(game_manager.options)

    # send question with option
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for option in game_manager.options:
        # logger.info(f" {option=} keybord")
        keyboard.add(option)

    msg = bot.send_message(chat_id,
                     f"📝 Question: {game_manager.question} - ???\nChoose the correct translation:",
                     reply_markup=keyboard)

    # 60 second
    Timer(5, handle_timeout).start()

def handle_timeout():
    pass


@bot.message_handler(func=lambda msg: msg.text in game_manager.options)
def handle_answer(message):
    logger.info(f"get message from {message.from_user} - {message.text} ")

    corr, ans_user = game_manager.answer, message.text
    game_manager.update_scores_failure(message.from_user.id, corr, ans_user)

    # send private response to user
    bot.send_message(message.from_user.id,
                     f"You {'✅ Correct!' if corr == ans_user else '❌ Wrong!'} , the answer is: {corr}")

    # delete message after the user write
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        logger.error(f"Failed to delete message: {e}")


