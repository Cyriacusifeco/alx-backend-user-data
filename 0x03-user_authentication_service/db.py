#!/usr/bin/env python3
"""
Main file
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """
        Find and return a user from the users table based on input arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering the query.

        Returns:
            User: The found User object.

        Raises:
            NoResultFound: If no result is found for the given query.
            InvalidRequestError: If wrong query arguments are passed.
        """
        if not kwargs:
            raise InvalidRequestError

        columns = User.__table__.columns.keys()

        for key in kwargs.keys():
            if key not in columns:
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id, **kwargs):
        """
        Update user method
        """
        try:
            user = self.find_user_by(id=user_id)
            
            # Check if the provided kwargs correspond to user attributes
            valid_attributes = [column.key for column in User.__table__.columns]
            for key in kwargs.keys():
                if key not in valid_attributes:
                    raise ValueError(f"Invalid attribute: {key}")
            
            # Update user attributes and commit changes
            for key, value in kwargs.items():
                setattr(user, key, value)
            self._session.commit()
        except NoResultFound:
            raise NoResultFound("User not found")


if __name__ == "__main__":
    my_db = DB()

    user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
    print(user_1.id)

    user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
    print(user_2.id)
