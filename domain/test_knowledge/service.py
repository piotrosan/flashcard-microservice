from infrastructure.database.api.test_knowledge_database_api import \
    TestKnowledgeDBAPI


class TestKnowledgeService:

    def __init__(self, infrastructure_db: TestKnowledgeDBAPI):
        self.infrastructure_db = infrastructure_db

    def get_test(self, id_knowledge: int):
        return self.infrastructure_db.query_test_knowledge_from_id(
            id_knowledge
        )

    def get_flash_card_for_test_and_user(
            self,
            hash_identifier: str,
            test_id: int
    ):
        self.infrastructure_db.query_test_knowledge_from_id()

    def get_random_test_for_user(self, hash_identifier: str):
        pass

    def list_test(self):
        pass

    def list_test_for_user(self, hash_identifier: str, page_id: int):
        pass

