from collections import defaultdict
from typing import List


class DBManager:
    stupid_db = defaultdict(list)

    def get_user_quest_ids(self, user_id: str) -> List[str]:
        return self.stupid_db[user_id]

    def get_quest_xml(self, quest_id: str):
        try:
            file_path = f"/tmp/{quest_id}.xml"
            with open(file_path) as f:
                return f.read()
        except Exception:
            raise ValueError

    def save_quest(self, user_id: str, quest_id: str):
        self.stupid_db[user_id].append(quest_id)


db_manager = DBManager()
