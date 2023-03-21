from typing import Optional
from pydantic import BaseModel, EmailStr, validator


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    dob: str
    additional_info: Optional[str]

    @validator('phone')
    def phone_validator(cls, v):
        if len(v) != 10:
            raise ValueError('Invalid phone number')
        return v

    @validator('dob')
    def dob_validator(cls, v):
        try:
            datetime.datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Invalid date format')
        return v


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactOut(ContactBase):
    id: int

    class Config:
        orm_mode = True
