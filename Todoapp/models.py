from sqlalchemy.orm import foreign

from .database import Base
from sqlalchemy import Integer, Column, String, Boolean, ForeignKey


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String,unique=True)
    username = Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean,default=True)
    role = Column(String)
    phone_number = Column(String)




class Todos(Base):
    __tablename__ = 'todos'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    descrip = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean,default = False)
    owner_id = Column(Integer,ForeignKey('users.id'))