from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
import time
import uuid


@dataclass
class ChatMessage:
    id: str
    role: str  # "user" | "assistant"
    content: str
    created_at: float
    error: bool = False

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
        }


@dataclass
class Conversation:
    messages: List[ChatMessage] = field(default_factory=list)

    def add_user(self, content: str) -> ChatMessage:
        msg = ChatMessage(
            id=str(uuid.uuid4()),
            role="user",
            content=content.strip(),
            created_at=time.time(),
        )
        self.messages.append(msg)
        return msg

    def add_assistant(self, content: str, error: bool = False) -> ChatMessage:
        msg = ChatMessage(
            id=str(uuid.uuid4()),
            role="assistant",
            content=content.strip(),
            created_at=time.time(),
            error=error,
        )
        self.messages.append(msg)
        return msg

    def clear(self) -> None:
        self.messages.clear()

    def to_provider_messages(self) -> list[dict]:
        return [m.to_dict() for m in self.messages if not m.error]

    def last_user_message(self) -> Optional[ChatMessage]:
        for m in reversed(self.messages):
            if m.role == "user":
                return m
        return None
