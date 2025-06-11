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

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class AssociationUserGroupUser(Base):

    __tablename__ = "association_user_group_user"

    left_user_id: Mapped[int] = mapped_column(
        ForeignKey("flash_card_user.id"), primary_key=True
    )
    right_user_group_id: Mapped[int] = mapped_column(
        ForeignKey("user_groups.id"), primary_key=True
    )

    user: Mapped["User"] = relationship(
        back_populates="asso_user")
    user_group: Mapped["UserGroup"] = relationship(
        back_populates="asso_user_group")


class User(Base):
    __tablename__ = "flash_card_user"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    hash_identifier = Column(String(255), unique=True, nullable=False)

    asso_user: Mapped[List["AssociationUserGroupUser"]] = relationship(
        back_populates="user"
    )
    user_groups: Mapped[List["UserGroup"]] = relationship(
        lazy='joined',
        secondary="association_user_group_user",
        back_populates="users"
    )

class UserGroup(Base):

    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(100), unique=True)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    roles: Mapped[List["Role"]] = relationship(back_populates="group")
    asso_user_group: Mapped[List["AssociationUserGroupUser"]] = relationship(
        back_populates="user_group"
    )
    users: Mapped[List["User"]] = relationship(
        lazy='joined',
        secondary="association_user_group_user",
        back_populates="user_groups"
    )


class Role(Base):

    __tablename__ = "user_group_roles"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_group_id = Column(Integer, ForeignKey("user_groups.id"))
    name = Column(String(100), unique=True)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    group: Mapped["UserGroup"] = relationship(
        lazy='joined',
        back_populates="roles"
    )
