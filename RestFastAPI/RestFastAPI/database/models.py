from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    dob = Column(Date)
    additional_info = Column(String, nullable=True)

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    dob: date
    additional_info: Optional[str]
