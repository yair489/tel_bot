from dataclasses import  field
import pydantic
from typing import Optional
#bunnet pyndantix


class Word(pydantic.BaseModel):
    word_id: str
    meaning: str
    similar_words: list
    sentence_with_word :str


class User(pydantic.BaseModel):
    id : int = pydantic.Field(serialization_alias="_id")
    username: str
    full_name: str
    language_target: str = "arabic"
    language_native: str = "hebrew"
    score: int = 0
    total_quiz: int = 0
    total_words: int = 0
    learned_words: list = field(default_factory=list)
