import random
import logging
from private.cls_word_user import Word
from pymongo import MongoClient

# Configure logging
logger = logging.getLogger(__name__)


class WordManager:
    COLLECTION_NAME = "words_hebrew_arabic"

    def __init__(self, db_uri="language_bot", collection_name=COLLECTION_NAME):
        self.client = MongoClient()  # Connect to MongoDB
        self.db = self.client.get_database(db_uri)
        self.collection = self.db.get_collection(collection_name)
        self.db_name = collection_name
        logger.info(f"Connected to MongoDB database: {db_uri}, collection: {collection_name}")

    def load_words(self):
        """
        Load all words from MongoDB collection.
        """
        words = list(self.collection.find({}, {"_id": 0}))
        logger.info(f"Loaded {len(words)} words from the database.")
        return words

    def get_new_word(self, user_id, user_manager):
        """
        Retrieve a new word that the user has not learned yet.
        """
        learned_words = set(user_manager.get_learned_words_list(user_id))
        words = self.load_words()

        if not words:
            logger.warning("No words found in the database.")
            return None

        random.shuffle(words)
        for word in words:
            if word["word_id"] not in learned_words:
                logger.info(f"User {user_id} is learning a new word: {word['word_id']}")
                return Word(**word)

        logger.info(f"User {user_id} has learned all available words.")
        return None

