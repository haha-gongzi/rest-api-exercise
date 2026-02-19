from pydantic import BaseModel, Field
from typing import List


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)


class User(BaseModel):
    id: int
    username: str


class CreateNoteRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


class Note(BaseModel):
    id: int
    user_id: int
    text: str
    created_at: str


class FDARequest(BaseModel):
    query: str = Field(min_length=1, max_length=200)
    limit: int = Field(default=3, ge=1, le=20)
    skip: int = Field(default=0, ge=0)
