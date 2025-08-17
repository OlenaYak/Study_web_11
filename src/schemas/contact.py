from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional

class ContactSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    extra_info: Optional[str] = None

class ContactCreate(ContactSchema):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    birthday: Optional[date]
    extra_info: Optional[str]

class ContactResponse(ContactSchema):
    id: int

    class Config:
        orm_mode = True
