from typing import List, Any, Iterator

from infrastructure.database.sql.api.test_knowledge_database_api import \
    TestKnowledgeDBAPI
from infrastructure.database.sql.models import TestKnowledge
from infrastructure.database.sql.models.auth import User
from infrastructure.routers.models.request.knowledge import \
    CreateKnowledgeRequest, UpdateKnowledgeRequest
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

    def get_tests(
            self,
            page_id: int
    ):
        return self.infrastructure_db.query_all_test_knowledge_paginate_generator(
            page=page_id
        )

    def get_tsts_know_for_user(
            self,
            user: User,
            page_id: int
    ) -> Iterator[Any]:
        return self.infrastructure_db.qet_tsts_know_for_user(
            page_id,
            user.hash_identifier
        )

    def get_random_test_for_user(
            self,
            user: User
    ) -> Iterator[Any]:
        count = self.infrastructure_db.get_count_test_knowledge()
        id_knowledge = random_from(count)
        return self.infrastructure_db.get_tsts_with_cards_for_user(
            user.hash_identifier,
            id_knowledge,
        )


    def get_test_for_user(
            self,
            id_knowledge: int,
            user: User
    ):
        return self.infrastructure_db.qet_tsts_know_for_user(
            id_knowledge,
            user.hash_identifier
        )

    def get_tsts_know_with_cards_for_user(
            self,
            hash_identifier: str,
            id_test_knowledge: int
    ):
        return self.infrastructure_db.get_tsts_with_cards_for_user(
            hash_identifier,
            id_test_knowledge
        )

    def update_test_knowledge(self, test_data: UpdateKnowledgeRequest):
        return self.infrastructure_db.update_test(
            test_data.model_dump(mode='python')
        )