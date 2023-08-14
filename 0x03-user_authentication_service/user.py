#!/usr/bin/env python3
"""
Main file
"""
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    """
    User model for the 'users' table.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)


# Print table name and column details
if __name__ == "__main__":
    print(User.__tablename__)

    for column in User.__table__.columns:
        print(f"{column}: {column.type}")
