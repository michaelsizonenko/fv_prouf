from pydantic import BaseModel


class User(BaseModel):
    id: int = None
    email: str
    password: str
    name: str


class UserOut(BaseModel):
    name: str
    email: str


class UserDel(BaseModel):
    name: str
    email: str
    password: str

