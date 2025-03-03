import random
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = "7861450739:AAHPeoXzDOoMVvPzGQ5U30C1BJ7d2elKHhg"


# Vocabulary list (word, meaning, example)
WORDS = [
    ("Hello", "שלום", "אני אומר שלום לכל מי שאני פוגש."),
    ("Sun", "שמש", "השמש זורחת בבוקר."),
    ("Water", "מים", "אני שותה מים כל יום."),
    ("Book", "ספר", "אני קורא ספר לפני השינה."),
    ("House", "בית", "הבית שלי נמצא בירושלים."),
    ("Tree", "עץ", "יש עץ גדול בגינה שלי."),
    ("Dog", "כלב", "למשפחה שלי יש כלב חמוד."),
    ("Love", "אהבה", "אהבה היא הרגש החזק ביותר."),
    ("Friend", "חבר", "החבר הכי טוב שלי גר לידי."),
    ("Food", "אוכל", "אני אוהב אוכל ישראלי.")
]


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

def add_user_to_json():
async def start(update: Update, context: CallbackContext) -> None:
    """ Sends a welcome message with available commands. """
    welcome_message = (
        "Hello! I’m your Language Learning Bot. 📚\n\n"
        "🔹 Learn new words\n"
        "🔹 Take quizzes based on words you've learned\n\n"
        "Click a button to get started!"
    )
    keyboard = [
        [InlineKeyboardButton("📖 Learn a Word", callback_data="learn")],
        [InlineKeyboardButton("🧠 Take a Quiz", callback_data="quiz")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

def add_word_to_user():
    pass
async def learn_word(update: Update, context: CallbackContext) -> None:
    """ Sends a new word, avoiding repetition. """
    user_words = context.user_data.get("learned_words", set())
    last_learned = context.user_data.get("last_learned", None)

    # Get an unseen word
    available_words = [word for word in WORDS if word[0] not in user_words]
    if not available_words:
        await update.callback_query.message.reply_text("🎉 You've learned all available words!")
        return

    # Ensure we don’t repeat the last learned word
    word, meaning, example = random.choice(available_words)
    while word == last_learned and len(available_words) > 1:
        word, meaning, example = random.choice(available_words)

    # Store the learned word
    user_words.add(word)
    context.user_data["learned_words"] = user_words
    context.user_data["last_learned"] = word

    response = f"📝 Word: {word}\n📖 Meaning: {meaning}\n✍ Example: {example}"

    # Next step buttons
    keyboard = [
        [InlineKeyboardButton("🧠 Take a Quiz", callback_data="quiz")],
        [InlineKeyboardButton("📖 Learn Another Word", callback_data="learn")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.reply_text(response, parse_mode="Markdown", reply_markup=reply_markup)


def get_learned_words():
    #option to filter just words that we didnt do
    pass

def edit_learned_words():
    pass
async def quiz(update: Update, context: CallbackContext) -> None:
    """ Creates a quiz question based on words the user has learned, avoiding repetition. """
    user_words = context.user_data.get("learned_words", set())
    last_quizzed = context.user_data.get("last_quizzed", None)

    if not user_words:
        await update.callback_query.message.reply_text(
            "❗ You haven't learned any words yet. Click 'Learn a Word' first!")
        return

    # Get words that haven't been quizzed recently
    learned_word_data = [word for word in WORDS if word[0] in user_words]
    question_data = random.choice(learned_word_data)

    # Ensure we don’t repeat the last quiz word
    while question_data[0] == last_quizzed and len(learned_word_data) > 1:
        question_data = random.choice(learned_word_data)

    word, correct_meaning, _ = question_data
    context.user_data["last_quizzed"] = word  # Store last quizzed word

    # Generate answer choices (shuffle correct + 3 wrong meanings)
    all_meanings = [entry[1] for entry in WORDS if entry[0] != word]
    wrong_answers = random.sample(all_meanings, min(3, len(all_meanings)))
    options = wrong_answers + [correct_meaning]
    random.shuffle(options)

    # Store correct answer in context
    context.user_data["correct_answer"] = correct_meaning

    # Create buttons
    keyboard = [[InlineKeyboardButton(option, callback_data=f"quiz_answer_{option}")] for option in options]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.reply_text(f"🧠 Quiz Time!\n\nWhat does '{word}' mean?",
                                                   reply_markup=reply_markup, parse_mode="Markdown")


async def check_answer(update: Update, context: CallbackContext) -> None:
    """ Checks if the user's quiz answer is correct and offers next steps. """
    query = update.callback_query
    selected_answer = query.data.replace("quiz_answer_", "")
    correct_answer = context.user_data.get("correct_answer")

    if selected_answer == correct_answer:
        response = "✅ Correct! Well done! 🎉"
    else:
        response = f"❌ Wrong! The correct answer was: {correct_answer}."

    # Next step buttons
    keyboard = [
        [InlineKeyboardButton("📖 Learn a Word", callback_data="learn")],
        [InlineKeyboardButton("🧠 Take Another Quiz", callback_data="quiz")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.answer()
    await query.edit_message_text(f"{response}\n\nWhat would you like to do next?",
                                  parse_mode="Markdown", reply_markup=reply_markup)


async def button_handler(update: Update, context: CallbackContext) -> None:
    """ Handles all button clicks. """
    query = update.callback_query
    query.answer()

    if query.data == "learn":
        await learn_word(update, context)
    elif query.data == "quiz":
        await quiz(update, context)
    elif query.data.startswith("quiz_answer_"):
        await check_answer(update, context)


def main():
    """ Runs the bot. """
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))  # Handles all button clicks

    app.run_polling()


if name == "main":
    main()
