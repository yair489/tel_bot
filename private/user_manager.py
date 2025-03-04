import logging
from pymongo import MongoClient
from datetime import datetime
import json
import random
from dataclasses import asdict
from private.model import User, Word, MyWords, Group
import bunnet

# Configure logging
logger = logging.getLogger(__name__)
class UserManager:
    def __init__(self, db_name="language_bot", collection_name="users"):
        """Initialize the UserManager with a connection to MongoDB."""
        self.client = MongoClient()  # Connect to MongoDB
        self.db = self.client.get_database(db_name)
        self.collection = self.db.get_collection(collection_name)
        self.db_name = db_name
        bunnet.init_bunnet(self.db , document_models=[User, Group, Word])


    def add_user(self, user : User):
        """Adds a new user if they don't already exist."""
        a = User.find_one(User.id == user.id).upsert({"$set": {User.full_name : user.full_name}} , on_insert=user).run()# self.collection.find_one({"_id": user_data.id}):
        logger.info(f"User {user.id} added  successfully!")

    def update_user(self, user_id: int, update_fields: dict):
        """
        Updates a user in the database by their _id.
        :param user_id: The user's identifier (_id)
        :param update_fields: A dictionary of fields to update
        :return: The result of the document update
        """
        # result = self.collection.update_one(
        #     {"_id": user_id},  # חיפוש המשתמש לפי ה-_id
        #     update_fields  # עדכון ה-total_quiz
        # )
        result = self.collection.update_one(
            {"_id": user_id},  # Finds the user by _id
            {"$set": update_fields}  # Updates the fields with the provided data
        )
        if result.modified_count:
            logger.info(f"User {user_id} updated successfully.")  # Success message if user was updated
        else:
            logger.info(f"No changes made to user {user_id} (maybe user not found).")  # Message if no update occurred
        return result

    def add_or_update_learned_word(self, user_id, word):
        o = User.find_one(User.id== user_id).run()
        o.learned_words.append(MyWords(word_id=word.word_id, correct=word.meaning, date_time=datetime.now()))
        o.save()
        logger.info(f"update learned words in user {user_id} ")

    def get_user(self, user_id):
        """Retrieves user data by ID."""
        logger.info(f"Retrieving user '{user_id}")
        return User.find_one(User.id== user_id).run()

    def get_learned_words_list(self, user_id):
        """Returns a list of learned word IDs for a given user."""
        logger.info(f"get_learned_words_list")
        user = self.get_user(user_id)
        if not user:
            return []
        return [word.word_id for word in user.learned_words]


    def get_learned_words_obj(self, user_id):
        user = self.get_user(user_id)
        return user.learned_words

    def get_new_words(self, user_id):
        """Returns a new word that the user has not learned yet."""
        learned_words = set(self.get_learned_words_list(user_id))

        with open("word_heb_arabic.json", "r", encoding="utf-8") as file:
            words = json.load(file)

        # Try to find a new word that is not in the learned words list
        for _ in range(100):  # Attempt up to 100 times
            word = random.choice(words)
            if word["word_id"] not in learned_words:
                return word

        logger.warning(f"No new words found for user {user_id}.")
        return None  # No new words found

    def increase_user_score(self, user_id, points=1):
        """Increases the user's score by a given number of points (default is 1)."""
        o = User.find_one(User.id== user_id).run()
        o.score += points
        o.save()
        logger.info(f"User {user_id} score increased by {points}!")

    def increment_total_quiz(self, user_id):
        """Increments the total number of quizzes taken by the user."""
        o = User.find_one(User.id == user_id).run()
        o.total_quiz += 1
        o.save()
        logger.info(f"User {user_id} total_quiz incremented!")

    def increment_total_words(self, user_id):
        """Increments the total number of learned words."""
        o = User.find_one(User.id == user_id).run()
        o.total_words += 1
        o.save()
        logger.info(f"User {user_id} total_words incremented!")