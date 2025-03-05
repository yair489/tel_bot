🌍 Language Bot

The Team

🏆 [Suleiman Awiwi](https://github.com/slemanaweiwi) 

🏆 [Yair Turgeman](https://github.com/yair489)

🏆 [Mendy Segal](https://github.com/Mendysegal20)

About this Bot

Language Bot is a Telegram bot designed to help users learn Arabic in an interactive way! 🚀

✨ Features

✅ Learn Arabic Words – Get a new word with its meaning, similar words, and an example sentence.

✅ Take Quizzes – Test your knowledge by taking quizzes based on words you've learned.

✅ Show Learned Words – View all words you've learned so far.

✅ Hear the Word – Click a button to listen to the correct pronunciation. 🎧

✅ Join a Group Chat & Play Together – At the start of the game, users can join a group chat to learn new words together and play fun language-learning challenges! 🎮👥

✅ Future Plans – We plan to support more languages and allow users to choose their native and target languages.

Try the Bot Now!
👉[Try the Bot Now!](t.me/@Language_boost_bot)

📸 Screenshots / Demo
🚧 [VIDEO](https://github.com/user-attachments/assets/a95aba67-5626-4956-89b5-671db5ca7d8f)



📢 Instructions for Developers

Prerequisites

uv (Manages Python & dependencies)

MongoDB (for storing user progress & learned words)

🚀 Setup

1️⃣ Clone this repository
git clone  https://github.com/GrunitechStudents/bot-hackathon-language_team_suleiman_mendy_yair.git

cd bot-hackathon-language_team_suleiman_mendy_yair

2️⃣ Create a Telegram Bot via BotFather and get an API Token.https://telegram.me/BotFather

3️⃣ Create a bot_secrets.py file and add your bot token:

BOT_TOKEN = 'your-telegram-bot-token'
MONGO_URI = 'your-mongodb-connection-string'
GEMINI_API_KEY = 'your-gemini-api-key'

▶️ Running the Bot
Run the bot with uv (This will install Python 3.13 and dependencies automatically):

uv run bot.py

📌 Additional Notes

💡 Learning System: The bot fetches words using Gemini AI and stores user progress in MongoDB.

💡 Data Storage:
Words database: word_heb_arabic.json (or MongoDB)

User progress: Stored in MongoDB for persistent tracking.

💡 Scalability: Future versions will support multiple languages and allow users to pick both their native and target languages.
