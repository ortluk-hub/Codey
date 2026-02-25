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
        if not self.is_valid_summary(summary):
            raise ValueError("summary must include non-empty 'topic' and 'summary' fields")
        self.long_term_path.parent.mkdir(parents=True, exist_ok=True)
        self.long_term_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    def load_long_term_summary(self) -> dict:
        if not self.long_term_path.exists():
            return {}
        return json.loads(self.long_term_path.read_text(encoding="utf-8"))

    @staticmethod
    def is_valid_summary(summary: dict) -> bool:
        topic = summary.get("topic") if isinstance(summary, dict) else None
        content = summary.get("summary") if isinstance(summary, dict) else None
        return isinstance(topic, str) and bool(topic.strip()) and isinstance(content, str) and bool(content.strip())
