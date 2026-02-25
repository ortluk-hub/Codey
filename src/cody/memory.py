"""Memory storage for short-term and long-term conversation context."""

from dataclasses import dataclass, field
import json
from pathlib import Path


@dataclass
class MemoryStore:
    long_term_path: Path
    short_term: dict[str, list[dict]] = field(default_factory=dict)

    def append_short_term(self, conversation_id: str, role: str, content: str) -> None:
        history = self.short_term.setdefault(conversation_id, [])
        history.append({"role": role, "content": content})

    def get_short_term(self, conversation_id: str) -> list[dict]:
        return list(self.short_term.get(conversation_id, []))

    def save_long_term_summary(self, summary: dict) -> None:
        self.long_term_path.parent.mkdir(parents=True, exist_ok=True)
        self.long_term_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    def load_long_term_summary(self) -> dict:
        if not self.long_term_path.exists():
            return {}
        return json.loads(self.long_term_path.read_text(encoding="utf-8"))
