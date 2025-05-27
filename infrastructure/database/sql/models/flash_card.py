import re

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
from sqlalchemy.orm import validates


class FlashCard(Base):

    __tablename__ = "flash_card"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    word = Column(String(255), nullable=False)
    translate = Column(String(255), nullable=False)
    user_email = Column(String(255), nullable=False)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    test_knowledge: Mapped["AssociationKnowledgeFlashCard"] = relationship(
        back_populates="parent")

    @validates("user_email", include_removes=True)
    def validate_email(self, key, email: str, is_remove):
        patter_set = r"[^!#$%&‘*+–/=?\\^_`.{\\|}~ | ^a-zA-Z]"
        local_part, domain, *rest = email.split("@")
        if rest:
            raise ValueError("Invalid email address, contain more than one @")
        if not local_part and not domain:
            raise ValueError("Invalid email address, not contain any of @")
        if len(domain) > 253:
            raise ValueError("Invalid email address, to long domain dns")

        compile_for_invalid_char = re.search(
            patter_set, f"{local_part}{domain}")

        if not compile_for_invalid_char:
            raise ValueError(
                f"Invalid email address contain any of "
                f"prohibited char {compile_for_invalid_char.groups()}"
            )
        return email