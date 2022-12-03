import json

class DBManager:
    # TODO
    def get_user_quest_ids(self, user_id: str):
        authors = open_authors()
        return authors[user_id]

    def get_quest_xml(self, quest_id: str):
        # While we don't have DB
        file_path = f"/tmp/{quest_id}.xml"
        with open(file_path) as f:
            return f.read()


    def save_quest(self, user_id: str, quest_id: str):
        authors = open_authors()
        if user_id not in authors.keys():
            authors[user_id] = []
        authors[user_id].append(quest_id)
        close_authors()
        pass

    # def open_quests():
    #     with open('quests.json') as f:
    #         quests = json.load(f)
    #     return quests

    def open_authors():
        with open('authors.json') as f:
            authors = json.load(f)
        return authors

    def close_authors():
        with open('authors.json') as f:
            authors = json.dump(f)
        return


db_manager = DBManager()
