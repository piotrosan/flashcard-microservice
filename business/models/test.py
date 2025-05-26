from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    BOOLEAN,
    ForeignKey,
    Table,
    Enum
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from business.models.base import Base


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

    left_id: Mapped[int] = mapped_column(
        ForeignKey("test_knowledge.id"), primary_key=True
    )
    right_id: Mapped[int] = mapped_column(
        ForeignKey("flash_card.id"), primary_key=True
    )
    child: Mapped["FlashCard"] = relationship(back_populates="test_knowledge")
    parent: Mapped["TestKnowledge"] = relationship(
        back_populates="flash_cards")


class TestKnowledge(Base):

    __tablename__ = "test_knowledge"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    flash_cards: Mapped[
        List["AssociationKnowledgeFlashCard"]
    ] = relationship(back_populates="child")
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    planned_start = Column(DateTime)