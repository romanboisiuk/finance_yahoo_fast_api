from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from db import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    Date = Column(Date)
    Open = Column(String)
    High = Column(String)
    Low = Column(String)
    Close = Column(String)
    Adj_Close = Column(String)
    Volume = Column(Integer)
    company_id = Column(Integer, ForeignKey("company.id"))
