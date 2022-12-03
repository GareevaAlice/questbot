class DBManager:
    # TODO
    def get_user_quest_ids(self, user_id: str):
        return ["quest_id", "quest_id"]

    def get_quest_xml(self, quest_id: str):
        # While we don't have DB
        try:
            file_path = f"/tmp/{quest_id}.xml"
            with open(file_path) as f:
                return f.read()
        except:
            raise ValueError

    def save_quest(self, user_id: str, quest_id: str):
        pass


db_manager = DBManager()
