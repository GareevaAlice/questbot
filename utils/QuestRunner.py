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
    def __init__(self, quest: dict):
        self.quest = quest['quest']

    def get_info(self) -> QuestInfo:
        info = QuestInfo(name=self.quest['info']['name'],
                         summary=self.quest['info']['summary'])
        return info

    def get_step(self, prev_answer_id: str) -> Step:
        steps = self.quest['steps']['step']
        if type(steps) is not list:
            steps = [steps]

        for step in steps:
            prev_answer_ids = step['prev_answer_ids']['value']
            if type(prev_answer_ids) is not list:
                prev_answer_ids = [prev_answer_ids]

            if prev_answer_id in set(prev_answer_ids):
                answers = step['answers']['answer']
                if type(answers) is not list:
                    answers = [answers]

                return Step(prev_answer_id=prev_answer_id,
                            text=step['text'],
                            answers=[Answer(id=answer['id'],
                                            text=answer['text']) for answer in answers])
        raise ValueError
