from dataclasses import dataclass
from typing import List


@dataclass
class QuestInfo:
    name: str
    summary: str


@dataclass
class Answer:
    id: str
    text: str


@dataclass
class Step:
    prev_answer_id: str
    text: str
    answers: List[Answer]

