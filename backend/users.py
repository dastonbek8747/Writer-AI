from pydantic import BaseModel, Field, model_validator, EmailStr, ValidationError
from sqlalchemy import Column, Integer, String, Text
from db import Base


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords don't match")
        return self


class UserResponse(BaseModel):
    email: EmailStr


class UserRegister(UserCreate):
    pass


class UsersLogin(BaseModel):
    email: EmailStr
    password: str


class ChatRequest(BaseModel):
    message: str
    session_id: str


class ChatHistoryRequest(BaseModel):
    session_id: str


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)


class Chats(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)

    session_id = Column(String(100), index=True)

    user_request = Column(Text)

    ai_response = Column(Text)
