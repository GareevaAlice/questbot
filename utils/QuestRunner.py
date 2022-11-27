from utils.dataclasses import QuestInfo, Step, Answer

quests = {"123": {"info": {"name": "Название", "summary": "Описание"},
                  "steps": [{"prev_answer_ids": ["start"],
                             "text": "text_start",
                             "answers": [{"id": "1", "text": "text1"},
                                         {"id": "2", "text": "text2"}]},
                            {"prev_answer_ids": ["1"],
                             "text": "text1",
                             "answers": [{"id": "2", "text": "text2"},
                                         {"id": "end", "text": "end"}]},
                            {"prev_answer_ids": ["2"],
                             "text": "text2",
                             "answers": [{"id": "1", "text": "text1"},
                                         {"id": "end", "text": "end"}]},
                            {"prev_answer_ids": ["end"],
                             "text": "end",
                             "answers": []}
                            ]
                  }
          }


class QuestRunner:
    # TODO
    def __init__(self, quest_id: str):
        if quest_id not in quests:
            raise ValueError
        self.quest = quests[quest_id]

    def get_info(self) -> QuestInfo:
        info = QuestInfo(name=self.quest['info']['name'],
                         summary=self.quest['info']['summary'])
        return info

    def get_step(self, prev_answer_id: str) -> Step:
        for step in self.quest['steps']:
            if prev_answer_id in set(step['prev_answer_ids']):
                return Step(prev_answer_id=step['prev_answer_ids'],
                            text=step['text'],
                            answers=[Answer(id=answer['id'],
                                            text=answer['text']) for answer in step['answers']])
        raise ValueError
