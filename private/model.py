from dataclasses import  field
from datetime import datetime
import bunnet
import pydantic
from bunnet import Document
from typing import Optional
#bunnet pyndantix


class Word(Document):
    word_id: str
    meaning: str
    similar_words: list
    sentence_with_word :str


class MyWords(pydantic.BaseModel):
    word_id: str
    correct : str
    date_time : datetime


class User(Document):
    id: int = pydantic.Field(serialization_alias="_id")
    username: str
    full_name: str
    language_target: str = "arabic"
    language_native: str = "hebrew"
    score: int = 0
    total_quiz: int = 0
    total_words: int = 0
    learned_words: list[MyWords] = []

class GroupUser(pydantic.BaseModel):
    full_name: str
    username: int
    score: int = 0
    failure: int = 0

class Group(Document):
    id: int = pydantic.Field(serialization_alias="_id")
    language_target: str = "arabic"
    language_native: str = "hebrew"
    scores: dict[int, GroupUser] = {}
    # learned_words: list[MyWords] = []

