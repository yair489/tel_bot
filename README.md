# 🌍 Language Bot

![Language Bot](https://github.com/user-attachments/assets/417b10ef-c13c-467c-a988-39082cf24489)

## 🎯 About this Bot
**Language Bot** is a Telegram bot designed to help users learn Arabic interactively! 🚀

## 👥 The Team
🏆 [Suleiman Awiwi](https://github.com/slemanaweiwi)  
🏆 [Yair Turgeman](https://github.com/yair489)  
🏆 [Mendy Segal](https://github.com/Mendysegal20)  

---

## ✨ Features
✅ **Learn Arabic Words** – Get a new word with its meaning, similar words, and an example sentence.  
✅ **Take Quizzes** – Test your knowledge with interactive quizzes.  
✅ **Show Learned Words** – View all the words you've learned so far.  
✅ **Hear the Word** – Click a button to listen to the correct pronunciation. 🎧  
✅ **Join a Group & Play Together** – Learn new words and play language challenges with friends! 🎮👥  
✅ **Future Plans** – Support for more languages and customizable learning preferences.  

---

## 🚀 Try the Bot Now!
👉 [Try the Bot Now!](http://t.me/Language_boost_bot)

---

## 📸 Screenshots / Demo
🚧 [Watch Demo](https://github.com/user-attachments/assets/a95aba67-5626-4956-89b5-671db5ca7d8f)

---

## 📢 Instructions for Developers
### 🔧 Prerequisites
- **uv** (Manages Python & dependencies)
- **MongoDB** (For storing user progress & learned words)

### 🚀 Setup
1️⃣ Clone this repository:
```sh
git clone https://github.com/GrunitechStudents/bot-hackathon-language_team_suleiman_mendy_yair.git
cd bot-hackathon-language_team_suleiman_mendy_yair
```
2️⃣ Create a Telegram bot via [BotFather](https://telegram.me/BotFather) and obtain an API Token.

3️⃣ Create a `bot_secrets.py` file and add your credentials:
```python
BOT_TOKEN = 'your-telegram-bot-token'
MONGO_URI = 'your-mongodb-connection-string'
GEMINI_API_KEY = 'your-gemini-api-key'
```

### ▶️ Running the Bot
Run the bot using **uv** (installs Python 3.13 and dependencies automatically):
```sh
uv run bot.py
```

---

## 📌 Additional Notes
💡 **Learning System** – The bot fetches words using Gemini AI and stores user progress in MongoDB.  
💡 **Data Storage**:
   - **Words database**: `word_heb_arabic.json` (or MongoDB)
   - **User progress**: Stored in MongoDB for persistent tracking.  
💡 **Scalability** – Future versions will support multiple languages and allow users to choose their native and target languages.  

---

## 🎨 Canva Presentation
📢 [View Canva Presentation](https://www.canva.com/design/DAGg2Bdh6qQ/tlZ-gjuJzDkxueFlHRxHIA/view?utm_content=DAGg2Bdh6qQ&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h65c86d3b02)
