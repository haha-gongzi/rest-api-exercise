from fastapi import FastAPI, HTTPException, status
from typing import List

from .models import (
    CreateUserRequest,
    User,
    CreateNoteRequest,
    Note,
    FDARequest,
)
from .store import InMemoryStore, UsernameAlreadyExists, UserNotFound
from .fda_client import fetch_drug_labels, build_note_text_from_fda, FDAClientError

app = FastAPI(title="REST API In-class Exercise")

store = InMemoryStore()


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(req: CreateUserRequest) -> User:
    try:
        u = store.create_user(req.username)
        return User(id=u.id, username=u.username)
    except UsernameAlreadyExists:
        raise HTTPException(status_code=409, detail="username already exists")


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    try:
        u = store.get_user(user_id)
        return User(id=u.id, username=u.username)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="user not found")


@app.get("/users", response_model=List[User])
def list_users() -> List[User]:
    users = store.list_users()
    return [User(id=u.id, username=u.username) for u in users]


@app.post("/users/{user_id}/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
def add_note(user_id: int, req: CreateNoteRequest) -> Note:
    try:
        n = store.add_note(user_id, req.text)
        return Note(id=n.id, user_id=n.user_id, text=n.text, created_at=n.created_at)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="user not found")


@app.get("/users/{user_id}/notes", response_model=List[Note])
def list_notes(user_id: int) -> List[Note]:
    try:
        notes = store.list_notes(user_id)
        return [Note(id=n.id, user_id=n.user_id, text=n.text, created_at=n.created_at) for n in notes]
    except UserNotFound:
        raise HTTPException(status_code=404, detail="user not found")


@app.post("/users/{user_id}/notes/from-fda", response_model=Note, status_code=status.HTTP_201_CREATED)
def add_note_from_fda(user_id: int, req: FDARequest) -> Note:
    # ensure user exists
    try:
        store.get_user(user_id)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="user not found")

    try:
        data = fetch_drug_labels(req.query, req.limit, req.skip)
        note_text = build_note_text_from_fda(data, req.query, req.limit, req.skip)
    except FDAClientError as e:
        raise HTTPException(status_code=502, detail=str(e))

    n = store.add_note(user_id, note_text)
    return Note(id=n.id, user_id=n.user_id, text=n.text, created_at=n.created_at)
