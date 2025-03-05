import random
import logging
from private.model import Group , GroupUser
from pymongo import MongoClient
import bunnet
import matplotlib.pyplot as plt
from io import BytesIO
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

    def update_scores_failure(self, username, correct, ans):
        if not self.my_group:
            logger.error("Group not found.")
            return

        # קביעת הניקוד והכשלון כערכים מספריים
        score = int(correct == ans)
        failure = int(correct != ans)

        print(f"Updating score for {username}: Correct={correct}, Answer={ans}, Score={score}, Failure={failure}")

        # אם המשתמש לא קיים, ניצור אותו
        if username not in self.my_group.scores:
            user = GroupUser(full_name="", username=username, score=score, failure=failure)
            self.my_group.scores[username] = user
            logger.info(f"User {username} added to the group with initial score and failure.")
        else:
            # עדכון הניקוד וכמות הכשלונות
            user = self.my_group.scores[username]
            user.score += score
            user.failure += failure

        # שמירת השינויים
        self.my_group.save()

        logger.info(
            f"Scores and failures updated for {username}. New score: {user.score}, New failure: {user.failure}.")
    # def create_plt(self):
    #     print(self.my_group.scores)
    def get_scores(self):
        return self.my_group.scores
    def generate_score_charts(self , scores):
        for user_id, user in scores.items():
            plt.figure(figsize=(5, 3))
            plt.bar(["Score", "Failure"], [user.score, user.failure], color=["green", "red"])
            plt.xlabel("Category")
            plt.ylabel("Count")
            plt.title(f"User: {user.username}")

            # שמירת התמונה לזיכרון במקום לקובץ
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format="png")
            img_buffer.seek(0)
            plt.close()

            yield user.username, img_buffer

    def py_ques(self):
        questions = [
            # Decorators
            (
                "What does a Python decorator return?",
                "A function",
                "A string",
                "An integer",
                "A class"
            ),

            # JSON
            (
                "Which method converts a Python dictionary to a JSON string?",
                "`json.dumps()`",
                "`json.loads()`",
                "`json.encode()`",
                "`json.stringify()`"
            ),

            # List Comprehension
            (
                "How do you create a list of squares from 1 to 5?",
                "[x**2 for x in range(1,6)]",
                "[x^2 for x in range(1,5)]",
                "[x**2 for x in range(1,5)]",
                "[x*x for x in range(5)]"
            ),

            # Unicode
            (
                "What does `ord('😀')` return?",
                "128512",
                "256",
                "65536",
                "1114112"
            ),

            # Generators (unchanged)
            (
                "What will be printed when calling `list(gen())` in the following code?\n\n"
                "```python\n"
                "def gen():\n"
                "    yield from [1, 2, 3]\n"
                "    yield 4\n\n"
                "print(list(gen()))\n"
                "```",
                "[1, 2, 3, 4]",
                "[[1, 2, 3], 4]",
                "[1, 2, 3, [4]]",
                "[1, [2, 3], 4]"
            )
        ]
        for question in questions:
            q = question[0]
            answer = question[1]
            options = [question[1] ,  question[2] , question[3] , question[4] ]
            yield q, answer, options



if __name__ == "__main__":
    game_manager = GameManager(123214)