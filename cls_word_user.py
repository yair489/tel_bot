from dataclasses import dataclass, field


@dataclass
class Word:
    word_id: str
    meaning: str
    similar_words: list
    sentence_with_word :str

@dataclass
class User:
    _id: int
    username: str
    language_target: str = "arabic"
    language_native: str = "hebrew"
    score: int = 0
    total_quiz: int = 0
    total_words: int = 0
    learned_words: list = field(default_factory=list)
