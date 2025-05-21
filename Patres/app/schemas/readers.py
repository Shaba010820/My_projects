from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class ReaderBase(BaseModel):
    name: str
    email: EmailStr


class ReaderCreate(ReaderBase):
    pass


class ReaderUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class ReaderRead(ReaderBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
