from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime, timezone


class UsernameAlreadyExists(Exception):
    pass


class UserNotFound(Exception):
    pass


@dataclass
class _UserRow:
    id: int
    username: str


@dataclass
class _NoteRow:
    id: int
    user_id: int
    text: str
    created_at: str


class InMemoryStore:
    def __init__(self) -> None:
        self._next_user_id = 1
        self._next_note_id = 1
        self._users: Dict[int, _UserRow] = {}
        self._username_to_id: Dict[str, int] = {}
        self._notes_by_user: Dict[int, List[_NoteRow]] = {}

    def create_user(self, username: str) -> _UserRow:
        key = username.strip()
        if key in self._username_to_id:
            raise UsernameAlreadyExists()

        user = _UserRow(id=self._next_user_id, username=key)
        self._next_user_id += 1

        self._users[user.id] = user
        self._username_to_id[key] = user.id
        self._notes_by_user[user.id] = []
        return user

    def get_user(self, user_id: int) -> _UserRow:
        if user_id not in self._users:
            raise UserNotFound()
        return self._users[user_id]

    def list_users(self) -> List[_UserRow]:
        return list(self._users.values())

    def add_note(self, user_id: int, text: str) -> _NoteRow:
        self.get_user(user_id)  # raises if not found

        now = datetime.now(timezone.utc).isoformat()
        note = _NoteRow(
            id=self._next_note_id,
            user_id=user_id,
            text=text,
            created_at=now,
        )
        self._next_note_id += 1
        self._notes_by_user[user_id].append(note)
        return note

    def list_notes(self, user_id: int) -> List[_NoteRow]:
        self.get_user(user_id)
        return list(self._notes_by_user[user_id])
