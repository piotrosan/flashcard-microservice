from typing import List, Any

from infrastructure.database.sql.api.test_knowledge_database_api import \
    TestKnowledgeDBAPI
from infrastructure.database.sql.models import TestKnowledge
from infrastructure.routers.models.request.knowledge import \
    CreateKnowledgeRequest
from infrastructure.supporter.generic import random_from


class TestKnowledgeService:

    def __init__(self, infrastructure_db: TestKnowledgeDBAPI):
        self.infrastructure_db = infrastructure_db

    def insert(self, create_data: CreateKnowledgeRequest) -> List[Any]:
       return list(self.infrastructure_db.insert(
           create_data.model_dump(mode='Python')
       ))

    def get_test(self, id_knowledge: int):
        return self.infrastructure_db.query_test_knowledge_from_id(
            id_knowledge
        )

    def get_flash_cards_for_test_and_user(
            self,
            hash_identifier: str,
            id_knowledge: int
    ):
        return self.infrastructure_db.query_test_knowledge_with_flash_cards_for_user(
            id_knowledge,
            hash_identifier
        )

    def get_random_test_for_user(
            self,
            hash_identifier: str
    ):
        count = self.infrastructure_db.get_count_test_knowledge()
        id_knowledge = random_from(count)
        return self.infrastructure_db.query_test_knowledge_with_flash_cards_for_user(
            id_knowledge,
            hash_identifier
        )


    def get_test_for_user(
            self,
            id_knowledge: int,
            hash_identifier: str
    ):
        return self.infrastructure_db.query_test_knowledge_with_flash_cards_for_user(
            id_knowledge,
            hash_identifier
        )


    def list_test(
            self,
            page_id: int
    ):
        return self.infrastructure_db.query_all_test_knowledge_paginate_generator(
            page=page_id
        )

    def list_test_for_user(
            self,
            hash_identifier: str,
            page_id: int
    ):
        return self.infrastructure_db.query_tests_for_user_paginate(
            hash_identifier,
            page_id
        )

    def update_test_from_id(self, id_knowledge: int, data: dict):
        return self.infrastructure_db.query_test_knowledge_from_id(
            id_knowledge
        )