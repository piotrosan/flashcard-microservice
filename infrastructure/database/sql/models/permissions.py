from infrastructure.database.sql.models.base import Base

from typing import List

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    BOOLEAN,
    ForeignKey,
    Table,
    Enum,
    UniqueConstraint, JSON
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(100), unique=True)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    role: Mapped["Role"] = relationship(back_populates="group")


class Role(Base):
    __tablename__ = "user_group_roles"


    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_group_id = Column(Integer, ForeignKey("user_groups.id"))
    name = Column(String(100), unique=True)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    group: Mapped["UserGroup"] = relationship(back_populates="role")
