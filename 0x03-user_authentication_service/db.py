#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
# 1. Create user
from user import Base, User
# 2. Find user
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError, NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        1. create user
        Add a new user to Database
        """
        user = User(email=email, hashed_password=hashed_password)
        # Add new User object to session
        self._session.add(user)
        # commits any pending changes to the database
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """
        2. Find user
        Find a user by keyword arguments
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound('Not found')
        except InvalidRequestError:
            raise InvalidRequestError('Invalid')

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        3. Update a user
        Update a user by user_id
        and commit the changes in databes
        """
        # Find user
        user = self.find_user_by(id=user_id)

        # Check if attribute are valid
        for key in kwargs:
            if hasattr(user, key):
                setattr(user, key, kwargs[key])
            else:
                raise ValueError(f'Attribute {key} doesn\'t exist on User')

        # Commit the changes
        self._session.commit()
