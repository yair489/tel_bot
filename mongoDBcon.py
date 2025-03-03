# pip install feedparser
import datetime
from pprint import pprint
from pymongo import MongoClient
import pymongo


class CounterDB:
    def __init__(self, db_name="counter_bot"):
        self.client = pymongo.MongoClient()
        self.db = self.client.get_database(db_name)
        self.users = self.db.get_collection("users")
        self.db_name = db_name

    def drop_db(self):
        self.client.drop_database(self.db_name)

    def inc_value(self, chat_id: int, value: int):
        d = self.users.find_one_and_update(
            {"chat_id": chat_id},
            {"$inc": {"v": value}},
            upsert=True,
            return_document=pymongo.ReturnDocument.AFTER,
        )
        return d["v"]

    def reset_value(self, chat_id: int):
        self.users.update_one(
            {"chat_id": chat_id},
            {"$set": {"v": 0}},
            upsert=True,
        )

    def get_value(self, chat_id: int):
        return self.users.find_one({"chat_id": chat_id})["v"]

# client = MongoClient()
# client = MongoClient(host="127.0.0.1")
# dic={
#         "_id": 12345678,
#         "username": "YairT",
#         "language_target": "French",
#         "language_native": "English",
#         "score": 5,
#         "total_quiz": 10,
#         "total_words": 20,
#         "learned_words": [
#             {
#                 "word_id": "fr_apple",
#                 "correct": False,
#                 "date_time": "10.2.2023"
#             },
#             {
#                 "word_id": "fr_banana",
#                 "correct": False,
#                 "date_time": "10.2.2023"
#             }
#         ]
#     }
# db = client.get_database("bot_language")
# articles = db.get_collection("users")
# articles.insert_one(dic)