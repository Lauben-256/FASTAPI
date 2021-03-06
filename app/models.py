from enum import unique
from tkinter import CASCADE
from .database import Base 
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, ForeignKey 
from sqlalchemy.sql.expression import text 
from sqlalchemy.sql.sqltypes import TIMESTAMP 
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User") # Fetch user based off the owner id 


""" USER ACCOUNTS """

class User(Base): # Every SQLAlchemy Model must inherit from Base
    __tablename__ = "users" # Table Name in Postgres Database
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


""" VOTES MODEL """
class Vote(Base):
    __tablename__ = "votes" 
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)