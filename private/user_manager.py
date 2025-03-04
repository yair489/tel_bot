import logging
from pymongo import MongoClient
from datetime import datetime
import json
import random
from dataclasses import asdict
from private.cls_word_user import User , Word

# Configure logging
logger = logging.getLogger(__name__)
class UserManager:
    def __init__(self, db_name="language_bot", collection_name="users"):
        """Initialize the UserManager with a connection to MongoDB."""
        self.client = MongoClient()  # Connect to MongoDB
        self.db = self.client.get_database(db_name)
        self.collection = self.db.get_collection(collection_name)
        self.db_name = db_name

    def add_user(self, user_data):
        """Adds a new user if they don't already exist."""
        if self.collection.find_one({"_id": user_data.id}):
            logger.warning("User already exists!")
            return
        self.collection.insert_one(user_data.model_dump(by_alias=True))
        logger.info(f"User {user_data.id} added  successfully!")

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

        """Adds or updates a word in the user's learned_words list."""
        word_id, correct = word.word_id , word.meaning
        user = self.collection.find_one({"_id": user_id})
        if not user:
            logger.error("User not found!")
            return

        learned_words = user.get("learned_words", [])
        existing_word = next((word for word in learned_words if word["word_id"] == word_id), None)

        if existing_word:
            existing_word["correct"] = correct  # Update correctness
            existing_word["date_time"] = datetime.now().strftime("%d.%m.%Y")  # Update timestamp
        else:
            learned_words.append({
                "word_id": word_id,
                "correct": correct,
                "date_time": datetime.now().strftime("%d.%m.%Y")
            })

        self.collection.update_one({"_id": user_id}, {"$set": {"learned_words": learned_words}})
        logger.info(f"Learned word '{word_id}' updated for user {user_id}.")

    def get_user(self, user_id):
        """Retrieves user data by ID."""
        logger.info(f"Retrieving user '{user_id}")
        return self.collection.find_one({"_id": user_id})

    def get_learned_words_list(self, user_id):
        """Returns a list of learned word IDs for a given user."""
        logger.info(f"get_learned_words_list")
        user = self.get_user(user_id)
        if not user:
            return []
        return [word["word_id"] for word in user.get("learned_words", [])]

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
        self.collection.update_one({"_id": user_id}, {"$inc": {"score": points}})
        logger.info(f"User {user_id} score increased by {points}!")

    def increment_total_quiz(self, user_id):
        """Increments the total number of quizzes taken by the user."""
        self.collection.update_one({"_id": user_id}, {"$inc": {"total_quiz": 1}})
        logger.info(f"User {user_id} total_quiz incremented!")

    def increment_total_words(self, user_id):
        """Increments the total number of learned words."""
        self.collection.update_one({"_id": user_id}, {"$inc": {"total_words": 1}})
        logger.info(f"User {user_id} total_words incremented!")



# Example usage
if __name__ == "__main__":

    user_manager = UserManager()

    # Create a new user
    user_data = {
        "_id": 1005995332,
        "username": "Unknown",
        "full_name": "Ytyyyyyyyyyyy",
        "language_target": "arabic",
        "language_native": "hebrew",
        "score": 0,
        "total_quiz": 0,
        "total_words": 0,
        "learned_words": []
    }
    user_data = User(**user_data)
    user_manager.add_user(user_data)

    # Add or update a learned word
    user_manager.add_or_update_learned_word(1005995332, "yairrrr", True)

    # Increase user score
    user_manager.increase_user_score(1005995332, 5)

    # Increment total quizzes
    user_manager.increment_total_quiz(1005995332)

    # Retrieve user data
    user = user_manager.get_user(1005165332)
    logging.info(user)

    # Get a new word the user has not learned yet
    new_word = user_manager.get_new_words(1005165332)
    logging.info(new_word)
