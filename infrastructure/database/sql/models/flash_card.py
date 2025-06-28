from typing import List

from infrastructure.database.sql.models.base import Base
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String, ARRAY, ForeignKey
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func



class Language(Base):
    __tablename__ = "language"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    shortcut = Column(String(5), nullable=False)
    full_name = Column(String(50), nullable=False)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    flash_cards: Mapped[List["FlashCard"]] = relationship(
        back_populates='language')

class FlashCard(Base):

    __tablename__ = "flash_card"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    word = Column(String(255), nullable=False)
    translate = Column(ARRAY(String(255)), nullable=False)
    language_id = Column(ForeignKey('language.id'), nullable=False)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    asso_flash_card: Mapped[
        List["AssociationKnowledgeFlashCard"]
    ] = relationship(
        back_populates="flash_card")

    test_knowledges: Mapped[List["TestKnowledge"]] = relationship(
        lazy='joined',
        secondary="association_knowledge_flash_card",
        back_populates="flash_cards"
    )
    language: Mapped["Language"] = relationship(back_populates='flash_cards')