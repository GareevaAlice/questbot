import os
from collections import defaultdict
from dataclasses import dataclass
from typing import Set, Dict, List

from utils.Quest import Quest, Step

catalog_folder = "catalog"
tmp_folder = "/tmp"


@dataclass
class PlayState:
    current_step: Step
    visited: Set[str]


class DBManager:
    _authors_db: Dict[str, Set[str]] = defaultdict(set)
    _quests_db: Dict[str, Quest] = defaultdict(Quest)
    _users_db: Dict[str, Dict[str, PlayState]] = defaultdict(dict)

    def is_author(self, user_id: str, quest_id: str) -> bool:
        return quest_id in self._authors_db[user_id]

    def can_continue(self, user_id: str, quest_id: str) -> bool:
        return quest_id in self._users_db[user_id]

    def get_user_quest_ids(self, user_id: str) -> List[str]:
        return list(self._authors_db[user_id])

    def get_catalog_quest_ids(self) -> List[str]:
        return list(self._authors_db["admin"])

    def get_quest(self, quest_id: str) -> Quest:
        if quest_id not in self._quests_db:
            raise ValueError
        return self._quests_db[quest_id]

    def get_current_play_state(self, user_id: str, quest_id: str) -> PlayState:
        if quest_id not in self._users_db[user_id]:
            raise ValueError
        return self._users_db[user_id][quest_id]

    def save_quest(self, quest_path: str, user_id: str) -> Quest:
        quest = Quest(quest_path, user_id)
        self._quests_db[quest.quest_info.id] = quest
        self._authors_db[user_id].add(quest.quest_info.id)
        return quest

    def save_catalog_quests(self):
        for quest_file in os.listdir(catalog_folder):
            self.save_quest(f"{catalog_folder}/{quest_file}", user_id="admin")

    def save_play_state(self, user_id: str, quest_id: str, play_state: PlayState):
        self._users_db[user_id][quest_id] = PlayState(current_step=play_state.current_step,
                                                      visited=play_state.visited)

    def delete_play_state(self, user_id: str, quest_id: str):
        if quest_id in self._users_db[user_id]:
            del self._users_db[user_id][quest_id]

    def delete_quest(self, user_id: str, quest_id: str):
        if quest_id in self._quests_db:
            del self._quests_db[quest_id]
        if user_id in self._authors_db:
            self._authors_db[user_id].remove(quest_id)
        self.delete_play_state(user_id, quest_id)


db_manager = DBManager()
