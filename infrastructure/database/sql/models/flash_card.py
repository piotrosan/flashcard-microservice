from infrastructure.database.sql.models.base import Base
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func



class FlashCard(Base):

    __tablename__ = "flash_card"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    word = Column(String(255), nullable=False)
    translate = Column(String(255), nullable=False)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    test_knowledge: Mapped["AssociationKnowledgeFlashCard"] = relationship(
        back_populates="parent")
