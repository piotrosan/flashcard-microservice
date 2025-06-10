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


association_user_user_group = Table(
    "association_user_user_group",
    Base.metadata,
    Column("user", ForeignKey("flash_card_user.id")),
    Column("groups", ForeignKey("user_groups.id")),
)


class User(Base):
    __tablename__ = "flash_card_user"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    hash_identifier = Column(String(255), unique=True, nullable=False)

    user_groups: Mapped[List["UserGroup"]] = relationship(
        secondary=association_user_user_group,
        back_populates="users"
    )


class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(100), unique=True)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    role: Mapped[List["Role"]] = relationship(back_populates="group")
    users: Mapped[List["User"]] = relationship(
        secondary=association_user_user_group,
        back_populates="user_groups"
    )

class Role(Base):
    __tablename__ = "user_group_roles"


    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_group_id = Column(Integer, ForeignKey("user_groups.id"))
    name = Column(String(100), unique=True)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    group: Mapped["UserGroup"] = relationship(back_populates="roles")
