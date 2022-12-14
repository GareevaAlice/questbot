from dataclasses import dataclass
from typing import List, Dict

import xmltodict

from utils.XMLChecker import xml_checker


@dataclass
class QuestInfo:
    id: str
    title: str
    summary: str
    author_id: str


@dataclass
class Answer:
    text: str
    next_step_id: str


@dataclass
class Step:
    text: str
    answers: List[Answer]


def get_quest_xml(quest_path: str):
    try:
        with open(quest_path) as f:
            return f.read()
    except Exception:
        raise ValueError("Не смогли найти файл с квестом.")


class Quest:
    quest_info: QuestInfo
    begin_step: Step
    steps_dict: Dict[str, Step]

    def __init__(self, quest_path: str, author_id: str):
        xml_checker.check(quest_path)
        xml = get_quest_xml(quest_path)

        quest_id = quest_path.split('.')[0].split('/')[-1]
        self.quest = xmltodict.parse(xml)['quest']
        self.quest_info = \
            QuestInfo(
                id=quest_id,
                title=self.quest['info']['title'],
                summary=self.quest['info']['summary'],
                author_id=author_id
            )

        self.steps_dict = self._steps_dict()
        if "start" not in self.steps_dict:
            raise ValueError("Нет начального шага с id start")
        self.begin_step = self.steps_dict["start"]

    def _steps_dict(self) -> Dict[str, Step]:
        steps = self.quest['steps']['step']
        if type(steps) is not list:
            steps = [steps]
        steps_dict: Dict[str, Step] = dict()
        for step in steps:
            answers = step['answers']
            if answers:
                answers = answers['answer']
                if type(answers) is not list:
                    answers = [answers]
            else:
                answers = []
            steps_dict[step['@id']] = \
                Step(text=step['text'],
                     answers=[Answer(text=answer['text'],
                                     next_step_id=answer['next_step_id']) for answer in answers])
        return steps_dict

    def get_step(self, step_id: str) -> Step:
        if step_id not in self.steps_dict:
            raise ValueError(
                f"Квест был сделан некорректно - ссылка на шаг с id {step_id}, которого не существует")
        return self.steps_dict[step_id]
