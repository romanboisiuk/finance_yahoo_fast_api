import databases
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///data.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
database = databases.Database(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    date = Column(String)
    open = Column(String)
    high = Column(String)
    low = Column(String)
    close = Column(String)
    adj_close = Column(String)
    volume = Column(Integer)
    company_id = Column(Integer, ForeignKey("company.id"))


items = Item.__table__
