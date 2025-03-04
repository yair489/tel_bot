import bot_handler
import logging
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")  # replace to main
    bot_handler = bot_handler.bot.polling(none_stop=True)
    # bot_handler.run()
