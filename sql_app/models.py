from typing import Text
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, DateTime
from sqlalchemy.sql import func
from .database import Base


class Posts(Base):
    __tablename__ = "user_posts"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=False, nullable=False)
    dateCreated = Column(DateTime(timezone=True), nullable=False,server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, unique=True, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    dateCreated = Column(DateTime(timezone=True), nullable=False,server_default=func.now())
