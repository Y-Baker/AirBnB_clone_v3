#!/usr/bin/python3
""" holds class User"""
import string
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
    
    def __setattr__(self, key: str, val) -> None:
        '''The most important one
        Sets an attribute of this class to a given value'''
        if key == 'password':
            if type(val) is str and not is_valid_hash(val):
                hashed = md5(bytes(val, 'utf-8'))
                super().__setattr__(key, hashed.hexdigest())
            else:
                super().__setattr__(key, val)
        else:
            super().__setattr__(key, val)

    def __update__(self, other_dict):
        """updates user with another dict"""
        for key, value in other_dict.items():
            if key == 'password' and not is_valid_hash(value):
                    value = md5(value.encode()).hexdigest()
            else:
                setattr(self, key, value)

    def __setitem__(self, key, value):
        """set key from user"""
        if key == 'password' and not is_valid_hash(value):
            value = md5(value.encode()).hexdigest()
        else:
            setattr(self, key, value)
            

def is_valid_hash(password):
    """Check if the string appears to be an MD5 hash"""
    return len(password) == 32 and all(c in string.hexdigits for c in password)
