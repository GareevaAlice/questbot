from dataclasses import dataclass
from typing import List, Dict, Set, Union

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
    not_visited: Set[str]
    visited: Set[str]


@dataclass
class Step:
    id: str
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
    start_step: Step
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
        self.start_step = self.steps_dict["start"]

    def _get_list(self, found_list: dict, element_name: str) -> List[Union[dict, str]]:
        if found_list:
            found_list = found_list[element_name]
            if type(found_list) is not list:
                found_list = [found_list]
        else:
            found_list = []
        return found_list

    def _steps_dict(self) -> Dict[str, Step]:
        steps = self.quest['steps']['step']
        if type(steps) is not list:
            steps = [steps]
        steps_dict: Dict[str, Step] = dict()
        for step in steps:
            answers = self._get_list(step.get("answers", None), "answer")
            step_id = step['@id']
            steps_dict[step_id] = \
                Step(id=step_id,
                     text=step['text'],
                     answers=[Answer(text=answer['text'],
                                     next_step_id=answer['next_step_id'],
                                     not_visited=set(
                                         self._get_list(answer.get("not_visited", None), "id")),
                                     visited=set(self._get_list(answer.get("visited", None), "id"))
                                     ) for answer in answers])
        return steps_dict

    def get_step(self, step_id: str) -> Step:
        if step_id not in self.steps_dict:
            raise ValueError
        return self.steps_dict[step_id]
