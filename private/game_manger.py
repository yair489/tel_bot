import random
import logging
from private.model import Group , GroupUser
from pymongo import MongoClient
import bunnet

# Configure logging
logger = logging.getLogger(__name__)


# Configure logging
logger = logging.getLogger(__name__)

class GameManager:
    def __init__(self):
        self.id_chat = None
        self.my_group = None
        self.question = None
        self.answer = None
        self.options = None


    def new_question(self , question , answer , options):
        self.question = question
        self.answer = answer
        self.options = options
        logger.info(f"{question=} , {answer=} , {options=} IN {logger.name}")
    def add_group(self, id_chat):
        self.id_chat = id_chat
        self.my_group = Group(id=id_chat)
        self.my_group.save()
        logger.info(f"New group : {id_chat} IN {logger.name}")

    def update_scores_failure(self, username, score=1, failure=10):
        # check if right or not


        # if group found
        if not self.my_group:
            logger.error("Group not found.")
            return

        # if user found
        if username not in self.my_group.scores:
            logger.info(f"User {username} not found in the group.")
            # if not found create  new one
            user = GroupUser(full_name="", username=username, score=score, failure=failure)
            self.my_group.scores[username] = user
            logger.info(f"User {username} added to the group.")
        else:
            # update score  failure
            user = self.my_group.scores[username]
            user.score += score  # new score
            user.failure += failure  # failure
        # save change
        self.my_group.save()
        logger.info(f"Scores and failure updated for {username}. New score: {user.score}, New failure: {user.failure}.")


if __name__ == "__main__":
    game_manager = GameManager(123214)