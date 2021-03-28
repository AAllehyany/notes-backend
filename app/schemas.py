from typing import List, Optional


from pydantic import BaseModel

class AdminBase(BaseModel):
    email: str

class AdminCreate(AdminBase):
    password: str

class Admin(AdminBase):
    id: int

    class Config:
        orm_mode=True


class ClientBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str


class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int

    class Config:
        orm_mode=True

