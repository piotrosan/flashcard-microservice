import re
from typing import List
from sqlalchemy.orm import mapped_column

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    ForeignKey,
    String
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from infrastructure.database.sql.models.base import Base
from sqlalchemy.orm import validates


"""
    Usage:
        p1 = Parent()
        c1 = Child()
        p1.children.append(c1)
        
        # redundant, will cause a duplicate INSERT on Association
        p1.child_associations.append(Association(child=c1))
"""


class AssociationKnowledgeFlashCard(Base):

    __tablename__ = "association_knowledge_flash_card"

    test_knowledge_id: Mapped[int] = mapped_column(
        ForeignKey("test_knowledge.id"), primary_key=True
    )
    flash_card_id: Mapped[int] = mapped_column(
        ForeignKey("flash_card.id"), primary_key=True
    )
    test_knowledge: Mapped["TestKnowledge"] = relationship(
        back_populates="asso_test_knowledge")
    flash_card: Mapped["FlashCard"] = relationship(
        back_populates="asso_flash_card")


class TestKnowledge(Base):

    __tablename__ = "test_knowledge"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    planned_start = Column(DateTime, nullable=True)
    user_identifier = Column(String(255), nullable=False)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    asso_test_knowledge: Mapped[
        List["AssociationKnowledgeFlashCard"]
    ] = relationship(back_populates="test_knowledge")
